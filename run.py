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
VIZ_PARAMS = 'config/viz.json' ## make this file

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

        # one room viz with default inputs
        temp = load_parameters(SCALE_MODEL_PARAMS)
        one_room(temp['input_dir'], temp['output_dir'], False) #implement additional input variable in one_room()



    if 'visualize' in targets:
        # one room viz using website / airavata inputs
        temp = load_parameters(SCALE_MODEL_PARAMS)
        temp_viz = load_parameters(VIZ_PARAMS)
        one_room(temp['input_dir'], temp['output_dir'], True) #implement viz params and viz code
        # visualize_infection() takes in timesteps of infection and returns a plotted visualization w/ red = inf, green = not inf

        # plot_infection() demonstrates the 'animations' with an XY plot of number individuals infected (X) vs timesteps of 5 mins (Y)


        # TODO: get help from Kaushik w/ Airavata inputs

        # TODO: get help from team for website integration


        # set up variables

    return


if __name__ == '__main__':
    # run via:
    # python run.py analysis
    targets = sys.argv[1:]
    main(targets)
