import fiftyone as fo
import os

name = "mini"
dataset_dir = "datasets_processing/data/mini"

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

# Export the dataset
dataset.export(
    export_dir="yolo",
    dataset_type=fo.types.YOLOv5Dataset,
    label_field=label_field,
)
