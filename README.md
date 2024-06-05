### FOR TRAINING THE MODEL –
1. Open the desired IDE or notebook and create a new Python virtual environment.<br>`python -m venv .venv`
2. Download and install PYTORCH and CUDA versions compatible with the system in the environment.<br>`!pip3 install torch torchvision torchaudio --index-url
https://download.pytorch.org/whl/cu118`<br>
3. Import torch and check whether CUDA detects the device's GPU.<br>`import torch`<br>`torch.cuda.is_available()`<br>`print(torch.cuda.get_device_name(0))`<br>
4. Install ULTRALYTICS and run the code to train the model and test the model.<br>`!pip install ultralytics`<br><br>

### FOR DEPLOYING AND RUNNING THE WEB APP –
1. Install the necessary packages from requirements.txt.<br> `%pip install requirements.txt.`
2. Create a file named [NAME].py and write the code to deploy the web app.<br>
3. Run the Streamlit web app.<br>`streamlit run [NAME].py`
4. The web app can be deployed in Streamlit cloud service by uploading the code in the GitHub 
repository.
