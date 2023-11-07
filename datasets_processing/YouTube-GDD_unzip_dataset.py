import zipfile
import os
from pathlib import Path
from dotenv import find_dotenv


def chdir_to_projects_root():
    project_dir = Path(find_dotenv()).parent
    os.chdir(project_dir)


def unzip_arhive(path_to_zip_file, directory_to_extract_to):
    with zipfile.ZipFile(path_to_zip_file, "r") as zip_ref:
        zip_ref.extractall(directory_to_extract_to)


if __name__ == "__main__":
    path_to_data_zip = "datasets_processing/data/YouTube-GDD.zip"
    path_to_labels_zip = "datasets_processing/data/labels.zip"

    chdir_to_projects_root()
    
    path_to_folder, dataset_name = os.path.split(path_to_data_zip)
    dataset_name = os.path.splitext(dataset_name)[0]
    dataset_name += "_src"
    directory_to_extract_to = os.path.join(path_to_folder, dataset_name)

    unzip_arhive(path_to_data_zip, directory_to_extract_to)
    unzip_arhive(path_to_labels_zip, directory_to_extract_to)
