#ArtistLocationMap.py
#Name: Cooper Kinnan
#Date: 4/20/2025
#Assignment: Lab 10

import music
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Get music data
data = music.get_music()

# Extract artist locations
artist_names = []
latitudes = []
longitudes = []
popularity = []

for record in data:
    artist_data = record['artist']
    name = artist_data.get('name')
    lat = artist_data.get('latitude')
    lon = artist_data.get('longitude')
    pop = artist_data.get('hotttnesss')
    
    if name and lat is not None and lon is not None and pop is not None:
        artist_names.append(name)
        latitudes.append(lat)
        longitudes.append(lon)
        popularity.append(pop * 100)  # Scale to 0-100

# Create DataFrame
artist_df = pd.DataFrame({
    'Artist': artist_names,
    'Latitude': latitudes,
    'Longitude': longitudes,
    'Popularity': popularity
})

# Drop any rows with missing data
artist_df = artist_df.dropna()

print(f"Found {len(artist_df)} artists with valid location data")

# Create a world map
plt.figure(figsize=(14, 8))

# Set up the map background
plt.title('Global Distribution of Artists by Popularity', fontsize=16)
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)

# Set map boundaries
plt.xlim(-180, 180)
plt.ylim(-90, 90)

# Draw gridlines
plt.grid(alpha=0.3)

# Create custom colormap
colors = [(0.5, 0.5, 0.9), (0.9, 0.2, 0.2)]  # Light blue to red
cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=100)

# Draw scatter plot with popularity as size and color
scatter = plt.scatter(
    artist_df['Longitude'], 
    artist_df['Latitude'],
    c=artist_df['Popularity'],
    s=artist_df['Popularity'] * 2,  # Adjust size by popularity
    alpha=0.7,
    cmap=cmap,
    edgecolors='black',
    linewidths=0.5
)

# Add a colorbar
cbar = plt.colorbar(scatter)
cbar.set_label('Artist Popularity Score (0-100)', fontsize=12)

# Add contour lines for continents (very simplified)
# This is just to give an idea of where the continents are
continents_x = [-100, -70, 0, 30, 100, 140]
continents_y = [40, -20, 50, 0, 30, -30]
plt.plot(continents_x, continents_y, 'k-', alpha=0.3, linewidth=1)

# Save the figure
plt.tight_layout()
plt.savefig('artist_location_map.png')

print("Map created and saved as 'artist_location_map.png'")

# Analysis of artists by region
# Define rough regions
def get_region(lon, lat):
    if lon < -30:
        return "Americas"
    elif lon < 60:
        return "Europe/Africa"
    else:
        return "Asia/Pacific"

artist_df['Region'] = artist_df.apply(lambda row: get_region(row['Longitude'], row['Latitude']), axis=1)

# Count artists by region
region_counts = artist_df['Region'].value_counts()
print("\nArtist distribution by region:")
for region, count in region_counts.items():
    print(f"- {region}: {count} artists")

# Calculate average popularity by region
region_popularity = artist_df.groupby('Region')['Popularity'].mean()
print("\nAverage artist popularity by region:")
for region, avg_pop in region_popularity.items():
    print(f"- {region}: {avg_pop:.2f}")