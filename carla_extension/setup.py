import glob
import os
import sys
import random


def set_system_path_to_carla_egg(relative_path):
    try:
        file_name = "carla-*%d.%d-%s.egg" % (
            sys.version_info.major,
            sys.version_info.minor,
            'win-amd64' if os.name == 'nt' else 'linux-x86_64')
        sys.path.append(glob.glob(os.path.join(relative_path, file_name))[0])
    except IndexError:
        pass


def get_n_unique_spawn_points(world, n):
    """Sample a list of n unique spawn points for the given world"""
    max_number_samples = len(world.get_map().get_spawn_points())
    if n <= max_number_samples:
        return random.sample(world.get_map().get_spawn_points(), k=n)
    else:
        print("Number of requested spawn points is to high.")
        print("n has been set to the max value, which is {}.".format(max_number_samples))
        return random.sample(world.get_map().get_spawn_points(), k=max_number_samples)
