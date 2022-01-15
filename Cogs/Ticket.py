import discord
from discord.ext import commands

import asyncio
import aiofiles
from datetime import datetime


class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        self.client.ticket_configs = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for file in ['ticket_configs.txt']:
            async with aiofiles.open(file, mode="a") as temp:
                pass

        async with aiofiles.open("ticket_configs.txt", mode="r") as file:
            lines = await file.readlines()
            for line in lines:
                data = line.split(" ")
                self.client.ticket_configs[int(
                    data[0])] = [int(data[1]),
                                 int(data[2]),
                                 int(data[3])]

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.id != self.client.user.id and str(
                payload.emoji) == "🎫":
            msg_id, channel_id, category_id = self.client.ticket_configs[
                payload.guild_id]

            if payload.message_id == msg_id:
                guild = self.client.get_guild(payload.guild_id)

                for category in guild.categories:
                    if category.id == category_id:
                        break

                channel = guild.get_channel(channel_id)

                ticket_channel = await category.create_text_channel(
                    f"ticket-{payload.member.name}",
                    topic=
                    f"A ticket for {payload.member.name}#{payload.member.discriminator}.",
                    permission_synced=True)

                await ticket_channel.set_permissions(payload.member, read_messages=True, send_messages=True)

                message = await channel.fetch_message(msg_id)
                await message.remove_reaction(payload.emoji, payload.member)

                embed = discord.Embed(
                    title="Thanks for Requesting Support!",
                    description=f"Hey {payload.member.display_name}, this is your ticket!",
                    color=payload.member.guild.me.color,
                    timestamp=datetime.utcnow()
                )
                embed.set_footer(text="Type *close to close the ticket", icon_url=payload)
                await ticket_channel.send(f"{payload.member.mention}", embed=embed)

                try:
                    await self.client.wait_for(
                        "message",
                        check=lambda m: m.channel == ticket_channel and m.
                        author == payload.member and m.content == "*close",
                        timeout=3600)

                except asyncio.TimeoutError:
                    await ticket_channel.delete()

                else:
                    await ticket_channel.delete()

    @commands.command(aliases=['ctic'])
    @commands.is_owner()
    async def configticket(self, ctx, msg: discord.Message = None, category: discord.CategoryChannel = None):
        if msg is None or category is None:
            await ctx.channel.send("Failed to configure the ticket as an argument was not given or was invalid.", delete_after=60)
            return

        self.client.ticket_configs[ctx.guild.id] = [
            msg.id, msg.channel.id, category.id
        ]  # this resets the configuration

        async with aiofiles.open("ticket_configs.txt", mode="r") as file:
            data = await file.readlines()

        async with aiofiles.open("ticket_configs.txt", mode="w") as file:
            await file.write(
                f"{ctx.guild.id} {msg.id} {msg.channel.id} {category.id}\n")

            for line in data:
                if int(line.split(" ")[0]) != ctx.guild.id:
                    await file.write(line)

        await msg.add_reaction("🎫")
        await ctx.channel.send(f"✅ Successfully configured ticket system for **{ctx.guild.name}**.", delete_after=60)

    @commands.command(aliases=['tcon'])
    @commands.is_owner()
    async def ticket_config(self, ctx):
        try:
            msg_id, channel_id, category_id = self.client.ticket_configs[
                ctx.guild.id]

        except KeyError:
            await ctx.channel.send("❌ You have not configured the ticket system yet.", delete_after=60)

        else:
            embed = discord.Embed(title="Ticket System Configurations", color=discord.Color.green(), timestamp=datetime.utcnow())
            embed.description = f"**Reaction Message ID**: {msg_id}\n"
            embed.description += f"**Ticket Category ID**: {category_id}\n\n"


def setup(client):
    client.add_cog(Ticket(client))
