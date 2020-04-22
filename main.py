import discord as ds
from discord.ext import commands

TOKEN = "NzAyMTEwOTI1NDQ0MDg3ODE5.Xp7W4g.Sprc3UNRXfNT2nA_lwZKLK2gg3E"

client = commands.Bot(command_prefix="^_^")


@client.event
async def on_ready():
    global client
    print("Оhai ^_^")


@client.command(pass_context=True)
async def hi(ctx):
    author = ctx.message.author
    await ctx.send(f"Ohai, {author.mention} ^_^")

client.run(TOKEN)

