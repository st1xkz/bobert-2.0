import discord
from discord.ext import commands

import os
import googletrans
from datetime import datetime
import asyncio
import requests
import io
import aiohttp
from io import BytesIO
from PIL import Image

class utils(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.client.ses = aiohttp.ClientSession()

    @commands.command(aliases=['tr'], help="Translator. [Available languages](https://pastebin.com/6SPpG1ed)", usage="<language> <text>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def translate(self, ctx, lang_to, *args):
        lang_to = lang_to.lower()
        if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
            pass
        
        text = ' '.join(args)
        translator = googletrans.Translator()
        text_translated = translator.translate(text, dest=lang_to).text
        await ctx.send(text_translated)

    @commands.command(case_insensitive=True, aliases = ['rem'], help="Sets a reminder", usage="<time> <reminder>")
    async def remind(self, ctx, time, *, reminder):
        print(time)
        print(reminder)

        seconds = 0
        if reminder is None:
            await ctx.send("Please specify what do you want me to remind you about.", delete_after=5)

        if time.lower().endswith("d"):
            seconds += int(time[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} days"
        if time.lower().endswith("h"):
            seconds += int(time[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hours"
        elif time.lower().endswith("m"):
            seconds += int(time[:-1]) * 60
            counter = f"{seconds // 60} minutes"
        elif time.lower().endswith("s"):
            seconds += int(time[:-1])
            counter = f"{seconds} seconds"

        if seconds == 0:
            await ctx.send("Please specify a proper duration, type `*help remind` for more information.", delete_after=5)
        elif seconds < 300:
            await ctx.send("The minimum duration is 5 minutes.", delete_after=5)
        elif seconds > 7776000:
            await ctx.send("The maximum duration is 90 days.", delete_after=5)
        else:
            embed = discord.Embed(
                title="Reminder Set 🔔",
                description=f"Alright {ctx.author.name}, your reminder for \"{reminder}\" has been set and will end in {counter}.",
                color=ctx.author.color,
                timestamp=datetime.utcnow()
            )
            await ctx.reply(embed=embed)
            await asyncio.sleep(seconds)

            embed = discord.Embed(
                title="Reminder 🔔",
                description=f"Hi, you asked me to remind you about \"{reminder}\" {counter} ago.",
                color=0x2f3136,
                timestamp=datetime.utcnow()
            )
            await ctx.author.send(embed=embed)
            return
        
    @commands.command(pass_context=True, help="Displays text in code format", usage="<text>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def code(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send("```" + msg.replace("`", "") + "```")
        
    @commands.command(aliases=['qu'], help="Quotes a users' message using the message ID and/or channel ID", usage="[channel_id]-<message_id>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def quote(self, ctx, msg: discord.Message):
        embed = discord.Embed(
            title="Message Link",
            url=f"{msg.jump_url}",
            description=f">>> {msg.content}",
            colour=msg.author.colour,
            timestamp=datetime.utcnow()
            )
        embed.set_author(name=str(msg.author), icon_url=msg.author.avatar_url)
        embed.set_footer(text=f"Message quoted by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @quote.error
    async def quote_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            message = (f"🌿 This command cannot be used in Direct Messages")
        await ctx.send(message)

    @commands.command(aliases=['calc'], help="Calculator (e.g. 2+2)", usage="<equation>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def calculate(self, ctx, expr):
        if "+" in expr:
            nums1, operation, nums2 = expr.partition("+")
            solution = int(nums1)+int(nums2)
        elif "-" in expr:
            nums1, operation, nums2 = expr.partition("-")
            solution = int(nums1)-int(nums2)
        elif "*" in expr:
            nums1, operation, nums2 = expr.partition("*")
            solution = int(nums1)*int(nums2)
        elif "/" in expr:
            nums1, operation, nums2 = expr.partition("/")
            solution = int(nums1)/int(nums2)
        else:
            await ctx.send('Please type a valid operation type.')
            return
        embed = discord.Embed(
            title="Calculator",
            color=0xffffff
        )
        embed.add_field(name="Input", value=f"```cpp\n{expr}\n```")
        embed.add_field(name="Output", value=f"```cpp\n{solution}\n```", inline=False)
        await ctx.send(embed=embed)
        
    @commands.command(pass_context=True, aliases=['color', 'gc'], help="Displays color of specified hex code (you can add up to 10)", usage="<hex_code>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def getcolor(self, ctx, *, colour_codes):
        colour_codes = colour_codes.split()
        size = (60, 80) if len(colour_codes) > 1 else (200, 200)
        if len(colour_codes) > 10:
            return await ctx.send("You can only supply and maximum of **10** hex codes.", delete_after=5)
            
        for colour_code in colour_codes:
            if not colour_code.startswith("#"):
                colour_code = "#" + colour_code
            image = Image.new("RGB", size, colour_code)
            with io.BytesIO() as file:
                image.save(file, "PNG")
                file.seek(0)

                embed = discord.Embed(
                    title=f"Color {colour_code}",
                color=0x2f3136,
                timestamp=datetime.utcnow()
                )
                img = discord.File(file, "Color.png")
                embed.set_image(url="attachment://Color.png")
                embed.set_footer(text=f"Requested by {ctx.author}")
                await ctx.send(embed=embed, file=img)
            await asyncio.sleep(1)

    @commands.command(aliases=['ce'], help="Creates a custom emoji", usage="<media_file> <name>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def createemoji(self, ctx, url: str, *, name):
        async with self.client.ses.get(url) as r:
            try:
                if r.status in range(200, 299):
                    img = BytesIO(await r.read())
                    bytes = img.getvalue()
                    emoji = await ctx.guild.create_custom_emoji(image=bytes, name=name)
                    await ctx.send(f"Successfully created emoji: <:{emoji.name}:{emoji.id}>")

                else:
                    await ctx.send(f"Error occurred when making request: {r.status}")
            except discord.HTTPException:
                embed = discord.Embed(
                    title="Something went wrong",
                    description="Please make sure you have no spaces when naming your emoji, you have the correct file link, and the file size isn't too big. You can upload your emoji up to 128x128 pixels (256kb) but Discord resizes it to 32x32.",
                    color=0xFF4040,
                    timestamp=datetime.utcnow()
                )
                await ctx.send(embed=embed)

    @commands.command(aliases=['de'], help="Deletes specified emoji", usage="<emoji>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deleteemoji(self, ctx, emoji: discord.Emoji):
        if ctx.author.guild_permissions.manage_emojis:
            await ctx.send(f"Successfully deleted emoji: {emoji}")
            await emoji.delete()

    @commands.command(aliases=['d'], help="Defines a word", usage="<word>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def define(self, ctx, word):
        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en_US/{word}')
        if response.status_code == 404:
            await ctx.reply(f"No word called \"{word}\" found.")
            return

        else:
            wordx = response.json()
            the_dictionary = wordx[0]
            meanings = the_dictionary['meanings']
            definitions = meanings[0]
            definition = definitions['definitions']
            meaningg = definition[0]
            meaning = meaningg['definition']
            example = meaningg.get('example', 'None')
            synlist = meaningg.get('synonyms', 'None')

            if isinstance(synlist, str):
                synlist = (synlist)
            synlist = ', '.join(synlist)

            if not synlist:
                synlist = "None"

            async with ctx.typing():
                embed = discord.Embed(
                        title=f"`{word.lower()}`",
                        color=ctx.author.color,
                        timestamp=datetime.utcnow()
                    )
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/900458968588120154/912960931284267068/oed_sharing.png")
                embed.add_field(name="Definition:", value=f"{meaning}")
                embed.add_field(name="Example:", value=f"\"{example}\"", inline=False)
                embed.add_field(name="Synonyms:", value=f"`{synlist}`", inline=False)
                embed.set_footer(text=f"Oxford Dictionaries: definition for {word.lower()}")
                await ctx.send(embed=embed)

    @commands.command(aliases=['cin'], help="Creates an invite from a specified channel or the current channel", usage="[<#channel_id/mention]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def createinvite(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel
        invite = await channel.create_invite(max_age=0, max_uses=0)
        message = await ctx.send("Creating your invite link...")
        async with ctx.typing():
            await asyncio.sleep(3)
            await message.edit(content="Setting the duration...")
        async with ctx.typing():
            await asyncio.sleep(5)
            await message.edit(content="Almost got it...")  
        async with ctx.typing():
            await asyncio.sleep(5)
            await message.edit(content=f"**Done!** Here's your invite: {invite}")
            return

            
def setup(client):
    client.add_cog(utils(client))