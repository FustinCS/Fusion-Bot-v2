import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DISCORD_TOKEN")
app_id = os.getenv("APP_ID")

intents = discord.Intents.all()
intents.guilds = True

bot = commands.Bot(command_prefix='.', intents=intents, application_id=app_id)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


# need sync commands to update the slash commands    
@bot.command(name='sync')
async def sync(ctx: commands.Context):
    synced = await bot.tree.sync()
    await ctx.send(f"Synced {len(synced)} commands!")

# load all cogs
async def load():
    for filename in os.listdir('./bot/cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# driver code to launch bot
async def main():
    await load()
    await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
    