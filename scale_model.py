## positional code: replace w/ square/circular desks TODO
import math
import random
import numpy as np
import pandas as pd
from scipy import stats

# TODO:
# update droplet transmission
# update aerosol transmission
# move relevant code to SchoolABM
# add viz for 1-room infection

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
    inf_index = random.sample(set(range(25)), 2)
    uninf_index = list(range(25))
    inf_array = []


    # double check this
    for i in inf_index:
        uninf_index.remove(i)
        inf_array.append(i)
    return uninf_index, inf_index, inf_array, positions


################ TODO ###############

uninf_index, inf_index, inf_array, student_pos = init_positions(900, 25)

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


# Use Chu
chu_distance_curve = 1/2.02


# Use Chen

##### TODO: Get data from default.json ############
# setup default parameters

floor_area = 900  # ft2
mean_ceiling_height = 12  # ft
air_exchange_rate = 3  # /hr (air changes per hour (ACH))

##Assumed Parameter Identified as 0.2 for Classrooms, 1.0 for outdoors##
primary_outdoor_air_fraction = 0.2  # 1.0 = natural ventilation
aerosol_filtration_eff = 0  # >0.9997 HEPA, =0.2-0.9 MERVs, =0 no filter

#Average daily RH for San Diego is 69%
relative_humidity = 0.69 #nice
physical_params = [floor_area, mean_ceiling_height, air_exchange_rate, primary_outdoor_air_fraction,
                        aerosol_filtration_eff, relative_humidity]

# Physiological Parameters
breathing_flow_rate = 0.5  # m3/hr
max_aerosol_radius = 2  # micrometers
physio_params = [breathing_flow_rate, max_aerosol_radius]

# Disease Parameters
exhaled_air_inf = 30  # infection quanta/m3, changes with acitivity type.
max_viral_deact_rate = 0.3  # /hr
disease_params = [exhaled_air_inf, max_viral_deact_rate]

# Precautionary Parameters
mask_passage_prob = .1 # 1 = no masks, ~0.1 cloth, <0.05 N95
risk_tolerance = 0.1  # expected transmissions per infector
prec_params = [mask_passage_prob, risk_tolerance]


def droplet_infect(infect_id, uninfect_id, infected):
    distance = get_distance(infect_id, uninfect_id, student_pos)
    time = infected[infect_id]
    transmission_baseline = infective_df[infective_df.x == -1 * time]['gamma']

    # get distance from chu
    distance_multiplier = get_dist_multiplier(distance)



    # approximate student time spent breathing vs talking vs loudly talking
    breathing_type_multiplier = np.random.choice([.1, .5, 1], p=[.2, .05, .75])
    # whisper, loud, heavy

    mask_multiplier = mask_passage_prob # equivalent to aerosol masks

    # convert transmission rate / hour into transmission rate / step
    hour_to_fivemin_step = 5/60
    # test if necessary

    return transmission_baseline * distance_multiplier * breathing_type_multiplier * mask_multiplier * hour_to_fivemin_step

def return_aerosol_transmission_rate(floor_area, room_height,
                            air_exchange_rate,
                            aerosol_filtration_eff, relative_humidity, breathing_flow_rate,
                            exhaled_air_inf, max_viral_deact_rate, mask_passage_prob,
                            max_aerosol_radius=2, primary_outdoor_air_fraction=0.2):

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

# transmission_aerosol_percent(length, width, height, num_occupants, num_infectious, num_masks, \
# airchanges = 3, filters = 0, UV = 0, event_duration = 5, background_CO2=415), \
# temperature=30, humidity=65, pressure=0.95)

# def transmissio



def get_distance(infect_id, uninfect_id, student_pos):
    x1y1 = student_pos[infect_id]
    x2y2 = student_pos[uninfect_id]
    return math.sqrt(((x2y2[0]-x1y1[0])**2) + ((x2y2[1] - x1y1[1])**2))

def get_dist_multiplier(distance):
    return distance * chu_distance_curve




def one_room(input_dir, output_dir):
    num_out_test = 0



    ######### TODO ###################

    # loop through day
    days = 1
    classes = 3
    steps = 12 # TODO: 5 mins / step = 1 hour / class

    # use these to generate plot of num_infected by step count, assuming all else equal
    step_count = 0
    infect_plot_dict = {}


    # temp
    min = 1
    max = 0

    # generate plotline of num_infected using minimum default input: no masks, bad airflow, etc

    # generate plotline of num_infected using maximum default input: n-95 masks, barriers, vents, etc

    num_infected = 2

    # Aerosol transmission in this room (assumes well-mixed room)
    air_transmission = return_aerosol_transmission_rate(floor_area, mean_ceiling_height,
                            air_exchange_rate,
                            aerosol_filtration_eff, relative_humidity, breathing_flow_rate,
                            exhaled_air_inf, max_viral_deact_rate, mask_passage_prob,
                            max_aerosol_radius=2, primary_outdoor_air_fraction=0.2)


    for i in range(days):

        # Loop through classes in each day (3 classes)
        for c in range(classes):

            # Loop through 5 minute steps in each class
            for s in range(steps):
                step_count += 1

                ## Droplet Infection
                # Loop through infected students
                for i_student in inf_index:
                    # Loop through uninfected and calculate likelihood of infection
                    for u_student in uninf_index:
                        try:
                            transmission = droplet_infect(i_student, u_student, infected).iloc[0]
                            if transmission < min:
                                min = transmission
                            if transmission > max:
                                max = transmission
                        except:
                            transmission = 0
                            # print(transmission, 't')
                            # print(u_student, i_student)
                            # print(inf_index)
                            # print(uninf_index)

                        # store transmission for distribution: plot at end


                        if np.random.choice([True, False], p=[transmission, 1-transmission]):


                            # add u to infected
                            num_out_test += 1
                            inf_array.append(u_student)
                            # also calculate time until symptoms for u_studnet

                            uninf_index.remove(u_student)


        ## Aerosol Infection
        # Loop through infected and uninfected for pairwise calculations

        #### TODO 2/14 #################### Use updated Kaushik Code
#         for i in inf_index:
#
#             for u in uninf_index:
# #                 return_aerosol_transmission_rate()
#                 a_transmit = .5
#                 if np.random.choice([True, False], p=[a_transmit, 1-a_transmit])
#                 pass

    out = 2 # count number students in inf_index
    print('this is the number of infected students: ' + str(len(inf_array)))
    print(inf_array)
    print(min, max, 'min, max')

    # Viz Output: TODO 2/14
    # create viz of students @ each step:
    # change color when infected

    # Create viz for spread of aerosol to different parts of the room?
    # Look into particle spread


    return len(inf_array)
