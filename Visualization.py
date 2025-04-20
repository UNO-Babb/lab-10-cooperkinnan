import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def set_plot_style():
    """Set the visual style for matplotlib plots"""
    plt.style.use('seaborn-v0_8-whitegrid')
    
def plot_decade_trend(df):
    """
    Create a line plot showing music trends over decades.
    
    Args:
        df (pandas.DataFrame): The prepared music dataframe with a 'decade' column
        
    Returns:
        fig: A matplotlib figure object
    """
    if 'decade' not in df.columns or 'song_hotttnesss' not in df.columns:
        st.error("Required columns for decade trend visualization are missing!")
        return None
    
    # Group by decade and calculate mean hotttnesss
    decade_data = df.groupby('decade')['song_hotttnesss'].agg(['mean', 'count']).reset_index()
    decade_data = decade_data[decade_data['count'] > 10]  # Filter out decades with too few songs
    
    # Create the figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(decade_data['decade'], decade_data['mean'], marker='o', linewidth=2)
    
    # Add labels and title
    ax.set_xlabel('Decade', fontsize=12)
    ax.set_ylabel('Average Song Popularity (Hotttnesss)', fontsize=12)
    ax.set_title('Music Popularity Trend by Decade', fontsize=14)
    
    # Add data labels
    for x, y in zip(decade_data['decade'], decade_data['mean']):
        ax.annotate(f'{y:.1f}', 
                   (x, y),
                   textcoords="offset points",
                   xytext=(0, 10),
                   ha='center')
    
    # Set y-axis to start from 0
    ax.set_ylim(bottom=0)
    
    # Add grid lines
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Rotate x-tick labels for better readability
    plt.xticks(decade_data['decade'], rotation=45)
    
    plt.tight_layout()
    return fig

def plot_key_distribution(df):
    """
    Create a bar chart showing the distribution of music keys.
    
    Args:
        df (pandas.DataFrame): The music dataframe with song_key column
        
    Returns:
        fig: A matplotlib figure object
    """
    if 'song_key' not in df.columns:
        st.error("Required column 'song_key' for key distribution visualization is missing!")
        return None
    
    # Map numeric keys to musical notation
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
    
    # Count the key distribution
    key_counts = df['song_key'].value_counts().reset_index()
    key_counts.columns = ['key', 'count']
    
    # Convert numeric keys to musical notation
    key_counts['key_name'] = key_counts['key'].map(lambda x: key_mapping.get(x, 'Unknown'))
    
    # Sort by musical notation
    key_counts = key_counts.sort_values('key')
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot horizontal bars
    bars = ax.barh(key_counts['key_name'], key_counts['count'], color='skyblue')
    
    # Add count labels to the bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 5, bar.get_y() + bar.get_height()/2, f'{width:.0f}',
                ha='left', va='center')
    
    # Add labels and title
    ax.set_xlabel('Number of Songs', fontsize=12)
    ax.set_ylabel('Musical Key', fontsize=12)
    ax.set_title('Distribution of Songs by Musical Key', fontsize=14)
    
    # Add grid lines
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    return fig

def create_tempo_histogram(df):
    """
    Create a histogram showing the distribution of song tempos.
    
    Args:
        df (pandas.DataFrame): The music dataframe with song_tempo column
        
    Returns:
        fig: A plotly figure object
    """
    if 'song_tempo' not in df.columns:
        st.error("Required column 'song_tempo' for tempo histogram is missing!")
        return None
    
    # Create histogram with Plotly
    fig = px.histogram(
        df, 
        x='song_tempo',
        nbins=30,
        title='Distribution of Song Tempos (BPM)',
        labels={'song_tempo': 'Tempo (BPM)'},
        color_discrete_sequence=['#3366CC']
    )
    
    # Add tempo categories annotation
    fig.add_annotation(
        x=60, y=0.9,
        xref="x", yref="paper",
        text="Slow",
        showarrow=False,
        font=dict(size=14)
    )
    
    fig.add_annotation(
        x=120, y=0.9,
        xref="x", yref="paper",
        text="Medium",
        showarrow=False,
        font=dict(size=14)
    )
    
    fig.add_annotation(
        x=180, y=0.9,
        xref="x", yref="paper",
        text="Fast",
        showarrow=False,
        font=dict(size=14)
    )
    
    # Add vertical lines to mark tempo categories
    fig.add_vline(x=90, line_dash="dash", line_color="gray")
    fig.add_vline(x=150, line_dash="dash", line_color="gray")
    
    # Update layout
    fig.update_layout(
        xaxis_title="Tempo (BPM)",
        yaxis_title="Number of Songs",
        bargap=0.1,
    )
    
    return fig

def plot_loudness_vs_popularity(df):
    """
    Create a scatter plot showing the relationship between song loudness and popularity.
    
    Args:
        df (pandas.DataFrame): The music dataframe with song_loudness and song_hotttnesss columns
        
    Returns:
        fig: A plotly figure object
    """
    if 'song_loudness' not in df.columns or 'song_hotttnesss' not in df.columns:
        st.error("Required columns for loudness vs popularity visualization are missing!")
        return None
    
    # Create a scatter plot
    fig = px.scatter(
        df,
        x='song_loudness',
        y='song_hotttnesss',
        title='Relationship Between Song Loudness and Popularity',
        labels={
            'song_loudness': 'Loudness (dB)',
            'song_hotttnesss': 'Popularity Score'
        },
        opacity=0.7,
        color_discrete_sequence=['#FF5733']
    )
    
    # Add trendline
    fig.update_traces(marker=dict(size=8))
    
    # Add a trend line
    fig.update_layout(
        xaxis_title="Loudness (dB)",
        yaxis_title="Popularity Score",
        showlegend=False
    )
    
    # Add a trend line using plotly's built-in functionality
    fig = px.scatter(
        df,
        x='song_loudness',
        y='song_hotttnesss',
        trendline='ols',
        title='Relationship Between Song Loudness and Popularity',
        labels={
            'song_loudness': 'Loudness (dB)',
            'song_hotttnesss': 'Popularity Score'
        },
        opacity=0.7
    )
    
    return fig

def create_artist_location_map(df):
    """
    Create a map visualization of artist locations.
    
    Args:
        df (pandas.DataFrame): The music dataframe with artist location data
        
    Returns:
        fig: A plotly figure object
    """
    # Filter out rows without valid coordinates
    map_df = df.dropna(subset=['artist_latitude', 'artist_longitude'])
    
    if len(map_df) == 0:
        st.error("No valid location data found for mapping!")
        return None
    
    # Add popularity for size reference
    map_df['size'] = map_df['artist_hotttnesss'].fillna(0) * 50 + 10
    
    # Create the map
    fig = px.scatter_geo(
        map_df,
        lat='artist_latitude',
        lon='artist_longitude',
        hover_name='artist_name',
        size='size',
        color='artist_hotttnesss',
        color_continuous_scale=px.colors.sequential.Viridis,
        projection='natural earth',
        title='Global Distribution of Artists by Popularity',
        labels={'artist_hotttnesss': 'Artist Popularity'}
    )
    
    # Update layout
    fig.update_layout(
        geo=dict(
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
            showocean=True,
            oceancolor='rgb(230, 255, 255)'
        )
    )
    
    return fig
