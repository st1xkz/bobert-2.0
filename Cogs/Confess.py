import discord
from discord.ext import commands

import asyncio
from discord.utils import get
from datetime import datetime


class Confess(commands.Cog):
    def __init__(self, client: discord.ext.commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id == 806649868314869760:
            channel = self.client.get_channel(806649868314869760)
            log_channel = self.client.get_channel(806649188146348043)
            await message.delete()
            embed = discord.Embed(
                title="Success",
                description=
                f"I've received your confession and sent it to the <#806649874379964487> channel!",
                color=0x2f3136)
            embed.set_footer(text="Confessions")
            await message.channel.send(embed=embed, delete_after=1)

            channel = self.client.get_channel(806649874379964487)

            embed = discord.Embed(title="Confession",
                                  description=f"{message.content}",
                                  color=discord.Colour.random())
            embed.set_footer(text="All confessions are anonymous.")
            await channel.send(embed=embed)

            embed = discord.Embed(
                description=
                f"**Message deleted in <#806649868314869760>** \n{message.content}",
                color=0xFF4040)
            embed.set_author(name=message.author.display_name + " " + "(" + str(message.author) + ")", icon_url=message.author.avatar_url)
            embed.set_footer(text=f"Author: {message.author.id} | Message: {message.id}")
            await log_channel.send(embed=embed)

    @commands.command(help="Sends user's confession to the <#806649874379964487> channel through DMs")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def confess(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            log_channel = self.client.get_channel(806649188146348043)
            embed = discord.Embed(
                color=0x2f3136,
                title=" ",
                description=
                "⚠️ **Do not send random, pointless messages** \n\n⚠️ **Do not harass anyone** \n\n⚠️ **Add content warnings, trigger warnings, or spoil anything that could be potentially harmful or triggering to somebody. If your post requires them and does not contain them, your post will be deleted until it is added.** \n\n👇**send your confessions down below**👇",
                timestamp=datetime.utcnow())
            embed.set_author(name=str(ctx.author),
                             icon_url=ctx.author.avatar_url)
            embed.set_footer(text="Confessions")
            demand = await ctx.send(embed=embed)

            try:
                msg = await self.client.wait_for(
                    'message',
                    timeout=600,
                    check=lambda message: message.author == ctx.author and
                    message.channel == ctx.channel)
                if msg:
                    channel = get(self.client.get_all_channels(),
                                  name="﹕confessions")
                    embed = discord.Embed(title="Confession", description=f"{msg.content}", color=discord.Colour.random())
                    embed.set_footer(text="All confessions are anonymous.")
                    await channel.send(embed=embed)
                    await demand.delete()

                    embed = discord.Embed(
                        description=
                        f"**Message deleted in DMs** \n{msg.content}",
                        color=0xFF4040)
                    embed.set_author(name=ctx.author.display_name + " " + "(" + str(ctx.author) + ")", icon_url=ctx.author.avatar_url)
                    embed.set_footer(text=f"Author: {ctx.author.id} | Message: {ctx.message.id}")
                    await log_channel.send(embed=embed)

            except asyncio.TimeoutError:
                await ctx.send(
                    "Confessions has been timed out due to **10 minutes** of inactivity."
                )
                await demand.delete()

        else:
            await ctx.send("🌿 This command can only be used in Direct Messages")


def setup(client):
    client.add_cog(Confess(client))
