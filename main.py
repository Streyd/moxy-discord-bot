import discord as ds
from discord.ext import commands

TOKEN = "NzAyMTEwOTI1NDQ0MDg3ODE5.Xp-76Q.7rkQcesALlFwED8mg8B0oTW29K8"

client = commands.Bot(command_prefix="^_^")
client.remove_command("help")


wordlst = ['hello']

command_names = ["clear", "kick", "ban", "unban"]
command_discriptions = ["Clean chat", "Kick member", "Ban member", "Unban member"]

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
    emb = ds.Embed(title="That's what i can do (´｡• ᵕ •｡`)")

    for command in command_names:
        emb.add_field(name=f"**{client.command_prefix}{command}**",
                      value=f"*{command_discriptions[command_names.index(command)]}*")

    await ctx.send(embed=emb)


client.run(TOKEN)

