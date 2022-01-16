import discord
from discord.ext import commands

import random
from discord.utils import get
from imports import *
from datetime import datetime

class welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener(name='on_member_update')
    async def welcome_role(self, before, after):
        if before.guild.id == 781422576660250634:
            role = discord.utils.find(lambda r: r.id == 816858066330320897, after.guild.roles)
            if role in after.roles and role not in before.roles:
                channel = self.client.get_channel(781422576660250637)
                await channel.send(f"You made it {after.mention}! Welcome to **{after.guild.name}**, enjoy your stay 💚")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("Welcome message sent in DMs.")
        languages = random.choice(langs)
        embed = discord.Embed(
            title=f"Welcome to {member.guild.name}!",
            description="This is a 13+ voluntary non-professional hangout server based around mental health and mental illness with the purpose to make it easier to connect with new people and friends. To get started, head over to <#785551273734176828>. Once you've found the secret word, type it in <#784967488139558942> to verify that you are human. If you ever want to rejoin, use **[this link](https://discord.gg/nbKzQaK2su)**.",
            color=member.guild.me.color,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f"{languages} {member.name}!", icon_url=member.avatar_url)
        embed.set_thumbnail(url=f"{member.guild.icon_url}")
        embed.set_footer(text="The highlighted text are hyperlinks and can be clicked/tapped.", icon_url=member.guild.icon_url)
        await member.send(embed=embed)

def setup(client):
    client.add_cog(welcome(client))