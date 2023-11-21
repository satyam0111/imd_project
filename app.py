import streamlit as st
import requests
import numpy as np
from PIL import Image

# API URL and headers
url = "https://infcloud.navan.ai/inference?model_name=1637745904_3441ccc1"
headers = {'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoiMTYzNzc0NTkwNCIsIm1vZGVsX2lkIjoiMzQ0MWNjYzEifQ.AU0Qu5jjlJc7T1QO6FpQAp-9FWKz4EqiRsesEsmFKnE'}

def classify_image(image_file):
    # Read the image file
    image = Image.open(image_file)

    # Convert the image to a format compatible with the API
    image_data = np.asarray(image).astype('uint8')
    image_data = image_data.reshape((1, image_data.shape[0], image_data.shape[1], image_data.shape[2]))

    # Prepare the payload for the API request
    payload = {
        'data': '''{
            "input":
            [
              {
                "name": "input_1",
                "data_type": "TYPE_FP32",
                "size": [
                  240,
                  240,
                  3
                ]
              }
            ],
            "output":
            [
              {
                "name": "dense_3",
                "data_type": "TYPE_FP32",
                "size": [
                  4
                ]
              }
            ]
          }'''
    }

    # Send the image data to the API
    files = [('file', ('<file>', image_file.read(), 'image/jpeg'))]
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    final=eval(response.text)
    st.write(final)
    st.write(type(final))
    class_id=final[0][2]
    st.write(class_id)
    # Interpret the class ID and classify the image
    if class_id == "0":
        classification = "Segmentation Paper"
    elif class_id == "1":
        classification = "Grade 1"
    elif class_id == "2":
        classification = "Grade 2"
    else:
        classification = "Grade 3"

    return classification

# Initialize the Streamlit app
st.title("Segmentation Paper or Grade Classification")

# Upload the image file
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

if uploaded_file is None:
    st.info("Please upload an image file")
else:
    # Classify the uploaded image
    classification = classify_image(uploaded_file)

    # Display the classification results
    st.success("The uploaded image is classified as '{}'".format(classification))
