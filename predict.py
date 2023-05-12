from ultralytics import YOLO
from PIL import Image
import cv2
import json
import time
from tqdm import tqdm
from glob import glob

model = YOLO("./n8_320.pt")

for video_path in tqdm(glob("./videos/*")):
    video_name = video_path.split("/")[-1].split(".")[0]
    res = {
        "res": [],
    }
    results = model.track(video_path, imgsz=320,conf=0.25, show=False, \
                      tracker="bytetrack.yaml", augment=True, stream=True)
    for r in results:
        if (len(r.boxes)):
            res["res"].append(r.boxes[0].xywh.tolist()[0])
        else:
            res["res"].append([])    
    with open(f"./predict/{video_name}.txt", "w") as f:
        f.write(str(res))
    with open(f"./predict/{video_name}.json", "w") as f:
        f.write(json.dumps(res))

print("Done!!!")