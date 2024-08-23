from tensorflow.keras.models import load_model

# Load the model (use the appropriate file extension based on what you saved)
model = load_model("../saved_models/potato_model.keras")
# or
# model = load_model("../saved_models/potato_model.h5")
# Example input data to test the model (make sure it has the right shape)
import numpy as np

# Suppose your model expects input of shape (1, height, width, channels)
test_input = np.random.rand(1, 64, 64, 3)  # Replace with real data

# Predict using the loaded model
predictions = model.predict(test_input)

# Print the predictions
print(predictions)
