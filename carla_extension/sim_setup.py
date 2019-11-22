import random


def get_n_unique_spawn_points(world, n):
    """Sample a list of n unique spawn points for the given world"""
    max_number_samples = len(world.get_map().get_spawn_points())
    if n <= max_number_samples:
        return random.sample(world.get_map().get_spawn_points(), k=n)
    else:
        print("Number of requested spawn points is to high.")
        print("n has been set to the max value, which is {}.".format(max_number_samples))
        return random.sample(world.get_map().get_spawn_points(), k=max_number_samples)


def create_basic_camera_blueprint(blueprint_library, camera_type, attributes):
    camera_blueprint = blueprint_library.find("sensor.camera.{}".format(camera_type))
    for name, value in attributes.items():
        camera_blueprint.set_attribute(name, value)

    return camera_blueprint
