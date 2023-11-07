import fiftyone as fo
import os

name = "YouTube-GDD"
dataset_dir = "voc"

# The splits to load
splits = ["train", "val"]

# Load the dataset, using tags to mark the samples in each split
dataset = fo.Dataset(name)
for split in splits:
    dataset.add_dir(
        dataset_dir=dataset_dir,
        dataset_type=fo.types.VOCDetectionDataset,
        split=split,
        tags=split,
    )

# View summary info about the dataset
print(dataset)

# Print the first few samples in the dataset
print(dataset.head())

label_field = "ground_truth"

# Export the dataset
dataset.export(
    export_dir="cvat",
    dataset_type=fo.types.CVATImageDataset,
    label_field=label_field,
)

os.rename("cvat\data", "cvat\images")
os.rename("cvat\labels.xml", "cvat\annotations.xml")
