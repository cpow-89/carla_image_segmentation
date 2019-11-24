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


image_segmentation_mask_to_labels = {
    0: "Unlabeled",
    1: "Building",
    2: "Fence",
    3: "Other",
    4: "Pedestrian",
    5: "Pole",
    6: "Road line",
    7: "Road",
    8: "Sidewalk",
    9: "Vegetation",
    10: "Car",
    11: "Wall",
    12: "Traffic sign"
}

labels_to_image_segmentation_mask = {
    "Unlabeled": 0,
    "Building": 1,
    "Fence": 2,
    "Other": 3,
    "Pedestrian": 4,
    "Pole": 5,
    "Road line": 6,
    "Road": 7,
    "Sidewalk": 8,
    "Vegetation": 9,
    "Car": 10,
    "Wall": 11,
    "Traffic sign": 12
}