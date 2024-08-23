from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from tensorflow import keras

app = FastAPI()

# Allow CORS for frontend running on localhost:5173
origins = [
    "http://localhost",
    "http://localhost:5173",  # Port where frontend is running
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models on startup
@app.on_event("startup")
async def load_models():
    global potato_MODEL, tomato_MODEL, pepper_MODEL, groundnut_MODEL, blackgram_MODEL
    try:
        potato_MODEL = tf.keras.models.load_model("../saved_models/potato_model.keras")
        # tomato_MODEL = tf.keras.models.load_model("../saved_models/tomato_model")
        # pepper_MODEL = tf.keras.models.load_model("../saved_models/pepper_model")
        # groundnut_MODEL = tf.keras.models.load_model("../saved_models/groundnut_model")
        # blackgram_MODEL = tf.keras.models.load_model("../saved_models/blackgram_model")
    except Exception as e:
        raise RuntimeError(f"Error loading models: {e}")

# Class names
p_CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]
t_CLASS_NAMES = ['Early Blight', 'Late Blight', 'YellowLeaf Curl Virus', 'Mosaic Virus', 'Healthy']
pep_CLASS_NAMES = ['Bell Bacterial Spot', 'Bell Healthy']
g_CLASS_NAMES = ['Early Leaf Spot', 'Early Rust', 'Healthy Leaf', 'Late Leaf Spot', 'Nutrition Deficiency', 'Rust']
b_CLASS_NAMES = ['Anthracnose', 'Healthy', 'Leaf Crinkle', 'Powdery Mildew', 'Yellow Mosaic']

# Image preprocessing function
def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data)).convert("RGB")  # Ensure the image is in RGB format
    image = image.resize((256, 256))  # Resize the image to the required input size
    image = np.array(image) / 255.0  # Normalize the image to [0, 1]
    return image

# Prediction route for different plants
@app.post("/predict/{plant}")
async def predict(plant: str, file: UploadFile = File(...)):
    # Validate plant type
    valid_plants = ["potato", "tomato", "pepper", "groundnut", "blackgram"]
    if plant not in valid_plants:
        raise HTTPException(status_code=400, detail="Invalid plant type")

    # Read and preprocess the image
    try:
        image = read_file_as_image(await file.read())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {e}")

    img_batch = np.expand_dims(image, 0)  # Add a batch dimension

    # Make predictions based on the selected plant type
    try:
        if plant == "potato":
            predictions = potato_MODEL.predict(img_batch)
            predicted_class = p_CLASS_NAMES[np.argmax(predictions[0])]
        # elif plant == "tomato":
        #     predictions = tomato_MODEL.predict(img_batch)
        #     predicted_class = t_CLASS_NAMES[np.argmax(predictions[0])]
        # elif plant == "pepper":
        #     predictions = pepper_MODEL.predict(img_batch)
        #     predicted_class = pep_CLASS_NAMES[np.argmax(predictions[0])]
        # elif plant == "groundnut":
        #     predictions = groundnut_MODEL.predict(img_batch)
        #     predicted_class = g_CLASS_NAMES[np.argmax(predictions[0])]
        # elif plant == "blackgram":
        #     predictions = blackgram_MODEL.predict(img_batch)
        #     predicted_class = b_CLASS_NAMES[np.argmax(predictions[0])]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {e}")

    confidence = np.max(predictions[0])
    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }

# Main function to run the server
if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
