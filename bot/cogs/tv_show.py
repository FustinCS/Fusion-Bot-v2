import discord
from discord import app_commands
from discord.ext import commands
from utils.anilist.pagination import ButtonView
from utils.tv_show.create_tv_embed import create_tv_embeds
from utils.tv_show.database_retrieval import add_watched_show, ShowExistsException, get_user_watch_list, remove_watched_show
from utils.tv_show.fetch_show_data import fetch_show_data

class TVShow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("tv_show.py is ready!")

    @app_commands.command(name="tv-profile", description="Displays TV Shows List")
    async def tv_profile(self, interaction: discord.Interaction):
        await interaction.response.send_message("TV Show Profile")

    @app_commands.command(name="display-tv-data", description="Displays TV Show Data")
    async def display_tv_data(self, interaction: discord.Interaction, show_name: str):
        show_data = fetch_show_data(show_name)

        print(show_data.show_id)
        print(show_data.name)
        print(show_data.total_seasons)
        print(show_data.seasons)

        await interaction.response.send_message("Success!")
    
    @app_commands.command(name="tv-display", description="Displays TV Show Profile")
    async def tv_display(self, interaction: discord.Interaction):
        watch_data = get_user_watch_list(interaction.user.id)
        embeds = create_tv_embeds(watch_data, interaction.user.name)

        if len(embeds) == 0:
            await interaction.response.send_message("No TV Shows Found!")

        view = ButtonView(embeds)
        await interaction.response.send_message(embed=embeds[0], view=view)


    @app_commands.command(name="tv-add", description="Add TV Show to Profile")
    async def tv_add(self, interaction: discord.Interaction, show_name: str):
        try:
            show_data = fetch_show_data(show_name)
            add_watched_show(interaction.user.id, show_data)
            await interaction.response.send_message(f"`{show_data.name}` added to list.")

        except ShowExistsException:
            await interaction.response.send_message("Show already exists in profile!")
        except Exception:
            await interaction.response.send_message("Failed to add show to profile! (Unknown Error)")
            

    @app_commands.command(name="tv-remove", description="Remove TV Show from Profile")
    async def tv_remove(self, interaction: discord.Interaction, show_name: str):
        try:
            show_data = fetch_show_data(show_name)
            removed = remove_watched_show(interaction.user.id, show_data.show_id)

            if not removed:
                await interaction.response.send_message("Show not found in profile!")

            await interaction.response.send_message(f"`{show_data.name}` removed from list.")
        except Exception:
            await interaction.response.send_message("Failed to remove show from profile! (Unknown Error)")

async def setup(bot):
    await bot.add_cog(TVShow(bot))