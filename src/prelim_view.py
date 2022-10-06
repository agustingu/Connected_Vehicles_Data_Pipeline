#%%
import pandas as pd


df = pd.read_csv('log_0153_1970-01-01_00-00-41-142.log.001_out.csv')
df_filtered = df[abs(df['latitude']) > 10] 


# The data seems to be factored by 10^7 for coordinates
df_filtered['longitude'] = df_filtered['longitude'].div(10000000)
df_filtered['latitude'] = df_filtered['latitude'].div(10000000)
df_filtered['Dsecond'] = df_filtered['Dsecond'].div(1000)
print(df_filtered.head())
df_filtered.plot(x ='longitude', y='latitude', kind = 'scatter')

# %%
import folium
gainesville = folium.Map(zoom_start=10,
    location=[29.63693, -82.349996])
# %%
for _, indx in df_filtered.iterrows():
    folium.Marker(location=[indx["latitude"], indx["longitude"]]).add_to(gainesville)
gainesville 

# %%
folium.CircleMarker(location=(29.63693, -82.349996),radius=0, # center
fill_color='blue').add_to(gainesville)
gainesville
# %%
folium.CircleMarker(location=(29.69693, -82.409996),radius=0,  # ul
fill_color='blue').add_to(gainesville)
gainesville
# %%
# %%
folium.CircleMarker(location=(29.59693, -82.409996),radius=0, # ll
fill_color='blue').add_to(gainesville)
gainesville
# %%
# %%
folium.CircleMarker(location=(29.59693, -82.309996),radius=0, #lr
fill_color='blue').add_to(gainesville)
gainesville
# %%
# %%
folium.CircleMarker(location=(29.69693, -82.309996),radius=0, # ur
fill_color='blue').add_to(gainesville)
gainesville
# %%
