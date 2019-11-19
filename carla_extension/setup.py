import glob
import os
import sys


def set_system_path_to_carla_egg(relative_path):
    try:
        file_name = "carla-*%d.%d-%s.egg" % (
            sys.version_info.major,
            sys.version_info.minor,
            'win-amd64' if os.name == 'nt' else 'linux-x86_64')
        sys.path.append(glob.glob(os.path.join(relative_path, file_name))[0])
    except IndexError:
        pass
