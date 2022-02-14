import disnake
from disnake.ext import commands

from datetime import datetime
from random import randint

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['mc'], help="Displays how many members are in the server")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def membercount(self, ctx):
	    a = ctx.guild.member_count
	    embed = disnake.Embed(title=f"members in {ctx.guild.name}", description=a, color=randint(0, 0xffffff))
	    await ctx.send(embed=embed)

    @membercount.error
    async def membercount_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            message = (f"🌿 This command cannot be used in Direct Messages")
        await ctx.send(message)

    @commands.command(aliases=['cetde'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def creationdate(self, ctx):
        bot = self.bot.get_user(836109275016462396)
        creationDate = bot.created_at.strftime("%a %#d %B %Y, %I:%M %p")
        await ctx.send(f"Creation Date: **{creationDate}**")
      
    @commands.command(aliases=['server', 'srv'], help="Displays server info")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def serverinfo(self, ctx):
        total_categories = len(ctx.guild.categories)
        total_text_channels = len(ctx.guild.text_channels)
        total_voice_channels = len(ctx.guild.voice_channels)
        total_chan_and_cat = total_text_channels  + total_voice_channels + total_categories
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]
      
        embed = disnake.Embed(
            color=0x2f3136,
            title='Server Information',
            description=str(ctx.guild.description),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=f"{ctx.guild.icon.url}")
        embed.add_field(name='Name', value=f"{ctx.guild.name}")
        embed.add_field(name='Region', value=f"{ctx.guild.region}")
        embed.add_field(name='Owner', value=f"{ctx.guild.owner.mention}")
        embed.add_field(name='Member Count', value=f"{ctx.guild.member_count}")
        embed.add_field(name='Channel and Category Count', value=total_chan_and_cat)
        embed.add_field(name='Role Count', value=len(ctx.guild.roles))
        embed.add_field(name='Emoji Count', value=len(ctx.guild.emojis))
        embed.add_field(name='Total Invites', value=len(await ctx.guild.invites()))
        embed.add_field(name='Bots', value=', '.join(list_of_bots), inline=False)
        embed.add_field(name='Creation Date', value=ctx.guild.created_at.strftime(f"%a, %#d %B %Y @ %H:%M:%S %p"))
        embed.add_field(name='Verification Level', value=str(ctx.guild.verification_level))
        embed.add_field(name='Default Message Notifications', value='All Messages' if ctx.guild.default_notifications is disnake.NotificationLevel.all_messages else 'Only_mentions')
        embed.add_field(name='Explicit Content Filter', value=str(ctx.guild.explicit_content_filter))
        embed.add_field(name='Total Boosts', value=f"{ctx.guild.premium_subscription_count}")
        embed.add_field(name='Boost Tier', value=f"{ctx.guild.premium_tier}")
        embed.set_footer(text=f'Guild ID: {ctx.message.guild.id}', avatar_url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    @serverinfo.error
    async def serverinfo_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            message = (f"🌿 This command cannot be used in Direct Messages")
            await ctx.send(message)

    @commands.command(aliases=['user', 'whois'], help="Displays given users' info", usage="<@user/user_id>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def userinfo(self, ctx, *, member: disnake.Member = None):
        if member == None:
            member = ctx.message.author
            
        embed = disnake.Embed(
            title="User Information", 
            timestamp=datetime.utcnow(),
            colour=ctx.author.colour
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Name", value=member.name+"#"+member.discriminator)
        embed.add_field(name="Nickname", value=member.nick)
        embed.add_field(name="Bot?", value=member.bot)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Account Created",value=member.created_at.strftime("%a %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined",value=member.joined_at.strftime("%a %#d %B %Y, %I:%M %p UTC"))
        if len(member.roles) > 1:
                role_string = ', '.join([role.mention for role in member.roles][1:])
                embed.add_field(name="Roles [{}]".format(len(member.roles)-1), value=role_string, inline=False)
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join Position", value=str(members.index(member)+1))
        embed.add_field(name="Status", value=member.status)
        embed.add_field(name="Activity", value=f"{str(member.activity.type).split('.')[-1].title() if member.activity else 'N/A'} {member.activity.name if member.activity else ''}")
        embed.add_field(name="Boosted", value=bool(member.premium_since))
        embed.set_footer(text=f'Requested by {ctx.author}', avatar_url=member.avatar.url)
        await ctx.send(embed=embed)
        
    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            message = (f"🌿 This command cannot be used in Direct Messages")
        await ctx.send(message)
    

def setup(bot):
    bot.add_cog(info(bot))