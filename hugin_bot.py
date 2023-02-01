from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import datetime
import json

# Load environment variables from .env file
load_dotenv()

# Set prefix to an '!' and nullify the built-in help command so that I can use my own
bot = commands.Bot(command_prefix='!', help_command=None)


# FUNCTIONS --------------------------------------------------------------------------------------

# Scrape the featured article from the Valheim news page and return its title, summary, and link
def scrape_featured_article():
    # Make a GET request to the news page
    url = "https://www.valheimgame.com/news"
    page = requests.get(url)
    # Parse the HTML of the page
    soup = BeautifulSoup(page.text, "html.parser")

    # Find the div element with class "container relative z-20"
    featured = soup.find("div", class_="container relative z-20")
    # Find the div element with class "news-featured-content" within it
    content = featured.find("div", class_="news-featured-content")

    # Extract the title, summary, and link for the featured article
    title = content.find("h1").text
    summary = content.find("div", class_="text-content font-body text-white text-base font-normal leading-relaxed text-opacity-50 pt-1").text
    link = featured.find("a")["href"]

    # Return the title, summary, and link as a tuple
    return (title, summary, "https://www.valheimgame.com" + link)

# Use the Steam API to get the most recent news for the given game ID
def get_steam_news(appID, count):
    # Get the API key from the environment variables
    api_key = os.getenv("STEAM_KEY")
    # Set the headers for the API request
    headers = {"Content-Type": "application/json", "X-API-Key": api_key}

    # Set the URL and parameters for the API request
    url = "http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/"
    params = {"appid": appID, "count": count, "maxlength": 300, "format": "json"}

    # Make the GET request to the API
    response = requests.get(url, params=params, headers=headers)

    # If the request was successful, return the news items
    if response.status_code == 200:
        steam_object = response.json()
        return steam_object['appnews']['newsitems']
    # If the request was unsuccessful, return an error message
    else:
        return "Connection Error"


# EVENTS -------------------------------------------------------------------------

# When the client is ready, print a message to the console
@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user}!')

# When a message is received, check if it is "!help" and send a response with command instructions
@bot.command()
async def help(ctx):
    help_message = '''
    **\nHugin is here to help vikings with their journey in Valheim**
The following commands can help lead the way

**NEWS**
!featured = Get the latest news release from the official Valheim website
!news = Get the latest news release from the official Valheim Steam page

**FOOD**
!raw = Get a list of all the foods you can eat raw and their effects
!cooking = Get a list of everything that can be cooked at the cooking station and their effects
!cauldron = Get a list of every recipe that can be made at the cauldron, the ingredients, and their effect
!recipe "food name" = Get cauldron recipe for specified food. Must use double quotes around food name if more than one word
!oven = Get a list of every recipe that can be made at the stone oven, the ingredients, and their effect

**ENEMIES**
!creature "creature name" = Get information on a specific creature. Must use double quotes around creature name if more than one word
!bosses = Get a list of all the bosses in Valheim and a short description of each boss
!boss "boss name" = Get information on a specific boss. Double quotes not necessary.
'''
    await ctx.send(help_message)

# Return the featured news article from the official Valheim Steam page
@bot.command()
async def featured(ctx):
    # Call the scrape_featured_article() function to get the featured article
    title, summary, link = scrape_featured_article()
    # Format the message with the title, summary, and link for the featured article
    message_text = f"**{title}**\n{summary}\nRead more {link}"
    # Send the message to the Discord channel
    await ctx.send(message_text)

# Return the featured news article from the official Valheim website
@bot.command()
async def news(ctx):
    # Call the get_steam_news() function to get the most recent news
    news = get_steam_news(892970, 1)
    for item in news:
        # Convert the UNIX timestamp to a human-readable date and time
        timestamp = item['date']
        dt = datetime.datetime.fromtimestamp(timestamp)
        formatted_date = dt.strftime("%d-%m-%y %H:%M:%S")
        # Format the message with the title, date, contents, and link for the news item
        news_text = f"**{item['title']}** {formatted_date}\n{item['contents']}\n{item['url']}"
        # Send the message to the Discord channel
        await ctx.send(news_text)

@bot.command()
async def raw(ctx):
    # Get the text file with the cauldron recipes
    with open('.\\files\\raw_food.txt', 'r') as file:
        await ctx.send("Here are all the foods that can be eaten raw:\n\n" + file.read())
        file.close()

@bot.command()
async def cooking(ctx):
    # Get the text file with the cauldron recipes
    with open('.\\files\cooking_station_recipes.txt', 'r') as file:
        await ctx.send("Here are all the foods that can be cooked at the cooking station:\n\n" + file.read())
        file.close()

@bot.command()
async def cauldron(ctx):
    # Get the text file with the cauldron recipes
    with open('.\\files\cauldron_recipes.txt', 'r') as file:
        await ctx.send("Here are all the recipes that can be made at the cauldron:\n\n" + file.read())
        file.close()

@bot.command()
async def recipe(ctx, food):
    # Get JSON data of cauldron recipes
    with open('.\\files\cauldron_dict.txt', 'r') as file:
        data = json.load(file)
        file.close()
    for item in data:
        if item['name'].lower() == food.lower():
            name = item['name']
            ingredients = item['ingredients']
            cauldron_level = item['level']
            buffs = item['buffs']
            await ctx.send(f'''
            **{name}**
{ingredients}
{cauldron_level}
{buffs}
''')

@bot.command()
async def oven(ctx):
    # Get the text file with the cauldron recipes
    with open('.\\files\stone_oven_recipes.txt', 'r') as file:
        await ctx.send("Here are all the recipes that can be made at the stone oven:\n\n" + file.read())
        file.close()

@bot.command()
async def bosses(ctx):
    # Create list to hold description of each boss
    boss_desc = []
    # Get the text file with the details of bosses
    with open('.\\files\\boss_dict.txt', 'r') as file:
        data = json.load(file)
        file.close()
    for item in data:
        boss_desc.append(f'**{item["name"]}**\nFound in {item["biome"]}\n{item["desc"]}')
    for i in range(len(boss_desc)):
        await ctx.send(boss_desc[i])

@bot.command()
async def boss(ctx, name):
    with open('.\\files\\boss_dict.txt', 'r') as file:
        data = json.load(file)
        file.close()
    for item in data:
        if item['name'].lower() == name.lower():
            await ctx.send(f'''
            **{item['name']}**
{item['desc']}
**Biome: **{item['biome']}
**To find: **{item['find']}
**To summon: **{item['summon']}
**Loot: **{item['loot']}
**Power: **{item['power']}
{item['guide']}''')

@bot.command(help="Get information on a specific creature. Double quotes required around creature name if more than one word")
async def creature(ctx, name):
    with open('.\\files\creature_scrape.txt', 'r') as file:
        data = json.load(file)
        file.close()
    for item in data:
        if item['name'].lower() == name.lower():
            await ctx.send(f'''
            **{item['name']}**
**Found in:** {item['biome']}
**Drops:** {', '.join(item['drops'])}''')

# RUN BOT -------------------------------------------------------------------------

# Run the client using the Discord API token from the environment variables
bot.run(os.getenv('TOKEN'))

# Get the name of the guild from the environment variables
guild_name = os.getenv('GUILD')
guild = None

# Find the guild with the given name
for g in bot.guilds:
    if g.name == guild_name:
        guild = g
        break

# If the guild was not found, print an error message
if guild is None:
    print(f'Guild with name {guild_name} not found!')
