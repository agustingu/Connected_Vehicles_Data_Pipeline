#%%
import pandas as pd


df = pd.read_csv('log_0143_2022-09-07_15-10-52-333.log_out.csv')
df_filtered = df[abs(df['latitude']) > 10] 


# The data seems to be factored by 10^7 for coordinates
df_filtered['longitude'] = df_filtered['longitude'].div(10000000)
df_filtered['latitude'] = df_filtered['latitude'].div(10000000)
df_filtered['Dsecond'] = df_filtered['Dsecond'].div(1000)
print(df_filtered.head())
df_filtered.plot(x ='longitude', y='latitude', kind = 'scatter')

# %%
import folium
gainesville = folium.Map(zoom_start=15,
    location=[29.63693, -82.349996])
# %%
for _, indx in df_filtered.iterrows():
    folium.Marker(location=[indx["latitude"], indx["longitude"]]).add_to(gainesville)
gainesville 

# %%
