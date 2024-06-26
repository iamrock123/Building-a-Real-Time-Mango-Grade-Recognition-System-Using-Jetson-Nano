# Building-a-Real-Time-Mango-Grade-Recognition-System-Using-Jetson-Nano
## Overview

Using AI to identify fruit grades, addressing shortage of fruit screeners during harvest season.

## Main Features

-Reducing training costs by utilizing transfer learning to train object detection models.

-Enhancing recognition accuracy with a multi-faceted detection process designed on Jetson Nano Developer Kit.

-Displaying recognition results in real-time on a mobile application using Google Cloud Platform.

- **Sentiment Prediction**

## How to Run

To run this program, follow these steps:

1. **Create a virtual environment (optional)**
    ```sh
    conda create --name stockApp python==3.10.12
    conda activate stockApp
    ```

2. **Install the Python dependencies**
    ```sh
    pip install -r requirements.txt
    ```

3. **Enter your API key**
    - Edit line 23:
        ```python
        os.environ["NVIDIA_API_KEY"] = "please enter your own api key"
        ```
    - Edit line 30:
        ```python
        api_key = 'please enter your own api key'
        ```

4. **Run the APP with Streamlit**
    ```sh
    streamlit run .\streamlit_stock_app.py
    ```


## References

- [Stock Market Sentiment Prediction with OpenAI and Python](https://www.insightbig.com/post/stock-market-sentiment-prediction-with-openai-and-python)
- [Algorithmic Trading & Quantitative Analysis Using Python](https://www.udemy.com/course/algorithmic-trading-quantitative-analysis-using-python/?couponCode=ST21MT61124)
- [Financial Programming with Ritvik, CFA](https://www.youtube.com/watch?v=fdFfpEtv5BU&t=289s&ab_channel=FinancialProgrammingwithRitvik%2CCFA)
