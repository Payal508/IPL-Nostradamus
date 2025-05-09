from data_extraction import DataExtractor
from tkinter.ttk import Combobox
import tkinter as tk
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


class EDAfrm:
    def __init__(self):
        self.frame = tk.Tk()
        self.frame.title('Exploratory Data Analysis')
        self.frame.geometry('1920x1080')
        self.date = tk.StringVar()

        obj = DataExtractor()
        self.df = obj.get_cleaned_data()

        self.cmb = Combobox(self.frame, state='readonly', textvariable=self.date)
        
        # Populate combobox with unique dates (or any other relevant category)
        self.list = sorted(self.df['date'].unique().tolist())  # Assuming 'date' is a column
        self.cmb['values'] = self.list
        self.cmb.bind('<<ComboboxSelected>>', self.new)

        # Display the combobox in the window
        self.cmb.place(x=100, y=50)

        # Create figure and axes for plotting
        fig1 = Figure(figsize=(5, 5), dpi=100)
        fig2 = Figure(figsize=(5, 5), dpi=100)

        self.plot1 = fig1.add_subplot(111)
        self.plot2 = fig2.add_subplot(111)

        # Initialize plots
        self.update_plots()

        # Create canvas for each plot
        canvas1 = FigureCanvasTkAgg(fig1, master=self.frame)
        canvas2 = FigureCanvasTkAgg(fig2, master=self.frame)

        canvas1.draw()
        canvas2.draw()

        # Place canvases in the window
        canvas1.get_tk_widget().place(x=200, y=150)
        canvas2.get_tk_widget().place(x=850, y=150)

    def update_plots(self):
        # Generate bar and pie charts based on the data
        teams = list(self.df['winner'].unique())
        y = []
        x = []
        
        for team in teams:
            y.append(self.df['winner'].value_counts()[team])
            team_name = ''.join([word[0].upper() for word in team.split()])
            x.append(team_name)

        self.plot1.clear()  # Clear previous plot
        self.plot2.clear()  # Clear previous pie chart

        self.plot1.bar(x, y, color='skyblue')
        self.plot2.pie(self.df['winner'].value_counts(), labels=x, autopct='%0.2f%%', colors=['#99ff99', '#ff9999'])

    def new(self, event):
        # Called when a new item is selected from combobox
        selected_date = self.date.get()
        
        # Filter the dataframe based on the selected date (or category)
        filtered_df = self.df[self.df['date'] == selected_date]
        
        # Recompute plots for the filtered data
        self.df = filtered_df  # Update with filtered data
        self.update_plots()

    def show_dialog(self):
        self.frame.mainloop()
