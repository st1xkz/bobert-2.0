import discord
from discord.ext import commands

import json
from datetime import datetime


class ticket(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ct'])
    @commands.has_permissions(administrator=True)
    async def createticket(self, ctx, channel: discord.TextChannel=None):
        if channel is None:
            await ctx.send('Please include the channel or channel ID with this command')
            return

        title = channel.name
        guild = ctx.guild

        with open('./databases/ticket.json') as file:
            ticket_data = json.load(file)

        # Check if guild has any open tickets, if not create key and append
        # channel ID
        if not str(guild.id) in ticket_data.keys():
            ticket_data[str(guild.id)] = []

        ticket_data[str(guild.id)].append(channel.id)
        with open('./databases/ticket.json', 'w') as file:
            json.dump(ticket_data, file, indent=4)

        # creates new embed with reaction
        ticket_embed = discord.Embed(
            title=f"Welcome to {guild.name}!",
            color=0xffffff,
            description=f"{title}",
            timestamp=datetime.utcnow()
        )
        ticket_embed.set_thumbnail(url=f"{ctx.message.guild.icon_url}")
        send_ticket_embed = await channel.send(embed=ticket_embed)

        await send_ticket_embed.add_reaction('🎫')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def close(self, ctx, role: discord.Role):
        if role in ctx.author.roles:
            await role.delete(reason="Removed by command")
            await ctx.message.channel.delete(reason=None)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member == self.client.user:
            return

        guild = self.client.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        ch_category = channel.category
        message = await channel.fetch_message(payload.message_id)

        # Immediately remove user's reaction
        await message.remove_reaction(payload.emoji, payload.member)

        with open('./databases/ticket.json', 'r') as file:
            ticket_data = json.load(file)

        ticket_channels = ticket_data[str(guild.id)]

        if channel.id in ticket_channels:
            # gets guild and roles
            member_role = discord.utils.get(
                guild.roles, name=f'{payload.member.display_name}')
            if member_role is None:
                # creates new role
                permissions = discord.Permissions(
                    send_messages=True, read_messages=True)
                member_role = await guild.create_role(name=f'{payload.member.display_name}', permissions=permissions)

            # Assigns role to member
            await payload.member.add_roles(member_role, reason=None, atomic=True)

            # overwrites role permissions
            admin_role = discord.utils.get(guild.roles, name='Admin')

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member_role: discord.PermissionOverwrite(read_messages=True),
                admin_role: discord.PermissionOverwrite(
                    read_messages=True)
            }

            # creates new channel
            new_support_channel = await guild.create_text_channel(
                name=f'ticket-{member_role.name}',
                topic=f'New ticket for {payload.member.name}#{payload.member.discriminator}.\nRole: {member_role.mention}',
                category=ch_category,
                position=0,
                overwrites=overwrites
            )

            embed = discord.Embed(
                title="Thanks for Requesting Support!",
                description=f"Hey {payload.member.display_name}, this is your ticket! Please state what you made this ticket for, any issues you are experiencing and/or what you have tried and a staff member will be with you as soon as they can.\n\n**Remember to:**\n • Know that **no one** is obligated to answer you if they feel that you are trolling or misusing this ticket system.\n • **Make sure** to be as clear as possible when explaining and provide as many details as you can.\n • **Be patient** as we (staff members) have our own lives *outside of discord* and we tend to get busy most days. We are human, so you should treat us as such!\n\nAbusing/misusing this ticket system may result in punishment that varies from action to action.",
                color=payload.member.guild.me.color,
                timestamp=datetime.utcnow()
            )
            embed.set_footer(
                text="Closes when a staff member closes the ticket", icon_url=payload.member.avatar_url)
            await new_support_channel.send(f"{payload.member.mention}", embed=embed)


def setup(client):
    client.add_cog(ticket(client))