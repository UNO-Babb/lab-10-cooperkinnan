#MusicalAttributes.py
#Name: Cooper Kinnan
#Date: 4/20/2025
#Assignment: Lab 10

import music
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Get music data
data = music.get_music()

# Extract musical attributes
keys = []
tempos = []
loudness = []
duration = []
years = []
popularity = []

# Key mapping
key_mapping = {
    0: 'C',
    1: 'C#',
    2: 'D',
    3: 'D#',
    4: 'E',
    5: 'F',
    6: 'F#',
    7: 'G',
    8: 'G#',
    9: 'A',
    10: 'A#',
    11: 'B'
}

for record in data:
    song_data = record['song']
    
    key = song_data.get('key')
    tempo = song_data.get('tempo')
    loud = song_data.get('loudness')
    dur = song_data.get('duration')
    year = song_data.get('year')
    pop = song_data.get('hotttnesss')
    
    if key is not None and key in key_mapping:
        keys.append(key_mapping[key])
    
    if tempo is not None:
        tempos.append(tempo)
    
    if loud is not None:
        loudness.append(loud)
    
    if dur is not None:
        duration.append(dur / 60)  # Convert to minutes
    
    if year is not None and pop is not None:
        years.append(year)
        popularity.append(pop * 100)  # Scale to 0-100

print(f"Extracted data from {len(data)} songs")

# Create a figure with 2x2 subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Key Distribution
key_counts = pd.Series(keys).value_counts().sort_index()
axes[0, 0].bar(key_counts.index, key_counts.values, color='skyblue')
axes[0, 0].set_title('Distribution of Musical Keys', fontsize=14)
axes[0, 0].set_xlabel('Key')
axes[0, 0].set_ylabel('Number of Songs')
axes[0, 0].grid(alpha=0.3)

# 2. Tempo Distribution
axes[0, 1].hist(tempos, bins=20, color='lightgreen', edgecolor='black')
axes[0, 1].set_title('Distribution of Song Tempos', fontsize=14)
axes[0, 1].set_xlabel('Tempo (BPM)')
axes[0, 1].set_ylabel('Number of Songs')
axes[0, 1].axvline(x=90, color='red', linestyle='--', alpha=0.7, label='Slow/Medium')
axes[0, 1].axvline(x=150, color='blue', linestyle='--', alpha=0.7, label='Medium/Fast')
axes[0, 1].legend()
axes[0, 1].grid(alpha=0.3)

# 3. Loudness vs. Popularity Scatter Plot
axes[1, 0].scatter(loudness, popularity, alpha=0.5, c='purple')
axes[1, 0].set_title('Relationship Between Loudness and Popularity', fontsize=14)
axes[1, 0].set_xlabel('Loudness (dB)')
axes[1, 0].set_ylabel('Popularity Score')

# Calculate and display correlation
if loudness and popularity:
    correlation = np.corrcoef(loudness, popularity)[0, 1]
    axes[1, 0].annotate(f'Correlation: {correlation:.2f}', 
                        xy=(0.05, 0.95), 
                        xycoords='axes fraction',
                        fontsize=12,
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
axes[1, 0].grid(alpha=0.3)

# 4. Duration Distribution
axes[1, 1].hist(duration, bins=20, color='salmon', edgecolor='black')
axes[1, 1].set_title('Distribution of Song Durations', fontsize=14)
axes[1, 1].set_xlabel('Duration (minutes)')
axes[1, 1].set_ylabel('Number of Songs')
axes[1, 1].grid(alpha=0.3)

# Adjust spacing between subplots
plt.tight_layout()

# Save the figure
plt.savefig('musical_attributes_analysis.png')

print("Musical attributes analysis completed and saved as 'musical_attributes_analysis.png'")

# Additional analysis: classify songs by tempo
slow_songs = sum(1 for tempo in tempos if tempo < 90)
medium_songs = sum(1 for tempo in tempos if 90 <= tempo < 150)
fast_songs = sum(1 for tempo in tempos if tempo >= 150)

print("\nSongs by tempo category:")
print(f"- Slow (<90 BPM): {slow_songs} songs ({slow_songs/len(tempos)*100:.1f}%)")
print(f"- Medium (90-150 BPM): {medium_songs} songs ({medium_songs/len(tempos)*100:.1f}%)")
print(f"- Fast (>150 BPM): {fast_songs} songs ({fast_songs/len(tempos)*100:.1f}%)")

# Calculate average song durations by decade
song_data = pd.DataFrame({'Year': years, 'Duration': duration})
song_data['Decade'] = (song_data['Year'] // 10) * 10
decade_durations = song_data.groupby('Decade')['Duration'].mean()

print("\nAverage song duration by decade:")
for decade, avg_duration in decade_durations.items():
    print(f"- {decade}s: {avg_duration:.2f} minutes")