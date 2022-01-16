import discord
from discord.ext import commands

import json
from random import randint
from datetime import datetime

class ticket(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ct'])
    @commands.has_permissions(administrator=True)
    async def createticket(self, ctx, *args):
        format_args = list(args)

        guild_id = ctx.message.guild.id
        channel_id = int(format_args[0].strip('<').strip('>').replace('#', ''))
        title = ' '.join(format_args[1:])

        with open('./databases/ticket.json', 'r') as file:
            ticket_data = json.load(file)
            new_ticket = str(guild_id)

            # updates existing ticket
            if new_ticket in ticket_data:
                ticket_data[new_ticket] += [channel_id]
                with open('./databases/ticket.json', 'w') as update_ticket_data:
                    json.dump(ticket_data, update_ticket_data, indent=4)

            # add new ticket
            else:
                ticket_data[new_ticket] = [channel_id]
                with open('./databases/ticket.json', 'w') as new_ticket_data:
                    json.dump(ticket_data, new_ticket_data, indent=4)

        # create new embed with reaction
        ticket_embed = discord.Embed(
            title=f"Welcome to {ctx.message.guild.name}!",
            color=randint(0, 0xffffff),
            description=f"{title}",
            timestamp=datetime.utcnow()
        )
        ticket_embed.set_thumbnail(url=f"{ctx.message.guild.icon_url}")
        send_ticket_embed = await self.client.get_channel(channel_id).send(embed=ticket_embed)

        await send_ticket_embed.add_reaction('🎫')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def close(self, ctx, mentioned_user):
        mentioned_role = mentioned_user.strip('<@&>')
        get_mentioned_role = [items.name for items in ctx.message.author.guild.roles if f'{items.id}' in
                              f'{mentioned_role}']
        get_role = discord.utils.get(ctx.message.author.guild.roles, name=f'{get_mentioned_role[0]}')

        await get_role.delete(reason='Removed by command')
        await ctx.message.channel.delete(reason=None)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.id != self.client.user.id:
            with open('./databases/ticket.json', 'r') as file:
                ticket_data = json.load(file)

            channel_id = list(ticket_data.values())
            user_channel_id = payload.channel_id

            for items in channel_id:
                if user_channel_id in items:
                    # get guild and roles
                    find_guild = discord.utils.find(lambda guild: guild.id == payload.guild_id, self.client.guilds)
                    guild_roles = discord.utils.get(find_guild.roles, name=f'{payload.member.name}')

                    if guild_roles is None:
                        # create new role
                        permissions = discord.Permissions(send_messages=True, read_messages=True)
                        await find_guild.create_role(name=f'{payload.member.name}', permissions=permissions)

                        # assign new role
                        new_user_role = discord.utils.get(find_guild.roles, name=f'{payload.member.name}')
                        await payload.member.add_roles(new_user_role, reason=None, atomic=True)

                        # overwrite role permissions
                        admin_role = discord.utils.get(find_guild.roles, name='Admin')

                        overwrites = {
                            find_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                            new_user_role: discord.PermissionOverwrite(read_messages=True),
                            admin_role: discord.PermissionOverwrite(read_messages=True)
                        }

                        # create new channel
                        create_channel = await find_guild.create_text_channel(
                            'ticket-{}'.format(new_user_role), topic=f"New ticket for {payload.member.name}#{payload.member.discriminator}\n\n**Staff Tip**: To close a ticket, use this format **close <user_role>**", overwrites=overwrites)

                        embed = discord.Embed(
                            title="Thanks for Requesting Support!",
                            description=f"Hey {payload.member.display_name}, this is your ticket! Please state what you made this ticket for, any issues you are experiencing and/or what you have tried and a staff member will be with you as soon as they can.\n\n**Remember to:**\n • Know that **no one** is obligated to answer you if they feel that you are trolling or misusing this ticket system.\n • **Make sure** to be as clear as possible when explaining and provide as many details as you can.\n • **Be patient** as we (staff members) have our own lives *outside of Discord* and we tend to get busy most days. We are human, so you should treat us as such!\n\nAbusing/misusing this ticket system may result in punishment that varies from action to action.",
                            color=payload.member.guild.me.color,
                            timestamp=datetime.utcnow()
                        )
                        embed.set_footer(text="Closes after a period of inactivity, or when a staff member types *close <@user_role>", icon_url=payload.member.avatar_url)
                        await create_channel.send(f"{payload.member.mention}", embed=embed)

def setup(client):
    client.add_cog(ticket(client))