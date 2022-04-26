import discord
from discord.ext import commands

import os 
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import matplotlib.pyplot as plt
import youtube_dl 
import datetime
import time 
import requests
import json


try:
    with open('discord_py/SECRET.txt') as f:
        info = f.readlines()
except FileNotFoundError:
    with open('SECRET.txt') as f:
        info = f.readlines()

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('tobi-348315-fa9ceafcf825.json', scope)
client =  gspread.authorize(creds)
sheet = client.open('TOBI.log').sheet1
secondSheet = client.open('TOBI.log').worksheet("Reported Log")

intents = discord.Intents(messages=True, guilds=True, members=True)
client = commands.Bot(command_prefix="=", intents=intents, case_insensitive=True)

@client.event
async def on_ready():  # Event client ready
    await client.change_presence(status=discord.Status.idle,activity=discord.Game('=list')) #Change status to =help
    print(f'Running on {len(client.guilds)} server')
    print(f'{client.user.name} is online')  # Print TOBI is online
    print('='*50)

@client.command()  # list commands
async def list(ctx):  # Contact list word
    embed = discord.Embed(title = "List commands", description = "Use '=list'",color = ctx.author.color)
    embed.add_field(name="Basic", value=
    "TOBI but in json file\n"
    "**Network**        for Check TOBI Network (.ms)\n"
    "**spawn**          for spawn TOBI to channel\n"
    "**weather**        for check weather today\n"
    "**covid**          for check daily covid\n"
    "**covid_stat**     for Covid stat in duration by Graph and total\n")
    embed.add_field(name="Audio", value=
    "**play 'url'**     for play song\n"
    "**stop**           for stop song\n"
    "**pause**          for pause song\n"
    "**resume**         for resume song\n" )
    embed.add_field(name="Tobi", value=
    "**tobiinfo**       for TOBI information\n"
    "**git**            for GitHub\n"
    "**updateinfo**     for TOBI update command or function\n")
    await ctx.send(embed=embed)

@client.event 
async def on_member_join(member):
    i = 1
    while True:
        if not sheet.row_values(i):
            word = [str(member.guild), str(member), str(member.id), str(datetime.date.today()), f'{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}']
            sheet.insert_row(word, i)
            break
        else:
            pass
        i += 1

@client.event
async def on_member_remove(member): # remove
    i = 1
    while True:
        if str(member) == str(sheet.cell(i, 2).value):
            sheet.update_cell(i, 6, str(datetime.date.today()))
            break
        else:
            pass
        i += 1

@client.command() # ping pong
async def ping(ctx):
    print(f'Ping command activated by {ctx.author.name} on channel {ctx.channel.name} server {ctx.author.guild.name}') 
    await ctx.send("pong")

@client.command()
async def covid(ctx):
    print(f'Covid command activated by {ctx.author.name} on channel {ctx.channel.name} server {ctx.author.guild.name}') # TODO
    response = requests.get('https://covid19.ddc.moph.go.th/api/Cases/today-cases-all')
    data = json.loads(response.text)
    text = data[0]
    update = text['update_date']
    embed = discord.Embed(title = f'Covid-19 🤮' ,description = f'Update {update}',color = discord.Color.green())
    embed.add_field(name='New case 🦠',value= text['new_case'])
    embed.add_field(name='Total case 🧫',value= text['total_case'])
    embed.add_field(name='Total case excludeabroad 📜',value= text['total_case_excludeabroad'])
    embed.add_field(name='New death ☠️',value= text['new_death'])
    embed.add_field(name='Total death 😇',value= text['total_death'])
    embed.add_field(name='New recovered',value= text['new_recovered'])
    embed.add_field(name='Total recovered',value= text['total_recovered'])

    await ctx.send(embed = embed)

@client.command()
async def covid_stat(ctx, key=None):
    
    response = requests.get("https://covid19.ddc.moph.go.th/api/Cases/timeline-cases-all")
    data = response.json()

    case = []
    date = []

    for x in range(len(data)):
        date.append(data[x]["txn_date"])
        case.append(data[x]['new_case'])

    embed = discord.Embed(title= f'Covid-19 In duration {date[0]} to {date[len(data) - 1]}',color = discord.Color.blue())

    if key == None:
        plt.title(f'Covid-19 during {date[0]} to {date[len(data) - 1]}')
        fig = plt.figure()
        plt.plot(date,case)
        fig.savefig('covid.png', dpi = 100, facecolor = 'white')

        file = discord.File("covid.png", filename="covid.png")
        embed.set_image(url="attachment://covid.png")
        embed.add_field(name="Total case", value=data[len(data) - 1]['total_case'])
        embed.add_field(name="Total case excludeabroad", value=data[len(data) - 1]['total_case_excludeabroad'])
        embed.add_field(name="Total death", value=data[len(data) - 1]['total_death'])
        embed.add_field(name="Total recovered", value=data[len(data) - 1]['total_recovered'])
        embed.set_footer(text=f"Update Information {data[len(data) - 1]['update_date']}")
        await ctx.send(file=file, embed=embed)

    else:

        await ctx.send('Not in a range')

@client.command(invoke_without_command = True) #tobiinfo
async def tobiinfo(ctx):
    print(f'Info command activated by {ctx.author.name} on channel {ctx.channel.name} server {ctx.author.guild.name}')
    em = discord.Embed(title = "TOBI information.json", description = "Use '=tobiinfo'",color = ctx.author.color)
    em.add_field(name = "Info",value=
    "Build by Mr. Narongkorn kitrungrot\n"
    "Version 10.1 (26/4/2022)\n"
    "Born 12/7/2020\n"
    "Discordbot.py © TOB · Narongkorn,Hosted by TOB Raspberrypi, distributed under the PSUWIT license")

    em.add_field(name='Github', value='https://github.com/T0b1e/Discord.tob.git')
    em.add_field(name='Supporter',value='https://ko-fi.com/narongkorn')
    em.add_field(name='Report reqest',value='https://forms.gle/2yhJfcPBpTbmWsFbA')

    await ctx.send(embed = em)

@client.command()  # git
async def git(ctx):
    print(f'Git command activated by {ctx.author.name} on channel {ctx.channel.name} server {ctx.author.guild.name}')
    em = discord.Embed(title = "Github repo", description = "Use '=git'",color = ctx.author.color)
    em.add_field(name = "Github",value="https://github.com/T0b1e/Discord.tob.git")
    await ctx.send(embed = em)

@client.command()
@commands.has_permissions(ban_members = True)
async def report(ctx, member : discord.Member = None, text = None):
    row = 2
    col = 5
    while True:

        if not secondSheet.row_values(row):
            try:
                word = [str(member.guild), str(member), str(member.id), 1, str(text)]
                secondSheet.insert_row(word, row)
                await ctx.send('reported')
                break
            except AttributeError:
                await ctx.send('User Not Found (Ex : =report TOBI#7555)')
                break
        if str(member) == str(secondSheet.cell(row, 2).value):
            if int(secondSheet.cell(row, 4).value) >= 10:
                await ctx.send('You Made Too Much Troble')
                await ctx.send('You receive TIMEOUT(24.hr) in 5 minute :)') 
                await member.ban(reason=text)
                secondSheet.update_cell(row, 4, 1)
                break

            else:
                secondSheet.update_cell(row, 4, int(secondSheet.cell(row, 4).value) + 1)
                await ctx.send('reported')
                break

        row += 1
        col += 1
    
@client.command(pass_context = True)
async def spawn(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
       
        await channel.connect()
    else:
        await ctx.send("you're not in the voice channel")
    print(f'Spawn command activated by {ctx.author.name} at {channel} on server {ctx.author.guild.name}')

client.run(int(info[1], 2).to_bytes((int(info[1], 2).bit_length() + 7) // 8, 'big').decode())