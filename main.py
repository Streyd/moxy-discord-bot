import discord as ds
from discord.ext import commands

TOKEN = "NzAyMTEwOTI1NDQ0MDg3ODE5.Xp-76Q.7rkQcesALlFwED8mg8B0oTW29K8"

client = commands.Bot(command_prefix="^_^")
client.remove_command("help")


wordlst = ['hello']

command_names = ["clear", "kick", "ban", "unban", "mute", "unmute", "deaf", "undeaf", "hex", "pure"]
command_discriptions = [
                        "Clean chat", "Kick member", "Ban member",
                        "Unban member", "Mute member", "Unmute member", "Deafen member", "Undeafen member",
                        "Mute & deafen member", "Unmute & undeafen member",
                        ]

def is_me(msg):
    return msg.author == client.user


def is_user(msg):
    return msg.content[:3] == "^_^"


def both(msg):
    return msg.author == client.user or msg.content[:3] == "^_^"


@client.event
async def on_ready():
    global client
    print("Оhayo ♡")


@client.event
async def on_message(message):
    await client.process_commands(message)
    msg = message.content.lower()
    if msg in wordlst:
        await message.channel.send("Oh")


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
                "Sorry, I don't understand you. Can you send an amount of messages you wnt to delete? (⌒_⌒;)")


@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: ds.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Rest in peace, {member.mention} (￣^￣)ゞ F")


@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: ds.Member, *, reason=None, delete_message_days=1):
    await member.ban(reason=reason, delete_message_days=delete_message_days)
    await ctx.send(f"{member.mention}, in a prison (ｏ・_・)ノ ")


@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    prison = await ctx.guild.bans()

    for prisoner in prison:
        print(prisoner.user.name + "#" + prisoner.user.discriminator)
        if prisoner.user.name + "#" + prisoner.user.discriminator == member:
            await ctx.guild.unban(prisoner.user)
            await ctx.send(f"Welcome back, {prisoner.user.mention}. We missed you ヾ(\*'▽'\*)")


@client.command(pass_context=True)
async def help(ctx):
    emb = ds.Embed(title="That's what i can do (´｡• ᵕ •｡`)", color=ds.Color.magenta())

    for command in command_names:
        emb.add_field(name=f"**{client.command_prefix}{command}**",
                      value=f"{command_discriptions[command_names.index(command)]}")
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

client.run(TOKEN)

