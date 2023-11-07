import fiftyone as fo
import os

name = "MockAttack"
dataset_dir = "datasets_processing\data\weapons_images_2fps_src"

# Load the dataset, using tags to mark the samples in each split
dataset = fo.Dataset(name)

dataset.add_dir(
    dataset_dir=dataset_dir,
    dataset_type=fo.types.VOCDetectionDataset,
    tags="train",
)

# View summary info about the dataset
print(dataset)

# Print the first few samples in the dataset
print(dataset.head())

label_field = "ground_truth"

# выполнить remap классов в датасете
view = dataset.map_labels(
    "ground_truth", {"Knife": "weapon", "Short_rifle": "weapon", "Handgun": "weapon"}
)
view.save()

# Export the dataset
dataset.export(
    export_dir="cvat",
    dataset_type=fo.types.CVATImageDataset,
    label_field=label_field,
)

os.rename(os.path.join("cvat", "data"), os.path.join("cvat", "images"))
os.rename(os.path.join("cvat", "labels.xml"), os.path.join("cvat", "annotations.xml"))
