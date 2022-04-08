import shutil
import subprocess
from itertools import dropwhile

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import os.path
from os import path
import csv
import pandas
import time

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
df = pandas.read_csv(csv_path)
print(df)

# csv_path = csv_folder
# csv_name = os.path.basename(csv_path)
# path_of_csv_before_moving = csv_path.rsplit('\\', 1)[0]
# csv_path = csv_path + '\\' + csv_name
# print(csv_path)
# df = pandas.read_csv(csv_path)
# print(df)
