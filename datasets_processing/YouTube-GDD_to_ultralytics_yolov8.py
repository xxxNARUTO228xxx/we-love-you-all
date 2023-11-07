import os
import shutil
from data_utils import create_yolov8_yaml, move_files


if __name__ == "__main__":
    path_to_dataset = "datasets_processing/data/YouTube-GDD_src"
    test_subset = False

    os.chdir(path_to_dataset)

    path_for_yaml = "data.yaml"
    class_dct = {"0": "person", "1": "weapon"}
    create_yolov8_yaml(path_for_yaml, class_dct, test_subset=test_subset)

    for subset in ["train", "val"]:
        os.makedirs(subset)
        os.makedirs(os.path.join(subset, "images"))
        os.makedirs(os.path.join(subset, "labels"))

        move_files(f"YouTube-GDD\images\{subset}", f"{subset}\images")
        move_files(f"labels\{subset}", f"{subset}\labels")

    os.rename("val", "valid")

    shutil.rmtree("YouTube-GDD", ignore_errors=True)
    shutil.rmtree("labels", ignore_errors=True)

    print("Ultralitics YOLOv8 dataset YouTube-GDD готов!")
