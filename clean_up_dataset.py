import os
from shutil import copyfile
from carla_extension.sim_to_disk import create_directory


def clean_up_file_names_preserving_run_id(path):
    files = os.listdir(path)

    for index, file in enumerate(files):
        frame_info = file.split("_")[-1]
        new_file_name = file.replace(frame_info, "".join([str(index), ".png"]))
        os.rename(os.path.join(path, file),
                  os.path.join(path, new_file_name))


def list_all_img_files_that_have_label():
    image_files = os.listdir(os.path.join(".", "output", "images"))
    label_files = os.listdir(os.path.join(".", "output", "labels"))
    return set(image_files) & set(label_files)


def create_validation_set_file(valid_run_list):
    source_file_list = os.listdir(os.path.join(".", "output", "images"))
    complete_data_file_list = list_all_img_files_that_have_label()

    valid_file_name_list = []
    for file in complete_data_file_list:
        run_id = file.split("_")[0].replace("run", "")
        if file in source_file_list:
            if run_id in valid_run_list:
                valid_file_name_list.append(file)

    with open(os.path.join(".", "dataset", "valid.txt"), 'w') as f:
        for item in valid_file_name_list:
            f.write("%s\n" % item)


def copy_valid_image_files_to_dataset(src_name):
    dst_dir = os.path.join(".", "dataset", src_name)
    create_directory(dst_dir)
    src_dir = os.path.join(".", "output", src_name)
    source_file_list = os.listdir(os.path.join(".", "output", src_name))
    complete_data_file_list = list_all_img_files_that_have_label()

    for file in complete_data_file_list:
        if file in source_file_list:
            copyfile(os.path.join(src_dir, file),
                     os.path.join(dst_dir, file))
