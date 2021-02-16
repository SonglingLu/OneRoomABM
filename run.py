import sys
import json
import shutil

import numpy as np
import pandas as pd
import math
from scipy import stats
import matplotlib.pyplot as plt

sys.path.insert(0, 'src')

from etl import get_data
from scale_model import init_positions, droplet_infect, return_aerosol_transmission_rate, get_distance, get_dist_multiplier, one_room

# Targets:
DATA_PARAMS = 'config/default_config.json'
SCALE_MODEL_PARAMS = 'config/scale_room.json'

def load_parameters(filepath):
    '''
    Loads input and output directories
    '''
    with open(filepath) as fp:
        parameter = json.load(fp)

    return parameter


def main(targets):
    '''
    Runs the main project pipeline logic, given the targets.
    '''

    if 'test' in targets: # Visualize the time until infectiveness of a newly infected individual
        # temp = load_parameters(DATA_PARAMS)
        # data = get_data(temp['input_dir'], temp['output_dir'])

        temp = load_parameters(SCALE_MODEL_PARAMS)
        one_room(temp['input_dir'], temp['output_dir'])

    return


if __name__ == '__main__':
    # run via:
    # python run.py analysis
    targets = sys.argv[1:]
    main(targets)
