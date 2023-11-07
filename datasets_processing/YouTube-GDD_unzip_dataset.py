import os
from data_utils import chdir_to_projects_root, unzip_arhive


if __name__ == "__main__":
    path_to_data_zip = "datasets_processing/data/YouTube-GDD.zip"
    path_to_labels_zip = "datasets_processing/data/labels.zip"

    chdir_to_projects_root(а)

    path_to_folder, dataset_name = os.path.split(path_to_data_zip)
    dataset_name = os.path.splitext(dataset_name)[0]
    dataset_name += "_src"
    directory_to_extract_to = os.path.join(path_to_folder, dataset_name)

    unzip_arhive(path_to_data_zip, directory_to_extract_to)
    unzip_arhive(path_to_labels_zip, directory_to_extract_to)
