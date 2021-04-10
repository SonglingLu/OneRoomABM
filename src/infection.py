# imports
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd

def generate_infectivity_curves():
    '''
    in:
    -

    out:
    variables with which to plot or sample from


    cite:
    Temporal paper

    Chu

    '''
    s_l_s_symptom_countdown = [0.6432659248014824, -0.07787673726582335, 4.2489459496009125]
    x_symptom_countdown = np.linspace(0, 17, 1000)

    s_l_s_infectivity_density = [20.16693271833812, -12.132674385322815, 0.6322296057082886]
    x_infectivity = np.linspace(-10, 8, 19)

    chu_distance = 2.02

    return [s_l_s_symptom_countdown, x_symptom_countdown, s_l_s_infectivity_density, x_infectivity, chu_distance]

def plot_infectivity_curves(in_array):
    '''
    plot our sampling process with 2 vertically stacked plots

    with titles and labels


    Density plot of # individuals who become infective that day
    - proxy for infectivity

    Lognorm plot of estimated days until symptoms appear

    '''
    fig, ax = plt.subplots(1)
    fig2, ax2 = plt.subplots(1)
    sls_symp_count, x_symp_count, s_l_s_infectivity_density, x_infectivity, distance_multiplier = in_array
    l_shape, l_loc, l_scale = sls_symp_count
    g_shape, g_loc, g_scale = s_l_s_infectivity_density
    countdown_curve = stats.lognorm(s=l_shape, loc=l_loc, scale=l_scale)

    infective_df = pd.DataFrame({'x': list(x_infectivity), 'gamma': list(stats.gamma.pdf(x_infectivity, a=g_shape, loc=g_loc, scale=g_scale))})


    ax.plot(x_symp_count, countdown_curve.pdf(x_symp_count), 'k-', lw=2)

    ax2.plot(x_infectivity, infective_df.gamma)

    return
