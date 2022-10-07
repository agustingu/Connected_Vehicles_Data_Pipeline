import argparse
from distutils.log import error
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

    if main_args.study_area == 'Trapezium':

        long_range, lat_range = (-82.374776, -82.336804), (29.621407, 29.655639)

    elif main_args.study_area == '13th':

        long_range, lat_range = (-82.341403, -82.335938), (29.633769, 29.655721)

    elif main_args.study_area == '16th':

        long_range, lat_range = (-82.345213, -82.336024), (29.634396,  29.637880)

    elif main_args.study_area == '34th':

        long_range, lat_range = (-82.375123, -82.369755), (29.611155, 29.621211)

    elif main_args.study_area == 'Archer':

        long_range, lat_range = (-82.378203, -82.333047), (29.611511, 29.647491)

    else:
        raise error('See help in ariguement for study area')

    main_args.lat_range = lat_range
    main_args.long_range = long_range



    if main_args.extract_logs == True: #--------------------------------------
        print('\n       Initiate Logs Extraction \n')
        data_folder = main_args.data_folder
        

        logs_list_names = get_all_logs_from_path(parent_path, data_folder)

        # iterate over all logs
        for i in logs_list_names:

            try:
                
                get_txt_from_logs(i, parent_path, data_folder)

            except :

                print('File {} cannot be extracted'.format(i))

                pass
            
        convert_txts_to_csv()
    else:
        print('extract_logs set as False')


    if main_args.generate_htmls == True: #--------------------------------------
        print('Calling visualizer')
        vis = Visualizer()
        valid_files = vis.identify_csv_within_gnv(parent_path, main_args)
        vis.export_html_valid_logs_on_map(valid_files)

    if main_args.scatter_on == True: #--------------------------------------
        print('Calling visualizer')
        vis = Visualizer()
        valid_files = vis.identify_csv_within_gnv(parent_path, main_args)

        vis.generate_scatter_plots(valid_files)

if __name__ == "__main__":

    parser = argparse.ArgumentParser("parsing args for data extraction")

    parser.add_argument("--data_folder", type=str, default="\\2520203122717008854\\20220909_150020\\logs\\",
                        help="Folder where logs are stored")

    parser.add_argument('--extract_logs', type=str_to_bool, default='False',
                        help='perform extraction of logs to csv')

    parser.add_argument('--generate_htmls', type=str_to_bool, default='True',
                        help='genrates plots from CSV files with reasonable coordinates')
    
    parser.add_argument('--scatter_on', type=str_to_bool, default='True',
                        help='generate scatter plot by file name')
    
    parser.add_argument('--study_area', type=str, default='Archer',
                        help='Define study area, Trapezium or by road')

    parser.add_argument('--long_range', type=tuple, default=(0, 0), 
                        help='lower bound left of a polygon to filter coordinates')

    parser.add_argument('--lat_range', type=tuple, default=(0,  0),  
                        help='lower bound left of a polygon to filter coordinates') 


    
    args = parser.parse_args()

    run_logs_pipeline(args)

    print('Data Extraction logs->csv  Terminated')