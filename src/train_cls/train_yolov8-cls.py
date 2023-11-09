from ultralytics import YOLO

# Load a model
model = YOLO('yolov8x-cls.pt')  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data='data_clf_split', epochs=200, imgsz=64)