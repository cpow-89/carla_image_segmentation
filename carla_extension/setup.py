import random
import carla


def get_n_unique_spawn_points(world, n):
    """Sample a list of n unique spawn points for the given world"""
    max_number_samples = len(world.get_map().get_spawn_points())
    if n <= max_number_samples:
        return random.sample(world.get_map().get_spawn_points(), k=n)
    else:
        print("Number of requested spawn points is to high.")
        print("n has been set to the max value, which is {}.".format(max_number_samples))
        return random.sample(world.get_map().get_spawn_points(), k=max_number_samples)


def create_ego_vehicle_camera_sensors(config_camera_sensors, blueprint_library):
    ego_camera_sensors = []
    for camera_sensor_name, camera_sensor_values in config_camera_sensors.items():
        camera_blueprint = blueprint_library.find("sensor.camera.{}".format(camera_sensor_name))
        for attr_name, attr_value in camera_sensor_values["attributes"].items():
            camera_blueprint.set_attribute(attr_name, attr_value)
        ego_camera_sensors.append(camera_blueprint)
        camera_transform = carla.Transform(carla.Location(x=camera_sensor_values["location"]["x"],
                                                          y=camera_sensor_values["location"]["y"],
                                                          z=camera_sensor_values["location"]["x"]))
        ego_camera_sensors.append((camera_blueprint, camera_transform))
    return ego_camera_sensors
