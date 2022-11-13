import sys
import requests
import banana_dev as banana
from io import BytesIO
from PIL import Image

#File_id of file in google drive
file_id = sys.argv[1:][0]

#FileId needed to download training images from folder UploadedImgs/
model_inputs = {"file_id": file_id }

api_key = ""
model_key = ""

# Prod - call the training model
res = banana.run(api_key, model_key, model_inputs)

# Get back file_id of model.ckpt in google drive
print(res["modelOutputs"])
