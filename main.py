import discord
from discord.ext import commands
import os  # play os

import matplotlib.pyplot as plt
import youtube_dl 
import time  # Class,Count
import requests
import json

try:
    with open('discord_py/SECRET.txt') as f:
        info = f.readlines()
except FileNotFoundError:
    with open('SECRET.txt') as f:
        info = f.readlines()

client = commands.Bot(command_prefix="=")

@client.event
async def on_ready():  # Event client ready
    await client.change_presence(status=discord.Status.idle,activity=discord.Game('=list')) #Change status to =help
    print("ID :" , client.user.id)
    print(f'Running on {len(client.guilds)} server')
    print(time.strftime("%a, %d %b %Y %H:%M:%S"))
    print(f'{client.user.name} is online')  # Print TOBI is online
    print('='*50)

@client.command()  # list commands
async def list(ctx):  # Contact list word
    embed = discord.Embed(title = "List commands", description = "Use '=list'",color = ctx.author.color)
    embed.add_field(name="Basic", value=
    "TOBI but in json file\n"
    "**Network**        for Check TOBI Network (.ms)\n"
    "**userinfo**       for Check user information (Join server, Role)\n"
    "**search**         for Search something on wikipedia)\n"
    "**gacha _ _**      for random number from fisrt to second\n"
    "**prize _ _**      for Give away prize from Admin by set time and prize\n"
    "**poll**           for vote Good or Bad (No limit user)\n"
    "**spawn**          for spawn TOBI to channel\n"
    "**weather**        for check weather today\n"
    "**covid**          for check daily covid\n"
    "**covid_stat**     for Covid stat in duration by Graph and total\n"
    "**lotetry**        for lotetry today\n"
    "**bomb**           for delete message in channel\n")
    embed.add_field(name="Report", value=
    "**report**         for report User by Issue to Admin to discuss and Vote\n")
    embed.add_field(name="Math", value=
    "**plus _ _**       for plus the numbers\n"
    "**minus _ _**      for minus the numbers\n"
    "**multiplie _ _**  for multiplie the numbers\n"
    "**divide __**      for divide the numbers\n"
    "**sqrt __**        for Square root the numbers\n"
    "**expo __**        for exponent the numbers\n"
    "**fac __**        for factorial the numbers\n")
    embed.add_field(name="Audio", value=
    "**play 'url'**     for play song\n"
    "**stop**           for stop song\n"
    "**pause**          for pause song\n"
    "**resume**         for resume song\n" )
    embed.add_field(name="ADMIN", value=
    "only Admin or mod can acess this permission\n"
    "**mute @___**      for muted someone\n"
    "**unmute @___**    for unmuted someone\n"
    "**kick @___**      for kick someone from the server\n"
    "**ban @___**       for ban someone from the server\n"
    "**vote**           for vote member when Vote was started\n")
    embed.add_field(name="Tobi", value=
    "**tobiinfo**       for TOBI information\n"
    "**git**            for GitHub\n"
    "**updateinfo**     for TOBI update command or function\n")
    await ctx.send(embed=embed)


@client.command(description="Gets the bot's latency.")
async def Network(ctx): #Network
    latency = round(client.latency * 1000, 1)
    print(f'Network command activated by {ctx.author.name} status {latency} on server {ctx.author.guild.name}')
    await ctx.send(f"Network = {latency}ms")

@client.event 
async def on_member_join(member): # join
    role = discord.utils.get(member.server.roles,name = 'USERS') 
    await client.add_roles(member, role) #Give user USER role to new member
    print(f'{member} has joined the server.') #TODO

@client.event
async def on_member_remove(member): # remove
    print(f'{member} has removed the server.')

@client.command() # ping pong
async def ping(ctx):
    print(f'Ping command activated by {ctx.author.name} on channel {ctx.channel.name} server {ctx.author.guild.name}') 
    await ctx.send("pong")

@client.command()
async def weather(ctx, city='Songkhla'):
    print(f'Weather command activated by {ctx.author.name} on channel {ctx.channel.name} server {ctx.author.guild.name}')
    city = city
    api = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=06c921750b9a82d8f5d1294e1586276f"
    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']
    sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunrise'] - 21600))
    sunset = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunset'] - 21600))
    embed = discord.Embed(title=f'Weather {city}', description='Today list', color=discord.Color.blue())

    if condition == 'Thunderstorm':
        embed.add_field(name=f'Today : {condition} ⛈', value=f'{str(temp)} °C')

    if condition == 'Drizzle':
        embed.add_field(name=f'Today : {condition} 🌧', value=f'{str(temp)} °C')

    if condition == 'Rain':
        
        embed.add_field(name=f'Today : {condition} 🌧',value=f'{str(temp)} °C')

    if condition == 'Snow':
        embed.add_field(name=f'Today : {condition} 🌨',value=f'{str(temp)} °C')

    if condition == 'Atmosphere':
        embed.add_field(name=f'Today : {condition} 🌬',value=f'{str(temp)} °C')

    if condition == 'Clear':
        embed = discord.Embed(title=f'Weather {city}',description='Today list',color = discord.Color.blue())
        embed.add_field(name=f'Today : {condition} ☁️',value=f'{str(temp)} °C')

    if condition == 'Clouds':
        embed = discord.Embed(title=f'Weather {city}',description='Today list',color = discord.Color.blue())
        embed.add_field(name=f'Today : {condition} ⛅️',value=f'{str(temp)} °C')

    embed.add_field(name='Min temp🌡 :',value=f'{str(min_temp)} °C')
    embed.add_field(name='Max temp💥 :',value=f'{str(max_temp)} °C')
    embed.add_field(name='Pressure✨ :',value=f'{str(pressure)} °C')
    embed.add_field(name='Humidity☄️ :',value=f'{str(humidity)} ')
    embed.add_field(name='Wind Speed🌫 :',value=f'{str(wind)} ')
    embed.add_field(name='Sunrise☀️ :',value=f'{str(sunrise)} pm')
    embed.add_field(name='Sunset🌤 :',value=f'{str(sunset)} pm')

    await ctx.send(embed = embed)

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

        #await ctx.send(file=discord.File('covid.png'))
        await ctx.send(file=file, embed=embed)
    
    else:

        await ctx.send('Not in a range')

@client.command() #Kick
async def kick(ctx, member :discord.Member, *,reason = "Kick because you don't follow the rules"):
    print(f'Kick command activated by {ctx.author.name} to {member} on channel {ctx.channel.name} server {ctx.author.guild.name}')
    await member.kick(reason=reason)


@client.command() #Ban
async def ban(ctx, member :discord.Member, *,reason = "Ban because you don't follow the rules"):
    print(f'Ban command activated by {ctx.author.name} to {member} on channel {ctx.channel.name} server {ctx.author.guild.name}')
    await member.ban(reason=reason)

@client.command(invoke_without_command = True) #tobiinfo
async def tobiinfo(ctx):
    print(f'Info command activated by {ctx.author.name} on channel {ctx.channel.name} server {ctx.author.guild.name}')
    em = discord.Embed(title = "TOBI information.json", description = "Use '=tobiinfo'",color = ctx.author.color)
    em.add_field(name = "Info",value=
    "Build by Mr. Narongkorn kitrungrot\n"
    "Version 0.11.1 (2/11/2021)\n"
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


@client.command()  # poll
async def poll(ctx,*,message):
    print(f'Poll command activated by {ctx.author.name} on channel {ctx.channel.name} server {ctx.author.guild.name}')
    em = discord.Embed(title = "Vote", description = f"{message}",color = ctx.author.color)
    em.add_field(name = "Poll",value="I vote bote of them so it will count 1 first")
    msg = await ctx.channel.send(embed=em)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')
    x = len(message.reactions)
    print(x)


@client.command() #Vote
async def vote(ctx, member :discord.Member):
    print(f'Vote command activated by {ctx.author.name} on channel {ctx.channel.name} server {ctx.author.guild.name}')
    await ctx.send(f"Recieve Vote {member}")
    time.sleep(10)
    await ctx.channel.purge(limit=2)

@client.command(pass_context = True)  # spawn
async def spawn(ctx):

    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        
        await channel.connect()
    else:
        await ctx.send("you're not in the voice channel")

    print(f'Spawn command activated by {ctx.author.name} at {channel} on server {ctx.author.guild.name}')

@client.command()  # play
async def play(ctx, url):
    channel = ctx.message.author.voice.channel
    embed_play = discord.Embed(title = f'Play {url}',description = 'Playing music in queue',color = ctx.author.color) 
    msg = await ctx.send(embed = embed_play) 
    await msg.add_reaction('🎶')
    print(f'Play command activated by {ctx.author.name} play {url} at {channel} on server {ctx.author.guild.name}')
    song_there = os.path.isfile("song.mp3")

    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return
    
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name= str(channel))#Finish
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()  # leave
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)   
    print(f'Leave command activated by {ctx.author.name} on server {ctx.author.guild.name}')
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()  # pause
async def pause(ctx):
    embed_pause = discord.Embed(title = f'pause  song',description = 'Playing music in queue',color = ctx.author.color)
    print(f'Pause command activated by {ctx.author.name} on server {ctx.author.guild.name}')
    msg = await ctx.send(embed = embed_pause)
    await msg.add_reaction('🔇')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()  # resume
async def resume(ctx):
    embed_resume = discord.Embed(title = f'Resume the song song',description = 'Playing music in queue',color = ctx.author.color)
    print(f'Resume command activated by {ctx.author.name} on server {ctx.author.guild.name}')
    msg = await ctx.send(embed = embed_resume)
    await msg.add_reaction('🔉')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()  # stop
async def stop(ctx):
    embed_stop = discord.Embed(title = 'Stop song',description = 'Stop playing music in queue',color = ctx.author.color)
    print(f'Stop command activated by {ctx.author.name} on server {ctx.author.guild.name}')
    msg = await ctx.send(embed = embed_stop)
    await msg.add_reaction('🔴')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    
client.run(int(info[1], 2).to_bytes((int(info[1], 2).bit_length() + 7) // 8, 'big').decode())