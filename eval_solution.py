from airlift.evaluators.utils import doeval, doeval_single_episode
from solution.mysolution import MySolution
import os
import time
import click
import csv

def write_results(env_info, step_metrics):
    timestr = time.strftime("%Y-%m-%d-%H%M%S")
    with open("envinfo_{}.csv".format(timestr), 'w', newline='') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(env_info._fields)
        csvwriter.writerow(env_info)
    with open("metrics_{}.csv".format(timestr), 'w', newline='') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(("step",) + step_metrics[0]._fields)
        for step, metric in enumerate(step_metrics):
            csvwriter.writerow((step,) + metric)

@click.command()
@click.option('--scenarios',
              default="./scenarios",
              help='Folder containing the evaluation pkl files (or path to a single pkl file to run)')
@click.option('--solution-seed',
              type=int,
              default=123,
              help='Starting seed for the solution')
@click.option('--env-seed',
              type=int,
              default=44,
              help='Seed for the environment (when running a single pkl file)')
@click.option('--render/--no-render',
              default=False,
              help='Render the episode (rendering only works when running a single pkl file)')
@click.option('--render-mode',
              default="human",
              help='Render mode ("human" or "video")')
def run_evaluation(scenarios, solution_seed, env_seed, render, render_mode):
    """Evaluates solution against a set of scenario pkl files, or a single pkl file. csv files will be written with results."""
    if os.path.isdir(scenarios):
        doeval(scenarios, MySolution(), start_solution_seed=solution_seed)
    elif os.path.isfile(scenarios):
        env_info, metrics, time_taken, total_solution_time, step_metrics = \
            doeval_single_episode(
                test_pkl_file=scenarios,
                env_seed=env_seed,
                solution=MySolution(),
                solution_seed=solution_seed,
                render=render,
                render_mode=render_mode)
        write_results(env_info, step_metrics)
    else:
        raise Exception("Scenarios not found")

if __name__ == "__main__":
    run_evaluation()
