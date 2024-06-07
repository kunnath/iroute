import cv2
import numpy as np

# Correct paths to your files
prototxt_path = "./model/deploy.prototxt"
caffemodel_path = "./model/mobilenet_iter_73000.caffemodel"

# Load the model
try:
    net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
    print(net)
    print("Model loaded successfully.")
except cv2.error as e:
    print(f"Error loading model: {e}")

# Initialize the camera
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    print("Camera opened successfully.")

# Capture a frame
ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame from camera.")
else:
    print("Frame captured successfully.")

# Preprocess the frame (assuming the model expects a 224x224 image)
blob = cv2.dnn.blobFromImage(frame, scalefactor=1.0, size=(224, 224), mean=(104, 117, 123))

# Set the input to the model
net.setInput(blob)

# Perform inference
output = net.forward()

# Print output (depends on the model, usually a classification or detection result)
print("Output from the model:", output)

# Release the camera
cap.release()