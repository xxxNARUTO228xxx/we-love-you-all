import datumaro as dm

dataset = dm.Dataset.import_from("shells", "coco")

# keep only annotated images
dataset.select(lambda item: len(item.annotations) != 0)

# произвести переиндексацию название изображений
# dataset.transform('reindex')

# export the resulting dataset in COCO format
dataset.export("result_dataset", "open_images", save_images=True)
