import os
import shutil
import zipfile
from pathlib import Path
from dotenv import find_dotenv


def create_yolov8_yaml(path_for_yaml, class_dct, test_subset=True):
    yaml_file = ["train: ../train/images", "val: ../valid/images"]

    if test_subset:
        yaml_file.append("test: ../test/images")

    yaml_file.extend(["", "", "names:"])

    for key in class_dct:
        yaml_file.append(f"{key}: {class_dct[key]}")

    # Writing to file
    write_file(path_for_yaml, yaml_file)


def write_file(path_for_file, yaml_file):
    with open(path_for_file, "w") as file:
        for line in yaml_file:
            file.write(f"{line}\n")


def get_file_paths(directory):
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]


def move_files(source_dir, target_dir):
    file_names = os.listdir(source_dir)

    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)


def chdir_to_projects_root():
    project_dir = Path(find_dotenv()).parent
    os.chdir(project_dir)


def unzip_arhive(path_to_zip_file, directory_to_extract_to):
    with zipfile.ZipFile(path_to_zip_file, "r") as zip_ref:
        zip_ref.extractall(directory_to_extract_to)
