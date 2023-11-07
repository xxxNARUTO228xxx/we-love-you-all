import os
import shutil


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
