from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
print("lo00000000000000000000000000000000ading the model")


model = tf.keras.models.load_model(os.path.join(os.getcwd(),"model","pneumonia_cnn.keras"))

print("loading finished")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    print("hrrrrrrr")
    IMG_SIZE = (224, 224)
    img = Image.open(io.BytesIO(await file.read())).convert("RGB")
    img = img.resize(IMG_SIZE)

# 3. Convert to numpy
    img_array = np.array(img) / 255.0

# 4. Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    print("Raw prediction:", prediction)

    prob = prediction[0][0]
    print("probability is::::::::::::::::::::::",prob)
    if prob > 0.5:
        return {
            "result": "Pneumonia Detected",
            "confidence": round(float(prob) * 100, 2)
        }
    else:
        return {
            "result": "Normal",
            "confidence": round((1 - float(prob)) * 100, 2)
        }
