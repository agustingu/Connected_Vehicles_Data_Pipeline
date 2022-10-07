from cProfile import label
import pandas as pd
import matplotlib.pyplot as plt
import folium
import utm
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
            # print('eval csv ', csv)
            # import pdb; pdb.set_trace()
            csv_path = parent_path + data_folder + csv

            df_ = pd.read_csv(csv_path)

            min_x, max_x =  df_.longitude.min()/10000000, df_.longitude.max()/10000000
            min_y, max_y =  df_.latitude.min()/10000000, df_.latitude.max()/10000000

            if min_x >= long_range[0] and max_x <= long_range[1] and min_y >= lat_range[0] and max_y <= lat_range[1]:

                print('{} is INSIDE the defined polygon'.format(csv))

                files_with_coord_in_gnv.append(csv_path)

            else:
                print('{} is OUT of the define polygon'.format(csv))


        return files_with_coord_in_gnv


  
    def export_html_valid_logs_on_map(self, valid_files):
        """Export html files that are within the define polygon in main args

        :param valid_files: files that are within the polygon
        :type valid_files: list
        """        

        # create map
        gainesville = folium.Map(zoom_start=13, location=[29.63693, -82.349996],
                                zoom_control=False,
                                scrollWheelZoom=False,
                                dragging=False)


        for f in valid_files:

            # read csv use pandas. Later use numpy for efficiency
            df = pd.read_csv(f)
            df.longitude = df.longitude/10000000
            df.latitude = df.latitude/10000000

            # plot coordinates on html file and save it in the html out folder
            for _, indx in df.iterrows():

                folium.Marker(location=[indx["latitude"], indx["longitude"]]).add_to(gainesville)

            gainesville.save(f[:92] + 'html_out\\' + f[100:] + '.html')

            


    def generate_scatter_plots(self, valid_files):
        """Generate scatter plot of valid files. First transform coordinates to utm,
        the plotting all in one figure  

        :param valid_files: files that are within the design polygon    
        :type valid_files: list of paths
        """  
        # instantiate figure object      
        fig, axes = plt.subplots()

        # loop over valid files
        for f in valid_files:

            # read and apply scalling factors to data points
            df = pd.read_csv(f)
            df.longitude = df.longitude/10000000
            df.latitude = df.latitude/10000000

            # initiate empty lists
            x = []
            y = []

            # convert each value to later appending to each utm coordinate list (x,y)
            for _, indx in df.iterrows():

                u = utm.from_latlon(indx["latitude"], indx["longitude"])
                # import pdb; pdb.set_trace()
                y.append(u[0])
                x.append(u[1])

            

            axes.scatter(x, y, label=str(f[100:]))

        axes.set_title('Scatter plot by log file on utm system')   
        axes.legend(loc=(1.04, 0))
        
        fig.savefig('scatter_by_log', bbox_inches='tight')