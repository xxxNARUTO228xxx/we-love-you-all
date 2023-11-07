import os
from data_utils import get_label_from_pascal_voc_xml
from glob import glob

if __name__ == "__main__":
    path_to_pascal_voc_xmls_dir = (
        "datasets_processing\data\weapons_images_2fps_src\Images"
    )

    search_extension_mask = os.path.join(path_to_pascal_voc_xmls_dir, "*.xml")
    xml_files_paths = glob(search_extension_mask)

    datasets_labels = set()
    for xml_file_path in xml_files_paths:
        labels = get_label_from_pascal_voc_xml(xml_file_path)
        if labels:
            datasets_labels.update(set(labels))

    datasets_labels = list(datasets_labels)
    for idx, label in enumerate(datasets_labels):
        print(idx, label)
