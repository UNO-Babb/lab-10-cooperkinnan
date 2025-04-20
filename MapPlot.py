#MapPlot.py
#Name: Cooper Kinnan
#Date: 4/20/2025
#Assignment: Lab 10

import music
import pandas as pd
import matplotlib.pyplot as plt

# Get music data (need to call the function)
data = music.get_music()

# First check the structure of a single record
print("Sample data structure:")
sample_record = data[0]
print(f"Keys in data: {list(sample_record.keys())}")
print(f"Keys in song: {list(sample_record['song'].keys())}")

# Extract years and popularity (hotttnesss) from each song
years = []
popularity = []

for record in data:
    song_data = record['song']
    year = song_data.get('year')
    pop = song_data.get('hotttnesss')  # hotttnesss is the popularity metric
    
    if year is not None and pop is not None:
        years.append(year)
        popularity.append(pop * 100)  # Scale to 0-100 for better readability

# Create and clean the dataframe
df = pd.DataFrame({'Year': years, 'Popularity': popularity})
df = df.groupby('Year').mean().reset_index()

# Plot popularity over time
plt.figure(figsize=(12, 6))
plt.plot(df['Year'], df['Popularity'], marker='o', linewidth=2)
plt.title("Average Song Popularity Over Time", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Popularity (0-100)", fontsize=12)
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# Add annotations for decades
for decade in range(1960, 2030, 10):
    if decade in df['Year'].values:
        plt.axvline(x=decade, color='gray', linestyle='--', alpha=0.5)

# Clean the data by removing extreme outliers
df_clean = df[(df['Popularity'] > 0) & (df['Popularity'] <= 100)]

# Save the figure
plt.tight_layout()
plt.savefig('popularity_over_time.png')

# Don't try to display the plot interactively in headless environment
# plt.show()

print(f"Analysis complete. Analyzed {len(years)} songs across {len(df)} years.")
print("Plot saved as 'popularity_over_time.png'")