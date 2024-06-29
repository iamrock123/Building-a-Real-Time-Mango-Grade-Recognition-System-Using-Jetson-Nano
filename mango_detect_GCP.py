#!/usr/bin/python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import jetson.inference
import jetson.utils
import argparse
import sys
import RPi.GPIO as GPIO
import time
from datetime import datetime
from pyfcm import FCMNotification
from firebase_admin import credentials, initialize_app, storage

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# Init firebase with your credentials
cred = credentials.Certificate("Please Use Your Own Firebase Certificate")
initialize_app(cred, {'storageBucket': 'mango-46711.appspot.com'})
push_service = FCMNotification(api_key="Please Use Your Own API Key")
registration_id = "Please Use Your Own Registration ID"

# create video output object 
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)

# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# create video sources
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW) #LED1 GPIO Setup
GPIO.setup(11, GPIO.OUT,  initial=GPIO.LOW) #LED2 GPIO Setup
GPIO.setup(13, GPIO.IN) #Button GPIO Setup

current_state = "StandBy"
mango1Img = -1 #Initialize for the mango image 1 current state
mango2Img = -1 #Initialize for the mango image 2 current state
mango3Img = -1 #Initialize for the mango image 3 current state
flag = 0
A_num = 0 #Class A counter
B_num = 0 #Class B counter
C_num = 0 #Class C counter
# Initialize image label & url
mango1Img_label = ""
mango2Img_label = ""
mango3Img_label = ""
mango1Img_url = ""
mango2Img_url = ""
mango3Img_url = ""


try:
# process frames until the user exits
    while True:
        # capture the next image
        img = input.Capture()
        
        # Record current time
        now = datetime.now()
        current_time = now.strftime("%Y_%m_%d %H:%M:%S")
        
        # detect objects in the image (with overlay)
        detections = net.Detect(img, overlay=opt.overlay)

        # print the detections
        # print("detected {:d} objects in image".format(len(detections)))
        for detection in detections:
            print(detection)
            # Current state process
            if(flag == 1):
                mango1Img = detection.ClassID
                current_state = "MangoIMG1Check"
                print(current_state)
            elif(flag == 2):
                mango2Img = detection.ClassID
                current_state = "MangoIMG2Check"
                print(current_state)
            elif(flag == 3):
                mango3Img = detection.ClassID
                current_state = "MangoIMG3Check"
                print(current_state)
            else:
                current_state = "StandBy"
                print(current_state)
            # when user press the button
            if(GPIO.input(13)==GPIO.LOW):
                print("pressed!")
                if(flag == 0):
                    flag = 1 # if state = StandBy, change state to MangoIMG1Check
                    GPIO.output(7, GPIO.HIGH)
                    GPIO.output(11, GPIO.LOW)
                elif(flag == 1):
                    # Record image label
                    if(mango1Img == 1):
                        mango1Img_label = 'A Class'
                    elif(mango1Img == 2):
                        mango1Img_label = 'B Class'
                    elif(mango1Img == 3):
                        mango1Img_label = 'C Class'
                    # Please change to your own path 
                    # mango1Check_image = '/home/jetsonnano/jetson-inference/python/examples/img/mango1'+current_time+'.jpg'
                    mango1Check_image = './mango1'+current_time+'.jpg'
                    # Store image
                    jetson.utils.saveImageRGBA(mango1Check_image, img, 360, 640)
                    fileName = mango1Check_image
                    bucket = storage.bucket()
                    blob = bucket.blob(fileName)
                    blob.upload_from_filename(fileName)

                    # Make public access from the URL
                    blob.make_public()
                    print("your file url", blob.public_url)
                    mango1Img_url = blob.public_url
                    if(mango1Img == 3):
                        # if mango1Img is Class C, save result and change state to state = StandBy
                        flag = 0
                        GPIO.output(7, GPIO.LOW)
                        GPIO.output(11, GPIO.LOW)
                        C_num += 1
                        total_mango = 'C Class'
                        data_message = {
                            "Type" : "a",
                            "Mango1Image" : 'C Class',
                            "Mango1ImageURL" : mango1Img_url,
                            "Mango2Image" : "None",
                            "Mango2ImageURL" : "",
                            "Mango3Image" : "None",
                            "Mango3ImageURL" : "",
                            "TotalClass" : total_mango,
                            "CurrentTime" : current_time,
                            "CardNum" : "1"
                        }
                        # Push the image information to the Firebase for the React Native information card
                        result = push_service.single_device_data_message(registration_id=registration_id, data_message=data_message)
                    else:
                        flag = 2 # change state to state = MangoIMG2Check
                        GPIO.output(7, GPIO.LOW)
                        GPIO.output(11, GPIO.HIGH)
                elif(flag == 2):
                    # Record image label
                    if(mango2Img == 1):
                        mango2Img_label = 'A Class'
                    elif(mango2Img == 2):
                        mango2Img_label = 'B Class'
                    elif(mango2Img == 3):
                        mango2Img_label = 'C Class'
                    # Please change to your own path 
                    # mango2Check_image = '/home/jetsonnano/jetson-inference/python/examples/img/mango2'+current_time+'.jpg'
                    mango2Check_image = './mango2'+current_time+'.jpg'
                    # Store image
                    jetson.utils.saveImageRGBA(mango2Check_image, img, 360, 640)
                    fileName = mango2Check_image
                    bucket = storage.bucket()
                    blob = bucket.blob(fileName)
                    blob.upload_from_filename(fileName)

                    # Make public access from the URL
                    blob.make_public()
                    print("your file url", blob.public_url)
                    mango2Img_url = blob.public_url
                    if(mango1Img == 2 or mango2Img == 2):
                        # if mango1Img or mango2Img is Class B, save result and change state to state = StandBy
                        flag = 0
                        GPIO.output(7, GPIO.LOW)
                        GPIO.output(11, GPIO.LOW)
                        B_num += 1
                        total_mango = 'B Class'
                        data_message = {
                            "Type" : "a",
                            "Mango1Image" : mango1Img_label,
                            "Mango1ImageURL" : mango1Img_url,
                            "Mango2Image" : mango2Img_label,
                            "Mango2ImageURL" : mango2Img_url,
                            "Mango3Image" : mango3Img_label,
                            "Mango3ImageURL" : mango3Img_url,
                            "TotalClass" : total_mango,
                            "CurrentTime" : current_time,
                            "CardNum" : "2"
                        }
                        # Push the image information to the Firebase for the React Native information card
                        result = push_service.single_device_data_message(registration_id=registration_id, data_message=data_message)
                    elif(mango2Img == 3):
                        # if mango2Img is Class C, save result and change state to state = StandBy
                        flag = 0
                        GPIO.output(7, GPIO.LOW)
                        GPIO.output(11, GPIO.LOW)
                        C_num += 1
                        total_mango = 'C Class'
                        data_message = {
                            "Type" : "a",
                            "Mango1Image" : mango1Img_label,
                            "Mango1ImageURL" : mango1Img_url,
                            "Mango2Image" : mango2Img_label,
                            "Mango2ImageURL" : mango2Img_url,
                            "Mango3Image" : mango3Img_label,
                            "Mango3ImageURL" : mango3Img_url,
                            "TotalClass" : total_mango,
                            "CurrentTime" : current_time,
                            "CardNum" : "2"
                        }
                        # Push the image information to the Firebase for the React Native information card
                        result = push_service.single_device_data_message(registration_id=registration_id, data_message=data_message)
                    flag = 3 # change state to state = MangoIMG3Check
                    GPIO.output(7, GPIO.HIGH)
                    GPIO.output(11, GPIO.HIGH)
                elif(flag == 3):
                    # Record image label
                    if(mango3Img == 1):
                        mango3Img_label = 'A Class'
                    elif(mango3Img == 2):
                        mango3Img_label = 'B Class'
                    elif(mango3Img == 3):
                        mango3Img_label = 'C Class'
                    # Please change to your own path 
                    # mango3Check_image = '/home/jetsonnano/jetson-inference/python/examples/img/mango3'+current_time+'.jpg'
                    mango3Check_image = './mango3'+current_time+'.jpg'
                    # Store image
                    jetson.utils.saveImageRGBA(mango3Check_image, img, 360, 640)
                    fileName = mango3Check_image
                    bucket = storage.bucket()
                    blob = bucket.blob(fileName)
                    blob.upload_from_filename(fileName)

                    # Make public access from the URL
                    blob.make_public()
                    print("your file url", blob.public_url)
                    mango3Img_url = blob.public_url
                    if(mango3Img == 1):
                        A_num += 1
                        total_mango = 'A Class'
                    elif(mango3Img == 2):
                        B_num += 1
                        total_mango = 'B Class'
                    elif(mango3Img == 3):
                        C_num += 1
                        total_mango = 'C Class'
                    data_message = {
                            "Type" : "a",
                            "Mango1Image" : mango1Img_label,
                            "Mango1ImageURL" : mango1Img_url,
                            "Mango2Image" : mango2Img_label,
                            "Mango2ImageURL" : mango2Img_url,
                            "Mango3Image" : mango3Img_label,
                            "Mango3ImageURL" : mango3Img_url,
                            "TotalClass" : total_mango,
                            "CurrentTime" : current_time,
                            "CardNum" : "3"
                        }
                    # Push the image information to the Firebase for the React Native information card
                    result = push_service.single_device_data_message(registration_id=registration_id, data_message=data_message)
                    flag = 0 # save result and change state to state = StandBy
                    GPIO.output(7, GPIO.LOW)
                    GPIO.output(11, GPIO.LOW)
                time.sleep(2)

        # render the image
        output.Render(img)

        # update the title bar
        output.SetStatus("{:s} | Network {:.0f} FPS | {:s}".format(opt.network, net.GetNetworkFPS(),current_state))

        # print out performance info
        # net.PrintProfilerTimes()

        # exit on input/output EOS
        if not input.IsStreaming() or not output.IsStreaming():
            break


finally:
    data_message = {
        "Type" : "b",
        "AclassNum" : str(A_num),
        "BclassNum" : str(B_num),
        "CclassNum" : str(C_num),
        "CurrentTime" : current_time
    }
    # Push the image information to the Firebase for the React Native quantity of mango grades for each batch and historical quantity chart
    result = push_service.single_device_data_message(registration_id=registration_id, data_message=data_message)
    
    total_mango_classNum = "A Class : " + str(A_num) + " , B Class : " + str(B_num) + " , C Class : " + str(C_num) + " , current time : " + current_time
    print(total_mango_classNum) # Display the total class results
    GPIO.cleanup()
