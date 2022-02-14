import disnake
from disnake.ext import commands

import time

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Shows the bot's latency")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        start_time = time.time()
        message = await ctx.send(f"Pong! 🏓 \nWs Latency: **{round(self.bot.latency * 1000)}ms**")
        end_time = time.time()

        await message.edit(content=f"Pong! 🏓 \nWS Latency: **{round(self.bot.latency * 1000)}ms** \nAPI Latency: **{round((end_time - start_time) * 1000)}ms**")

    @commands.command(aliases=['purge'], help="Deletes a certain number of messages (deletes 10 messages by default)", usage="<amount>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount)
        await ctx.channel.send(f"**{amount}** messages were removed", delete_after=5)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            message = (f"🚫 This command requires you to either be an Admin or have the `Manage Messages` permission to use it.")
        await ctx.send(message, delete_after=5)

    @commands.command(aliases=['lk'], help="Locks a channel", usage="<#channel>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: disnake.TextChannel):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"⚠️ {channel.mention} is now in lockdown.")

    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            message = (f"🚫 This command requires you to either be an Admin or have the `Manage Channels` permission to use it.")
            await ctx.send(message, delete_after=5)

    @commands.command(aliases=['uk'], help="Unlocks a channel", usage="<#channel>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: disnake.TextChannel):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"⚠️ {channel.mention} has been unlocked.")

    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            message = (f"🚫 This command requires you to either be an Admin or have the `Manage Channels` permission to use it.")
        await ctx.send(message, delete_after=5)

    @commands.command(aliases=['sl'], help="Locks the entire server")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def serverlockdown(self, ctx):
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)

        for channel in ctx.guild.text_channels:
            await channel.send("⚠️ Server is now in lockdown.", delete_after=60.0)

    @serverlockdown.error
    async def serverlockdown_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            message = (f"🚫 This command requires you to either be an Admin or have the `Manage Channels` permission to use it.")
        await ctx.send(message, delete_after=5)

    @commands.command(aliases=['sul'], help="Unlocks the entire server")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def serverunlock(self, ctx):
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=None)

        for channel in ctx.guild.text_channels:
            await channel.send("⚠️ Server has been unlocked.", delete_after=60.0)

    @serverunlock.error
    async def serverunlock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            message = (f"🚫 This command requires you to either be an Admin or have the `Manage Channels` permission to use it.")
        await ctx.send(message, delete_after=5)

    @commands.command(help="Toggles commands", usage="<command>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def toggle(self, ctx, *, command):
        command = self.bot.get_command(command)

        if command is None:
            await ctx.send(f"No command called \"{command}\" found.")

        elif ctx.command == command:
            await ctx.send("This command cannot be disabled.")
        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send(f"**✅ {command.qualified_name} {ternary}!**")

    @toggle.error
    async def toggle_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            message = (f"🚫 This command requires you to have the `Administrator` permission to use it.")
            await ctx.send(message, delete_after=5)

def setup(bot):
    bot.add_cog(mod(bot))