# Building-a-Real-Time-Mango-Grade-Recognition-System-Using-Jetson-Nano
## Overview

The concept of this work originates from the aging agricultural population, where during harvest seasons, farmers lack experienced fruit graders to help with sorting fruits by quality. This often results in farmers misjudging the grades, leading to financial losses. By using public dataset for training the mango grading model, enhances accuracy with multi-faceted detection process and using Jetson Nano for a cost-effective and efficient system, assisting farmers during fruit harvesting seasons when skilled fruit sorters are in short supply.

This system also received an Honorable Mention in the 2023智慧感測聯網創新應用競賽-智慧視覺組

## Main Features

-Reducing training costs by utilizing transfer learning to train object detection models.

-Enhancing recognition accuracy with a multi-faceted detection process designed on Jetson Nano Developer Kit.

-Displaying recognition results in real-time on a mobile application using Google Cloud Platform.

## Hardware Introduction

1. **Jetson Nano 4GB Developer Kit**

2. **Logitech C270 HD WEBCAM**

3. **LED, Button, BreadBoard, Dupont Line**

## How to Run

To run this program, follow these steps:

1. **Download the image of JetPack 4.6, and write it to the microSD for Jetson Nano**
    - Get Started With Jetson Nano Developer Kit: https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write
    - JetPack SDK 4.6 Release Page: https://developer.nvidia.com/embedded/jetpack-sdk-46

3. **Install the jetson-inference from dusty-nv**
   Two way to install jetson-inference.
    - Building the Project from Source: https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md
    - Running the Docker Container: https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-docker.md
      
4. **Download this project**
    ```sh
    streamlit run .\streamlit_stock_app.py
    ```

5. **Run the APP with Streamlit**
    ```sh
    streamlit run .\streamlit_stock_app.py
    ```


## References

- [Stock Market Sentiment Prediction with OpenAI and Python](https://www.insightbig.com/post/stock-market-sentiment-prediction-with-openai-and-python)
- [Algorithmic Trading & Quantitative Analysis Using Python](https://www.udemy.com/course/algorithmic-trading-quantitative-analysis-using-python/?couponCode=ST21MT61124)
- [Financial Programming with Ritvik, CFA](https://www.youtube.com/watch?v=fdFfpEtv5BU&t=289s&ab_channel=FinancialProgrammingwithRitvik%2CCFA)
