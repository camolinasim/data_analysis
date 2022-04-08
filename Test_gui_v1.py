#!/usr/bin/env python3


from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QDialog, QListWidget, \
    QVBoxLayout, QListWidgetItem
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
import sys, os, glob
from tkinter import *
from tkinter.ttk import *
import controller
import shutil
import os.path
from os import path
import pandas as pd

# importing askopenfile function
# from class filedialog
from tkinter.filedialog import askopenfilename

from random import randint


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.w = None
        loadUi("Title_screen_gui_color.ui", self)
        self.btn_create_project.clicked.connect(self.show_create_window)
        self.btn_open_project.clicked.connect(self.show_open_window)
        self.btn_open_project.clicked.connect(self.show_open_window)
        self.btn_anayze_data.clicked.connect(self.show_data_analysis_window)

    def show_data_analysis_window(self):
        if self.w is None:
            self.w = DataAnalysisWindow()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    def show_create_window(self):
        if self.w is None:
            self.w = ProjectCreateWindow()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    def show_open_window(self):
        if self.w is None:
            window = Tk()  # create and hide root tinker window
            window.withdraw()
            settings = self.openFile()
            window.destroy()
            self.show_selected_project(settings)
            ##self.close()
            self.w = SelectedProjectWindow()
            self.w.generateScenarioList(settings=settings)
            self.w.lbl_project_x.setText("Project: " + settings[0][1])
            self.w.show()

        else:
            self.w.close()
            self.w = None

    def openFile(self):
        settings = []
        filepath = askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                   title="Open file okay?",
                                   filetypes=(("text files", "*.txt"),
                                              ("all files", "*.*")))
        file = open(filepath, 'r')
        for line in file:
            print(line.strip().split(":"))
            settings.append(line.strip().split(":"))
        file.close()
        return settings

    def show_selected_project(self, settings):
        print("here we are")
        print(settings)


class DataAnalysisWindow(QWidget):
    def __init__(self):
        super(DataAnalysisWindow, self).__init__()
        loadUi("data_analysis.ui", self)
        self.btn_open_pcap.clicked.connect(self.read_pcap)

    def read_pcap(self):
            ########### OPENING PCAP ###########
            Tk().withdraw()
            path_of_selected_pcap = askopenfilename()
            # correcting path from C:/x/x/x/x.pcap -> C:\\x\\x\\x\\x\ x.pcap
            path_of_selected_pcap = os.path.normpath(path_of_selected_pcap)
            path_of_selected_pcap_no_extension = path_of_selected_pcap.replace(".pcap", "")
            pcap_folder_location = path_of_selected_pcap.rsplit('http.pcap', 1)
            pcap_folder_location = pcap_folder_location[0].rsplit('\\', 1)[0]
            csv_folder = pcap_folder_location + "\\csv_files"
            name_of_csv = os.path.basename(path_of_selected_pcap_no_extension + '.csv')

            csv = csv_folder + "\\" + name_of_csv
            csv_exists = os.path.exists(csv)
            print(csv)
            print(csv_exists)
            if (not csv_exists):
                run_this_shit = '"C:\\Program Files\\Wireshark\\tshark.exe" -r ' + path_of_selected_pcap + ' -T fields -E header=y -E separator=, -E quote=d -E occurrence=f -e frame.number -e _ws.col.Time -e ip.src -e ip.dst -e ip.proto -e frame.len -e _ws.col.Info >' + path_of_selected_pcap_no_extension + '.csv'
                stream = os.popen(run_this_shit)
                output = stream.read()
                print(output)

            ########### CREATING FOLDER FOR CSVs ###########

            if not path.exists(csv_folder):
                os.mkdir(csv_folder)

            ########## CREATING DATAFRAME FOR DATA MANIPULATION ###########
            if (not csv_exists):
                csv_path = path_of_selected_pcap_no_extension + '.csv'
                move_this_pcap = csv_path
                over_here = csv_folder
                shutil.move(move_this_pcap, over_here)

            csv_path = csv_folder + "\\" + name_of_csv
            df = pd.read_csv(csv_path)
            pcap_content = df.to_string(index=False)
            # print(pcap_content)
            rows = pcap_content.split("\n")
            # print(rows[2])
            for row in rows:
                # layout = QHBoxLayout()
                print(row)  # reemplazar con lo que quieres que haga el loop


class ProjectCreateWindow(QWidget):

    def __init__(self):
        super(ProjectCreateWindow, self).__init__()
        loadUi("project_creation_gui.ui", self)
        self.btn_create_project.clicked.connect(self.createfolder)

    def createfolder(self):
        directory = self.txt_path.toPlainText()
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                self.createSettings(directory)
        except OSError:
            print('Error creating directory: ' + directory)

    def createSettings(self, directory):

        project_name = self.txt_project_name.toPlainText()
        complete_name = os.path.join(directory + '/', project_name)
        f = open(complete_name + ".txt", "w")


class SelectedProjectWindow(QWidget):

    def __init__(self):
        super(SelectedProjectWindow, self).__init__()
        loadUi("selected_project.ui", self)
        self.btn_return_home.clicked.connect(self.goHome)
        self.btn_run_scn.clicked.connect(self.RUNCORE)
        # self.lw_scn_list.addItem("Test_SU1")
        # QListWidgetItem("Test_SU2", self.lw_scn_list)
        # QListWidgetItem("Test_SU3", self.lw_scn_list)
        # self.lw_scn_list.itemSelectionChanged.connect(self.generateScenarioList)

    def generateScenarioList(self, settings):
        print("create list from scenarios in folder")
        #
        # cwd = os.getcwd()
        # fulName=  cwd+'/test_for_name' +'/ScenarioUnits/' +'*.txt'
        # array = glob.glob(fulName)

        # for x in array:
        #    QListWidgetItem(x, self.lw_scn_list)

        # print(os.listdir('/test_for_name'))

    def goHome(self):
        self.close()

    def RUNCORE(self):
        print("###RUNNING CORE###")
        vm_list = "ubuntu(practicum)"
        controller.start_vm(vm_list)



app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.show()
app.exec()