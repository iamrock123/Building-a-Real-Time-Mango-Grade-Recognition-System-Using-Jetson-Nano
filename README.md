# Building-a-Real-Time-Mango-Grade-Recognition-System-Using-Jetson-Nano
## Overview

The concept of this work originates from the aging agricultural population, where during harvest seasons, farmers lack experienced fruit graders to help with sorting fruits by quality. This often results in farmers misjudging the grades, leading to financial losses. By using public dataset for training the mango grading model, enhances accuracy with multi-faceted detection process and using Jetson Nano for a cost-effective and efficient system, assisting farmers during fruit harvesting seasons when skilled fruit sorters are in short supply.

This system also received an Honorable Mention in the 2023智慧感測聯網創新應用競賽-智慧視覺組.

Demo Youtube Link: 

## Main Features

1. Reducing training costs by utilizing transfer learning to train object detection models.

2. Enhancing recognition accuracy with a multi-faceted detection process designed on Jetson Nano Developer Kit.

3. Displaying recognition results in real-time on a mobile application using Google Cloud Platform.

## Hardware Introduction

1. **Jetson Nano 4GB Developer Kit**

2. **Logitech C270 HD WEBCAM**

3. **LED, Button, BreadBoard, Dupont Line**

## How to Run

To run this program, follow these steps:

1. **Download the image of JetPack 4.6, and write it to the microSD for Jetson Nano**
    - Get Started With Jetson Nano Developer Kit: https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write
    - JetPack SDK 4.6 Release Page: https://developer.nvidia.com/embedded/jetpack-sdk-46

2. **Install the jetson-inference from dusty-nv**
   Two way to install jetson-inference.
    - Building the Project from Source: https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md
    - Running the Docker Container: https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-docker.md
      
3. **Download this project**
    ```sh
   git clone https://github.com/iamrock123/Building-a-Real-Time-Mango-Grade-Recognition-System-Using-Jetson-Nano.git
    ```

4. **Run the project with different version**
   4.1 ***Running with Firebase of GCP***
    - If running with Firebase of GCP, you need to install the Python SDK and setup from Firebase website: https://firebase.google.com/docs/admin/setup#python
    - Init firebase with your credentials from line 55 ~ 58:
    ```python
    cred = credentials.Certificate("Please Use Your Own Firebase Certificate")
    initialize_app(cred, {'storageBucket': 'your-own.appspot.com'})
    push_service = FCMNotification(api_key="Please Use Your Own API Key")
    registration_id = "Please Use Your Own Registration ID"
    ```
    - Runng the python program of mango_detect_GCP.py:
    ```sh
    python3 mango_detect_GCP.py --model=./mango-grading.onnx --labels=./labels.txt --input-blob=input_0 --output-cvg=scores --output-bbox=boxes /dev/video0
    ```
    - Running with MQTT: 
    ```sh
    python3 mango_detect_MQTT.py --model=./mango-grading.onnx --labels=./labels.txt --input-blob=input_0 --output-cvg=scores --output-bbox=boxes /dev/video0
    ```
    - Running at Local: 
    ```sh
    python3 mango_detect_local.py --model=./mango-grading.onnx --labels=./labels.txt --input-blob=input_0 --output-cvg=scores --output-bbox=boxes /dev/video0
    ```

## References

- [Get Started With Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#intro)
- [JetPack SDK 4.6 Release Page](https://developer.nvidia.com/embedded/jetpack-sdk-46)
- [Re-training SSD-Mobilenet](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-ssd.md)
