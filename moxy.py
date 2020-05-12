import discord as ds
from discord.ext import commands
import constants
import youtube_dl
from discord.utils import get
import os
from discord import utils
import data.db_session as db_session
from data.commands import Commands


client = commands.Bot(command_prefix=constants.PREFIX)
client.remove_command("help")



def is_me(msg):
    return msg.author == client.user


def is_user(msg):
    return msg.content[:3] == "^_^"


def both(msg):
    return msg.author == client.user or msg.content[:3] == "^_^"


@client.event
async def on_ready():
    global client
    print("Оhayo")
    await client.change_presence(status=ds.Status.online, activity=ds.Game("^_^help"))


@client.event
async def on_message(message):
    await client.process_commands(message)
    msg = message.content.lower()
    if msg in constants.WORDLST:
        await message.channel.send("Ohayo")
    if message.content[:3] == "^_^" and message.content[3:] not in constants.COMMANDS and message.content.count(" ") == 0:
        db_session.global_init("data/db/custom_commands.sqlite")
        session = db_session.create_session()
        if session.query(Commands).filter(Commands.command_name == message.content[3:]).first():
            command = session.query(Commands).filter(Commands.command_name == message.content[3:]).first()
            if not command.is_private or (command.is_private and message.author == command.author):
                emb = ds.Embed(title=command.text, color=ds.Color.magenta())
                emb.set_image(url=command.img)
                await message.channel.send(embed=emb)


@client.event
async def on_raw_reaction_add(ctx):
    if ctx.message_id == constants.ROLE_POST_ID:
        channel = client.get_channel(ctx.channel_id)
        message = await channel.fetch_message(ctx.message_id)
        member = utils.get(message.guild.members,
                           id=ctx.user_id)

        try:
            emoji = str(ctx.emoji)
            role = utils.get(message.guild.roles, id=constants.ROLES[emoji])

            if (len([i for i in member.roles if i.id not in constants.EXECUTION_ROLES]) <= constants.MAX_ROLES_PER_MEMBER):
                await member.add_roles(role)
                print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
            else:
                await message.remove_reaction(ctx.emoji, member)
                print('[ERROR] Too many roles for user {0.display_name}'.format(member))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))


@client.event
async def on_raw_reaction_remove(ctx):
    channel = client.get_channel(ctx.channel_id)
    message = await channel.fetch_message(ctx.message_id)
    member = utils.get(message.guild.members,
                       id=ctx.user_id)

    try:
        emoji = str(ctx.emoji)
        role = utils.get(message.guild.roles, id=constants.ROLES[emoji])

        await member.remove_roles(role)
        print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))

    except KeyError as e:
        print('[ERROR] KeyError, no role found for ' + emoji)
    except Exception as e:
        print(repr(e))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, ds.ext.commands.CommandNotFound):
        print("[ERROR] Command not found")
        return
    raise error


@client.command(pass_context=True)
async def hi(ctx):
    author = ctx.message.author
    await ctx.send(f"Ohayo, {author.mention} ^_^")


@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount="10"):
    if amount == "answers":
        deleted = await ctx.channel.purge(limit=100, check=is_me)
        await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))
    elif amount == "commands":
        deleted = await ctx.channel.purge(limit=100, check=is_user)
        await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))
    elif amount == "bot":
        deleted = await ctx.channel.purge(limit=100, check=both)
        await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))
    else:
        try:
            deleted = await ctx.channel.purge(limit=int(amount))
            await ctx.channel.send('Deleted {} message(s)'.format(len(deleted) - 1))
        except ValueError:
            await ctx.channel.send(
                "Sorry, I don't understand you. Can you send an amount of messages you want to delete? (⌒_⌒;)")


@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: ds.Member, *, reason=None):
    guild = member.guild.name
    await member.send(f"U have kicked from {guild}")
    await member.kick(reason=reason)
    await ctx.send(f"Rest in peace, {member.mention} (￣^￣)ゞ F")


@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: ds.Member, *, reason=None, delete_message_days=1):
    guild = ctx.guild
    await member.send(f"U have banned on {guild.name}")
    print(member)
    await member.ban(reason=reason, delete_message_days=delete_message_days)
    await ctx.send(f"{member.mention}, in a prison (ｏ・_・)ノ ")


@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    prison = await ctx.guild.bans()

    for prisoner in prison:
        if str(prisoner.user) == member:
            await ctx.guild.unban(prisoner.user)
            guild = ctx.guild
            invite = ds.Invite
            invite.guild = guild
            await ctx.send(f"Welcome back, {prisoner.user.mention}. We missed you ヾ(\*'▽'\*)")


@client.command(pass_context=True)
async def help(ctx):
    emb = ds.Embed(title="That's what i can do (´｡• ᵕ •｡`)", color=ds.Color.magenta())

    for command in constants.COMMANDS.keys():
        emb.add_field(name=f"**{client.command_prefix}{command}**",
                      value=f"{constants.COMMANDS[command]}")
        emb.set_thumbnail(url="https://avatars.mds.yandex.net/get-pdb/1956095/3a5f7825-06f5-4801-9d30-73c811a06471/s1200?webp=false")
    await ctx.send(embed=emb)


@client.command(pass_context=True)
async def mute(ctx, member: ds.Member, *, reason=None):
    if ctx.author.guild_permissions.mute_members:
        await member.edit(reason=reason, mute=True)
        await ctx.send(f"I have cast orchid {member.mention} ( ・∀・)・・・--------☆ ")


@client.command(pass_context=True)
async def unmute(ctx, member: ds.Member, *, reason=None):
    if ctx.author.guild_permissions.mute_members:
        await member.edit(reason=reason, mute=False)
        await ctx.send(f"{member.mention} have used black king bar w(ﾟｏﾟ)w")


@client.command(pass_context=True)
async def deaf(ctx, member: ds.Member, *, reason=None):
    if ctx.author.guild_permissions.deafen_members:
        await member.edit(reason=reason, deafen=True)
        await ctx.send(f"{member.mention} have been stunned w(ﾟｏﾟ)w ")


@client.command(pass_context=True)
async def undeaf(ctx, member: ds.Member, *, reason=None):
    if ctx.author.guild_permissions.deafen_members:
        await member.edit(reason=reason, deafen=False)
        await ctx.send(f"{member.mention} have been used lotus orb ")


@client.command(pass_context=True)
async def hex(ctx, member: ds.Member, *, reason=None):
    if ctx.author.guild_permissions.deafen_members:
        await member.edit(reason=reason, mute=True, deafen=True)
        await ctx.send(f"I have cast hex {member.mention} ( ・∀・)・・・--------☆ ")


@client.command(pass_context=True)
async def pure(ctx, member: ds.Member, *, reason=None):
    if ctx.author.guild_permissions.mute_members and ctx.author.guild_permissions.deafen_members:
        await member.edit(reason=reason, mute=False, deafen=False)
        await ctx.send(f"{member.mention} have been purificated")


@client.command(pass_context=True)
async def play(ctx, *, song_url: str):
    global voice_client
    guild = ctx.guild
    voice_client = get(client.voice_clients, guild=guild)
    voice_channel = ctx.message.author.voice.channel
    if not voice_client:
        if ctx.message.author.voice.channel:
            voice_client = await voice_channel.connect()
            song_here = os.path.isdir("./player")
            if song_here:
                for file in os.listdir("./player"):
                    os.remove(f"./player/{file}")
            voice_client = get(client.voice_clients, guild=guild)

            ydl_config = {
                "format": "bestaudio/best",
                "postprocessor": [{
                    "key": "FFmpegExtractAudio",
                    "preferedcodec": "mp3",
                    "preeredquality": "192"}],
                'outtmpl': os.path.join("./player", '%(title)s-%(id)s.%(ext)s')
            }
            with youtube_dl.YoutubeDL(ydl_config) as ydl:
                ydl.download([song_url])

            voice_client.play(ds.FFmpegPCMAudio("./player/" + os.listdir("./player")[0]))
            voice_client.source = ds.PCMVolumeTransformer(voice_client.source)
            voice_client.source.volume = 0.07
        else:
            ctx.send("Pls, join to voice channel")
    else:
        await ctx.send("I'm too busy")


client.run(constants.TOKEN)

