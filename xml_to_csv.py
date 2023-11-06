from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import multiprocessing
from tqdm import tqdm
import argparse


def parse_file(source_path: Path):
    with open(source_path, "r") as f:
        data = BeautifulSoup(f.read(), "xml")
    
    # collect general data
    # imageID
    image_id = data.find("filename").text

    # source
    source = data.find("source").find("database").text

    output = []
    # num objects in data
    objects = data.find_all("object")
    for obj in objects:
        # classname
        classname = obj.find("name").text
        xmin = float(obj.find("bndbox").find("xmin").text)
        xmax = float(obj.find("bndbox").find("xmax").text)
        ymin = float(obj.find("bndbox").find("ymin").text)
        ymax = float(obj.find("bndbox").find("ymax").text)
        is_truncated = int(obj.find("truncated").text)

        # append row to DF
        output.append({
            "ImageID": image_id,
            "Source": source,
            "ClassName": classname,
            "Confidence": 1,
            "XMin": xmin,
            "XMax": xmax,
            "YMin": ymin,
            "YMax": ymax,
            "IsOccluded": -1,
            "IsTruncated": is_truncated,
            "IsGroupOf": -1,
            "IsDepiction": -1,
            "IsInside": -1
        })

    return pd.DataFrame(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("xml_to_csv", "convert xml image markup to csv")
    parser.add_argument("--input_dir", "-i", type=Path, required=True)
    parser.add_argument("--output_path", "-o", type=Path, required=True)
    parser.add_argument("--cpu_count", "-c", type=int, required=False, default=multiprocessing.cpu_count())
    
    args = parser.parse_args()

    inputs = list(args.input_dir.glob("*.xml"))
    with multiprocessing.Pool(args.cpu_count) as p:
        results = list(tqdm(p.imap_unordered(parse_file, inputs), total=len(inputs)))
    results = pd.concat(results)
    results.to_csv(args.output_path, index=False)