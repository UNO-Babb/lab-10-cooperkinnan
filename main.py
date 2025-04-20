#main.py
#Name: Cooper Kinnan
#Date: 4/20/2025
#Assignment: Lab 10
import music
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def main():
    # Get music data
    data = music.get_music()
    print(f"Loaded {len(data)} music records")
    
    # Print a sample record to see its structure
    print("\nSample music record structure:")
    sample = data[0]
    print(f"Artist name: {sample['artist']['name']}")
    print(f"Song title: {sample['song']['title']}")
    print(f"Year: {sample['song']['year']}")
    print(f"Popularity: {sample['song']['hotttnesss']:.2f}")
    
    # Extract years and popularity data
    years = []
    popularity = []
    
    for record in data:
        year = record['song']['year']
        pop = record['song']['hotttnesss']
        if year is not None and pop is not None:
            years.append(year)
            popularity.append(pop * 100)  # Scale to 0-100
    
    # Create a dataframe and group by year
    df = pd.DataFrame({'Year': years, 'Popularity': popularity})
    df = df.groupby('Year').mean().reset_index()
    
    # Plot popularity over time
    plt.figure(figsize=(12, 6))
    plt.plot(df['Year'], df['Popularity'], marker='o', linewidth=2)
    plt.title("Average Song Popularity Over Time", fontsize=16)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Popularity (0-100)", fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Add vertical lines for decades
    for decade in range(1960, 2030, 10):
        if decade in df['Year'].values:
            plt.axvline(x=decade, color='gray', linestyle='--', alpha=0.5)
    
    # Clean the data by removing outliers
    df_clean = df[(df['Popularity'] > 0) & (df['Popularity'] <= 100)]
    
    # Save the figure
    plt.tight_layout()
    plt.savefig('popularity_by_year.png')
    print("Plot saved as 'popularity_by_year.png'")
    
    # Key distribution analysis
    # Create key mapping
    key_mapping = {
        0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
        6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'
    }
    
    # Extract keys
    keys = []
    for record in data:
        key = record['song'].get('key')
        if key is not None and key in key_mapping:
            keys.append(key_mapping[key])
    
    # Count keys
    key_counts = pd.Series(keys).value_counts().sort_index()
    
    # Plot key distribution
    plt.figure(figsize=(10, 6))
    plt.bar(key_counts.index, key_counts.values, color='skyblue')
    plt.title('Distribution of Songs by Musical Key', fontsize=16)
    plt.xlabel('Musical Key', fontsize=12)
    plt.ylabel('Number of Songs', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('key_distribution.png')
    print("Key distribution saved as 'key_distribution.png'")
    
    # Print data insights
    print("\nData Insights:")
    print(f"1. Analyzed {len(years)} songs with valid year and popularity data")
    
    # Most popular year
    most_popular_year = df.loc[df['Popularity'].idxmax()]
    print(f"2. The most popular year for music was {int(most_popular_year['Year'])} with an average popularity of {most_popular_year['Popularity']:.2f}")
    
    # Most common key
    most_common_key = key_counts.idxmax()
    print(f"3. The most common musical key is {most_common_key} with {key_counts[most_common_key]} songs")
    
    # Trend analysis
    early_years = df[df['Year'] < 1990]['Popularity'].mean()
    later_years = df[df['Year'] >= 1990]['Popularity'].mean()
    
    trend = "increased" if later_years > early_years else "decreased"
    print(f"4. Song popularity has {trend} over time. Average popularity before 1990: {early_years:.2f}, after 1990: {later_years:.2f}")
if __name__ == "__main__":
    main()