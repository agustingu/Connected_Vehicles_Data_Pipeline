import pandas as pd
import matplotlib.pyplot as plt
import folium
from src.logs_to_txt import get_all_logs_from_path

class Visualizer:
    def __init__(self) -> None:
        pass

    def identify_csv_within_gnv(self, parent_path, main_args):
        """Filter the files that have the coordinates within the define polygon (gainesville)

        :param parent_path: path where is the project
        :type parent_path: string
        :param main_args: argument of the scripts in main.py
        :type main_args: args
        :return: list of valid files
        :rtype: list
        """        

        data_folder = '\\Xtraction_scripts\\csv_out\\'
        
        all_csv = get_all_logs_from_path(parent_path, data_folder)

        files_with_coord_in_gnv = []

        lat_range, long_range  = main_args.lat_range,  main_args.long_range

        for csv in all_csv:
            csv_path = parent_path + data_folder + csv

            df_ = pd.read_csv(csv_path)

            min_x, max_x =  df_.longitude.min()/10000000, df_.longitude.max()/10000000
            min_y, max_y =  df_.latitude.min()/10000000, df_.latitude.max()/10000000

            if min_x >= long_range[0] and max_x <= long_range[1] and min_y >= lat_range[0] and max_y <= lat_range[1]:

                print('{} is INSIDE the defined polygon'.format(csv))

                files_with_coord_in_gnv.append(csv_path)

            else:
                print('{} is OUT of the define polygon'.format(csv))

            #TODO: save all path to txt for the record or at least the names

            return files_with_coord_in_gnv


            #TODO: Plot the valid files only
    