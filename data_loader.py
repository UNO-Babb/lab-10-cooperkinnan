import music
import pandas as pd
import numpy as np

def load_music_data():
    """
    Load the CORGIS music dataset and convert it to a pandas DataFrame for easier analysis.
    
    Returns:
        pandas.DataFrame: A DataFrame containing the music dataset
    """
    # Load the raw data from the music module
    raw_data = music.get_music()
    
    # Convert to pandas DataFrame for easier manipulation
    return pd.DataFrame(raw_data)

def explore_data_structure(df):
    """
    Explore and return basic information about the dataset structure.
    
    Args:
        df (pandas.DataFrame): The music dataset
        
    Returns:
        dict: A dictionary containing basic information about the dataset
    """
    structure = {
        "total_records": len(df),
        "columns": df.columns.tolist(),
        "sample_data": df.head(3).to_dict('records'),
        "data_types": {col: str(df[col].dtype) for col in df.columns}
    }
    
    # Extract nested structure information
    for col in df.columns:
        if df[col].dtype == 'object':
            # Get a non-null sample
            sample = df[col].dropna().iloc[0] if not df[col].dropna().empty else None
            if isinstance(sample, dict):
                structure[f"{col}_keys"] = list(sample.keys())
    
    return structure

def flatten_nested_features(df):
    """
    Flatten nested features in the DataFrame for easier analysis.
    
    Args:
        df (pandas.DataFrame): The music dataset with nested features
        
    Returns:
        pandas.DataFrame: A flattened DataFrame with extracted features
    """
    # Create a copy of the DataFrame to avoid modifying the original
    flattened_df = df.copy()
    
    # Process artist features
    artist_features = ['familiarity', 'hotttnesss', 'id', 'latitude', 'longitude', 'name', 'terms', 'terms_freq']
    for feature in artist_features:
        flattened_df[f'artist_{feature}'] = flattened_df['artist'].apply(
            lambda x: x.get(feature) if isinstance(x, dict) and feature in x else None
        )
    
    # Process song features - selecting a subset of important features
    song_features = ['duration', 'hotttnesss', 'key', 'loudness', 'tempo', 'time_signature', 'title', 'year']
    for feature in song_features:
        flattened_df[f'song_{feature}'] = flattened_df['song'].apply(
            lambda x: x.get(feature) if isinstance(x, dict) and feature in x else None
        )
    
    # Drop the original nested columns
    flattened_df = flattened_df.drop(['artist', 'song', 'release'], axis=1)
    
    return flattened_df
