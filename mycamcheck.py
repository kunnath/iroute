import cv2
import numpy as np
import time

# Correct paths to your files
prototxt_path = "./model/deploy.prototxt"
caffemodel_path = "./model/mobilenet_iter_73000.caffemodel"

# Load the model
try:
    net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
except cv2.error as e:
    print(f"Error loading model: {e}")
    exit()

# Define the list of class labels MobileNet SSD was trained to detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

def capture_image(cap):
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return None
    return frame

def detect_objects(image):
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    
    net.setInput(blob)
    detections = net.forward()

    objects = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:  # Confidence threshold
            idx = int(detections[0, 0, i, 1])
            label = CLASSES[idx]
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            objects.append({
                "label": label,
                "confidence": confidence,
                "box": (startX, startY, endX, endY)
            })

    return objects

def calculate_speed(objects1, objects2, time_diff):
    speeds = []
    for obj1 in objects1:
        for obj2 in objects2:
            if obj1['label'] == obj2['label']:
                (x1, y1) = ((obj1['box'][0] + obj1['box'][2]) / 2, (obj1['box'][1] + obj1['box'][3]) / 2)
                (x2, y2) = ((obj2['box'][0] + obj2['box'][2]) / 2, (obj2['box'][1] + obj2['box'][3]) / 2)
                displacement = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                speed = displacement / time_diff
                speeds.append({
                    "label": obj1['label'],
                    "speed": speed,
                    "displacement": displacement,
                    "time_diff": time_diff
                })
    return speeds

def draw_predictions(image, objects):
    for obj in objects:
        (startX, startY, endX, endY) = obj['box']
        label = "{}: {:.2f}%".format(obj['label'], obj['confidence'] * 100)
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
        y = startY - 15 if startY - 15 > 15 else startY + 15
        cv2.putText(image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    ret, frame1 = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return

    while True:
        start_time = time.time()
        frame2 = capture_image(cap)
        if frame2 is None:
            break

        objects1 = detect_objects(frame1)
        objects2 = detect_objects(frame2)

        time_diff = time.time() - start_time
        speeds = calculate_speed(objects1, objects2, time_diff)

        for speed_info in speeds:
            print(f"Object: {speed_info['label']}, Speed: {speed_info['speed']:.2f} pixels/sec, Displacement: {speed_info['displacement']:.2f} pixels, Time Difference: {speed_info['time_diff']:.2f} sec")

        # Display the frame with detected objects
        frame_with_predictions = draw_predictions(frame2, objects2)
        cv2.imshow("Image", frame_with_predictions)

        frame1 = frame2

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()