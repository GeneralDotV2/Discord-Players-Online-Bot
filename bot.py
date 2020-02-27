import json
from discord.ext import commands

config = json.load(open('config.json'))

client = commands.Bot(command_prefix=config['prefix'])


@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx):
    client.unload_extension('cogs.info')
    client.load_extension('cogs.info')
    await ctx.send("Reloaded.")
    print("Reloaded info cog.")

client.load_extension('cogs.info')
client.run(config['token'])
