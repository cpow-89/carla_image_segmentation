import os
import carla_extension.setup as carla_setup


carla_setup.set_system_path_to_carla_egg(os.path.join("..", "..", "carla", "PythonAPI", "carla", "dist"))

import carla


def main():
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    print("Done")


if __name__ == '__main__':
    main()
