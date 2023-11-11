from ultralytics import YOLO

model = YOLO("")

res = model.train(data="", epochs=10, batch=1, workers=20,
                  patience=5, save_period=2, seed=20, imgsz=1024)
