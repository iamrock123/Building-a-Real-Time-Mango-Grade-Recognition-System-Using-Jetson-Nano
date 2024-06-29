# Building a Real-Time Mango Grade Recognition System Using Jetson Nano

## Overview

The inspiration for this project stems from the challenges faced by the aging agricultural workforce. During harvest seasons, farmers often struggle to find experienced fruit graders, leading to misjudgments in fruit quality and financial losses. By leveraging a public dataset to train the mango grading model, this system enhances accuracy through a multi-faceted detection process and employs the Jetson Nano for a cost-effective, efficient solution. This assists farmers during critical times when skilled fruit sorters are scarce.

This project received an Honorable Mention in the 2023 智慧感測聯網創新應用競賽-智慧視覺組.

Demo YouTube Link: [Insert Link Here]

## Main Features

1. **Cost-Effective Training:** Reduces training costs by utilizing transfer learning for object detection models.
2. **Enhanced Accuracy:** Uses a multi-faceted detection process designed on the Jetson Nano Developer Kit.
3. **Real-Time Results:** Displays recognition results in real-time on a mobile application using Google Cloud Platform.

## Hardware Introduction

- **Jetson Nano 4GB Developer Kit**
- **Logitech C270 HD Webcam**
- **LED, Button, Breadboard, Dupont Line**

## How to Run

To run this program, follow these steps:

1. **Download and Prepare JetPack 4.6 for Jetson Nano**
    - [Get Started With Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write)
    - [JetPack SDK 4.6 Release Page](https://developer.nvidia.com/embedded/jetpack-sdk-46)

2. **Install jetson-inference from dusty-nv**
    - [Building the Project from Source](https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md)
    - [Running the Docker Container](https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-docker.md)

3. **Download this Project**
    ```sh
    git clone https://github.com/iamrock123/Building-a-Real-Time-Mango-Grade-Recognition-System-Using-Jetson-Nano.git
    ```

4. **Run the Project**
    - If `./mango-grading.onnx` is not working, please change to the `ssd-mobilenet.onnx` model.
    - To use your own model, follow the instructions [here](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-ssd.md).

### Running with Firebase on GCP
- Install the Python SDK and setup from [Firebase](https://firebase.google.com/docs/admin/setup#python)
- Initialize Firebase with your credentials:
    ```python
    cred = credentials.Certificate("Your Firebase Certificate")
    initialize_app(cred, {'storageBucket': 'your-own.appspot.com'})
    push_service = FCMNotification(api_key="Your API Key")
    registration_id = "Your Registration ID"
    ```
- Run the program:
    ```sh
    python3 mango_detect_GCP.py --model=./mango-grading.onnx --labels=./labels.txt --input-blob=input_0 --output-cvg=scores --output-bbox=boxes /dev/video0
    ```

### Running with MQTT
- Set up your MQTT Server from [Mosquitto](https://mosquitto.org/) or use a public MQTT server.
- Configure your MQTT server in the code:
    ```python
    mqttc.connect("Your MQTT Server IP", "Your MQTT Server Port")
    ```
- Run the program:
    ```sh
    python3 mango_detect_MQTT.py --model=./mango-grading.onnx --labels=./labels.txt --input-blob=input_0 --output-cvg=scores --output-bbox=boxes /dev/video0
    ```

### Running Locally
- To display information on the Jetson Nano, run the local script:
    ```sh
    python3 mango_detect_local.py --model=./mango-grading.onnx --labels=./labels.txt --input-blob=input_0 --output-cvg=scores --output-bbox=boxes /dev/video0
    ```

## References

- [Get Started With Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#intro)
- [JetPack SDK 4.6 Release Page](https://developer.nvidia.com/embedded/jetpack-sdk-46)
- [Re-training SSD-Mobilenet](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-ssd.md)
