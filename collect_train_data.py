import json
import os
import carla
import carla_extension.setup as carla_setup


def main():
    with open(os.path.join(".", "configs", "camera_sensors.json"), "r") as read_file:
        config_camera_sensors = json.load(read_file)

    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)

    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    spawn_points = carla_setup.get_n_unique_spawn_points(world, n=1)

    ego_vehicle_camera_sensors = carla_setup.create_ego_vehicle_camera_sensors(config_camera_sensors, blueprint_library)

    print("Done")


if __name__ == '__main__':
    main()
