import pandas as pd
import numpy as np
import random
import os
__all__ = ['get_music']
def generate_sample_music_data(n_records=200):
    """
    Generate sample music data for demonstration purposes.
    
    Args:
        n_records (int): Number of records to generate
        
    Returns:
        list: A list of dictionaries containing sample music data
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Sample artists
    artists = [
        "The Beatles", "Queen", "Michael Jackson", "Madonna", "Beyoncé",
        "Elvis Presley", "Taylor Swift", "Adele", "Ed Sheeran", "Rihanna",
        "Coldplay", "Kanye West", "Lady Gaga", "Bruno Mars", "Ariana Grande",
        "Justin Bieber", "Katy Perry", "Eminem", "Drake", "Billie Eilish"
    ]
    
    # Sample terms (genres)
    terms = [
        "rock", "pop", "hip hop", "r&b", "soul", "electronic", "jazz", 
        "blues", "country", "metal", "classical", "reggae", "folk", 
        "indie", "dance", "punk", "funk", "disco"
    ]
    
    # Sample song titles for each artist
    song_titles = {
        "The Beatles": ["Hey Jude", "Let It Be", "Yesterday", "Come Together"],
        "Queen": ["Bohemian Rhapsody", "We Will Rock You", "Radio Ga Ga"],
        "Michael Jackson": ["Thriller", "Billie Jean", "Beat It"],
        "Madonna": ["Like a Prayer", "Material Girl", "Vogue"],
        "Beyoncé": ["Crazy in Love", "Single Ladies", "Halo"],
        "Elvis Presley": ["Jailhouse Rock", "Can't Help Falling in Love", "Suspicious Minds"],
        "Taylor Swift": ["Shake It Off", "Blank Space", "Love Story"],
        "Adele": ["Hello", "Rolling in the Deep", "Someone Like You"],
        "Ed Sheeran": ["Shape of You", "Perfect", "Thinking Out Loud"],
        "Rihanna": ["Umbrella", "Diamonds", "Work"],
        "Coldplay": ["Viva la Vida", "Fix You", "Paradise"],
        "Kanye West": ["Stronger", "Gold Digger", "Power"],
        "Lady Gaga": ["Bad Romance", "Poker Face", "Born This Way"],
        "Bruno Mars": ["Uptown Funk", "Just the Way You Are", "24K Magic"],
        "Ariana Grande": ["Thank U, Next", "7 Rings", "No Tears Left to Cry"],
        "Justin Bieber": ["Sorry", "Love Yourself", "What Do You Mean?"],
        "Katy Perry": ["Roar", "Firework", "Dark Horse"],
        "Eminem": ["Lose Yourself", "The Real Slim Shady", "Not Afraid"],
        "Drake": ["Hotline Bling", "God's Plan", "One Dance"],
        "Billie Eilish": ["Bad Guy", "Lovely", "Ocean Eyes"]
    }
    
    # Generate data
    music_data = []
    
    for _ in range(n_records):
        # Choose a random artist
        artist_name = random.choice(artists)
        
        # Generate artist data
        artist_hotttnesss = random.uniform(0, 1)
        artist_familiarity = random.uniform(0, 1)
        artist_id = f"AR{random.randint(10000, 99999)}"
        
        # Generate location data (some might be None)
        has_location = random.random() > 0.2
        if has_location:
            latitude = random.uniform(-90, 90)
            longitude = random.uniform(-180, 180)
        else:
            latitude = None
            longitude = None
        
        # Generate artist terms
        artist_term_count = random.randint(1, 5)
        artist_terms = random.sample(terms, artist_term_count)
        artist_terms_freq = [random.uniform(0, 1) for _ in range(artist_term_count)]
        
        # Generate song data
        song_title = random.choice(song_titles[artist_name])
        song_hotttnesss = random.uniform(0, 1)
        song_duration = random.uniform(120, 400)  # 2-6.5 minutes
        song_key = random.randint(0, 11)  # 0=C, 1=C#, etc.
        song_tempo = random.uniform(60, 200)  # BPM
        song_time_signature = random.choice([3, 4, 5, 6])
        song_loudness = random.uniform(-15, -1)  # dB
        
        # Generate year (with some distribution over decades)
        decades = [1960, 1970, 1980, 1990, 2000, 2010, 2020]
        weights = [0.05, 0.1, 0.15, 0.2, 0.25, 0.2, 0.05]
        decade = random.choices(decades, weights=weights)[0]
        year = decade + random.randint(0, 9)
        
        # Create the record
        record = {
            "artist": {
                "familiarity": artist_familiarity,
                "hotttnesss": artist_hotttnesss,
                "id": artist_id,
                "latitude": latitude,
                "longitude": longitude,
                "location": "unknown",  # We don't have real location names
                "name": artist_name,
                "similar": random.uniform(0, 1),
                "terms": artist_terms[0] if artist_terms else "unknown",
                "terms_freq": artist_terms_freq[0] if artist_terms_freq else 0
            },
            "release": {
                "id": random.randint(10000, 99999),
                "name": random.randint(10000, 99999)
            },
            "song": {
                "artist_mbtags": [],
                "artist_mbtags_count": [],
                "bars_confidence": random.uniform(0, 1),
                "bars_start": [],
                "beats_confidence": random.uniform(0, 1),
                "beats_start": [],
                "duration": song_duration,
                "end_of_fade_in": random.uniform(0, 3),
                "hotttnesss": song_hotttnesss,
                "key": song_key,
                "key_confidence": random.uniform(0, 1),
                "loudness": song_loudness,
                "mode": random.randint(0, 1),
                "mode_confidence": random.uniform(0, 1),
                "start_of_fade_out": song_duration - random.uniform(0, 10),
                "tatums_confidence": [],
                "tatums_start": [],
                "tempo": song_tempo,
                "time_signature": song_time_signature,
                "time_signature_confidence": random.uniform(0, 1),
                "title": song_title,
                "year": year
            }
        }
        
        music_data.append(record)
    
    return music_data
# Cache for the dataset
_DATASET = None
def get_music():
    """
    Get the music dataset.
    
    Returns:
        list: A list of dictionaries containing music data
    """
    global _DATASET
    if _DATASET is None:
        # Generate sample data
        _DATASET = generate_sample_music_data(500)
    return _DATASET
if __name__ == '__main__':
    from pprint import pprint
    
    # Test the function
    data = get_music()
    print(f"Generated {len(data)} sample music records.")
    pprint(data[0])
