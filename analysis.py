import pandas as pd
import numpy as np
import streamlit as st

def get_decade_insights(df):
    """
    Generate insights about music trends across decades.
    
    Args:
        df (pandas.DataFrame): The prepared music dataframe
        
    Returns:
        str: Text with insights about decade trends
    """
    if 'decade' not in df.columns:
        return "Decade analysis not available - missing required data."
    
    # Group by decade
    decade_stats = df.groupby('decade').agg({
        'song_hotttnesss': ['mean', 'count'],
        'song_tempo': 'mean',
        'song_loudness': 'mean',
        'song_duration': 'mean'
    }).reset_index()
    
    # Flatten the multi-index
    decade_stats.columns = ['_'.join(col).strip('_') for col in decade_stats.columns.values]
    
    # Find the most popular decade
    most_popular_decade = decade_stats.loc[decade_stats['song_hotttnesss_mean'].idxmax()]['decade']
    
    # Find decade with most songs
    decade_with_most_songs = decade_stats.loc[decade_stats['song_hotttnesss_count'].idxmax()]['decade']
    
    # Analyze tempo trend
    tempo_increasing = decade_stats['song_tempo_mean'].iloc[-1] > decade_stats['song_tempo_mean'].iloc[0]
    
    # Analyze loudness trend
    loudness_trend = "increased" if decade_stats['song_loudness_mean'].iloc[-1] > decade_stats['song_loudness_mean'].iloc[0] else "decreased"
    
    # Generate insights
    insights = f"""
    ## Decade Analysis Insights
    
    - The most popular decade in the dataset (highest average popularity) is the {most_popular_decade}s.
    - The most represented decade with {decade_stats.loc[decade_stats['decade'] == decade_with_most_songs, 'song_hotttnesss_count'].values[0]:.0f} songs is the {decade_with_most_songs}s.
    - Song tempo has {'increased' if tempo_increasing else 'decreased'} over time, from approximately {decade_stats['song_tempo_mean'].iloc[0]:.1f} BPM to {decade_stats['song_tempo_mean'].iloc[-1]:.1f} BPM.
    - Song loudness has {loudness_trend} over the decades, reflecting changes in music production techniques.
    - The average song duration was {decade_stats['song_duration_mean'].iloc[-1]/60:.2f} minutes in recent years compared to {decade_stats['song_duration_mean'].iloc[0]/60:.2f} minutes in earlier decades.
    """
    
    return insights

def get_musical_attributes_insights(df):
    """
    Generate insights about musical attributes like key, tempo, and loudness.
    
    Args:
        df (pandas.DataFrame): The prepared music dataframe
        
    Returns:
        str: Text with insights about musical attributes
    """
    # Create key mapping for reference
    key_mapping = {
        0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
        6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'
    }
    
    # Check if required columns exist
    if 'song_key' not in df.columns or 'song_tempo' not in df.columns:
        return "Musical attributes analysis not available - missing required data."
    
    # Find most common key
    most_common_key = df['song_key'].value_counts().idxmax()
    most_common_key_name = key_mapping.get(most_common_key, 'Unknown')
    
    # Calculate average tempo
    avg_tempo = df['song_tempo'].mean()
    
    # Categorize songs by tempo
    slow_songs = (df['song_tempo'] < 90).sum()
    medium_songs = ((df['song_tempo'] >= 90) & (df['song_tempo'] < 150)).sum()
    fast_songs = (df['song_tempo'] >= 150).sum()
    
    # Find correlation between loudness and popularity
    if 'song_loudness' in df.columns and 'song_hotttnesss' in df.columns:
        loudness_popularity_corr = df['song_loudness'].corr(df['song_hotttnesss'])
    else:
        loudness_popularity_corr = "Not available"
    
    # Generate insights
    insights = f"""
    ## Musical Attributes Insights
    
    - The most common musical key is {most_common_key_name} (representing {df['song_key'].value_counts().iloc[0]/len(df)*100:.1f}% of songs).
    - The average tempo across all songs is {avg_tempo:.1f} BPM (beats per minute).
    - Tempo distribution: {slow_songs} slow songs (<90 BPM), {medium_songs} medium songs (90-150 BPM), and {fast_songs} fast songs (>150 BPM).
    - The correlation between song loudness and popularity is {loudness_popularity_corr if isinstance(loudness_popularity_corr, str) else loudness_popularity_corr:.2f}, which suggests that {'louder songs tend to be more popular' if isinstance(loudness_popularity_corr, float) and loudness_popularity_corr > 0.1 else 'there is no strong relationship between loudness and popularity'}.
    """
    
    return insights

def get_artist_insights(df):
    """
    Generate insights about artists in the dataset.
    
    Args:
        df (pandas.DataFrame): The prepared music dataframe
        
    Returns:
        str: Text with insights about artists
    """
    # Check if required columns exist
    if 'artist_name' not in df.columns or 'artist_hotttnesss' not in df.columns:
        return "Artist analysis not available - missing required data."
        
    # Count unique artists
    unique_artists = df['artist_name'].nunique()
    
    # Find top artists by popularity
    top_artists = df.sort_values('artist_hotttnesss', ascending=False).head(5)['artist_name'].tolist()
    
    # Analyze geographic distribution if location data is available
    has_location_data = 'artist_latitude' in df.columns and 'artist_longitude' in df.columns
    location_insights = ""
    
    if has_location_data:
        # Count artists with location data
        artists_with_location = df.dropna(subset=['artist_latitude', 'artist_longitude'])['artist_name'].nunique()
        
        # Group by rough geographic region
        df['region'] = 'Unknown'
        df.loc[df['artist_longitude'] < -30, 'region'] = 'Americas'
        df.loc[(df['artist_longitude'] >= -30) & (df['artist_longitude'] < 60), 'region'] = 'Europe/Africa'
        df.loc[df['artist_longitude'] >= 60, 'region'] = 'Asia/Pacific'
        
        region_counts = df['region'].value_counts()
        
        location_insights = f"""
        - {artists_with_location} out of {unique_artists} artists have geographical location data.
        - Geographic distribution of artists: {region_counts.get('Americas', 0)} from the Americas, {region_counts.get('Europe/Africa', 0)} from Europe/Africa, and {region_counts.get('Asia/Pacific', 0)} from Asia/Pacific region.
        """
    
    # Generate insights
    insights = f"""
    ## Artist Insights
    
    - The dataset contains {unique_artists} unique artists.
    - The top 5 most popular artists are: {', '.join(top_artists)}.
    {location_insights}
    """
    
    return insights
