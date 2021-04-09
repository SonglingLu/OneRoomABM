## TODO
# Make this file just functions
# make plots better:
# run 10k make raster is in 'air_flow'
#     This saves the grid overlay to a file
# ventilation calculation is in 'vent_setup'
#     This plots a line between the edges of the vent and the edges of the windows: directionally influences aerosol
# Implement masks as a function of this ventilation / time: i.e. reduced airflow


import math
import random
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import json

# TODO:
# add viz for 1-room infection
# plot infections / time

def init_positions(floor_area, n_students):
    # generate size of room based on circular/square desks
    positions = {}
    # grid desks
    rows = int(math.sqrt(n_students))
    count = 0
    for i in range(rows):
        for j in range(rows):
            positions[count] = [i, j]
            count += 1


    inf_index = random.sample(set(range(n_students)), 2)
    uninf_index = list(range(n_students))
    inf_array = []


    # double check this
    for i in inf_index:
        uninf_index.remove(i)
        inf_array.append(i)
    return uninf_index, inf_index, inf_array, positions




def return_aerosol_transmission_rate(floor_area, mean_ceiling_height,
                            air_exchange_rate,
                            aerosol_filtration_eff, relative_humidity, breathing_flow_rate,
                            exhaled_air_inf, max_viral_deact_rate, mask_passage_prob,
                            max_aerosol_radius=2, primary_outdoor_air_fraction=0.2):
    # Function to return transmission % from smaller droplets dispersing around the room
    # Same as SchoolABM

    mean_ceiling_height_m = mean_ceiling_height * 0.3048 #m3
    room_vol = floor_area * mean_ceiling_height  # ft3
    room_vol_m = 0.0283168 * room_vol  # m3

    fresh_rate = room_vol * air_exchange_rate / 60  # ft3/min
    recirc_rate = fresh_rate * (1/primary_outdoor_air_fraction - 1)  # ft3/min
    air_filt_rate = aerosol_filtration_eff * recirc_rate * 60 / room_vol  # /hr
    eff_aerosol_radius = ((0.4 / (1 - relative_humidity)) ** (1 / 3)) * max_aerosol_radius
    viral_deact_rate = max_viral_deact_rate * relative_humidity
    sett_speed = 3 * (eff_aerosol_radius / 5) ** 2  # mm/s
    sett_speed = sett_speed * 60 * 60 / 1000  # m/hr
    conc_relax_rate = air_exchange_rate + air_filt_rate + viral_deact_rate + sett_speed / mean_ceiling_height_m  # /hr
    airb_trans_rate = ((breathing_flow_rate * mask_passage_prob) ** 2) * exhaled_air_inf / (room_vol_m * conc_relax_rate)

    return airb_trans_rate #This is mean number of transmissions per hour between pair of infected / healthy individuals


def get_distance(infect_id, uninfect_id, student_pos):
    x1y1 = student_pos[infect_id]
    x2y2 = student_pos[uninfect_id]
    # print(student_pos)
    return math.sqrt(((x2y2[0]-x1y1[0])**2) + ((x2y2[1] - x1y1[1])**2))

def directional_air(matrix, row, col, direction='back'): # back of the bus = down
    # dir_matrix is a np.array
    # risk_matrix is a pd.dataframe

    # direction = a number 0-9
    # numpad directions:
    # 7 8 9   <^ ^ ^>
    # 4 5 6   <  -  >
    # 1 2 3   <v v v>
    #   0

    # fix this function now

    if direction == 'back':
        matrix[row][col] - 1
        matrix[row-1][col] + 1
        return matrix

    if direction == 'forward':
        #
        matrix[row][col] - 1
        matrix[row+1][col] + 1
        return matrix

    if direction == 'left':
        #
        matrix[row][col] - 1
        matrix[row][col-1] + 1
        return matrix

    if direction == 'right':
        matrix[row][col] - 1
        matrix[row][col+1] + 1
        return matrix

    if direction == 'left-back':
        #
        matrix[row][col] - 1
        matrix[row-1][col-1] + 1
        return matrix

    if direction == 'left-forward':
        matrix[row][col] - 1
        matrix[row+1][col-1] + 1
        return matrix

    if direction == 'right-back':
        matrix[row][col] - 1
        matrix[row-1][col+1] + 1
        return matrix

    if direction == 'right-forward':
        matrix[row][col] - 1
        matrix[row+1][col+1] + 1
        return matrix
    return



def matrix_avg(input_matrices):
    '''
    calculate mean for every mutual [i,j] in input
    list of np.arrays

    function to be used in calculating which seats are riskiest
    '''
    return



def create_color_viz(infect_times, num_students = 25):
    # implement having more students in the class

    # initialize positions of students
    positions = {}
    x_arr = []
    y_arr = []
    rows = int(math.sqrt(num_students))
    count = 0
    for i in range(rows):
        for j in range(rows):
            positions[count] = [i, j]
            x_arr.append(i)
            y_arr.append(j)
            count += 1

    inf_x_arr = []
    inf_y_arr = []
    for inf in infect_times.keys():
        # print(positions[inf])
        inf_x_arr.append(positions[inf][0])
        inf_y_arr.append(positions[inf][1])


        # color dot red

    # plot uninfected in blue
    plt.scatter(x_arr, y_arr, color='blue')
    # plot infected in red
    # only output last frame for now:
    plt.scatter(inf_x_arr, inf_y_arr, color='red')
    # add plt title and description
    plt.show()
    return

def create_plot_viz(infect_times, infect_distrib):
    # convert infection timestamps to step function plot
    times = infect_times.values()
    #
    # print('times', times)
    step_x_array = times
    step_y_array = [i for i in range(len(times))]
    plt.step(step_x_array, step_y_array) # label timestep and id # above each infection
    # add ax annotate? or plt annotate?
    # add plt title and description
    plt.show()

    # plot distribution of infection rate over course of model run
    plt.hist(infect_distrib)#, bins=50)
    plt.gca().set(title='Transmission likelihood distribution')
    # add plt title and description
    plt.show()

    return


def bus_infections():
    # create .1 x .1 x .1 m cubic space for bus
    length, width, height = 17, 23, 114

    # fill space with student getting on bus

    # seating plan

    # student behavior (get on bus, walk to assigned seat)

    # initialize aerosol exhalation with first student onto bus

    ## Float values in cubes are == 'potential proportional infectious quanta'
    ## i.e. value 0-1 with 1 = 'calculate aerosol infection'
    # mark as 'exposed'

    # initialize cubes with direction and velocity
    # particles in a given cube tend to move in the direction of the arrow:
    # i.e. a cube with direction [X+ Y+ Z-] and velocity 2
    # (1 - .1 * [velocity]) = .8 --> 80% of particles move in the +X +Y -Z direction



    return

def distance_demo():
    # this function produces a sliding scale of risk based on distance and initial infectivity

    # 'approx time '
    return




# Go by standards mandated by school district in terms of masks and setup
def one_room(input_dir, output_dir, viz_checkd, num_people=25, mask_type='cloth', num_days=5, num_class=3, vent_test=False):


    uninf_index, inf_index, inf_array, student_pos = init_positions(900, num_people)

    # setup variables and functions# output graphs
    # countdown until symptoms appear: probability curve
    shape, loc, scale =  (0.6432659248014824, -0.07787673726582335, 4.2489459496009125)
    x = np.linspace(0, 17, 1000)
    countdown_curve = stats.lognorm(s=shape, loc=loc, scale=scale)

    infected = {i: int(np.round(stats.lognorm.rvs(shape, loc, scale, size=1)[0], 0)) for i in inf_index}

    # bound the days for overflow errors
    for i in infected:
        if infected[i] > 17:
            infected[i] = 17
        if infected[i] < -10:
            infected[i] = -10
    # create infectiveness reference dataframe
    shape, loc, scale = (20.16693271833812, -12.132674385322815, 0.6322296057082886)
    x = np.linspace(-10, 8, 19)
    infective_df = pd.DataFrame({'x': list(x), 'gamma': list(stats.gamma.pdf(x, a=shape, loc=loc, scale=scale))})

    uninfected = {i: 0 for i in uninf_index}

    ##### TODO: Get these inputs from default only if not available in user input
    deff = open('src/data/default.json',)
    floor_plan = json.load(deff)
    # for i in floor_plan:
    #     print(i)
    # deff.close()
    floor_area = floor_plan['floor_area']  # ft2
    mean_room_height = floor_plan['mean_ceiling_height']  # ft
    air_exchange_rate = floor_plan['air_exchange_rate']  # /hr (air changes per hour (ACH))

    ##Assumed Parameter Identified as 0.2 for Classrooms, 1.0 for outdoors##
    primary_outdoor_air_fraction = floor_plan['primary_outdoor_air_fraction']  # 1.0 = natural ventilation
    aerosol_filtration_eff = floor_plan['aerosol_filtration_eff']  # >0.9997 HEPA, =0.2-0.9 MERVs, =0 no filter

    #Average daily RH for San Diego is 69%
    relative_humidity = floor_plan['relative_humidity']
    physical_params = [floor_area, mean_room_height, air_exchange_rate, primary_outdoor_air_fraction,
                            aerosol_filtration_eff, relative_humidity]

    # Physiological Parameters
    breathing_flow_rate = floor_plan['breathing_flow_rate']  # m3/hr
    max_aerosol_radius = floor_plan['max_aerosol_radius']  # micrometers
    physio_params = [breathing_flow_rate, max_aerosol_radius]

    # Disease Parameters
    exhaled_air_inf = floor_plan['exhaled_air_inf']  # infection quanta/m3, changes with acitivity type.
    max_viral_deact_rate = floor_plan['max_viral_deact_rate']  # /hr
    disease_params = [exhaled_air_inf, max_viral_deact_rate]

    # Precautionary Parameters
    mask_passage_prob = floor_plan['mask_passage_prob'] # 1 = no masks, ~0.1 cloth, <0.05 N95
    risk_tolerance = floor_plan['risk_tolerance']  # expected transmissions per infector
    prec_params = [mask_passage_prob, risk_tolerance]


    # Use Chu
    chu_distance_curve = 1/2.02
    # loop through day


    days = num_days
    classes = num_class
    steps = 12 # 5 mins / step = 1 hour / class

    # use these to generate plot of num_infected by step count, assuming all else equal
    step_count = 0
    infect_plot_dict = {}

    student_infections = {} # this dict stores # times each student infects another via droplet
    # which students are infected is already output

    # temp
    min = 1
    max = 0
    trans_array = []
    infection_timesteps = {}
    num_they_infect = {}
    for i in inf_index:
        infection_timesteps[i] = 0
    for j in range(num_people):
        num_they_infect[j] = 0

    # generate plotline of num_infected using minimum default input: no masks, bad airflow, etc

    # generate plotline of num_infected using maximum default input: n-95 masks, barriers, vents, etc

    num_infected = 2

    # Aerosol transmission in this room (assumes well-mixed room)
    air_transmission = return_aerosol_transmission_rate(floor_area, mean_room_height,
                            air_exchange_rate,
                            aerosol_filtration_eff, relative_humidity, breathing_flow_rate,
                            exhaled_air_inf, max_viral_deact_rate, mask_passage_prob=.1,
                            max_aerosol_radius=2, primary_outdoor_air_fraction=0.2)
    # print('air', air_transmission)

    # Loop through days in a week (5 days)
    for i in range(days):

        # Loop through classes in each day (3 classes)
        for c in range(classes):

            # Loop through 5 minute steps in each class (total of 12 steps / class)
            for s in range(steps):
                step_count += 1

                ## Droplet Infection
                # Loop through infected students
                for i_student in inf_index:
                    # Loop through uninfected and calculate likelihood of infection
                    for u_student in uninf_index:
                        try:
                            transmission = droplet_infect(i_student, u_student, infected, student_pos, infective_df, chu_distance_curve).iloc[0]
                            trans_array.append(transmission)
                            # print(transmission)
                        except:
                            # print('wrong')
                            transmission = droplet_infect(i_student, u_student, infected, student_pos, infective_df, chu_distance_curve)
                            # print(transmission)
                            # break
                            transmission = 0 # Out of bounds of infectivity

                        # print(transmission)
                        if np.random.choice([True, False], p=[transmission, 1-transmission]):


                            # add u to infected
                            inf_array.append(u_student)

                            infection_timesteps[u_student] = step_count
                            num_they_infect[u_student] += 1
                            # also calculate time until symptoms for u_student

                            uninf_index.remove(u_student)


            # Aerosol Infection
            #Loop through infected and uninfected for pairwise calculations

            # this is calculated after every class (hourly transmission rate in that space)
            for i in inf_index:

                for u in uninf_index:
                    a_transmit = air_transmission
                    if np.random.choice([True, False], p=[a_transmit, 1-a_transmit]):
                        # add u to infected
                        inf_array.append(u)
                        # also calculate time until symptoms for u_student

                        uninf_index.remove(u)
                    pass

    out = 2 # count number students in inf_index
    # print('this is the number of infected students: ' + str(len(inf_array)))
    # print('these are the infected student IDs: ' + str(inf_array))


    # print('this is when they were infected: ' + str(infection_timesteps))
    # print(np.min(trans_array), np.max(trans_array), 'min, max')
    # print(np.mean(trans_array), 'mean')

    # '''
    if viz_checkd:
        pass
        # create_color_viz(infection_timesteps, 25)
        # print(infection_timesteps, 'time')
        #
        # create_plot_viz(infection_timesteps, trans_array)
        # return inf_array, infection_timesteps
    # '''
    # create_color_viz(infection_timesteps, 25)
    # print(infection_timesteps, 'time')

    # create_plot_viz(infection_timesteps, trans_array)
    # also return list of IDs infected
    # print(num_they_infect)
    return inf_array, infection_timesteps# num_they_infect


def scatter_collect(input_dir, output_dir, viz_checkd, num_people=25, mask_type='cloth',
 num_days=5, num_class=3, vent_test=False, n_runs=10): # also add one_room inputs, use this as run.py command
    '''
    run one_room n=1000 times and take avg of # times each id is stored

    divide by # runs = % chance of each seat being infected in each seat:

    Y = # times infectious/infective/infected by the model
    X = avg distance from other points

    i.e. X =
    a dictionary with {ID: # of times infected}
    Y =
    a dictionary with {ID: # people infected}

    ### TODO: think of better X variable
    '''

    # if saved_scatter in folder: plot those values

    # for file in folder:
    # temp = open(), plot #s, close()
    # check if this json file exists
    # if yes, exit function: don't plot the same points twice

    fig, ax = plt.subplots()
    n_students = 25
    positions = {}
    # grid desks
    rows = int(math.sqrt(n_students))
    count = 0
    for i in range(rows):
        for j in range(rows):
            positions[count] = [i, j]
            count += 1

    # GET OUT THE RIGHT # OF INFECTED PEOPLE
    id_counts = {i: 0 for i in range(num_people)}
    actually_infected = {i: 0 for i in range(num_people)}
    # num_they_infect_ = {i: 0 for i in range(num_people)}
    for run in range(n_runs):
        infected, what_times = one_room("src/data/default", "src/data", viz_checkd=False, num_people=25, mask_type='cloth', num_days=5, num_class=3, vent_test=False)
        # , num_they_infect
        # print(infected)
        for id in infected:
            id_counts[id] += 1
        for new_infections in infected[2:]:
            actually_infected[id] += 1
        # print(what_times)
        # for i in range(len(num_they_infect)):
        #     num_they_infect_[i] += num_they_infect[i]
    # print(num_they_infect_)
    # x = id_counts.values()

    actual_infections = {id: num_times / n_runs for id, num_times in actually_infected.items()}

    # print(id_counts)
    # print(positions)
    x_arr = []
    y_arr = []
    c_arr = []
    for i in range(len(positions)):
        pos = positions[i]
        x_arr.append(pos[0])
        y_arr.append(pos[1])
        c_arr.append(actual_infections[i])
    plt.scatter(x_arr, y_arr, c=c_arr)
    plt.colorbar()
    plt.title('seat infectiveness risk')
    plt.show()

    # save all XY output to json file

    # temp = one_room
    # get one_room to output which IDs are infected and their distance from other individuals

    return

def get_dist_multiplier(distance, chu_distance_curve):
# TODO: update this function with correct Chu Calculation from SchoolABM
    # is it chu ** dist ? double check tonight
    bathroom_break = np.random.choice([True, False], p=[4/25, 21/25])
    mu, sigma = 0, .5 # mean, standard deviation in meters to simulate movement
    if bathroom_break:
        temp = np.random.normal(mu, sigma, 1)
        distance = distance + temp
    return (chu_distance_curve)**(distance)

def droplet_infect(infect_id, uninfect_id, infected, student_pos, infective_df, chu_distance_curve, mask_passage_prob=.1):
    # Function to return transmission % from larger droplets
    '''
    Function to calculate infection via 'large particles'
    Defined as exhaled airborne particles >5 micrometers in size

    - other papers cite 2 micrometers, 5, 10, 50, or even 100 micrometers as the cutoff

    [effect of distance on # of viral particles that reach that distance] *
    [probability of infectivity given time until symptoms are expected] *
    ([effect of breathing rate and quanta of virions in exhaled/inhaled air] *
    [effect of mask type]) ^ 2

    '''

    distance = get_distance(infect_id, uninfect_id, student_pos)
    time = infected[infect_id]
    try:
        transmission_baseline = infective_df[infective_df.x == -1 * time]['gamma']
    except:
        print('out of range')
        return 0

    # get distance from chu
    distance_multiplier = get_dist_multiplier(distance, chu_distance_curve)
    # approximate student time spent breathing vs talking vs loudly talking
    breathing_type_multiplier = np.random.choice([.5, .05, 1], p=[.2, .05, .75])#############################
    # whisper, loud, heavy

    mask_multiplier = np.random.choice([.05, .3, .5, 1], p=[.1, .5, .3, .1])
    #mask_passage_prob # equivalent to aerosol masks

    # convert transmission rate / hour into transmission rate / step
    hour_to_fivemin_step = 5/60 # hourly transmission rate --> (5-min) transmission rate
    # 5 minute timesteps

    return transmission_baseline * distance_multiplier * (breathing_type_multiplier * mask_multiplier)**2 * hour_to_fivemin_step / 100
