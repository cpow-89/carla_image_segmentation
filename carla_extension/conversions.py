import numpy as np


def convert_carla_bgra_image_stream_to_brga_array(carla_bgra_image_stream):
    """Convert a carla brga image stream to an numpy bgra array"""
    flat_brga_array = np.frombuffer(carla_bgra_image_stream.raw_data, dtype=np.dtype("uint8"))
    brga_array = np.reshape(flat_brga_array, (carla_bgra_image_stream.height, carla_bgra_image_stream.width, 4))
    return brga_array


def convert_brga_array_to_seg_mask(brga_array):
    """Convert a numpy brga array to a numpy 2d image segmentation mask"""
    return brga_array[:, :, 2]


def convert_carla_brga_image_stream_to_seg_mask(carla_bgra_image):
    """Convert a carla brga image stream to a numpy 2d image segmentation mask"""
    brga_array = convert_carla_bgra_image_stream_to_brga_array(carla_bgra_image)
    return convert_brga_array_to_seg_mask(brga_array)
