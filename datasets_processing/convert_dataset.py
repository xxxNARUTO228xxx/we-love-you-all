import datumaro as dm

dataset = dm.Dataset.import_from("data/MockAttach", "voc")
dataset.transform("shapes_to_boxes")
dataset.init_cache()
dataset._data._media_type = dm.Image
dataset.export("output_dataset", "cvat")
