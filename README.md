# hugin-bot
Discord bot that provides information on food, bosses, items etc. for survival game Valheim

This bot uses the discord.py commands library and includes a bunch of commands preceded by the '!' character.
These commands are designed to provide quick access to information about Valheim including, but not limited to, the following:

**NEWS**
!featured = Get the latest news release from the official Valheim website   (Uses bs4 library to scrape the article from valheimgame.com)
!news = Get the latest news release from the official Valheim Steam page    (Uses Steam API to get the latest news release from Steam)

**FOOD**
!raw = Get a list of all the foods you can eat raw and their effects
!cooking = Get a list of everything that can be cooked at the cooking station and their effects
!cauldron = Get a list of every recipe that can be made at the cauldron, the ingredients, and their effect
!recipe "food name" = Get cauldron recipe for specified food. Must use double quotes around food name if more than one word
!oven = Get a list of every recipe that can be made at the stone oven, the ingredients, and their effect

**BOSSES**
!bosses = Get a list of all the bosses in Valheim and a short description of each boss
!boss "boss name" = Get information on a specific boss. Double quotes not necessary.
