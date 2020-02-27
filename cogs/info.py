import requests
import json
import asyncio
import discord
from discord.ext import commands


class Info:
    def __init__(self, config, serverid, name):
        self.id = serverid
        self.name = name
        self.config = config

    def get_list(self):
        return requests.request("GET", (self.config['url'] + "/players/" + self.id)).text

    def get_players(self):
        page = json.loads(self.get_list())
        if "error" in page:
            return "> ```no players online```"
        players = ""
        for player in page:
            players += player['name'] + ", "
        return "> ```" + players[:-2] + "```"

    def get_info(self):
        return requests.request("GET", (self.config['url'] + "/status/" + self.id)).text

    def get_count(self):
        page = json.loads(self.get_list())
        if isinstance(page, dict):
            return 0
        return sum([1 for item in page if 'name' in item])

    def get_max(self):
        page = json.loads(self.get_info())
        return int(page['players_max'])

    def get_name(self):
        return self.name


config = json.load(open('config.json'))
servera = Info(config, config['server1']['id'], config['server1']['name'])
serverb = Info(config, config['server2']['id'], config['server2']['name'])
serverc = Info(config, config['server3']['id'], config['server3']['name'])
serverd = Info(config, config['server4']['id'], config['server4']['name'])


class Send(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass

    @commands.command()
    async def players(self, ctx, a=servera, b=serverb, c=serverc, d=serverd):
        count = [a.get_count(), b.get_count(), c.get_count(), d.get_count()]
        max_count = [a.get_max(), b.get_max(), c.get_max(), d.get_max()]

        embed = discord.Embed(
            color=0xCE422B,
            title="Playing Online: ({}/{})".format(sum(count), sum(max_count)),
        )
        embed.add_field(name="{}: ({}/{})".format(a.get_name(), count[0], max_count[0]), value=a.get_players(),
                        inline=False)
        embed.add_field(name="{}: ({}/{})".format(b.get_name(), count[1], max_count[1]), value=b.get_players(),
                        inline=False)
        embed.add_field(name="{}: ({}/{})".format(c.get_name(), count[2], max_count[2]), value=c.get_players(),
                        inline=False)
        embed.add_field(name="{}: ({}/{})".format(d.get_name(), count[3], max_count[3]), value=d.get_players(),
                        inline=False)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            count = [servera.get_count(), serverb.get_count(), serverc.get_count(), serverd.get_count()]
            max_count = [servera.get_max(), serverb.get_max(), serverc.get_max(), serverd.get_max()]
            await self.client.change_presence(
                status=discord.Status.dnd,
                activity=discord.Game("Online: ({}/{})".format(sum(count), sum(max_count)))
            )
            await asyncio.sleep(10)


def setup(client):
    client.add_cog(Send(client))
