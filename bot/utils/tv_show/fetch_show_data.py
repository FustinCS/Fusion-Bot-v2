from dataclasses import dataclass
from collections import namedtuple
import requests

Season = namedtuple('Season', ['season_number', 'episode_count'])

@dataclass
class ShowData:
    show_id: int
    name: str
    total_seasons: int
    image: int
    seasons: list[Season]


def fetch_show_data(show_name: str) -> ShowData:
    """
    Fetches TV show data from the TVMaze API.    
    """
    show_response = requests.get(f"https://api.tvmaze.com/singlesearch/shows?q={show_name}")
    show_data = show_response.json()
    
    show_id = show_data['id']
    name = show_data['name']
    image = show_data['image']['medium']

    season_response = requests.get(f"https://api.tvmaze.com/shows/{show_id}/seasons")
    season_data = season_response.json()

    total_seasons = len(season_data)
    
    seasons = []
    for season in season_data:
        season_number = season['number']
        episode_count = season['episodeOrder']
        seasons.append(Season(season_number, episode_count))
    
    return ShowData(show_id=show_id, name=name, total_seasons=total_seasons, image=image, seasons=seasons)

    