import os
import re
import pandas as pd

    
def get_list_of_values(string, strings):
    """return a list of values between labels from strings and

    :param string: lat, long, time, time
    :type string: string
    :param strings: xml with all information from logs
    :type strings: string
    :return: list of float with the value of a pacrticular label
    :rtype: list
    """    

    list_start_pts = []
    list_end_pts = []
    
    
    for m in re.finditer('<' + string + '>', strings):
        
        list_start_pts.append(m.end())
    
    for m in re.finditer('</' + string + '>', strings):
        
        list_end_pts.append(m.start())
    
    
    list_val = []
    
    if len(list_start_pts) == len(list_end_pts):

        for i in range(len(list_end_pts)):

            val = strings[list_start_pts[i]:list_end_pts[i]]
            if len(val) > 1:
                try:
                    list_val.append(float(val))
                except ValueError:
                    list_val.append('NaN')

    return list_val

def get_coordinates_from_strings(s):
    """Extract coordinates from xml reading file

    :param s: xml string 
    :type s: readable file
    :return: data frame with lat, long, time
    :rtype: dataframe
    """   
    #  -  -  -  -  -  -  -  -  -  -  -  -  <long> -  -  -  -  -  -  -  -  -  -  -  -  #
    long_coord = get_list_of_values('long', s)

    
    #  -  -  -  -  -  -  -  -  -  -  -  -  <lat> -  -  -  -  -  -  -  -  -  -  -  -  # 
    lat_coord = get_list_of_values('lat', s)

    #  -  -  -  -  -  -  -  -  -  -  -  -  <secMark> -  -  -  -  -  -  -  -  -  -  -  -  # 
    time_lectures = get_list_of_values('secMark', s)

    #  -  -  -  -  -  -  -  -  -  -  -  -  TO CSV  -  -  -  -  -  -  -  -  -  -  -  -  #            
    if len(lat_coord) == len(long_coord) and len(lat_coord) == len(time_lectures):
        
        print('\n Success to get equal size iterable coordinates + time lectures')



    else:
        print('\n fail to extract coordinates + time lectures of the same size. \n Procede to handle \
                this error by dropping values')
        print('lat len = {}  |  long len = {}  |  time len = {}'.format(len(lat_coord),
                                                                        len(long_coord),
                                                                        len(time_lectures)))

        lat_coord, long_coord, time_lectures = handle_different_list_sizes(lat_coord, long_coord, time_lectures)



    d = {'latitude': lat_coord, 'longitude':long_coord, 'Dsecond': time_lectures}
    df_coord = pd.DataFrame(d)
    return df_coord

        

def handle_different_list_sizes(lat_coord, long_coord, time_list):
    """drop exceding values from list that are above the min size of the list 

    :param lat_coord: latitudes coordinates
    :type lat_coord: list
    :param long_coord: longitude coordinates
    :type long_coord: list
    :param time_list: time in microsencods lectures
    :type time_list: list
    :return: the same attributes passed in the fucntion but with dropped values
    :rtype: tuple(lists)
    """    
    # min size of long, lat, time lists
    min_size = min(len(lat_coord), len(long_coord), len(time_list))

    # check if size is larger than min then drop values if required
    if len(lat_coord) > min_size:
        cut_t = len(lat_coord) - min_size
        lat_coord = lat_coord[:-cut_t]
        

    if len(long_coord) > min_size:
        cut_g = len(long_coord) - min_size
        long_coord = long_coord[:-cut_g]

    if len(time_list) > min_size:
        cut_s = len(time_list)  - min_size
        time_list = time_list[:-cut_s]


    return lat_coord, long_coord, time_list




def convert_txts_to_csv():
    """run the conversion of al txt to export them for individual csv files with coordinates in x,y, time.
    First create a path for each particular txt. Then it outputs csv file for each file
    """    
    # path where txt files are stored
    in_path = os.path.split(os.getcwd())[0] + '\\Xtraction_scripts\\txt_out\\'

    # path where the csv files are stored
    out_path = os.path.split(os.getcwd())[0] + '\\Xtraction_scripts\\csv_out\\'

    # get all files in the *in_path*
    all_files = os.listdir(in_path)

    # initiate all path as empty list to later append each file name
    all_paths = []

    for i in all_files: # iterates over all files in in_path

        file_path = in_path + i # indivvidual path for each .txt

        all_paths.append(file_path)
        
        with open(file_path,'r') as f: # read each file the export to csv

            s_ = f.read() # full string of each intividual txt file
                          
        df = get_coordinates_from_strings(s_)
        
        df.to_csv(out_path + i[:-3] + 'csv',  index=None)   
        

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
if __name__ == '__main__':
    print("calling methods from txt_to_csv")