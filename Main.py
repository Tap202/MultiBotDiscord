import discord
import youtube_dl
from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
import random 
import datetime
from datetime import timezone, tzinfo, timedelta
import os

players  = {}
data_dict = {'downloads': {}}
role = "Teste"

client = commands.Bot(command_prefix = '!')
status = cycle(['Esta', 'Mensagem', 'Muda', 'A', 'Cada', '2', 'Segundos'])



@client.event
async def on_ready():
    change_status.start()
    print('Bot ligado.')

@tasks.loop(seconds=2)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_member_join(member):
    await member.send('Bem vindo ao servidor')


@client.event
async def on_member_remove(member):
     await member.send('Saiu do servidor')

@client.command()
async def ping(ctx):
    await ctx.send(f'Ping do servidor é de {round(client.latency * 1000)}ms')

@client.command()
async def mensagem(ctx):
    await ctx.send('@everyone Hi this is a custom message\n If you need any help just type the command !help\n @everyone')

@client.command(aliases=['perguntas', 'Perguntas'])
async def pergunta(ctx, *, question):
    responses = ["Com certeza.",
                "Sim.",
                "Claramente.",
                "Não.",
                "Talvez.",
                "Claramente que não."]
    await ctx.send(f'Pergunta: {question}\nResposta: {random.choice(responses)}')

@client.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)

@client.command(pass_context=True, aliases=['join'])
async def JOIN(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"Entrei no canal: {channel}\n")

    await ctx.send(f"Entrei no canal: {channel}")


@client.command(pass_context=True, aliases=['leave'])
async def LEAVE(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Saí do canal: {channel}")
        await ctx.send(f"Saí do canal: {channel}")
    else:
        print("Não estou em nenhum canal de voz")
        await ctx.send("Não estou em nenhum canal de voz")


@client.command(pass_context=True, aliases=['play'])
async def PLAY(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Ficheiro antigo apagado")
    except PermissionError:
        print("Música ainda está a tocar")
        await ctx.send("Música ainda está a tocar")
        return

    await ctx.send("A preparar tudo")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("A fazer download\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renomeação do ficheiro: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Música pronta!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"A tocar: {nname[0]}")
    print("A tocar\n")


@client.command(pass_context=True, aliases=['pause'])
async def PAUSE(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Musica pausada")
        voice.pause()
        await ctx.send("Musica pausada")
    else:
        print("A musica não está a ser tocada, erro na pausa")
        await ctx.send("A musica não está a ser tocada, erro na pausa")


@client.command(pass_context=True, aliases=['resume'])
async def RESUME(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Musica resumida")
        voice.resume()
        await ctx.send("Musica resumida")
    else:
        print("A musica nao esta pausada")
        await ctx.send("A musica nao esta pausada")


@client.command(pass_context=True, aliases=['stop'])
async def STOP(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Musica parada")
        voice.stop()
        await ctx.send("Musica paradada")
    else:
        print("Nenhuma musica esta a ser tocada, erro a parar")
        await ctx.send("Nenhuma musica esta a ser tocada, erro a parar")


@client.command()
async def Adicionar(ctx,a:int,b:int):
    await ctx.send('O valor da soma é: ')
    await ctx.send(a+b)

@client.command()
async def Subtrair(ctx,a:int,b:int):
    await ctx.send('O valor da subtração é: ')
    await ctx.send(a-b)

@client.command()
async def Multiplicar(ctx,a:int,b:int):
    await ctx.send('O valor da multiplicação é:')
    await ctx.send(a*b)

@client.command()
async def Dividir(ctx,a:int,b:int):
    await ctx.send('O valor da divisão é: ')
    await ctx.send(a/b)

@client.command()
async def time(ctx):
    t = datetime.datetime.now()
    await ctx.send(t.strftime('São %Ih:%Mm:%Ss %p'))

@client.command()
async def on_member_join(member):
    role = get(member.add_roles ,name=ROLE)
    await member.add_roles(role)
    print(f"{member} was given {role}")

client.run('')