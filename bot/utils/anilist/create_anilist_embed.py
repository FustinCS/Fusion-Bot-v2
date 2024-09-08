from discord import Embed, Color
from utils.anilist.fetch_anilist_data import AnimeEntry

def create_anilist_embeds(entries: list[AnimeEntry], username: str) -> list[Embed]:
    """
    Creates a list of embeds to display the user's anime entries.
    """
    embeds = []

    for i in range(0, len(entries), 10):
        # fetch 10 entries at a time
        current_entries = entries[i:i + 10]

        embed = Embed(
            title=username,
            color=Color.blue()
        )

        embed.add_field(
            name="Title",
            value="\n".join([entry.title for entry in current_entries]),
            inline=True
        )

        embed.add_field(
            name="Score",
            value="\n".join([str(entry.score) for entry in current_entries]),
            inline=True
        )
        
        embed.add_field(
            name="Type",
            value="\n".join([entry.show_format for entry in current_entries]),
            inline=True
        )

        embeds.append(embed)

    return embeds