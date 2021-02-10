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

mostRecentSenateBill = list(congress.bills.introduced('senate', congress=117)['bills'][0].values())
mostRecentHouseBill = list(congress.bills.introduced('house', congress=117)['bills'][0].values())

senateInfo = {'Title' : mostRecentSenateBill[3], 
              'Details' : mostRecentSenateBill[5], 
              'Chamber' : "Senate", 
              'Sponsor' : mostRecentSenateBill[7] + " " + mostRecentSenateBill[9] + " " + mostRecentSenateBill[11] + " - " + mostRecentSenateBill[10], 
              'BillTracker' : mostRecentSenateBill[15], 
              'DateIntroduced' : mostRecentSenateBill[16]
             }

houseInfo = {'Title' : mostRecentHouseBill[3], 
             'Details' : mostRecentHouseBill[5], 
             'Chamber' : "House of Representatives", 
             'Sponsor' : mostRecentHouseBill[7] + " " + mostRecentHouseBill[9] + " " + mostRecentHouseBill[11] + " - " + mostRecentHouseBill[10], 
             'BillTracker' : mostRecentHouseBill[15], 
             'DateIntroduced' : mostRecentHouseBill[16]
            }

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

    updateBoolSenate = compareSenateData(senateInfo)
    updateBoolHouse = compareHouseData(houseInfo)

    if(updateBoolHouse == False & updateBoolSenate == False):
        await ctx.send("No new bills have been introduced.")
    
    if(updateBoolSenate == True):
        senateBill = readFile("senate.JSON")
        response = ("----------------------------------------\n" +
                    "A bill has been introduced in the Senate!"+
                    "\nTitle: " + mostRecentSenateBill[3] +
                    "\nDetails: " + mostRecentSenateBill[5] +
                    "\nChamber: " + "Senate" + 
                    "\nSponsor: " + mostRecentSenateBill[7] + " " + mostRecentSenateBill[9] + " " + mostRecentSenateBill[11] + " - " + mostRecentSenateBill[10] +
                    "\nBill Tracker: " + mostRecentSenateBill[15] + 
                    "\nDate Introduced: " + mostRecentSenateBill[16]
                    )
        await ctx.send(response)
    
    if(updateBoolHouse == True):
        houseBill = readFile("house.JSON")
        response = ("----------------------------------------\n" + 
                    "A bill has been introduced in the House!"+
                    "\nTitle: " + mostRecentHouseBill[3] +
                    "\nDetails: " + mostRecentHouseBill[5] +
                    "\nChamber: " + "House of Representatives" + 
                    "\nSponsor: " + mostRecentHouseBill[7] + " " + mostRecentHouseBill[9] + " " + mostRecentHouseBill[11] + " - " + mostRecentHouseBill[10] +
                    "\nBill Tracker: " + mostRecentHouseBill[15] + 
                    "\nDate Introduced: " + mostRecentHouseBill[16]
                    )
        await ctx.send(response)



@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, welcome to NJIT's Science and Politics Society! If you haven't already, be sure to register on our Highlander Hub page found in our Important Links channel. Also, be sure to follow our naming convention (First name, Last Initial) as it allows for easier attendance tracking (https://rebrand.ly/discordShortener). Thanks!")

bot.run(DISCORD_TOKEN)
