# Environment
from airlift.envs.airlift_env import AirliftEnv
from airlift.envs import PlaneType
from airlift.envs.generators.map_generators import PlainMapGenerator

# Generators
from airlift.envs.generators.world_generators import AirliftWorldGenerator
from airlift.envs.generators.airport_generators import RandomAirportGenerator
from airlift.envs.generators.route_generators import RouteByDistanceGenerator
from airlift.envs.generators.airplane_generators import AirplaneGenerator
from airlift.envs.generators.cargo_generators import StaticCargoGenerator

# Dynamic events
from airlift.envs.events.event_interval_generator import EventIntervalGenerator
from airlift.envs.generators.cargo_generators import DynamicCargoGenerator

# Starter kit solution
from solution.mysolution import MySolution

# Helper methods
from airlift.solutions import doepisode
from eval_solution import write_results

# Maximum number of steps the episode will run
max_cycles = 5000

# Use a plain map (this is faster to generate and captures essential elements of the scenario)
map_generator=PlainMapGenerator()

"""
Create an AirliftEnv using all the generators. There exist multiple generators for each aspect. For example instead of using the
DynamicCargoGenerator we can also use the StaticCargoGenerator.
"""

"""
Uncomment the scenario below that you would like to use.
"""


## A simple scenario with no dynamic events
# env = AirliftEnv(
#         world_generator=AirliftWorldGenerator(
#           plane_types=[PlaneType(id=0, max_range=1.0, speed=0.05, max_weight=5)],
#           airport_generator=RandomAirportGenerator(
#               max_airports=8,
#               make_drop_off_area=True,
#               make_pick_up_area=True,
#               num_drop_off_airports=2,
#               num_pick_up_airports=2,
#               mapgen=map_generator,
#           ),
#           route_generator=RouteByDistanceGenerator(
#               route_ratio=2,
#           ),
#           cargo_generator=StaticCargoGenerator(
#               num_of_tasks=4,
#               max_weight=3,
#               soft_deadline_multiplier=10,
#               hard_deadline_multiplier=20,
#           ),
#           airplane_generator=AirplaneGenerator(num_of_agents=2),
#           max_cycles=max_cycles
#         ),
#     )

## A more complicated scenario with dynamic events
env = AirliftEnv(
        world_generator=AirliftWorldGenerator(
          plane_types=[PlaneType(id=0, max_range=1.0, speed=0.05, max_weight=5)],
          airport_generator=RandomAirportGenerator(
              max_airports=8,
              make_drop_off_area=True,
              make_pick_up_area=True,
              num_drop_off_airports=2,
              num_pick_up_airports=2,
              mapgen=map_generator,
          ),
          route_generator=RouteByDistanceGenerator(
              route_ratio=2,
              poisson_lambda=1/2,
              malfunction_generator=EventIntervalGenerator(
                                        min_duration=10,
                                        max_duration=30),
          ),
          cargo_generator=DynamicCargoGenerator(
              cargo_creation_rate=1 / 100,
              max_cargo_to_create=10,
              num_initial_tasks=40,
              max_weight=3,
              max_stagger_steps=max_cycles / 2,
              soft_deadline_multiplier=10,
              hard_deadline_multiplier=20,
          ),
          airplane_generator=AirplaneGenerator(num_of_agents=2),
          max_cycles=max_cycles
        ),
    )

"""
Run a single episode utilizing the Solution we wrote with the above environment. 
"""
env_info, metrics, time_taken, total_solution_time, step_metrics = \
  doepisode(env,
            solution=MySolution(),
            render=True,
            render_sleep_time=0, # Set this to 0.1 to slow down the simulation
            env_seed=100,
            solution_seed=200,
            capture_metrics=True)

print("Missed Deliveries: {}".format(metrics.missed_deliveries))
print("Lateness:          {}".format(metrics.total_lateness))
print("Total flight cost: {}".format(metrics.total_cost))
print("Score:             {}".format(metrics.score))

write_results(env_info, step_metrics)

