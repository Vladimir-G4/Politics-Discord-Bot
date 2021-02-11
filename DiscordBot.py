# Vladimir Gutierrez Science and Politics Discord Bot 
# Began Feb. 8th, 2021 

from congress import Congress 
from dotenv import load_dotenv
from discord.ext import commands
import json
import os
import discord

load_dotenv()

API_KEY = os.getenv('API_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

congress = Congress(API_KEY)

bot = commands.Bot(command_prefix="politicsBot.")

rawSenateData = list(congress.bills.introduced('senate', congress=117)['bills'][0].values())
rawHouseData = list(congress.bills.introduced('house', congress=117)['bills'][0].values())

mostRecentSenateBill = {'Title' : rawSenateData[3], 'Details' : rawSenateData[5], 'Chamber' : "Senate", 'Sponsor' : rawSenateData[7] + " " + rawSenateData[9] + " " + rawSenateData[11] + " - " + rawSenateData[10], 'BillTracker' : rawSenateData[15], 'DateIntroduced' : rawSenateData[16]}
mostRecentHouseBill = {'Title' : rawHouseData[3], 'Details' : rawHouseData[5], 'Chamber' : "House of Representatives", 'Sponsor' : rawHouseData[7] + " " + rawHouseData[9] + " " + rawHouseData[11] + " - " + rawHouseData[10], 'BillTracker' : rawHouseData[15], 'DateIntroduced' : rawHouseData[16]}

def writeToFile(fileName, data):
    with open(fileName, 'w') as file:
        file.write(json.dumps(data))


def readFile(fileName):
    with open(fileName, 'r') as file:
        return(json.loads(file.read()))


def compareHouseData(data):
    dataFromFile = readFile("house.JSON")

    if(dataFromFile != data):
        writeToFile("house.JSON", data)
        return(True)
    else:
        return(False)


def compareSenateData(data):
    dataFromFile = readFile("senate.JSON")

    if(dataFromFile != data):
        writeToFile("senate.JSON", data)
        return(True)
    else:
        return(False)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name = "update")
async def update(ctx):

    updateBoolSenate = compareSenateData(mostRecentSenateBill)
    updateBoolHouse = compareHouseData(mostRecentHouseBill)

    if(updateBoolHouse == False and updateBoolSenate == False):
        await ctx.send("No new bills have been introduced.")
    
    if(updateBoolSenate == True):
        senateBill = readFile("senate.JSON")
        response = ("----------------------------------------\n" +
                    "A bill has been introduced in the Senate!"+
                    "\nTitle: " + mostRecentSenateBill.get('Title') +
                    "\nDetails: " + mostRecentSenateBill.get('Details') +
                    "\nChamber: " + mostRecentSenateBill.get('Chamber') + 
                    "\nSponsor: " + mostRecentSenateBill.get('Sponsor') +
                    "\nBill Tracker: " + mostRecentSenateBill.get('BillTracker') + 
                    "\nDate Introduced: " + mostRecentSenateBill.get('DateIntroduced')
                    )
        await ctx.send(response)
    
    if(updateBoolHouse == True):
        houseBill = readFile("house.JSON")
        response = ("----------------------------------------\n" + 
                    "A bill has been introduced in the Senate!"+
                    "\nTitle: " + mostRecentHouseBill.get('Title') +
                    "\nDetails: " + mostRecentHouseBill.get('Details') +
                    "\nChamber: " + mostRecentHouseBill.get('Chamber') + 
                    "\nSponsor: " + mostRecentHouseBill.get('Sponsor') +
                    "\nBill Tracker: " + mostRecentHouseBill.get('BillTracker') + 
                    "\nDate Introduced: " + mostRecentHouseBill.get('DateIntroduced')
                    )
        await ctx.send(response)

@bot.command()
async def DM(ctx, user: discord.User, *, message=None):
    message = (f"Hi {discord.User.name}, welcome to NJIT's Science and Politics Society! If you haven't already, be sure to register on our Highlander Hub page found in our Important Links channel. Also, be sure to follow our naming convention (First name, Last Initial) as it allows for easier attendance tracking (https://rebrand.ly/discordShortener). Thanks!")
    await user.send(message)

bot.run(DISCORD_TOKEN)
