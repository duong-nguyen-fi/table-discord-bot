import discord
from discord.ext import commands
import texttable

# IMPORT THE OS MODULE.
import os

# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
from dotenv import load_dotenv

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Prefix for bot commands
#bot = commands.Bot(command_prefix='/')
#bot = discord.Client(intents=discord.Intents.default())
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="<" , intents=intents)
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    guild_count = 0

    # LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
    for guild in bot.guilds:
        # PRINT THE SERVER'S ID AND NAME.
        print(f"- {guild.id} (name: {guild.name})")

        # INCREMENTS THE GUILD COUNTER.
        guild_count = guild_count + 1

    # PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the message starts with '/table'
    if message.content.startswith('/table'):
        # Extract the content after '/table'
        content = message.content[len('/table'):].strip()

        # Parse the content into rows
        rows = [line.strip().split(':') for line in content.split('\n')]

        # Convert Markdown table to ASCII table
        ascii_table = markdown_to_ascii(rows)

        # Reply with the ASCII table
        await message.channel.send('```\n' + ascii_table + '```')

    await bot.process_commands(message)


def markdown_to_ascii(rows):
    # Convert Markdown table to ASCII table
    table = texttable.Texttable()
    for row in rows:
        table.add_row([cell.strip() for cell in row])
    return table.draw()

bot.run(DISCORD_TOKEN)

