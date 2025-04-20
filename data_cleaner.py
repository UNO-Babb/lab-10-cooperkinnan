import pandas as pd
import numpy as np

def clean_music_data(df):
    """
    Clean the music dataset by handling missing values, outliers, and type conversions.
    
    Args:
        df (pandas.DataFrame): The original music dataframe
        
    Returns:
        pandas.DataFrame: Cleaned dataframe
    """
    # Make a copy to avoid modifying the original
    cleaned_df = df.copy()
    
    # Fill missing values for numeric columns with median or 0
    numeric_cols = cleaned_df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        # Fill with median for most numeric features
        if col.endswith('_year'):
            # For year, use a more meaningful value like the median
            median_year = cleaned_df[col].median()
            cleaned_df[col] = cleaned_df[col].fillna(median_year)
        else:
            # For other numeric values, fill with 0 or median depending on the context
            if 'hotttnesss' in col or 'familiarity' in col:
                cleaned_df[col] = cleaned_df[col].fillna(0)
            else:
                cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
    
    # Fill missing text data with 'Unknown' or appropriate placeholder
    text_cols = cleaned_df.select_dtypes(include=['object']).columns
    for col in text_cols:
        cleaned_df[col] = cleaned_df[col].fillna('Unknown')
    
    return cleaned_df

def handle_outliers(df, columns=None, method='clip'):
    """
    Handle outliers in the specified columns.
    
    Args:
        df (pandas.DataFrame): Input dataframe
        columns (list, optional): List of columns to process. If None, all numeric columns.
        method (str, optional): Method to handle outliers ('clip' or 'remove'). Defaults to 'clip'.
        
    Returns:
        pandas.DataFrame: Dataframe with handled outliers
    """
    # Make a copy to avoid modifying the original
    result_df = df.copy()
    
    # If no columns specified, use all numeric columns
    if columns is None:
        columns = result_df.select_dtypes(include=['float64', 'int64']).columns
    
    for col in columns:
        # Skip if column doesn't exist or isn't numeric
        if col not in result_df.columns or not pd.api.types.is_numeric_dtype(result_df[col]):
            continue
            
        # Calculate Q1, Q3 and IQR
        Q1 = result_df[col].quantile(0.25)
        Q3 = result_df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        # Define outlier bounds
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        if method == 'clip':
            # Clip values outside the bounds
            result_df[col] = result_df[col].clip(lower_bound, upper_bound)
        elif method == 'remove':
            # Remove rows with outlier values
            mask = (result_df[col] >= lower_bound) & (result_df[col] <= upper_bound)
            result_df = result_df[mask]
    
    return result_df

def prepare_data_for_analysis(df):
    """
    Prepare the data for analysis by creating derived features and normalizing values.
    
    Args:
        df (pandas.DataFrame): Cleaned dataframe
        
    Returns:
        pandas.DataFrame: Enhanced dataframe ready for analysis
    """
    # Create a copy to avoid modifying the original
    enhanced_df = df.copy()
    
    # Convert years to decades for easier trend analysis
    if 'song_year' in enhanced_df.columns:
        # Create a decade column (e.g., 1970, 1980, 1990)
        enhanced_df['decade'] = (enhanced_df['song_year'] // 10) * 10
        
        # Filter out unrealistic years (e.g., future years or very old ones)
        current_year = 2023  # Use the current year as a reference
        enhanced_df = enhanced_df[enhanced_df['song_year'] <= current_year]
        enhanced_df = enhanced_df[enhanced_df['song_year'] >= 1900]  # Assuming no relevant music data before 1900
    
    # Normalize hotttnesss and familiarity scores to 0-100 range for better interpretability
    for col in enhanced_df.columns:
        if 'hotttnesss' in col or 'familiarity' in col:
            # Some values might be outside 0-1 range, so we clip first
            enhanced_df[col] = enhanced_df[col].clip(0, 1)
            # Then scale to 0-100
            enhanced_df[col] = enhanced_df[col] * 100
    
    return enhanced_df
