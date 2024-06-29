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

# create video output object 
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)
	
# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# create video sources
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)

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

try:
# process frames until the user exits
    while True:
        # capture the next image
        img = input.Capture()

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
                    if(mango1Img == 3):
                        # if mango1Img is Class C, save result and change state to state = StandBy
                        flag = 0 
                        GPIO.output(7, GPIO.LOW)
                        GPIO.output(11, GPIO.LOW)
                        C_num += 1
                    else:
                        flag = 2 # change state to state = MangoIMG2Check
                        GPIO.output(7, GPIO.LOW)
                        GPIO.output(11, GPIO.HIGH)
                elif(flag == 2):
                    if(mango1Img == 2 or mango2Img == 2):
                        # if mango1Img or mango2Img is Class B, save result and change state to state = StandBy
                        flag = 0
                        GPIO.output(7, GPIO.LOW)
                        GPIO.output(11, GPIO.LOW)
                        B_num += 1
                    elif(mango2Img == 3):
                        # if mango2Img is Class C, save result and change state to state = StandBy
                        flag = 0
                        GPIO.output(7, GPIO.LOW)
                        GPIO.output(11, GPIO.LOW)
                        C_num += 1
                    flag = 3 # change state to state = MangoIMG3Check
                    GPIO.output(7, GPIO.HIGH)
                    GPIO.output(11, GPIO.HIGH)
                elif(flag == 3):
                    if(mango3Img == 1):
                        A_num += 1
                    elif(mango3Img == 2):
                        B_num += 1
                    elif(mango3Img == 3):
                        C_num += 1    
                    flag = 0 # save result and change state to state = StandBy
                    GPIO.output(7, GPIO.LOW)
                    GPIO.output(11, GPIO.LOW)
                time.sleep(2)

        # render the image
        output.Render(img)

        # update the title bar
        output.SetStatus("{:s} | Network {:.0f} FPS | {:s}".format(opt.network, net.GetNetworkFPS(),current_state))

        # print out performance info
        net.PrintProfilerTimes()

        # exit on input/output EOS
        if not input.IsStreaming() or not output.IsStreaming():
            break

finally:
    now = datetime.now()
    current_time = now.strftime("%Y/%m/%d %H:%M:%S")
    total_mango_classNum = "A Class : " + str(A_num) + " , B Class : " + str(B_num) + " , C Class : " + str(C_num) + " , current time : " + current_time
    print(total_mango_classNum) # Display the total class results
    GPIO.cleanup()
