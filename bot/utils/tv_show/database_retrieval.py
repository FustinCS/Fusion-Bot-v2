from dataclasses import dataclass
import os
from dotenv import load_dotenv
from supabase import Client
from utils.tv_show.fetch_show_data import ShowData
import os
import psycopg2

load_dotenv()

@dataclass
class ShowEntry:
    show_id: int
    name: str
    current_season: int
    current_episode: int
    total_episodes: int
    date_added: str


class ShowExistsException(Exception):
    pass


def connect_to_db():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname="postgres",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    return conn


def get_season_episode_count(user_id:int, show_id: int) -> int:
    connection = connect_to_db()
    try:
        cursor = connection.cursor()

        cursor.execute(""" 
            SELECT s.episodes
            FROM "Show" s
            JOIN "Watches" w ON s.show_id = w.show_id
            WHERE w.user_id = %s AND w.show_id = %s AND s.season = w.current_season
        """, (user_id, show_id))

        result = cursor.fetchone()
        
        if not result:
            raise Exception("Show not found in profile")
        
        return result[0]

    except Exception as e:
        raise Exception()
    finally:
        cursor.close()
        connection.close()


def get_user_watch_list(user_id: int) -> list[ShowEntry]:
    """
    Fetches all of the users currently watched shows.
    """
    connection = connect_to_db()
    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT DISTINCT
                w.show_id, 
                s.name, 
                w.current_season, 
                w.current_episode, 
                s2.episodes AS current_season_total_episodes,
                w.date_updated
            FROM 
                "Watches" w
            JOIN 
                "Show" s ON w.show_id = s.show_id
            LEFT JOIN 
                "Show" s2 ON w.show_id = s2.show_id AND w.current_season = s2.season
            WHERE 
                w.user_id = 251839702951264257
            ORDER BY 
                w.date_updated DESC;
        """, (user_id,))

        results = cursor.fetchall()

        watch_list = [ShowEntry(*result) for result in results]
        return watch_list

    except Exception as e:
        raise Exception()
    finally:
        cursor.close()
        connection.close()

def add_watched_show(user_id: int, entry: ShowData):
    connection = connect_to_db()
    
    # insert into user if doesn't exist
    try:
        cursor = connection.cursor()

        cursor.execute("BEGIN;")

        cursor.execute("""
            INSERT INTO "User" (user_id)
            VALUES (%s)
            ON CONFLICT (user_id) DO NOTHING;
        """, (user_id,))

        for season in entry.seasons:
            cursor.execute("""
                INSERT INTO "Show" (show_id, season, name, episodes)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (show_id, season) DO NOTHING;
            """, (entry.show_id, season.season_number, entry.name, season.episode_count))

        cursor.execute("""
            INSERT INTO "Watches" (user_id, show_id, current_season, current_episode)
            VALUES (%s, %s, %s, %s)
        """, (user_id, entry.show_id, 1, 0))

        connection.commit()

    except psycopg2.IntegrityError as e:
        connection.rollback()
        raise ShowExistsException()
    except Exception as e:
        connection.rollback()
        print(f'Transaction Failed {e}')
        raise Exception()
    finally:
        cursor.close()
        connection.close()


def remove_watched_show(user_id: int, show_id: int) -> int:
    connection = connect_to_db()
    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM "Watches"
            WHERE
                user_id = %s AND show_id = %s;
        """, (user_id, show_id))
        
        connection.commit()

        return cursor.rowcount

    except Exception as e:
        connection.rollback()
        raise Exception()
    finally:
        cursor.close()
        connection.close()


def update_episode(user_id: int, show_id: int, episode: int):
    connection = connect_to_db()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE "Watches"
            SET current_episode = %s, date_updated = NOW()
            WHERE user_id = %s AND show_id = %s;           
        """, (episode, user_id, show_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise Exception()
    finally:
        cursor.close()
        connection.close()

def update_season(user_id: int, show_id: int, season: int):
    connection = connect_to_db()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE "Watches"
            SET current_season = %s, current_episode = 0, date_updated = NOW()
            WHERE user_id = %s AND show_id = %s;
        """, (season, user_id, show_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise Exception()
    finally:
        cursor.close()
        connection.close()