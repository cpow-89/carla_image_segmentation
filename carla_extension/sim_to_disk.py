import carla_extension.conversions as conversions
from PIL import Image
import os


def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def save_seg_mask(carla_bgra_image, output_dir, run_id):
    file_path = os.path.join(output_dir, "run{}_fr_{}.png".format(run_id, carla_bgra_image.frame_number))
    image_seg_mask = conversions.convert_carla_brga_image_stream_to_seg_mask(carla_bgra_image)
    im = Image.fromarray(image_seg_mask)
    im.save(file_path)


def save_rgb_image(carla_rgb_image, output_dir, run_id):
    file_path = os.path.join(output_dir, "run{}_fr_{}.png".format(run_id, carla_rgb_image.frame_number))
    carla_rgb_image.save_to_disk(file_path)
