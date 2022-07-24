from posixpath import split
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import matplotlib.pyplot as plt
import datetime
import time 
import requests
import random
import json


try:
    with open('discord_py/SECRET.txt') as f:
        info = f.readlines()
except FileNotFoundError:
    with open('SECRET.txt') as f:
        info = f.readlines()

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('tobi-348315-fa9ceafcf825.json', scope)
clients = gspread.authorize(creds)
sheet = clients.open('TOBI.log').sheet1
secondSheet = clients.open('TOBI.log').worksheet("Reported Log")

intents = discord.Intents(messages=True, guilds=True, members=True)
client = commands.Bot(command_prefix="=", intents=intents, case_insensitive=True)
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():  # Event client ready
    await client.change_presence(status=discord.Status.idle,activity=discord.Game('=list')) #Change status to =help
    print(f'TOBI is online')  # Print TOBI is online


@client.event 
async def on_member_join(member):
    i = 2
    while True:
        if str(sheet.cell(i, 2).value) == str(member):
            break         
        else:
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


@client.event 
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound):
        print('Command not found') 
        embed = discord.Embed(title=f"Error!!!", description=f"Command not found.", color=ctx.author.color) 
        embed.add_field(name="Basic", value=
            "TOBI but in json file\n"
        "**Network**        for Check TOBI Network (.ms)\n"
        "**spawn**          for spawn TOBI to channel\n"
        "**report**         for check report user\n"
        "**covid**          for check daily covid\n"
        "**covid_stat**     for Covid stat in duration by Graph and total\n")
        embed.add_field(name="Tobi", value=
        "**tobiinfo**       for TOBI information\n"
        "**git**            for GitHub\n"
        "**updateinfo**     for TOBI update command or function\n")
        secondEmbed = discord.Embed(title=f"=help ___", description=f"Description", color=ctx.author.color) 
        await ctx.send(embed=embed)
        await ctx.send(embed=secondEmbed)


@slash.slash(name="lists", description="lists command")
async def lists(ctx : SlashContext):  # Contact list word
    """embed = discord.Embed(title = "List commands", description = "Use '=list'",color = ctx.author.color)
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
    await ctx.send(embed=embed)"""


@client.command()
async def helps(ctx, *arg):
    embed = discord.Embed(title=f"Help command", description=f"=help __", color=ctx.author.color) 
    if arg == None:
        embed.add_field(name='Put command after help command')
        embed.add_field(value='=help __')
    if arg == 'report':
        embed.add_field(name='For report user that do bad thing and if that user got report more than 10 time, The server will be punish you by ban')
        embed.add_field(value='=report (user#1234) (reason)')
    if arg == 'covid':
        embed.add_field(name='For checking daily covid-19 in thailand')
        embed.add_field(value='=covid (No argument requirment)')
    if arg == 'covid_stat':
        embed.add_field(name='For checking stat of covid-19 in thailand')
        embed.add_field(value='=covid_stat (No argume''nt requirment)')


def spam(message):
    count = 1
    words = []

    for x in (message.content).split():
        if x in words:
            count += 1
            return True
        
        if x not in words:
            words.append(x)


def nitro(message):
    words = ['Discord Nitro', 'nitro', 'discord nitro', 'free discord nitro', 'free discord', 'free']
    phrase = []
    for a in (message.content).split():
        phrase.append(a)
    
    for b in phrase:
        if b in words:
            return True
        if b not in words:
            pass
        else:
            return False

"""@client.event
async def on_message(message):
    if spam(message) == True:
        await message.delete()
    
    if nitro(message) == True:
        await message.delete()"""


@client.command() # ping pong
async def ping(ctx):
    print(f'Ping command activated by {ctx.author.name} on channel {ctx.channel.name} server {ctx.author.guild.name}') 
    await ctx.send("pong")


@client.command()
async def covid(ctx):
    print(f'Covid command activated by {ctx.author.name} on channel {ctx.channel.name} server {ctx.author.guild.name}')
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


@client.command()
async def git(ctx):
    em = discord.Embed(title = "Github repo", description = "Use '=git'",color = ctx.author.color)
    em.add_field(name = "Github (Old version)",value="https://github.com/T0b1e/Discord.tob")
    em.add_field(name = "Github (New version)",value="https://github.com/T0b1e/TOBI")
    await ctx.send(embed = em)


@client.command(alias = ['Report', 'REPORT'])
@commands.has_permissions(ban_members = True)
async def report(ctx, member : discord.Member, *, text):
    # print(member, text)

    # print('member',member,'text', text) #member Tob#2144 text (สำรอง)#5857 FIXBUG TODO
    row = 2
    col = 5
    if not text:
        await ctx.send('Why you report him (Add reason)')
    else:
        while True:

            if str(member) == str(secondSheet.cell(row, 2).value): # ถ้ามีชื่อ
                if int(secondSheet.cell(row, 4).value) >= 10:
                    await ctx.send('You Made Too Much Troble')
                    await ctx.send('You receive TIMEOUT(24.hr) in 5 minute :)') 
                    await member.ban(reason=' '.join(word))
                    secondSheet.update_cell(row, 4, 1)
                    break

                else:
                    secondSheet.update_cell(row, 4, int(secondSheet.cell(row, 4).value) + 1)
                    # แก้ที่ว่าถ้าหาก Column ตรงนะั้นมี Sorce อยู่แล้วให้เพิ่มไปอีกช่อง แต่ถ้ามันเกินลิมิตแล้วลบใหม่หมด 20
                    if not secondSheet.cell(row, col).value:
                        # print('Here with', col)
                        secondSheet.update_cell(row, col, str(text))
                    else:
                        # print('Here with', col+1)
                        secondSheet.update_cell(row, col+1, str(text) + str())
                    await ctx.send('reported')
                    break

            if not secondSheet.row_values(row): # ถ้าไม่มีชื่อ
                try:
                    word = [str(member.guild), str(member), str(member.id), 1, str(' '.join(word))]
                    secondSheet.insert_row(word, row)
                    await ctx.send('reported')
                    break
                except AttributeError:
                    await ctx.send('User Not Found (Ex : =report TOBI#7555)')
                    break
            

            row += 1
            col += 1

@client.command()
async def check_report(ctx, member : discord.Member):
    embed = discord.Embed(title = 'Report Status',color = ctx.author.color)
    embed.add_field(name= 'Information',value= f'Username: {member} ID: {member.id}')
    row = 2
    if member != None:
        while True:
            if str(member) == str(secondSheet.cell(row, 2).value):
                embed.add_field(name= 'Reported Time',value = f'You have been reported {int(secondSheet.cell(row, 4).value)} times')
            else:
                embed.add_field(name= "you're nicest person ever in this server", value='no one have been reported you before, keep nice')
            await ctx.send(embed=embed)
            break
    else:
        pass

@client.command(pass_context=True)
async def spawn(ctx):
    author = ctx.message.author
    channel = author.voice_channel

    print(f'Spawn command activated by {ctx.author.name} at {ctx.author.voice.channel} on server {ctx.author.guild.name}')

    await client.join_voice_channel(channel)


# randomize
@client.command()
async def randoms(ctx,*,message):
    em = discord.Embed(title= "Random Player Given", color=ctx.author.color)
    em.add_field(name=f"From {message}", value= f"Lucky Person is {random.choices(message.split())[0]}")
    await ctx.send(embed=em)


@client.command()
async def randomvc(ctx):
    em = discord.Embed(title= f"random user from voice chat {ctx.author.voice.channel}", color=ctx.author.color)

    if(ctx.author.voice):
        print('Here')
        # for x in (client.get_channel((ctx.author.voice.channel).id)).members:
        userInfo = (client.get_channel((ctx.author.voice.channel).id)).members
        memberList = [str(x) for x in userInfo]
        # print(random.choices([str(x) for x in userInfo]))
            
        em.add_field(name=f"From {memberList}", value= f"Lucky person is {random.choices([str(x) for x in userInfo])[0]}")

        await ctx.send(embed=em)

    else:
        await ctx.send("you're not in Voice chat yet")
        

client.run(int(info[1], 2).to_bytes((int(info[1], 2).bit_length() + 7) // 8, 'big').decode())