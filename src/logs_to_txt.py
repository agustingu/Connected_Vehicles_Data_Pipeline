
import os
import re


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def get_all_logs_from_path(parent_path, data_path):
    """Get all logs names in a directory

    :param parent_path: parent path of folder
    :type parent_path: string
    :param data_path: subfolder where logs are located
    :type data_path: string
    :return: all names that start with log in the data_path
    :rtype: list
    """    
    mypath = parent_path + data_path
    all_files = os.listdir(mypath)
    
    logs_list_names = []

    for j in all_files:
        
        if j[:3] == 'log':
            
            print('adding file name {} '.format(j))
            
            logs_list_names.append(j)
            
    return logs_list_names


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_txt_from_logs(file_name, parent_path, data_path):
    """Write to out_txt folder a .txt file for eah log in the data_path

    :param file_name: file name
    :type file_name: string
    :param parent_path: parent path of working folder
    :type parent_path: string
    :param data_path: folder where the data comes from see args on main.py
    :type data_path: string
    """    

    file_ = parent_path + data_path + file_name
    # read your file and store in string 's'
    with open(file_,'r') as f:
    
        s = f.read()
    
    # then remove non-XML element with re. Also remove <?xml ...?> part 
    # as your file consists of multiple xml logs
    s = re.sub(r'<\?xml.*?>', '', ''.join(re.findall(r'<.*>', s)))
    # wrap your s with a root element
    s = '<root>'+s+'</root>'
    
    # saving for backup
    save_path = os.path.split(os.getcwd())[0] + '\\Xtraction_scripts\\txt_out\\'

    text_file = open(save_path + file_name + "_out.txt", "w")
    n = text_file.write(s)
    text_file.close()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == '__main__':
    print("calling methods from logs_to_txt")