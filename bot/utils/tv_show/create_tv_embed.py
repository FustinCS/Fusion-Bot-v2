from discord import Embed, Color
from utils.tv_show.database_retrieval import ShowEntry

def create_tv_embeds(entries: list[ShowEntry], username: str) -> list[Embed]:
    """
    Creates a list of embeds to display TV show entries.
    """

    embeds = []

    for i in range(0, len(entries), 10):
        #fetch 10 entries at a time
        current_entries = entries[i:i + 10]
        
        embed = Embed(
            title=username,
            color=Color.random()
        )

        embed.add_field(
            name="Title",
            value="\n".join([entry.name for entry in current_entries]),
            inline=True
        )

        embed.add_field(
            name="Season",
            value="\n".join([str(entry.current_season) for entry in current_entries]),
            inline=True
        )

        episode_display = []
        for entry in current_entries:
            if entry.total_episodes == None or entry.total_episodes == 0:
                episode_display.append(f'{str(entry.current_episode)}')
            else:
                episode_display.append(f'{str(entry.current_episode)}/{str(entry.total_episodes)}')

        embed.add_field(
            name="Episode",
            value="\n".join(episode_display),
            inline=True
        )

        embeds.append(embed)

    return embeds