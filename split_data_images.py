import splitfolders


input_folder = "data_clf/train"

splitfolders.ratio(
    input_folder,
    output="output",
    seed=1337,
    ratio=(0.7, 0.2, 0.1),
    group_prefix=None,
    move=False,
)
