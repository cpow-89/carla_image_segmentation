# Source: https://github.com/carla-simulator/carla/blob/master/PythonAPI/examples/spawn_npc.py
# File is a slightly modified version of the original example code

"""Spawn NPCs into the simulation"""

import argparse
import logging
import random
import carla


def main():
    parser = create_arg_parser()
    args = parser.parse_args()

    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

    actor_list = []
    client = carla.Client(args.host, args.port)
    client.set_timeout(2.0)

    try:

        world = client.get_world()
        blueprints = world.get_blueprint_library().filter("vehicle.*")

        if args.safe:
            blueprints = [x for x in blueprints if int(x.get_attribute("number_of_wheels")) == 4]
            blueprints = [x for x in blueprints if not x.id.endswith("isetta")]
            blueprints = [x for x in blueprints if not x.id.endswith("carlacola")]

        spawn_points = world.get_map().get_spawn_points()
        number_of_spawn_points = len(spawn_points)

        if args.number_of_vehicles < number_of_spawn_points:
            random.shuffle(spawn_points)
        elif args.number_of_vehicles > number_of_spawn_points:
            msg = "requested %d vehicles, but could only find %d spawn points"
            logging.warning(msg, args.number_of_vehicles, number_of_spawn_points)
            args.number_of_vehicles = number_of_spawn_points

        batch = []
        for n, transform in enumerate(spawn_points):
            if n >= args.number_of_vehicles:
                break
            blueprint = random.choice(blueprints)
            if blueprint.has_attribute("color"):
                color = random.choice(blueprint.get_attribute("color").recommended_values)
                blueprint.set_attribute("color", color)
            blueprint.set_attribute("role_name", "autopilot")
            batch.append(carla.command.SpawnActor(blueprint, transform).
                         then(carla.command.SetAutopilot(carla.command.FutureActor, True)))

        for response in client.apply_batch_sync(batch):
            if response.error:
                logging.error(response.error)
            else:
                actor_list.append(response.actor_id)

        print("spawned %d vehicles, press Ctrl+C to exit." % len(actor_list))

        while True:
            world.wait_for_tick()

    finally:
        print("\ndestroying %d actors" % len(actor_list))
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])


def create_arg_parser():
    parser = argparse.ArgumentParser(description="Script for spawning random npc`s")
    parser.add_argument("--host",
                        metavar="H",
                        default="127.0.0.1",
                        help="IP of the host server (default: 127.0.0.1)")
    parser.add_argument("-p",
                        "--port",
                        metavar="P",
                        default=2000,
                        type=int,
                        help="TCP port to listen to (default: 2000)")
    parser.add_argument("-n",
                        "--number-of-vehicles",
                        metavar="N",
                        default=10,
                        type=int,
                        help="number of vehicles (default: 10)")
    parser.add_argument("-d",
                        "--delay",
                        metavar="D",
                        default=2.0,
                        type=float,
                        help="delay in seconds between spawns (default: 2.0)")
    parser.add_argument("--safe",
                        action="store_true",
                        help="avoid spawning vehicles prone to accidents")
    return parser


if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print("\ndone.")
