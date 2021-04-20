import asyncio
from dataclasses import fields
from datetime import datetime
import time

from discord import FFmpegPCMAudio

from discord import member, Embed
from discord.ext.commands import Cog

image = ['https://static-cdn.jtvnw.net/jtv_user_pictures/cfd5e66a-f247-4158-be16-5aa5068f13a0-profile_image-70x70.png'
         'https://static-cdn.jtvnw.net/jtv_user_pictures/d05c03ad-4e70-4734-9159-51fc1477d564-profile_image-70x70.png'
         'https://static-cdn.jtvnw.net/jtv_user_pictures/6b4441ff-a6bf-4609-bc1d-32cba5b51c61-profile_image-70x70.png']


class Info(Cog):
    def __init__(self, bot):
        self.bot = bot


from discord.ext import commands

client = commands.Bot(command_prefix='t?')

status = ['Tocando Musica', 'Run Turtle Run!!', 'Dormindo']

frasesproanbu = ['Deve ta dando o cu é a cara dele...','Resolvendo os bugs dele','Ta dormindo','Porque eu iria saber?','Tomara que tenham hackeado o codigo dele :D']

import discord
from discord.ext import tasks
import youtube_dl

from random import choice

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


#####INICIAR#####
@client.event
async def on_ready():
    change_status.start()
    print('Turtle Is Online!')


@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(
        f'**Bem Vindo** {member.mention}! Pronto pra correr? Fale ?commands para mostrar minhas habilidades!!')


#######PING#######

@client.command(name='ping')
async def ping(ctx):
    await ctx.send(f'**BUM!** Latencia: {round(client.latency * 1000)}ms')


#######OLA#######


@client.command(name='ola')
async def ola(ctx):
    respostas = ['Oi seu gostoso(a)', 'Olha onde????', 'Olaa! Tudo bem com você?', 'To com sono',
                 'Oi Amigo! Tava com saudade']
    await ctx.send(choice(respostas))


#######RUNTURTLE#######

@client.command(name='run')
async def run(ctx):
    respostas = ['To Correeendo!!', 'RUN TURTLE RUNNN!!!', 'No.', 'Pisquei te passei o pau e tu nao viu']
    await ctx.send(choice(respostas))


#######CREDITS#######

@client.command(name='credits')
async def run(ctx):
    await ctx.send('Made By: **DuxX**')
    await ctx.send('Obrigado **Sr DuxX** por ter me trazido a vida')
    await ctx.send('**ANBU** Chupa meu CU! Voce sempre sera inferior a minha presença')


#######MUSICAS#######


@client.command(name='play')
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send('Voce não esta em um canal de voz.')
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        if url == 'calaboca':
            player = await YTDLSource.from_url('https://www.youtube.com/watch?v=cMTrUCasbss', loop=client.loop)
        elif url == 'ola':
            player = await YTDLSource.from_url('https://www.youtube.com/watch?v=cMTrUCasbss', loop=client.loop)
        else:
            player = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send(f'**Tocando Agora:** {player.title}')


@client.command(name='stop')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()


#######STREAMERS#######


@client.command(name='streamers')
async def stremers(ctx):
    embed = discord.Embed(title='Stremer#1', color=discord.Colour.blue())
    embed.set_image(
        url='https://static-cdn.jtvnw.net/jtv_user_pictures/cfd5e66a-f247-4158-be16-5aa5068f13a0-profile_image-70x70.png')
    embed.add_field(name='ID:', value='@Dux')
    embed.add_field(name='URL:', value='https://www.twitch.tv/igdux')

    await ctx.send(embed=embed)

    embed = discord.Embed(title='Streamer#2', color=discord.Colour.blue())
    embed.set_image(
        url='https://static-cdn.jtvnw.net/jtv_user_pictures/6b4441ff-a6bf-4609-bc1d-32cba5b51c61-profile_image-70x70.png')
    embed.add_field(name='ID:', value='@F4')
    embed.add_field(name='URL:', value='https://www.twitch.tv/f4_zzz')

    await ctx.send(embed=embed)
    embed = discord.Embed(title='Streamer#3', color=discord.Colour.blue())
    embed.set_image(
        url='https://static-cdn.jtvnw.net/jtv_user_pictures/d05c03ad-4e70-4734-9159-51fc1477d564-profile_image-70x70.png')
    embed.add_field(name='ID:', value='@Héset')
    embed.add_field(name='URL:', value='https://www.twitch.tv/1heset')

    await ctx.send(embed=embed)
    embed = discord.Embed(title='Streamer#4', color=discord.Colour.blue())
    embed.set_image(
        url='https://static-cdn.jtvnw.net/jtv_user_pictures/216fb513-c711-4d1e-abd6-0503b9744c18-profile_image-70x70.png')
    embed.add_field(name='ID:', value='@Japoleca')
    embed.add_field(name='URL:', value='https://www.twitch.tv/japoleca')

    await ctx.send(embed=embed)


#######COMANDOS#######


@client.command(name='comandos')
async def comandos(ctx):
    embed = discord.Embed(title='Comandos', color=discord.Colour.blue())
    embed.add_field(name='**#1**:?ping', value='(Mostra Seu Ping!)')
    embed.add_field(name='**#2**:?play', value='(Da Play Na Sua Musica!)')
    embed.add_field(name='**#3**:?streamers', value='(Todos Os Streamers Do Servidor!)')
    embed.add_field(name='**#4**:?stop', value='(Para A Musica Atual!)')
    embed.add_field(name='**#5**:?ola', value='(Voce Fala Com O Turtle!)')
    embed.add_field(name='**#6**:?run', value='(Faz O Turtle Correr!)')
    embed.add_field(name='**#7**:?credits', value='(As Dedicações Do Meu DNA!)')
    embed.add_field(name='**#8**:?falaeai', value='(Eu Falo Eai No Voice!)')
    embed.add_field(name='**#9**:?xinganois', value='(Xingo Voces No Voice!)')

    await ctx.send(embed=embed)


#######MEMBROS#######


@client.command(name='membros')
async def membros(ctx):
    guild = member.guild
    await ctx.edit(name='---Quantidade De Membros--- **{}**'.format(guild.member_count))


@client.command(name="serverinfo")
async def serverinfo(ctx, statuses=None):
    embed = Embed(title="Informação Do Server",
                  colour=discord.Colour.blue(),
                  timestamp=datetime.utcnow())

    await ctx.send(embed=embed)



#######FALAS DO TURTLE#######


@client.command(name='falaeai')
async def falaeai(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('eai.wav')
        player = voice.play(source)

        time.sleep(6)
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()

        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.stop()


@client.command(name='xinganois')
async def xinganois(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('xingando.wav')
        player = voice.play(source)

        time.sleep(6)
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()

        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.stop()


@client.command(name='anbusheat')
async def anbusheat(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('anbu1.wav')
        player = voice.play(source)

        time.sleep(6)
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()

        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.stop()


@client.command(name='anbusheat2')
async def anbusheat(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('anbu2.wav')
        player = voice.play(source)

        time.sleep(6)
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()

        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.stop()


@client.command(name='turtle_cade_o_anbu')
async def turtle_cade_o_anbu(ctx):
    await ctx.send((choice(frasesproanbu)))



###################################################



@Cog.listener()
async def on_ready(self):
    if not self.bot.ready:
        self.bot.cogs_ready.ready_up("info")


@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))


def setup(bot):
    bot.add_cog(Info(bot))


client.run('')
