import discord
from discord import app_commands
from discord.ext import commands
from utils.anilist.fetch_anilist_data import create_entries_list, fetch_anilist_data

class Anilist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("anilist.py is ready!")

    @app_commands.command(name="anilist-profile", description="Displays anilist profile")
    async def anilist(self, interaction: discord.Interaction, username: str):
        data = fetch_anilist_data(username)
        entries = create_entries_list(data)

        await interaction.response.send_message(f"Success!")
        

async def setup(bot):
    await bot.add_cog(Anilist(bot))