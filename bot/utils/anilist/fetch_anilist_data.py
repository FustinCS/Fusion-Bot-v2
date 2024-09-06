import requests
from dataclasses import dataclass

@dataclass
class AnimeEntry:
    title: str
    score: float
    format: str


def fetch_anilist_data(username: str) -> list[AnimeEntry]:
    """
    Fetches data from Anilist GraphQL API.

    Params: username (str) - Anilist username
    """

    url = 'https://graphql.anilist.co'

    # create GraphQL query
    query = '''
            query ($username: String) {
                MediaListCollection (userName: $username, type: ANIME, status: COMPLETED, sort: SCORE_DESC) {
                    user {
                        name
                    }
                    lists {
                        entries {
                            progress
                            score(format: POINT_10_DECIMAL)
                            media {
                                title {
                                    english
                                    romaji
                                }
                                format
                            }
                        }
                    }
                }
            }
        '''
    
    variables = {
        'username': username
    }

    # gathering all the information from my query and storing it in variables via requests library
    response = requests.post(url, json={'query': query, 'variables': variables})
    json_data = response.json()

    return json_data


def create_entries_list(json_data: dict) -> list[AnimeEntry]:
    """
    Creates a list of all anime entries on the user's Anilist profile.
    """
    entries_json_data = json_data['data']['MediaListCollection']['lists'][0]['entries']
    entries = []

    for entry in entries_json_data:
        entries.append(_create_entry(entry))

    return entries


def _create_entry(entries_json_data: dict):
    """
    Creates a single entry object to store anime information.
    """
    entry = AnimeEntry()

    entry.title = entries_json_data['media']['title']['english']
    entry.score = entries_json_data['score']
    entry.format = entries_json_data['media']['format']

    return entry


        
        



