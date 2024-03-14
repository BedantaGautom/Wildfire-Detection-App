import streamlit as st  # type: ignore
import cv2
from ultralytics import YOLO
import requests # type: ignore
from PIL import Image
import os
from glob import glob
from numpy import random
import io

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Function to load the YOLO model
@st.cache_resource
def load_model(model_path):
    model = YOLO(model_path)
    return model

# Function to predict objects in the image
def predict_image(model, image, conf_threshold, iou_threshold):
    # Predict objects using the model
    res = model.predict(
        image,
        conf=conf_threshold,
        iou=iou_threshold,
        device='cpu',
    )
    
    class_name = model.model.names
    classes = res[0].boxes.cls
    class_counts = {}
    
    # Count the number of occurrences for each class
    for c in classes:
        c = int(c)
        class_counts[class_name[c]] = class_counts.get(class_name[c], 0) + 1

    # Generate prediction text
    prediction_text = 'Predicted '
    for k, v in sorted(class_counts.items(), key=lambda item: item[1], reverse=True):
        prediction_text += f'{v} {k}'
        
        if v > 1:
            prediction_text += 's'
        
        prediction_text += ', '

    prediction_text = prediction_text[:-2]
    if len(class_counts) == 0:
        prediction_text = "No objects detected"

    # Calculate inference latency
    latency = sum(res[0].speed.values())  # in ms, need to convert to seconds
    latency = round(latency / 1000, 2)
    prediction_text += f' in {latency} seconds.'

    # Convert the result image to RGB
    res_image = res[0].plot()
    res_image = cv2.cvtColor(res_image, cv2.COLOR_BGR2RGB)
    
    return res_image, prediction_text

def main():
    # Set Streamlit page configuration
    st.set_page_config(
        page_title="Wildfire Detection",
        page_icon="🔥",
        initial_sidebar_state="collapsed",
    )

    # Set custom CSS styles
    st.markdown(
        """
        <style>
        .container {
            max-width: 800px;
        }
        .title {
            text-align: center;
            font-size: 35px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .description {
            margin-bottom: 30px;
        }
        .instructions {
            margin-bottom: 20px;
            padding: 10px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # App title
    st.markdown("<div class='title'>Wildfire Detection</div>", unsafe_allow_html=True)

    # Description

    st.markdown(
    """
    <div style='text-align: center;'>
        <p>Welcome to our Wildfire Detection App! Powered by the <a href='https://github.com/ultralytics/ultralytics'>YOLOv8</a> detection model trained on the <a href='https://github.com/gaiasd/DFireDataset'>D-Fire: an image dataset for fire and smoke detection</a>.</p>
        <h3>📸 <strong>Try It Out!</strong></h3>
        <p>Experience the effectiveness of our detection model by uploading an image.</p>
    </div>
    """,
    unsafe_allow_html=True
)

    # Add a separator
    st.markdown("---")

    # Model selection
    col1, col2 = st.columns(2)
    with col1:
        model_type = st.radio("Select Model Type", ("Fire Detection", "General"), index=0)

    models_dir = "general-models" if model_type == "General" else "fire-models"
    model_files = [f.replace(".pt", "") for f in os.listdir(models_dir) if f.endswith(".pt")]
    
    with col2:
        selected_model = st.selectbox("Select Model Size", sorted(model_files), index=2)

    # Model and general info
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("What is General?"):
            st.caption("The General model is an additional model that was added for demonstration purposes.")
            st.caption("It is pre-trained on the COCO dataset, which consists of various objects across 80 classes.")
            st.caption("Please note that this model may not be optimized specifically for fire detection.")
            st.caption("For accurate fire and smoke detection, it is recommended to choose the Fire Detection model.")
            st.caption("The General model can be used to detect objects commonly found in everyday scenes.")
    
    with col2:
        with st.expander("Size Information"):
            st.caption("Models are available in different sizes, indicated by n, s, m, and l.")
            st.caption("- n: Nano")
            st.caption("- s: Small")
            st.caption("- m: Medium")
            st.caption("- l: Large")
            st.caption("The larger the model, the more precise the detections, but the slower the inference time.")
            st.caption("On the other hand, smaller models are faster but may sacrifice some precision.")
            st.caption("Choose a model based on the trade-off between speed and precision that best suits your needs.")

    # Load the selected model
    model_path = os.path.join(models_dir, selected_model + ".pt") #type: ignore
    model = load_model(model_path)

    # Add a section divider
    st.markdown("---")

    # Set confidence and IOU thresholds
    col1, col2 = st.columns(2)
    with col2:
        conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.20, 0.05)
        with st.expander("What is Confidence Threshold?"):
            st.caption("The Confidence Threshold is a value between 0 and 1.")
            st.caption("It determines the minimum confidence level required for an object detection.")
            st.caption("If the confidence of a detected object is below this threshold, it will be ignored.")
            st.caption("You can adjust this threshold to control the number of detected objects.")
            st.caption("Lower values make the detection more strict, while higher values allow more detections.")
    with col1:
        iou_threshold = st.slider("IOU Threshold", 0.0, 1.0, 0.5, 0.05)
        with st.expander("What is IOU Threshold?"):
            st.caption("The IOU (Intersection over Union) Threshold is a value between 0 and 1.")
            st.caption("It determines the minimum overlap required between the predicted bounding box")
            st.caption("and the ground truth box for them to be considered a match.")
            st.caption("You can adjust this threshold to control the precision and recall of the detections.")
            st.caption("Higher values make the matching more strict, while lower values allow more matches.")

    # Add a section divider
    st.markdown("---")

    # Image selection
    image = None
    image_source = st.radio("Select image source:", ("Upload from Computer"))
    if image_source == "Upload from Computer":
        # File uploader for image
        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
        else:
            image = None

    if image:
        # Display the uploaded image
        with st.spinner("Detecting"):
            prediction, text = predict_image(model, image, conf_threshold, iou_threshold)
            st.image(prediction, caption="Prediction", use_column_width=True)
            st.success(text)
        
        prediction = Image.fromarray(prediction)

        # Create a BytesIO object to temporarily store the image data
        image_buffer = io.BytesIO()

        # Save the image to the BytesIO object in PNG format
        prediction.save(image_buffer, format='PNG')

        # Create a download button for the image
        st.download_button(
            label='Download Prediction',
            data=image_buffer.getvalue(),
            file_name='prediciton.png',
            mime='image/png'
        )

        
if __name__ == "__main__":
    main()
