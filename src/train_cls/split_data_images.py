import splitfolders


input_folder = "data_clf"

splitfolders.ratio(
    input_folder,
    output="data_clf_split",
    seed=1337,
    ratio=(0.7, 0.2, 0.1),
    group_prefix=None,
    move=False,
)
