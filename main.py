import discord
from discord.ext import commands
import json
from mcstatus import MinecraftServer

#creating the bot
bot = commands.Bot(command_prefix="!")

#getting the bot token
with open("config.json") as f:
    config = json.load(f)
    
    token = config["token"]
    serverName = config["server"]
    
#when the bot goes online
@bot.event
async def on_ready():
    print("Papi is ready!")

#checks the status on the server
def online():
    #gets server info
    server = MinecraftServer.lookup(serverName)
    server = server.status()
    
    #makes the message to be outputed
    message = ""
    if server.players.online == 0:
        message = "No players online!"
    else:
        message += (str(server.players.online) + " out of " + str(server.players.max) + " online:\n")
        
        for player in server.players.sample:
            message += ("- " + player.name + "\n")
        
        return message

#command for the players that are online
@bot.command()
async def players(ctx):
    #gets the list of online players
    onlinePlayers = online()
    
    #makes an embed of the list
    embed = discord.Embed(title="Status") 
    embed.add_field(name="Players", value=onlinePlayers)
    
    #returns the embed
    await ctx.send(embed=embed)

bot.run(token)