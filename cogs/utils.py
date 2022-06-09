import os
import disnake
from disnake.ext import commands

import os
import json
import googletrans
from datetime import datetime
import asyncio
import requests
import io
import aiohttp
from io import BytesIO
from PIL import Image
from weather import *
from requests import get
from disnake import File, HTTPException, utils


my_secret = os.environ["WEATHER"]


class utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.img_ext = ("png", "jpg", "gif")
        self.bot.ses = aiohttp.ClientSession()

    @commands.command()
    async def weather(self, ctx, city: str):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        city_name = city
        complete_url = base_url + "appid=" + my_secret + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        channel = ctx.message.channel

        if x["cod"] != "404":
            y = x["main"]
            current_temp = y["temp"]
            current_temp_celsiuis = str(round(current_temp - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]

            embed = disnake.Embed(
                title=f"Weather in {city_name}",
                color=0x36393E,
                timestamp=datetime.utcnow(),
            )
            embed.add_field(
                name="Descripition", value=f"{weather_description}", inline=False
            )
            embed.add_field(
                name="Current Temperature",
                value=f"{current_temp_celsiuis}°C/",
                inline=False,
            )
            embed.add_field(
                name="Humidity(%)", value=f"**{current_humidity}%**", inline=False
            )
            embed.add_field(
                name="Atmospheric Pressure(hPa)",
                value=f"{current_pressure}hPa",
                inline=False,
            )
            embed.set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/commons/1/15/OpenWeatherMap_logo.png"
            )
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await channel.send(embed=embed)
        else:
            await channel.send("City not found.")

    @commands.command(
        aliases=["tr"],
        help="Translator. [Available languages](https://pastebin.com/6SPpG1ed)",
        usage="<language> <text>",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def translate(self, ctx, lang_to, *args):
        lang_to = lang_to.lower()
        if (
            lang_to not in googletrans.LANGUAGES
            and lang_to not in googletrans.LANGCODES
        ):
            pass

        text = " ".join(args)
        translator = googletrans.Translator()
        text_translated = translator.translate(text, dest=lang_to).text
        await ctx.send(text_translated)

    @commands.command(
        case_insensitive=True,
        aliases=["rem"],
        help="Sets a reminder",
        usage="<time> <reminder>",
    )
    async def remind(self, ctx, time, *, reminder):
        print(time)
        print(reminder)

        seconds = 0
        if reminder is None:
            await ctx.send(
                "Please specify what do you want me to remind you about.",
                delete_after=5,
            )

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
            await ctx.send(
                "Please specify a proper duration, type `*help remind` for more information.",
                delete_after=5,
            )
        elif seconds < 300:
            await ctx.send("The minimum duration is 5 minutes.", delete_after=5)
        elif seconds > 7776000:
            await ctx.send("The maximum duration is 90 days.", delete_after=5)
        else:
            embed = disnake.Embed(
                title="Reminder Set 🔔",
                description=f'Alright {ctx.author.name}, your reminder for "{reminder}" has been set and will end in {counter}.',
                color=ctx.author.color,
                timestamp=datetime.utcnow(),
            )
            await ctx.reply(embed=embed)
            await asyncio.sleep(seconds)

            embed = disnake.Embed(
                title="Reminder 🔔",
                description=f'Hi, you asked me to remind you about "{reminder}" {counter} ago.',
                color=0x2F3136,
                timestamp=datetime.utcnow(),
            )
            await ctx.author.send(embed=embed)
            return

    @commands.command(
        pass_context=True, help="Displays text in code format", usage="<text>"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def code(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send("```" + msg.replace("`", "") + "```")

    @commands.command(
        aliases=["qu"],
        help="Quotes a users' message using the message ID and/or channel ID",
        usage="[channel_id]-<message_id>",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def quote(self, ctx, msg: disnake.Message):
        embed = disnake.Embed(
            title="Message Link",
            url=f"{msg.jump_url}",
            description=f">>> {msg.content}",
            colour=msg.author.colour,
            timestamp=datetime.utcnow(),
        )
        embed.set_author(name=str(msg.author), icon_url=msg.author.avatar_url)
        embed.set_footer(
            text=f"Message quoted by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)

    @quote.error
    async def quote_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            message = f"🌿 This command cannot be used in Direct Messages"
        await ctx.send(message)

    @commands.command(
        aliases=["calc"], help="Calculator (e.g. 2+2)", usage="<equation>"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def calculate(self, ctx, expr):
        if "+" in expr:
            nums1, operation, nums2 = expr.partition("+")
            solution = int(nums1) + int(nums2)
        elif "-" in expr:
            nums1, operation, nums2 = expr.partition("-")
            solution = int(nums1) - int(nums2)
        elif "*" in expr:
            nums1, operation, nums2 = expr.partition("*")
            solution = int(nums1) * int(nums2)
        elif "/" in expr:
            nums1, operation, nums2 = expr.partition("/")
            solution = int(nums1) / int(nums2)
        else:
            await ctx.send("Please type a valid operation type.")
            return
        embed = disnake.Embed(title="Calculator", color=0xFFFFFF)
        embed.add_field(name="Input", value=f"```cpp\n{expr}\n```")
        embed.add_field(name="Output", value=f"```cpp\n{solution}\n```", inline=False)
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["color", "gc"],
        help="Displays color of specified hex code (you can add up to 10)",
        usage="<hex_code>",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def getcolor(self, ctx, *, colour_codes):
        colour_codes = colour_codes.split()
        size = (60, 80) if len(colour_codes) > 1 else (200, 200)
        if len(colour_codes) > 10:
            return await ctx.send(
                "You can only supply and maximum of **10** hex codes.", delete_after=5
            )

        for colour_code in colour_codes:
            if not colour_code.startswith("#"):
                colour_code = "#" + colour_code
            image = Image.new("RGB", size, colour_code)
            with io.BytesIO() as file:
                image.save(file, "PNG")
                file.seek(0)

                embed = disnake.Embed(
                    title=f"Color {colour_code}",
                    color=0x2F3136,
                    timestamp=datetime.utcnow(),
                )
                img = disnake.File(file, "Color.png")
                embed.set_image(url="attachment://Color.png")
                embed.set_footer(text=f"Requested by {ctx.author}")
                await ctx.send(embed=embed, file=img)
            await asyncio.sleep(1)

    @commands.command(
        aliases=["ae"], help="Creates an emoji", usage="<message_link> <emoji_name>"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def addemoji(self, ctx, link: str, name: str):
        guild = ctx.guild

        link_split = link.split("/")
        channel = guild.get_channel(int(link_split[5]))
        msg = await channel.fetch_message(int(link_split[6]))

        if msg.attachments:
            a = msg.attachments[0]
            r = get(a.url)
            img = r.content

            try:
                new_emoji = await guild.create_custom_emoji(
                    name=name,
                    image=img,
                    reason=f"Added by {ctx.author.name} via command",
                )

            except HTTPException as error:
                if "256.0 kb" in str(error):
                    return await ctx.edit_original_message(
                        content=f"Image file too large (Max: 256kb)"
                    )

                return await ctx.edit_original_message(
                    content=f"Error: Could not add custom emoji to this server"
                )

            return await ctx.edit_original_message(
                content=f"Custom emoji created: {new_emoji.name}"
            )

        await ctx.edit_original_message(
            content=f"Error: Link did not include a message that had a supported image"
        )

    @commands.command(aliases=["de"], help="Deletes an emoji", usage="<emoji_name>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deleteemoji(self, ctx, emoji: str):
        guild = ctx.guild

        emoji = utils.get(guild.emojis, name=emoji)

        if emoji:
            await guild.delete_emoji(
                emoji, reason=f"Deleted by {ctx.author.name} via command"
            )
            return await ctx.response.send_message(f"Target emoji deleted")

        await ctx.response.send_message(f"No emoji with that name was found")

    @commands.command(aliases=["d"], help="Defines a word", usage="<word>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def define(self, ctx, word):
        response = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{word}"
        )
        if response.status_code == 404:
            await ctx.reply(f'No word called "{word}" found.')
            return

        else:
            wordx = response.json()
            the_dictionary = wordx[0]
            meanings = the_dictionary["meanings"]
            definitions = meanings[0]
            definition = definitions["definitions"]
            meaningg = definition[0]
            meaning = meaningg["definition"]
            example = meaningg.get("example", "None")
            synlist = meaningg.get("synonyms", "None")

            if isinstance(synlist, str):
                synlist = synlist
            synlist = ", ".join(synlist)

            if not synlist:
                synlist = "None"

            async with ctx.typing():
                embed = disnake.Embed(
                    title=f"`{word.lower()}`",
                    color=ctx.author.color,
                    timestamp=datetime.utcnow(),
                )
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/900458968588120154/912960931284267068/oed_sharing.png"
                )
                embed.add_field(name="Definition:", value=f"{meaning}")
                embed.add_field(name="Example:", value=f'"{example}"', inline=False)
                embed.add_field(name="Synonyms:", value=f"`{synlist}`", inline=False)
                embed.set_footer(
                    text=f"Oxford Dictionaries: definition for {word.lower()}"
                )
                await ctx.send(embed=embed)

    @commands.command(
        aliases=["cin"],
        help="Creates an invite from a specified channel or the current channel",
        usage="[<#channel_id/mention]",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def createinvite(self, ctx, channel: disnake.TextChannel = None):
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


def setup(bot):
    bot.add_cog(utils(bot))
