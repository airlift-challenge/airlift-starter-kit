from airlift.evaluators.utils import doeval
from solution.mysolution import MySolution
import click

@click.command()
@click.option('--scenario-folder',
              default="./scenarios",
              help='Location of the evaluation pkl files')
def run_evaluation(scenario_folder):
    doeval(scenario_folder, MySolution())

if __name__ == "__main__":
    run_evaluation()
