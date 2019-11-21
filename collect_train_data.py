import json
import time
import os
import argparse
import carla
import carla_extension.sim_setup as sim_setup
import carla_extension.sim_teardown as sim_teardown
import carla_extension.sim_to_disk as save_to_disk


def main():
    parser = create_arg_parser()
    args = parser.parse_args()

    with open(os.path.join(".", "configs", "ego_camera_sensors.json"), "r") as read_file:
        config_camera_sensors = json.load(read_file)

    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)

    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    ego_vehicle_blueprint = blueprint_library.filter("model3")[0]

    rgb_camera_blueprint = sim_setup.create_basic_camera_blueprint(blueprint_library=blueprint_library,
                                                                   camera_type="rgb",
                                                                   attributes=config_camera_sensors["rgb"]["attributes"])
    rgb_camera_location = carla.Transform(carla.Location(x=0.5, z=1.7))
    rgb_camera_output_dir = os.path.join("output", "images")
    save_to_disk.create_directory(rgb_camera_output_dir)

    sem_seg_camera_blueprint = sim_setup.create_basic_camera_blueprint(blueprint_library=blueprint_library,
                                                                       camera_type="semantic_segmentation",
                                                                       attributes=config_camera_sensors["semantic_segmentation"]["attributes"])
    sem_seg_camera_location = carla.Transform(carla.Location(x=0.5, z=1.7))
    sem_seg_camera_output_dir = os.path.join("output", "labels")
    save_to_disk.create_directory(sem_seg_camera_output_dir)

    spawn_points = sim_setup.get_n_unique_spawn_points(world, n=args.n_runs)

    for run_id, spawn_point in enumerate(spawn_points):
        actor_list = []

        try:
            ego_vehicle = world.spawn_actor(ego_vehicle_blueprint, spawn_point)
            ego_vehicle.set_autopilot(True)
            actor_list.append(ego_vehicle)

            rgb_camera = world.spawn_actor(rgb_camera_blueprint, rgb_camera_location, attach_to=ego_vehicle)
            actor_list.append(rgb_camera)

            sem_seg_camera = world.spawn_actor(sem_seg_camera_blueprint, sem_seg_camera_location, attach_to=ego_vehicle)
            actor_list.append(sem_seg_camera)

            print("Run {} is set up".format(run_id))
            time.sleep(4)

            print("Run {} collects data".format(run_id))

            rgb_camera.listen(lambda image: save_to_disk.save_rgb_image(image, rgb_camera_output_dir, run_id))
            sem_seg_camera.listen(lambda image: save_to_disk.save_seg_mask(image, sem_seg_camera_output_dir, run_id))

            time.sleep(args.run_duration_in_seconds)

            print("Run {} done".format(run_id))

        finally:
            sim_teardown.clean_up(actor_list)


def create_arg_parser():
    parser = argparse.ArgumentParser(description="Collect data for image segmentation")
    parser.add_argument("-n",
                        "--n_runs",
                        type=int,
                        metavar="",
                        required=True,
                        help="Number of runs from different spawn points")

    parser.add_argument("-d",
                        "--run_duration_in_seconds",
                        type=int,
                        metavar="",
                        required=True,
                        help="Duration every single run gets per spawn point")

    return parser


if __name__ == '__main__':
    main()
