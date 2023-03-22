from airlift.envs import PlaneType
from airlift.envs.generators.cargo_generators import StaticCargoGenerator, DynamicCargoGenerator
from airlift.envs.airlift_env import AirliftEnv
from airlift.envs.events.event_interval_generator import EventIntervalGenerator
from airlift.envs.generators.airplane_generators import AirplaneGenerator
from airlift.envs.generators.airport_generators import RandomAirportGenerator
from airlift.envs.generators.route_generators import RouteByDistanceGenerator
from airlift.envs.generators.map_generators import PerlinMapGenerator
from airlift.envs.generators.world_generators import AirliftWorldGenerator
from airlift.envs.renderer import FlatRenderer
from airlift.solutions.solutions import doepisode

from solution.mysolution import MySolution

"""
Create an AirliftEnv using all the generators. There exist multiple generators for one thing. For example instead of using the
DynamicCargoGenerator we can also use the StaticCargoGenerator.
"""

"""
Uncomment the scenario below that you would like to use.
"""

## A simple scenario with no dynamic events
env = AirliftEnv(
    AirliftWorldGenerator(
        plane_types=[PlaneType(id=0, max_range=1.0, speed=0.05, max_weight=5)],
        airport_generator=RandomAirportGenerator(mapgen=PerlinMapGenerator(),
                                                 max_airports=8,
                                                 num_drop_off_airports=2,
                                                 num_pick_up_airports=2,
                                                 processing_time=1,
                                                 working_capacity=100,
                                                 airports_per_unit_area=2),
        route_generator=RouteByDistanceGenerator(route_ratio=2.5),
        cargo_generator=StaticCargoGenerator(num_of_tasks=4,
                                             soft_deadline_multiplier=10,
                                             hard_deadline_multiplier=20),
        airplane_generator=AirplaneGenerator(2),
    ),
    renderer=FlatRenderer(show_routes=True)
)

## A more complicated scenario with dynamic events
# env = AirliftEnv(
#     AirliftWorldGenerator(
#         plane_types=[PlaneType(id=0, max_range=1.0, speed=0.05, max_weight=5)],
#         airport_generator=RandomAirportGenerator(mapgen=PerlinMapGenerator(),
#                                                  max_airports=20,
#                                                  num_drop_off_airports=4,
#                                                  num_pick_up_airports=4,
#                                                  processing_time=4,
#                                                  working_capacity=1,
#                                                  airports_per_unit_area=2),
#         route_generator=RouteByDistanceGenerator(malfunction_generator=EventIntervalGenerator(1 / 300, 200, 300),
#                                                  route_ratio=2.5),
#         cargo_generator=DynamicCargoGenerator(cargo_creation_rate=1 / 100,
#                                               soft_deadline_multiplier=4,
#                                               hard_deadline_multiplier=12,
#                                               num_initial_tasks=40,
#                                               max_cargo_to_create=10),
#         airplane_generator=AirplaneGenerator(10),
#     ),
#     renderer=FlatRenderer(show_routes=True)
# )

"""
Run a single episode utilizing the Solution we wrote with the above environment. 
"""
env_info, metrics, time_taken, total_solution_time = \
  doepisode(env,
            solution=MySolution(),
            render=True,
            render_sleep_time=0, # Set this to 0.1 to slow down the simulation
            env_seed=100,
            solution_seed=200)

print("Missed Deliveries: {}".format(metrics.missed_deliveries))
print("Lateness:          {}".format(metrics.total_lateness))
print("Total flight cost: {}".format(metrics.total_cost))
print("Score:             {}".format(metrics.score))
