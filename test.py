# This file is used to locally verify your http server acts as expected
# Run it as: 'python3 test.py (file_id of training images in google drive)'

import sys
import requests
from io import BytesIO
from PIL import Image

#File_id of file in google drive
file_id = sys.argv[1:][0]

#Serverless approach: Just need fileId to download training images from folder UploadedImgs/
model_inputs = {"file_id": file_id }
res = requests.post('http://localhost:8000/', json = model_inputs)

#Get back file_id of the newly created model.ckpt stored now in googledrive folder Models/
print(res.json())