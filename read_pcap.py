import shutil
import subprocess
from itertools import dropwhile

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import os.path
from os import path
import csv

pcap_folder_location = "C:\\Users\\perro\Desktop\\folder_with_folders\\practicum\\data_analysis\\pcap_files"
# Creates a CSV with parsed data as output. CSV will be created in the same folder that the selected pcap exists.
def open_file_explorer_and_read_pcap():
    Tk().withdraw()

    # correcting path from C:/x/x/x/x.pcap -> C:\\x\\x\\x\\x\ x.pcap
    filename_with_pcap_extension = askopenfilename()
    filename_with_pcap_extension =os.path.normpath(filename_with_pcap_extension)

    filename = filename_with_pcap_extension.replace(".pcap", "")
    open_this_shit = '"C:\\Program Files\\Wireshark\\tshark.exe" -r ' + filename_with_pcap_extension + ' -T fields -E header=y -E separator=, -E quote=d -E occurrence=f -e frame.number -e _ws.col.Time -e ip.src -e ip.dst -e ip.proto -e frame.len -e _ws.col.Info > me_a_moron.csv'
    stream = os.popen(open_this_shit)
    output = stream.read()
    print(output)





    # csv_folder = pcap_folder_location + "csv_files"
    # if not path.exists(csv_folder):
    #     os.mkdir(csv_folder)
    # move_this_pcap = pcap_folder_location + filename + ".csv"
    # over_here = pcap_folder_location + "csv_files\\" + filename + ".csv"
    # shutil.move(move_this_pcap, over_here)

# ---------main----------- #

open_file_explorer_and_read_pcap()


