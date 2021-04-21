# Vladimir Gutierrez Science and Politics Discord Bot
# Began Feb. 8th, 2021

from congress import Congress
from dotenv import load_dotenv
from discord.ext import commands
from keep_alive import keep_alive
import json
import os
import discord
import asyncio

load_dotenv()

keep_alive()

API_KEY = os.getenv('API_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

congress = Congress(API_KEY)

bot = commands.Bot(command_prefix="politicsBot.")

mostRecentSenateBill = list(
    congress.bills.introduced('senate', congress=117)['bills'][0].values())
mostRecentHouseBill = list(
    congress.bills.introduced('house', congress=117)['bills'][0].values())

senateBillComparison = {
    'Title': mostRecentSenateBill[3],
    'Details': mostRecentSenateBill[5],
    'Chamber': "Senate",
    'Sponsor': mostRecentSenateBill[7] + " " + mostRecentSenateBill[9] + " " +
    mostRecentSenateBill[11] + " - " + mostRecentSenateBill[10],
    'BillTracker': mostRecentSenateBill[15],
    'DateIntroduced': mostRecentSenateBill[16]
}
houseBillComparison = {
    'Title': mostRecentHouseBill[3],
    'Details': mostRecentHouseBill[5],
    'Chamber': "House of Representatives",
    'Sponsor': mostRecentHouseBill[7] + " " + mostRecentHouseBill[9] + " " + mostRecentHouseBill[11] + " - " + mostRecentHouseBill[10],
    'BillTracker': mostRecentHouseBill[15],
    'DateIntroduced': mostRecentHouseBill[16]
}


def writeToFile(fileName, data):
    with open(fileName, 'w') as file:
        file.write(json.dumps(data))


def readFile(fileName):
    with open(fileName, 'r') as file:
        return (json.loads(file.read()))


def compareHouseData(data):
    dataFromFile = readFile("house.json")

    if (dataFromFile != data):
        writeToFile("house.json", data)
        return (True)
    else:
        return (False)


def compareSenateData(data):
    dataFromFile = readFile("senate.json")

    if (dataFromFile != data):
        writeToFile("senate.json", data)
        return (True)
    else:
        return (False)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    await bot.change_presence(activity=discord.Game(
        name="Politics Simulator 2021"))
    
async def autoUpdate(channel_id):
    
    global bot
    channel = bot.get_channel(channel_id)

    updateBoolSenate = compareSenateData(senateBillComparison)
    updateBoolHouse = compareHouseData(houseBillComparison)

    if (updateBoolHouse == False and updateBoolSenate == False):
        await channel.send("No new bills have been introduced.")

    if (updateBoolSenate == True):
        response = ("----------------------------------------\n" +
                    "A bill has been introduced in the Senate!" + "\nTitle: " +
                    senateBillComparison.get('Title') + "\nDetails: " +
                    senateBillComparison.get('Details') + "\nChamber: " +
                    senateBillComparison.get('Chamber') + "\nSponsor: " +
                    senateBillComparison.get('Sponsor') + "\nBill Tracker: " +
                    senateBillComparison.get('BillTracker') +
                    "\nDate Introduced: " +
                    senateBillComparison.get('DateIntroduced'))
        await channel.send(response)

    if (updateBoolHouse == True):
        response = ("----------------------------------------\n" +
                    "A bill has been introduced in the House!" + "\nTitle: " +
                    houseBillComparison.get('Title') + "\nDetails: " +
                    houseBillComparison.get('Details') + "\nChamber: " +
                    houseBillComparison.get('Chamber') + "\nSponsor: " +
                    houseBillComparison.get('Sponsor') + "\nBill Tracker: " +
                    houseBillComparison.get('BillTracker') +
                    "\nDate Introduced: " +
                    houseBillComparison.get('DateIntroduced'))
        await channel.send(response)


@bot.command(name="update")
async def update(ctx):

    updateBoolSenate = compareSenateData(senateBillComparison)
    updateBoolHouse = compareHouseData(houseBillComparison)

    if (updateBoolHouse == False and updateBoolSenate == False):
        await ctx.send("No new bills have been introduced.")

    if (updateBoolSenate == True):
        response = ("----------------------------------------\n" +
                    "A bill has been introduced in the Senate!" + "\nTitle: " +
                    senateBillComparison.get('Title') + "\nDetails: " +
                    senateBillComparison.get('Details') + "\nChamber: " +
                    senateBillComparison.get('Chamber') + "\nSponsor: " +
                    senateBillComparison.get('Sponsor') + "\nBill Tracker: " +
                    senateBillComparison.get('BillTracker') +
                    "\nDate Introduced: " +
                    senateBillComparison.get('DateIntroduced'))
        await ctx.send(response)

    if (updateBoolHouse == True):
        response = ("----------------------------------------\n" +
                    "A bill has been introduced in the House!" + "\nTitle: " +
                    houseBillComparison.get('Title') + "\nDetails: " +
                    houseBillComparison.get('Details') + "\nChamber: " +
                    houseBillComparison.get('Chamber') + "\nSponsor: " +
                    houseBillComparison.get('Sponsor') + "\nBill Tracker: " +
                    houseBillComparison.get('BillTracker') +
                    "\nDate Introduced: " +
                    houseBillComparison.get('DateIntroduced'))
        await ctx.send(response)
    
    await ctx.message.delete()

@bot.command()
async def DM(ctx, user: discord.User, *, message=None):
    message = (
        f"Hi {user.name}, welcome to NJIT's Science and Politics Society! If you haven't already, be sure to register on our Highlander Hub page found in our Important Links channel. Also, be sure to follow our naming convention (First name, Last Initial) as it allows for easier attendance tracking (https://rebrand.ly/discordShortener). Thanks!"
    )
    await user.send(message)
    await ctx.message.delete()


bot.run(DISCORD_TOKEN)
