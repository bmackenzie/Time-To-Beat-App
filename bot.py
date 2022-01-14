# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup
import pandas as pd
from howlongtobeatpy import HowLongToBeat
# docs https://pypi.org/project/howlongtobeatpy/
from fuzzywuzzy import process

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

client = discord.Client()

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@bot.command(name='game')
async def search(ctx, search_string):
    try:
        results = HowLongToBeat().search(search_string)
        names_dict = {result.game_name:result for result in results}

        best_match = process.extract(search_string, names_dict.keys(), limit = 1)
        game = names_dict[best_match[0][0]]

        time_main = f"{game.gameplay_main_label}: {game.gameplay_main} {game.gameplay_main_unit}"
        time_extra = f"{game.gameplay_main_extra_label}: {game.gameplay_main_extra} {game.gameplay_main_extra_unit}"
        time_completionist = f"{game.gameplay_completionist_label}: {game.gameplay_completionist} {game.gameplay_completionist_unit}"
        game_id = game.game_id

        response = f"{time_main}\n{time_extra}\n{time_completionist}"

        try:
            page = requests.get("https://howlongtobeat.com/game?id=" + game_id, headers = headers)
            soup = BeautifulSoup(page.text)
            div = soup.find_all("div", {"class": "game_chart"})
            rating = div[0].find_all('h5')[0].text
            response += f"\n{rating}"
        except:
            response+="\nRating not found"
    except:
        response ='Game Not Found, please check for typos'

    await ctx.send(response)

bot.run(TOKEN)
