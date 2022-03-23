import os
import disnake
from disnake.ext import commands
from keep_alive import keep_alive

my_secret = os.environ['TOKEN']

intents = disnake.Intents().all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('*'), status=disnake.Status.idle, activity=disnake.Game(name='SLOWLY getting rewritten in Hikari ❤️'), intents=intents)
bot.help_command = commands.MinimalHelpCommand()

@bot.event
async def on_ready():
    print('Bot is ready.'.format(bot))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        message = (f'Invalid arguments provided: Not enough arguments passed')
        await ctx.reply(message, delete_after=10)
    else:
        raise error

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        message = f"Looks like you've been doing that a lot. Take a break for **{round(error.retry_after)}s** before trying again. <:blobpainpats:903057516345303060>"
        await ctx.reply(message, delete_after=10)
    else:
        raise error

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"Cogs.{extension}")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"Cogs.{extension}")

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f"Cogs.{extension}")
    bot.load_extension(f"Cogs.{extension}")


# -------------------------


@bot.command()
async def rules(ctx):
    await ctx.message.delete()
    await ctx.send("https://cdn.discordapp.com/attachments/900458968588120154/916120630498299915/banner.png")
    embed = disnake.Embed(
        description="**__Welcome to Sage!__**\n\nFirst and foremost, be very welcome to this community! Make yourself at home, we don’t bite. :))\n\nBelow you will find some cards with a bunch of important information on them about the rules in here. Make sure you read all of them! ;)\n\n**__General Rules__**\n\nIn order for things to be kept civil and intact, we enforce the following:",
    color=0xd9c2ae,
    )
    await ctx.send(embed=embed)
    
    embed = disnake.Embed(
        title="📌 Discrimination and Hate",
        description=">>> • Discrimination against another person is not allowed. No person should be subjected to discrimination based on their beliefs, political views, religious or spiritual beliefs, race, ethnicity, sex, sexual orientation, gender, gender identity, physical or mental disability, gender expression, nationality/national origin, etc.",
    color=0xd9c2ae
    )
    await ctx.send(embed=embed)
    
    embed = disnake.Embed(
        title="📌 Drama",
        description=">>> • Do not bring and/or start unnecessary drama in any of the channels. Keep it in DM’s and away from the server, no one wants to start a fight.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)
    
    embed = disnake.Embed(
        title="📌 Advertising",
        description=">>> • Advertisements are not allowed. Do **__not__** promote your YouTube channel(s), Discord server(s), Twitch, or any other social media in this server or in DMs (Partners exempted. For more info regarding Partners, please refer to <#809215806323163136> and check the pins).",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)
    
    embed = disnake.Embed(
        title="📌 Spam",
        description=">>> • Spam content should be kept in the appropriate channel (<#852067978173481010>).",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)


    embed = disnake.Embed(
        title="📌 Profanity",
        description=">>> • Swearing is allowed as long as it doesn't offend anyone. This is a chill community so try keeping it that way.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = disnake.Embed(
        title="📌 SFW PFPs and Usernames",
        description=">>> • Your profile picture and username/nickname must be SFW (Safe for Work). Inappropriate profile pictures or offensive usernames/nicknames that include illegal/NSFW or having slurs/harsh swears in your username/nickname or any special characters that might cause difficulty in pinging you are not allowed. Your name must be typeable on a standard QWERTY keyboard.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = disnake.Embed(
        title="📌 Privacy & Safety",
        description=">>> • Do not scam or dox yourself/other people. Any attempt to scam or dox someone in any way, shape, or form will be severely reprimanded.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = disnake.Embed(
        title="📌 NSFW Content",
        description=">>> • Just like your favorite ocean, let's keep it clean. No NSFW/sexually explicit content, sexually implicit content or language anywhere on this server.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = disnake.Embed(
        title="📌 Appropriate Channels",
        description=">>> • Post in the appropriate channels. Read the channel topics or ask someone if you're confused.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = disnake.Embed(
        title="📌 Basic Respect",
        description=">>> • Respect everyone. This server's goal is to provide a friendly community where you can learn, grow, and support one another so please try to contribute to it. That does not mean this server is subject to your definition of 'fairness'. You are entitled to your own opinion, but **do not** spread hate. What staff says goes, so don't try to evade any request done by us.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = disnake.Embed(
        title="📌 Sensitive Topics",
        description=">>> • Add content warnings, trigger warnings, or spoil anything that could be potentially harmful or triggering to somebody. *For more info regarding this topic, please refer to <#809215806323163136> and check the pins.*\n\n🆘 If you are being abused, or in danger of harming yourself/others, please refer to the list of hotline/emergency numbers in <#796573173905752074> and seek help immediately as we are not trained professionals.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = disnake.Embed(
        title="📌 Discord's ToS & Guidelines",
        description=">>> • Respect and follow Discord’s **[ToS](https://discord.com/terms)** and **[Guidelines](https://discord.com/guidelines)** at all times, breaching it will result in you getting an instant ban on this server and a report to Discord staff.",
        color=0xd9c2ae
    )
    await ctx.send(embed=embed)

    embed = disnake.Embed(
        description=f"Not having read the rules will lead to punishment, and is no excuse.\n\nMisbehaving, rule-avoiding, and loopholing will lead to punishment. Punishments in this server vary from action to action. Once you've agreed with the rules, type *+agree* in the <#784967488139558942> channel but, **__try to evade them and you will not succeed.__**\n\n**__Privacy Notice__**\n\nBy speaking and remaining a member of this server, you acknowledge our tracking on some on your actions, such as message deletions, edits, and voice channel activity to aid in the moderation of this place. All this data is collected by an external service (<@242730576195354624>) which stores the information securely.\n\n**__Reporting Incidents__**\n\nIf you see someone breaking our rules, please create a ticket in the <#825445726783668234> channel to be able to directly talk to staff. If it's really urgent, you can also ping the <@&794401582514962473> role in the channel where the incident is taking place.\n\nIf you've received an infraction and would like to appeal it, you can either contact <@690631795473121280>, or create a ticket in the <#825445726783668234> channel and we will try our best to be of assistance.",
        color=0xd9c2ae
        )
    await ctx.send(embed=embed)

# -------------------------------------

@bot.command()
async def cl(ctx):
    await ctx.message.delete()
    embed = disnake.Embed(
        title="↬ 𝐜𝐥𝐚𝐬𝐬𝐢𝐜𝐬",
        description="<:Carnelian:930323208299761665> ― <@&900810972665626655> \n<:GiantsOrange:930323381071527978> ― <@&900974678917660723> \n<:BananaYellow:930323642859008041> ― <@&900974872488996924> \n<:MayGreen:930323861164154981> ― <@&900975279546179584> \n<:BrandeisBlue:930324050302074880> ― <@&900975574942625812> \n<:PigmentBlue:930324540620419112> ― <@&901362959920541716> \n<:Grape:930324381639520266> ― <@&900975582626578442>",
        color=0xffffff
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/794455644329082880/901720665642635284/color_banner.png")
    await ctx.send(embed=embed)

@bot.command()
async def ps(ctx):
    await ctx.message.delete()
    embed = disnake.Embed(
        title="↬ 𝐩𝐚𝐬𝐭𝐞𝐥𝐬",
        description="<:PastelRed:930262802571079740> ― <@&927730216502190090>\n<:CongoPink:930263463857635348> ― <@&927730535063760926>\n<:LightOrange:930264442585894982> ― <@&927731235042787369>\n<:VeryPaleYellow:930264608168607884> ― <@&927731254827290694>\n<:PastelYellow:930264794945159250> ― <@&927732145756184606>\n<:TeaGreen:930265184164012073> ― <@&927732779582652436>\n<:GrannySmithApple:930265369644498984> ― <@&927733066334634015>\n<:AeroBlue:930265983833243678> ― <@&927735721106743377>\n<:BlizzardBlue:930266881858891856> ― <@&927735736499863552>\n<:LightBlue:930267518080258078> ― <@&927735874945445919>\n<:PaleLavender:930268004837638204> ― <@&927736512819396631>\n<:Soap:930268226582093854> ― <@&927736793640620072>\n<:Wisteria:930268700773322762> ― <@&927737212789981224>",
        color=0xddf2ff
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/870013765683392544/933254901738397726/pastels.png")
    await ctx.send(embed=embed)

@bot.command()
async def nn(ctx):
    await ctx.message.delete()
    embed = disnake.Embed(
        title="↬ 𝐧𝐞𝐨𝐧𝐬",
        description="<:ElectricRed:937127075909873695> ―\n<:Red:937128993805725746> ―\n<:Coquelicot:937131406566514698> ―\n<:VividOrange:937132150845759529> ―\n<:MiddleYellow:937132738564223017> ―\n<:Yellow:937133280195641404> ―\n<:BrightGreen:937133888042569758> ―\n<:ElectricGreen:937134276602900502> ―\n<:Aqua:937134612918980648> ―\n<:Blue:937134949746749440> ―\n<:NeonBlue:937135237484412938> ―\n<:BrightPink:937135626187309087> ―\n<:ElectricPurple:937136102786097222> ―",
        color=0x0017ff
    )
    await ctx.send(embed=embed)

@bot.command()
async def dk(ctx):
    await ctx.message.delete()
    embed = disnake.Embed(
        title="↬ 𝐝𝐚𝐫𝐤𝐬",
        description="<:DarkScarlet:937162768283471963> ―\n<:BloodRed:937163475929690194> ―\n<:Sepia:937163802586251345> ―\n<:Mahogany:937164841314058261> ―\n<:DarkYellow:937165319330488371> ―\n<:DarkGreen:937166100943228968> ―\n<:ForestGreen:937166983575773235> ―\n<:CatalinaBlue:937168789328494592> ―\n<:CosmicCobalt:937169717133717514> ―\n<:LapisLazuli:937170062920544296> ―\n<:CyberGrape:937173198821277697> ―\n<:AmericanPurple:937174190363115590> ―",
        color=0x540011
    )
    await ctx.send(embed=embed)

@bot.command()
async def notifs(ctx):
    await ctx.message.delete()
    embed = disnake.Embed(
        title="Notifications",
        description="updates (📰) - pings about updates relating to the server\nevents (🎊) - pings that notify you when we are hosting an event\nannouncements (📣) - pings that notify you when we make an announcement",
        color=0xea4544
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/900458968588120154/947268239552045087/notifications.png")
    await ctx.send(embed=embed)


for filename in os.listdir("./cogs"): 
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
    (f"cogs.{filename[:-3]}")
    
keep_alive()
bot.run(my_secret)