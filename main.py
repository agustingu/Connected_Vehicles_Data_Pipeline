import argparse
import os

from pkg_resources import parse_requirements
from src.logs_to_txt import get_all_logs_from_path, get_txt_from_logs
from src.txt_to_csv import convert_txts_to_csv
# from src.visualizer import 
#-----------------------------------------------------------------------



def run_logs_pipeline(args):
    """Initiate the data pipeline extraction according to the folder where
    the logs are stored

    :param args: arguments, for now folder where the logs are located only
    :type args: args
    """    

    print('\n       Initiate Logs Extraction \n')
    data_folder = args.data_folder
    parent_path = os.path.split(os.getcwd())[0]
    print(parent_path)
    logs_list_names = get_all_logs_from_path(parent_path, data_folder)



    for i in logs_list_names:

        try:

            get_txt_from_logs(i, parent_path, data_folder)

        except :

            print('File {} cannot be extracted'.format(i))

            pass
        
    convert_txts_to_csv()


if __name__ == "__main__":

    parser = argparse.ArgumentParser("parsing args for data extraction")

    parser.add_argument("--data_folder", type=str, default="\\2520203122717008854\\20220909_150020\\logs\\",
                        help="Folder where logs are stored")
    
    args = parser.parse_args()

    run_logs_pipeline(args)

    print('Data Extraction logs->csv  Terminated')