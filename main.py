import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

my_secret = os.environ['TOKEN']

intents = discord.Intents().all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('*'), status=discord.Status.idle, activity=discord.Game(name='SLOWLY getting rewritten in Hikari ❤️'), intents=intents)
client.help_command = commands.MinimalHelpCommand()

@client.event
async def on_ready():
    print('Bot is ready.'.format(client))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        message = (f'Invalid arguments provided: Not enough arguments passed')
        await ctx.reply(message, delete_after=10)
    else:
        raise error

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        message = f"Looks like you've been doing that a lot. Take a break for **{round(error.retry_after)}s** before trying again. <:blobpainpats:903057516345303060>"
        await ctx.reply(message, delete_after=10)
    else:
        raise error

@client.command()
async def load(ctx, extension):
    client.load_extension(f"Cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")
    client.load_extension(f"Cogs.{extension}")


# -------------------------


@client.command()
@commands.is_owner()
async def rules(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/900458968588120154/916120630498299915/banner.png")
    embed = discord.Embed(
        description="**__Welcome to Sage!__**\n\nFirst and foremost, be very welcome to this community! Make yourself at home, we don’t bite. :))\n\nBelow you will find some cards with a bunch of important information on them about the rules in here. Make sure you read all of them! ;)\n\n**__General Rules__**\n\nIn order for things to be kept civil and intact, we enforce the following:",
    color=0xd9c2ae,
    )
    await ctx.send(embed=embed)
    
    embed = discord.Embed(
        title="📌 Discrimination and Hate",
        description=">>> • Discrimination against another person is not allowed. No person should be subjected to discrimination based on their beliefs, political views, religious or spiritual beliefs, race, ethnicity, sex, sexual orientation, gender, gender identity, physical or mental disability, gender expression, nationality/national origin, etc.",
    color=0xd9c2ae
    )
    await ctx.send(embed=embed)
    
    embed = discord.Embed(
        title="📌 Drama",
        description=">>> • Do not bring and/or start unnecessary drama in any of the channels. Keep it in DM’s and away from the server, no one wants to start a fight.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)
    
    embed = discord.Embed(
        title="📌 Advertising",
        description=">>> • Advertisements are not allowed. Do **__not__** promote your YouTube channel(s), Discord server(s), Twitch, or any other social media in this server or in DMs (Partners exempted. For more info regarding Partners, please refer to <#809215806323163136> and check the pins).",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)
    
    embed = discord.Embed(
        title="📌 Spam",
        description=">>> • Spam content should be kept in the appropriate channel (<#852067978173481010>).",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)


    embed = discord.Embed(
        title="📌 Profanity",
        description=">>> • Swearing is allowed as long as it doesn't offend anyone. This is a chill community so try keeping it that way.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = discord.Embed(
        title="📌 SFW PFPs and Usernames",
        description=">>> • Your profile picture and username/nickname must be SFW (Safe for Work). Inappropriate profile pictures or offensive usernames/nicknames that include illegal/NSFW or having slurs/harsh swears in your username/nickname or any special characters that might cause difficulty in pinging you are not allowed. Your name must be typeable on a standard QWERTY keyboard.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = discord.Embed(
        title="📌 Privacy & Safety",
        description=">>> • Do not scam or dox yourself/other people. Any attempt to scam or dox someone in any way, shape, or form will be severely reprimanded.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = discord.Embed(
        title="📌 NSFW Content",
        description=">>> • Just like your favorite ocean, let's keep it clean. No NSFW/sexually explicit content, sexually implicit content or language anywhere on this server.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = discord.Embed(
        title="📌 Appropriate Channels",
        description=">>> • Post in the appropriate channels. Read the channel topics or ask someone if you're confused.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = discord.Embed(
        title="📌 Basic Respect",
        description=">>> • Respect everyone. This server's goal is to provide a friendly community where you can learn, grow, and support one another so please try to contribute to it. That does not mean this server is subject to your definition of 'fairness'. You are entitled to your own opinion, but **do not** spread hate. What staff says goes, so don't try to evade any request done by us.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = discord.Embed(
        title="📌 Sensitive Topics",
        description=">>> • Add content warnings, trigger warnings, or spoil anything that could be potentially harmful or triggering to somebody. *For more info regarding this topic, please refer to <#809215806323163136> and check the pins.*\n\n🆘 If you are being abused, or in danger of harming yourself/others, please refer to the list of hotline/emergency numbers in <#796573173905752074> and seek help immediately as we are not trained professionals.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = discord.Embed(
        title="📌 Discord's ToS & Guidelines",
        description=">>> • Respect and follow Discord’s **[ToS](https://discord.com/terms)** and **[Guidelines](https://discord.com/guidelines)** at all times, breaching it will result in you getting an instant ban on this server and a report to Discord staff.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = discord.Embed(
        description=f"Not having read the rules will lead to punishment, and is no excuse.\n\nMisbehaving, rule-avoiding, and loopholing will lead to punishment. Punishments in this server vary from action to action. Once you've agreed with the rules, type *+agree* in the <#784967488139558942> channel but, **__try to evade them and you will not succeed.__**\n\n**__Privacy Notice__**\n\nBy speaking and remaining a member of this server, you acknowledge our tracking on some on your actions, such as message deletions, edits, and voice channel activity to aid in the moderation of this place. All this data is collected by an external service (<@242730576195354624>) which stores the information securely.\n\n**__Reporting Incidents__**\n\nIf you see someone breaking our rules, please send a direct message to <@690631795473121280> or <@575252669443211264> to help assist you with the situation. If it's really urgent, you can also ping the <@&794401582514962473> role in the channel where the incident is taking place.\n\nIf you've received an infraction and would like to appeal it, you can either contact <@690631795473121280>, <@575252669443211264>, or the <@&794401582514962473> team and we will try our best to be of assistance.",
        color=0xd9c2ae
        )
    await ctx.send(embed=embed)

# -------------------------------------

@client.command()
@commands.is_owner()
async def cl(ctx):
    embed = discord.Embed(
        title="↬ 𝐜𝐥𝐚𝐬𝐬𝐢𝐜𝐬",
        description="<:Carnelian:901342245251342347> ― <@&900810972665626655> \n<:GiantsOrange:901341397729292318> ― <@&900974678917660723> \n<:BananaYellow:901340502639673404> ― <@&900974872488996924> \n<:MayGreen:901344875679711242> ― <@&900975279546179584> \n<:BrandeisBlue:901345194316791829> ― <@&900975574942625812> \n<:PigmentBlue:901517835170353202> ― <@&901362959920541716> \n<:Grape:901345624493019187> ― <@&900975582626578442>",
        color=0xffffff
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/794455644329082880/901720665642635284/color_banner.png")
    await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def ps(ctx):
    embed = discord.Embed(
        title="↬ 𝐩𝐚𝐬𝐭𝐞𝐥𝐬"
    )
    await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def nn(ctx):
    embed = discord.Embed(
        title="↬ 𝐧𝐞𝐨𝐧𝐬"
    )
    await ctx.send(embed=embed)

for filename in os.listdir("./cogs"): 
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
    (f"cogs.{filename[:-3]}")
    
keep_alive()
client.run(my_secret)