import os
import discord
from discord.ext import commands

import praw
import random
from datetime import datetime, timedelta
from aiohttp import request
import asyncio
import typing
import emoji
from pyfiglet import Figlet
from Imps import text_to_owo
from Advice import responses
from Sites import sites
import io
import aiohttp

fig = Figlet(font='standard')
fig_small = Figlet(font='small')

def to_ascii(_input, small=False):
    if small:
        ascii_text = fig_small.renderText(_input)
    else:
        ascii_text = fig.renderText(_input)
    ascii_text = ascii_text.replace('```', '```')
    return'```\n' + ascii_text + '\n```'

    # Returns the random email and password based on Discord member's name
def login_generator(member):
    member = member.replace(" ", ".")
    domains = ['@aol.com', '@gmail.com', '@msn.com', '@hotmail.com',
               '@icloud.com', '@yahoo.com', '@aim.com', '@netscape.com']
    ran_email = ['hasASmallPeen', 'LovesBigButts', 'theFootFetishMaster', 'herpes_free_since_03', 'dildoSwaggins', 'PigBenis481933274', 'chillin_like_a_villiam_24', 'AssButt', 'ChynaIsHot', 'gl']
    email_full = member + random.choice(ran_email) + random.choice(domains)
    ran_password = random.choice(
        ['PASSWORD', '0123456', 'PA55W0RD', 'JESUSLOVESME', '244466666688888888', '111111', 'hArderDADDY6969', 'YamaDamaDiRingDikaDingDing', 'Punches_baby_pandas', 'peeinyourbutt', 'HardRock9inch', 'Turds3'])
 
    return email_full, ran_password
 
 
# Returns a random "common word" from a list of common words
def random_common_word():
    common_words = ['oop', 'yolo', 'sus', 'rat',
                    'no shot', 'random', 'nudes', 'peen', 'lol', 'lady']
    return random.choice(common_words)
 
 
# Random "Last message" from DM
def random_dm():
    messages = [
        'I hope nobody finds my nudes folder',
        'Honestly, I love the way my farts smell.'
        'You\'ll have to come over and checkout my e-girl bathwater collection.',
        'First of all, how dare you?',
        'What happens in Vegas, stays in Vegas.',
        'This one time at band camp...',
        'I hope blueballs aren\'t real.'
    ]
    return random.choice(messages)

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Checks how cool someone is", usage="[@member]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cool(self, ctx, member: discord.Member = None):
        if member:
            embed = discord.Embed(
                title="Cool Rate",
                description=f"{member.mention}, you are **{random.randrange(101)}%** cool! 😎",
                color=ctx.author.color
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Cool Rate",
                description=f"{ctx.author.mention}, you are **{random.randrange(101)}%** cool! 😎",
                color=ctx.author.color
            )
            await ctx.send(embed=embed)

    @commands.command(help="Checks how gay someone is", usage="[@member]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gay(self, ctx, member: discord.Member = None):
        if member:    
            embed = discord.Embed(
                title="Gay Rate",
                description=f"{member.mention}, you are **{random.randrange(101)}%** gay! 🏳️‍🌈",
                color=ctx.author.color
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Gay Rate",
                description=f"{ctx.author.mention}, you are **{random.randrange(101)}%** gay! 🏳️‍🌈",
                color=ctx.author.color
            )
            await ctx.send(embed=embed)

    @commands.command(help="Checks the size of someone's pp", usage="[@member]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pp(self, ctx, member: discord.Member = None):  
        pp = ['8D', '8=D', '8==D', '8===D', '8====D', '8=====D', '8======D', '8=======D', '8========D', '8=========D', '8==========D', '8===========D', '8============D', '8=============D']

        if member:
            embed = discord.Embed(
                title=f"{member}'s pp:",
                description=f"{random.choice(pp)}",
                color=ctx.author.color
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"Your pp:",
                description=f"{random.choice(pp)}",
                color=ctx.author.color
            )
            await ctx.send(embed=embed)

    @commands.command(name='ascii', help="Turns text to ascii", usage="<text>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _ascii(self, ctx, *, _input):
        ascii_text = to_ascii(_input)
        if len(ascii_text) < 2000:
            ascii_text = to_ascii(_input, True)
            if len(ascii_text) > 2000:
                await ctx.send('Error: Input is too long')
                return
            await ctx.send(ascii_text)

    @commands.command(name='8ball', help="Wisdom. Ask a question and the bot will give you an answer", usage="<question>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes – definitely.', 'You may rely on it.', 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', 'Don’t count on it.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
        await ctx.send(f'{random.choice(responses)}')

    @commands.command(help="Turns text to owo (e.g. hewwo)", usage="<text>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def owo(self, ctx, *, sentence):
        await ctx.send(text_to_owo(sentence))

    @commands.command(help="Don't be afraid to ask for advice!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def advice(self, ctx):
        await ctx.send(f'{random.choice(responses)}')

    @commands.command(help="Displays a random meme from Reddit")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx):
        reddit = praw.Reddit(client_id = "giMGsy3IEHdBx1eFEcobIg",
        client_secret = "2f8bSSJMOMGIp7Eo4d63y_uygVMAJg",
        user_agent = "praw123")

        memes_submissions = reddit.subreddit("memes").hot()
        post_to_pick = random.randint(1, 50)
        await ctx.send("Loading meme...", delete_after=3)

        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        async with ctx.typing():
            embed = discord.Embed(
                title=submission.title,
                color=discord.Colour.random(),
                timestamp=datetime.utcnow()
            )
            embed.set_image(url=submission.url)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text="Here is your meme!")
            await ctx.send(embed=embed)

    @commands.command(help="Repeats given text for x amount of times", usage="<amount> <text>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def repeat(self, ctx, amount: int, content="repeating..."):
        for i in range(amount):
            await ctx.send(content)

    @commands.command(aliases=['mock', 'dr'], help="Mocks given text (e.g. HahAhA)", usage="<text>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def drunkify(self, ctx, *, s):
        lst = [str.upper, str.lower]
        newText = await commands.clean_content().convert(ctx, ''.join(random.choice(lst)(c) for c in s))
        if len(newText) <= 380:
            await ctx.send(newText)
        else:
            try:
                await ctx.author.send(newText)
                await ctx.reply(f"The input was too large, so I sent it to your DMs!")
            except Exception:
                await ctx.reply(f"Something went wrong! The message may be too large or be malformed.")

    @commands.command(help="DMs given user through the bot", usage="<user_id> <text>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def dm(self, ctx, user_id=None, args=None):
        if user_id != None and args != None:
            try:
                target = await self.client.fetch_user(user_id)
                await target.send(args)

                await ctx.channel.send("Your message has been sent to the given user!")

            except:
                await ctx.channel.send("Something went wrong! I cannot DM the given user :(")

        else:
            await ctx.channel.send("A `user_id` and/or messages were not included.")

    @dm.error
    async def dm_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            message = (f"🌿 This command cannot be used in Direct Messages")
        await ctx.send(message)

    @commands.command(name='dmall', aliases=['dma'], help="DMs every user in the server through the bot", usage="<text>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def dm_all(self, ctx, *, args=None):
        if args != None:
            members = ctx.guild.members
            for member in members:
                try:
                    await member.send(args)
                    await ctx.send("Your message has been sent to everyone!")

                except:
                    await ctx.send("Something went wrong! I couldn't send the message :(")

    @dm_all.error
    async def dm_all_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            message = (f"🌿 This command cannot be used in Direct Messages")
        await ctx.send(message)
    
    @commands.command(aliases=['roll'], help="Roll dices (e.g. 2d1)", usage="<dice>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rolldice(self, ctx, dice: str):
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(f"🎲 **{rolls}** ({result})")

    @commands.command(aliases=['cf'], help="Flip a coin!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coinflip(self, ctx):
        choices = ["Heads!", "Tails!"]
        rancoin = random.choice(choices)
        await ctx.send(rancoin)

    @commands.command(aliases=['rev'], help="Reverses text", usage="<text>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def reverse(self, ctx, *, text: str):
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(t_rev)
      
    @commands.command(aliases=['ava'], help="Displays your/a user's profile picture", usage="[@user/user_id]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed(
            title=f"{member}'s Avatar",
            color=0x000100,
            timestamp=datetime.utcnow()
        )
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            message = (f"🌿 This command cannot be used in Direct Messages")
        await ctx.send(message)
     
    @commands.command(aliases=['jumbo'], help="Enlarges a specified emoji", usage="<emoji>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def enlarge(self, ctx, emoji: typing.Union[discord.Emoji, discord.PartialEmoji, str]):
        if type(emoji) is str:
            emoji_id = ord(emoji[0])
            await ctx.send(f'https://twemoji.maxcdn.com/v/latest/72x72/{emoji_id:x}.png')
        else:
            await ctx.send(emoji.url)
      
    @commands.command(aliases=['fact'], help="Random animal facts for dogs, cats, pandas, foxes, birds, and koalas", usage="<animal>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def animalfact(self, ctx, animal: str):
        if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", ":koala"):
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"
            message = ("Loading fact...")
            await ctx.send(message, delete_after=3)
            
            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]
            
                else:
                    image_link = None
            
            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                async with ctx.typing():
                    embed = discord.Embed(
                        title=f"{animal.title()} Fact",
                        description=data["fact"],
                        colour=ctx.author.colour,
                        timestamp=datetime.utcnow()
                    )
                    if image_link is not None:
                        embed.set_image(url=image_link)
                        await ctx.send(embed=embed)
              
                    else:
                        await ctx.send(f"API returned a {response.status} status.")
            
    @commands.command(aliases=['uls'], help="Gives you a random/useless website")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def useless(self, ctx): 
        randomsite = random.choice(sites)  
        embed = discord.Embed(
            title="Here's your useless website:",
            description=f"🌐 {randomsite}",
            colour=discord.Colour.random()
        )
        await ctx.send(embed=embed)

    @commands.command(help='Displays an image of a bird')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bird(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/bird')
            dogjson = await request.json()
            request2 = await session.get('https://some-random-api.ml/facts/bird')
            factjson = await request2.json()
            
        embed = discord.Embed(title="Have a cool bird!",colour=ctx.author.colour)
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    @commands.command(help='Displays an image of a fox')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fox(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/fox')
            dogjson = await request.json()
            request2 = await session.get('https://some-random-api.ml/img/fox')
            factjson = await request2.json()
            
        embed = discord.Embed(title="Have a cute fox!", colour=ctx.author.colour)
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    @commands.command(help='Displays an image of a panda')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def panda(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/panda')
            dogjson = await request.json()
            request2 = await session.get('https://some-random-api.ml/img/panda')
            factjson = await request2.json()
            
        embed = discord.Embed(title="Have a nice panda!", colour=ctx.author.colour)
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    @commands.command(help='Displays an image of a cat')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/cat')
            dogjson = await request.json()
            request2 = await session.get('https://some-random-api.ml/img/cat')
            factjson = await request2.json()
            
        embed = discord.Embed(title="Have a cute cat!", colour=ctx.author.colour)
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    @commands.command(help='Displays an image of a dog')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/dog')
            dogjson = await request.json()
            request2 = await session.get('https://some-random-api.ml/img/dog')
            factjson = await request2.json()
            
        embed = discord.Embed(title="Have a cute dog!", colour=ctx.author.colour)
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    @commands.command(help='Displays an image of a koala')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def koala(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/koala')
            dogjson = await request.json()
            request2 = await session.get('https://some-random-api.ml/img/koala')
            factjson = await request2.json()

        embed = discord.Embed(title="Have a cuddly koala!", colour=ctx.author.colour)
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    @commands.command(aliases=['kang'], help='Displays an image of a kangaroo')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kangaroo(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/kangaroo')
            dogjson = await request.json()
            request2 = await session.get('https://some-random-api.ml/facts/kangaroo')
            factjson = await request2.json()

        embed = discord.Embed(title="Have a nice kangaroo!", colour=ctx.author.colour)
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    @commands.command(aliases=['rac'], help='Displays an image of a raccoon')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def raccoon(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/raccoon')
            dogjson = await request.json()
            request2 = await session.get('https://some-random-api.ml/facts/raccoon')
            factjson = await request2.json()

        embed = discord.Embed(title="Have a cool raccoon!", colour=ctx.author.colour)
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    @commands.command(name='redpanda', aliases=['rpan'], help='Displays an image of a red panda')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def Red_panda(self, ctx):
        async with  aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/red_panda')
            dogjson = await request.json()
            request2 = await session.get('https://some-random-api.ml/img/red_panda')
            factjson = await request2.json()

        embed = discord.Embed(title="Have a fluffy red panda!", colour=ctx.author.colour)
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)
 
    @commands.command(name='hack', help="\"hacks\" a member")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hacker_man(self, ctx, member: discord.Member):
        ran_sleep = random.uniform(1.75, 2.25)
        email, password = login_generator(member.name)
        friends = random.randint(0, 1)
        _dm = random_dm()
        common_word = random_common_word()
        member_disc = str(member.discriminator)
        random_port = random.randint(1123, 8686)
        random_subnet = random.choice(('192.168.0.', '192.168.1.', '192.168.2.'))
        random_ip = random.randint(0, 254)
    
        msg = await ctx.send(f'Hacking {member.name} now...')
    
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        await msg.edit(content='Finding discord login... (2fa bypassed)')
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        await msg.edit(content=f'Found login info...\n**Email**: `{email}`\n**Password**: `{password}`')
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        await msg.edit(content=f'Fetching DMs with closest friends (if there are any friends at all)...')
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        if friends == 0:
            await msg.edit(content=f'No DMs found.')
        else:
            await msg.edit(content=f'DMs found...\n**Last DM**: "{_dm}"')
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        await msg.edit(content='Finding most common word...')
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        await msg.edit(content=f'Most common word = "{common_word}"')
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        await msg.edit(content=f'Injecting trojan virus into member discriminator: #{member_disc}')
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        await msg.edit(content='Setting up Epic Store account...')
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        await msg.edit(content='Hacking Epic Store account...')
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        await msg.edit(content='Finding IP address...')
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        await msg.edit(content=f'IP Address Found!\n**IP address**: {random_subnet}{random_ip}:{random_port}')
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        await msg.edit(content='Reporting account to Discord for breaking TOS...')
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        await msg.edit(content='Hacking medical records...')
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        await msg.edit(content='Selling member\'s data to the Governement...')
        async with ctx.typing():
            await asyncio.sleep(ran_sleep)
        await msg.edit(content=f'Finished hacking {member.name}!')
        await ctx.send('The *totally* real and **dangerous** hack is complete.')


def setup(client):
    client.add_cog(Fun(client))