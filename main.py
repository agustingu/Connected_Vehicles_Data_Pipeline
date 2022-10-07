import argparse
import os

from pkg_resources import parse_requirements
from src.logs_to_txt import get_all_logs_from_path, get_txt_from_logs
from src.txt_to_csv import convert_txts_to_csv
from src.visualizer import Visualizer
from src.logs_to_txt import str_to_bool
#-----------------------------------------------------------------------



def run_logs_pipeline(args):
    """Initiate the data pipeline extraction according to the folder where
    the logs are stored

    :param args: arguments, for now folder where the logs are located only
    :type args: args
    """    
    main_args = args
    parent_path = os.path.split(os.getcwd())[0]
    # import pdb; pdb.set_trace()

    if main_args.extract_logs == True: #--------------------------------------
        print('\n       Initiate Logs Extraction \n')
        data_folder = main_args.data_folder
        

        logs_list_names = get_all_logs_from_path(parent_path, data_folder)



        for i in logs_list_names:

            try:

                get_txt_from_logs(i, parent_path, data_folder)

            except :

                print('File {} cannot be extracted'.format(i))

                pass
            
        convert_txts_to_csv()
    else:
        print('extract_logs set as False')


    if main_args.generate_plots == True: #--------------------------------------
        print('Calling visualizer')
        vis = Visualizer()
        valid_files = vis.identify_csv_within_gnv(parent_path, main_args)


if __name__ == "__main__":

    parser = argparse.ArgumentParser("parsing args for data extraction")

    parser.add_argument("--data_folder", type=str, default="\\2520203122717008854\\20220909_150020\\logs\\",
                        help="Folder where logs are stored")

    parser.add_argument('--extract_logs', type=str_to_bool, default='True',
                        help='perform extraction of logs to csv')

    parser.add_argument('--generate_plots', type=str_to_bool, default='True',
                        help='genrates plots from CSV files with reasonable coordinates')

    parser.add_argument('--long_range', type=tuple, default=(-82.409996, -82.309996), # (29.59693, -82.409996)
                        help='lower bound left of a polygon to filter coordinates')

    parser.add_argument('--lat_range', type=tuple, default=(29.59693, 29.69693),  # (29.69693, -82.309996)
                        help='lower bound left of a polygon to filter coordinates')
    
    args = parser.parse_args()

    run_logs_pipeline(args)

    print('Data Extraction logs->csv  Terminated')