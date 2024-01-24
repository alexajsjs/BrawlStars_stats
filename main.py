import requests as req
from discord.ext import commands
from discord import app_commands
import discord
import Brawlstats

# Discord authentication information.
discord_token =
channel_id =

# Discord bot
bot = commands.Bot(intents=discord.Intents.all(), command_prefix="!")


# Functions
def user_info_embed(player_data):
    important_fields = {
        "Name": "name",
        "Trophies": "trophies",
        "Highest Trophies": "highestTrophies",
        "HighestPowerPlayPoints": "highestPowerPlayPoints",
        "Level": "expLevel",
        "Exp": "expPoints",
        "3vs3Victories": "3vs3Victories",
        "SoloVictories": "soloVictories",
        "DuoVictories": "duoVictories",
        "BestRoboRumbleTime": "bestRoboRumbleTime",
        "BestTimeAsBigBrawler": "bestTimeAsBigBrawler",
    }

    embed = discord.Embed(color=discord.Color.yellow(), description="Player statistics")

    for key in important_fields:
        embed.add_field(name=key, value=player_data[important_fields[key]], inline=True)

    return embed


def user_brawler_embed(player_data: dict, brawler: str):
    important_fields = {
        "Name": "name",
        "Power": "power",
        "Rank": "rank",
        "Trophies": "trophies",
        "HighestTrophies": "highestTrophies",
        "GearCount": "gears",
        "StarPowerCount": "starPowers"
    }

    embed = discord.Embed(color=discord.Color.yellow(), description="Player statistics")

    for i in player_data["brawlers"]:
        if i["name"].lower() == brawler.lower():
            for key in important_fields:
                if key != "GearCount" and key != "StarPowerCount":
                    embed.add_field(name=key, value=i[important_fields[key]], inline=True)
                else:
                    embed.add_field(name=key, value=len(i[important_fields[key]]), inline=True)

    return embed


# Runs when the bot first goes online
@bot.event
async def on_ready():
    print("Bot online")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)}")
    except Exception as e:
        print(e)


# Commands
@bot.tree.command(name="player")
@app_commands.describe(player_id="PlayerID")
async def user(interaction: discord.Interaction, player_id: str):
    player_data = Brawlstats.player_data(player_id)
    embed = user_info_embed(player_data)

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="brawler")
@app_commands.describe(player_id="PlayerID", brawler="brawler")
async def brawler(interaction: discord.Interaction, player_id: str, brawler: str):
    player_data = Brawlstats.player_data(player_id)
    embed = user_brawler_embed(player_data, brawler)

    await interaction.response.send_message(embed=embed)


# Run the bot
bot.run(discord_token)
