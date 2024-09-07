import discord
from discord import app_commands
from discord.ext import commands
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

async def setup(bot):
    await bot.add_cog(TVShow(bot))