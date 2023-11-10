import os
import shutil
from data_utils import move_files_by_extension


if __name__ == "__main__":
    path_to_dataset = "datasets_processing\data\weapons_images_2fps_src"
    annot_ext = ".xml"

    os.chdir(path_to_dataset)

    if not os.path.exists("./labels"):
        os.mkdir("labels")

    move_files_by_extension('./Images', annot_ext, './labels')

    os.rename("Images", "data")

    print("Fiftyone's Pascal VOC dataset Mock_attack готов!")
