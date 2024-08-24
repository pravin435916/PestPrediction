import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# Load the model
model = load_model("../saved_models/potato_model.keras")

# Function to preprocess the image
def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))  # Ensure that the size matches the training size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize as per training
    return img_array

# Load and preprocess the image
image_path = '../images/2.JPG'
img_array = preprocess_image(image_path)

# Make predictions
predictions = model.predict(img_array)

# Print raw predictions to inspect them
print(f"Raw Predictions: {predictions}")

# Assuming there are 3 classes: Early Blight, Healthy, Late Blight
class_labels = ['Healthy','Early Blight', 'Late Blight']

# Get the index of the highest probability
predicted_index = np.argmax(predictions)

# Get the corresponding class label
predicted_class = class_labels[predicted_index]

# Get the confidence of the prediction
confidence = predictions[predicted_index]

print(f"Predicted Class: {predicted_class}, Confidence: {confidence}")
