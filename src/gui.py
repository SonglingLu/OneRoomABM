# import
import tkinter as tk
from tkinter import ttk
import json
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from bus import bus_sim
from infection import return_aerosol_transmission_rate

def load_parameters_gui():
    '''
    Loads input and output directories
    '''
    with open('config/gui.json') as fp:
        parameter = json.load(fp)
    return parameter



class user_viz(tk.Frame):


    def __init__(self, parent=None):
        super(user_viz, self).__init__()
        self.pack(fill='both', expand=True)

        # separate input params
        self.input_params = load_parameters_gui()
        self.mask_wearing_percent = self.input_params["mask_wearing_percent"]
        self.num_students = self.input_params["number_students"]
        self.windows = self.input_params["windows"]
        # self.show_gui()
        self.label = tk.Label(self, text="Classroom / Bus Risk")
        self.label.grid(row=1, column=1)

        self.model_label = tk.Label(self, text="Model Type")
        self.model_label.grid(row=2, column=1)

        self.model_options = ["Classroom", "Bus"]
        self.model_var = tk.StringVar(self)
        self.model_var.set(self.model_options[0])

        # # trace if bus or classroom
        self.model_var.trace_add('write', self.update_var)
        # functionality for buttons only

        self.model_type = tk.OptionMenu(self,self.model_var, *self.model_options)#, style='raised.TMenubutton')
        self.model_type.grid(row=3, column=1)

        # Bus route (leave blank if choosing 'class')
        self.temp_label = tk.Label(self, text="Bus Route")
        self.temp_label.grid(row=1, column=2)
        self.temp_entry = tk.Entry(self)
        self.temp_entry.grid(row=2, column=2)

        # num_students
        self.students_label = tk.Label(self, text="Number of Students")
        self.students_label.grid(row=4, column=1)

        self.student_temp = tk.StringVar(self)

        # 28 (50% capacity)
        self.student_option_dict = {"Bus": [28, 56], "Classroom": [10, 25, 40]}

        self.students_var_list = self.student_option_dict[self.model_var.get()]
        self.students_var =  tk.StringVar(self)
        self.students_var.set(self.students_var_list[0])

        self.num_students = tk.OptionMenu(self, self.students_var, *self.students_var_list)
        self.num_students.grid(row=5, column=1)

        # mask_percent
        self.mask_wearing_label = tk.Label(self, text="Percent of students wearing masks")
        self.mask_wearing_label.grid(row=6, column=1)
        mask_options = ["100%", "90%", "80%"]
        self.mask_var = tk.StringVar(self)
        self.mask_var.set(mask_options[0])
        self.mask_wearing_choice = tk.OptionMenu(self, self.mask_var, *mask_options)
        self.mask_wearing_choice.grid(row=7, column=1)

        # selfs
        self.Frame_label = tk.Label(self, text="Windows Open (inches)")
        self.Frame_label.grid(row=8, column=1)
        self.Frame_options = {"Bus": ["0 inches", "6 inches"], "Classroom": ["0 inches", "3 inches", "6 inches", "9 inches", "12 inches"]}
        self.Frame_var = tk.StringVar(self)
        self.Frame_var.set(self.Frame_options[self.model_var.get()][0])
        self.Frame_choice = tk.OptionMenu(self, self.Frame_var, *self.Frame_options)
        self.Frame_choice.grid(row=9, column=1)

        # button widget for transmission params
        self.t_window = tk.Button(self, text="Transmission Parameters", command=self.openT_P)
        self.t_window.grid(row=4, column=2)
        # button widget for model run
        self.run_btn = tk.Button(self, text="Model Run", command=self.model_run)
        self.run_btn.grid(row=6, column=2)

        self.prev_run = tk.Button(self, text="Previous runs", command=self.viz_previous)
        self.prev_run.grid(row=8, column=2)

        # init other self variables for aerosol
        self.floor_area  = tk.StringVar()
        self.mean_ceiling_height  = tk.StringVar()
        self.air_exchange_rate  = tk.StringVar()
        self.primary_outdoor_air_fraction  = tk.StringVar()
        self.aerosol_filtration_eff  = tk.StringVar()
        self.relative_humidity  = tk.StringVar()
        self.breathing_flow_rate  = tk.StringVar()
        self.max_aerosol_radius  = tk.StringVar()
        self.exhaled_air_inf  = tk.StringVar()
        self.max_viral_deact_rate  = tk.StringVar()
        self.mask_passage_prob  = tk.StringVar()

    def update_var(self, *args):
        '''
        When Model Type is selected, alter lists for # students and windows open
        '''
        self.students_var_list = self.student_option_dict[self.model_var.get()]
        self.students_var.set(self.students_var_list[0])
        # self.student_temp.set(str(self.students_var_list))
        menu = self.num_students['menu']
        menu.delete(0, 'end')
        for i in self.students_var_list:
            menu.add_command(label=i, command = lambda new = i: self.students_var.set(i))

        temp = self.Frame_options[self.model_var.get()]
        self.Frame_var.set(temp[0])
        temp_menu = self.Frame_choice['menu']
        temp_menu.delete(0, 'end')
        for j in temp:
            temp_menu.add_command(label=j, command=lambda new=i: self.Frame_var.set(j))

    # function to open new window
    def openT_P(self):
        # top level opject to be treated as window
        self.newWindow = tk.Toplevel(self)
        # set geometry
        self.newWindow.geometry("200x200")

        # Label to show in top level
        self.temp_label = tk.Label(self.newWindow, text="ACH")
        self.temp_label.pack()
        self.num_students = tk.Entry(self.newWindow)
        self.num_students.pack()

        self.mask_wearing_label = tk.Label(self.newWindow, text="Mask Efficacy")
        self.mask_wearing_label.pack()
        self.mask_wearing_chance = tk.Entry(self.newWindow)
        self.mask_wearing_chance.pack()


        self.num_sims_label = tk.Label(self.newWindow, text="Number of Simulations")
        self.num_sims_label.pack()
        temp = tk.StringVar(window, value="100")
        self.num_sims_chance = tk.Entry(self.newWindow, textvariable=temp)
        self.num_sims_chance.pack()

        self.trip_length_label = tk.Label(self.newWindow, text="Trip Length")
        self.trip_length_label.pack()
        self.trip_length_chance = tk.Entry(self.newWindow)
        self.trip_length_chance.pack()

    # function to run model with user input
    def model_run(self):
        # get type:
        type = self.model_var.get()
        if type == "Bus":
            # run bus model
            window = self.Frame_var.get()
            num_students = int(self.students_var.get())
            print('n', num_students)
            mask = self.mask_var.get()
            num_sims = 100 # get from advanced
            trip_len = 60 # get from bus trip stops
            bus_type = "56"
            bus_trip, conc, chance_nonzero = bus_sim(window, num_students, mask, num_sims, trip_len, bus_type) # replace default with selected
            pd.Series(bus_trip).plot.kde()
            plt.show()

        elif type == "Classroom":
            pass # run class model

        else:
            print('model variable empty somehow')
        return

    def heatmaps(self):
        # plot concentration average heatmaps for every step
        return

    # visualize previous model runs
    def viz_previous():

        return

run = True

if run:
    window = tk.Tk()
    window.geometry("350x350")
    window.title("Bus and Classroom Risk")
    # window.withdraw()
    # set style
    style = ttk.Style(window)
    style.theme_use('clam')
    app = user_viz(window)
    window.mainloop()
    sys.exit("End gui.py")
