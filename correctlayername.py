import cv2
import numpy as np
from google.protobuf import text_format
from caffe.proto import caffe_pb2

# Correct paths to your files
prototxt_path = "./model/deploy.prototxt"
caffemodel_path = "./model/mobilenet_iter_73000.caffemodel"

# Function to read and print layer names from prototxt
def read_prototxt(prototxt_path):
    with open(prototxt_path, 'r') as f:
        net = caffe_pb2.NetParameter()
        text_format.Merge(f.read(), net)
        return net

def get_last_conv_layer(prototxt_path):
    net = read_prototxt(prototxt_path)
    last_conv_layer = None
    for layer in net.layer:
        if layer.type == 'Convolution':
            last_conv_layer = layer.name
    return last_conv_layer

# Get the correct last convolutional layer name
last_conv_layer_name = get_last_conv_layer(prototxt_path)
print(f"Last convolutional layer name: {last_conv_layer_name}")

# Load the model
try:
    net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
    print("Model loaded successfully.")
except cv2.error as e:
    print(f"Error loading model: {e}")
    net = None

# Initialize the camera
cap = cv2.VideoCapture(0)
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

# Proceed only if the model is loaded and a frame is captured
if net is not None and ret:
    # Preprocess the frame (assuming the model expects a 224x224 image)
    blob = cv2.dnn.blobFromImage(frame, scalefactor=1.0, size=(224, 224), mean=(104, 117, 123))

    # Set the input to the model
    net.setInput(blob)

    # Perform inference
    output = net.forward(last_conv_layer_name)

    # Print output (depends on the model, usually a classification or detection result)
    print("Output from the model:", output)

# Release the camera
cap.release()