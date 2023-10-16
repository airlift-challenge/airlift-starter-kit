#!/bin/bash

scenario_folder=${1:-./scenarios}
python eval_solution.py --scenario-folder ${scenario_folder}

$SHELL