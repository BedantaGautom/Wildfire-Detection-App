### FOR TRAINING THE MODEL –
1. Open the desired IDE or notebook and create a new Python virtual environment.
```
python -m venv .venv
``` 
2. Download and install PYTORCH and CUDA versions compatible with the system in the environment.
```
!pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
3. Import torch and check whether CUDA detects the device's GPU.
```
import torch
```
```
torch.cuda.is_available()
```
```
print(torch.cuda.get_device_name(0))
```
4. Install ULTRALYTICS and run the code to train the model and test the model.
```
!pip install ultralytics
```
<br>

### FOR DEPLOYING AND RUNNING THE WEB APP –
1. Install the necessary packages from requirements.txt.
```
%pip install requirements.txt.
```
2. Create a file named [NAME].py and write the code to deploy the web app.
3. Run the Streamlit web app.
```
streamlit run [NAME].py
```
4. The web app can be deployed in Streamlit cloud service by uploading the code in the GitHub 
repository.
