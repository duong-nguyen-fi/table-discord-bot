import discord
from discord.ext import commands
import texttable
import os
#import openai
from openai import OpenAI
# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
from dotenv import load_dotenv

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHAT_GPT_API = os.getenv("CHAT_GPT_API")
#openai.api_key = CHAT_GPT_API
openai = OpenAI(api_key=CHAT_GPT_API)

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
    table.header(["Ord", "Translation", "Bestämd", "Exampel"])
    for idx, row in enumerate(rows):
        if row:
            row[0] = verify_swedish_word(row[0].strip())
            # Get the value of the first cell
            first_cell = row[0].strip()
            if len(row) == 1:
                row.append(get_swedish_translation(first_cell))
            row.append(get_swedish_bestamd(first_cell))
            row.append(get_swedish_sentence(first_cell))
            table.add_row([cell.strip() for cell in row])
        else:
            table.add_row([])
    return table.draw()

def get_swedish_sentence(word):
    try:
        prompt = f"Use this word '{word}' in Swedish,  in a very simple sentence must be less than 20 word, and translate it in parenthesises"
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that helps beginner user learn Swedish."},
                {"role": "user", "content": prompt}
            ]
        )
        if response:
            #return response['choices'][0]['message']['content'].strip()
            return response.choices[0].message.content.strip()
        else:
            return "Sorry, I couldn't generate a sentence with that word."
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return ""

def get_swedish_bestamd(word):
    try:
        prompt = f"What is Bestämd form of the word '{word}' in Swedish, give short straightforward 1,2 word answer, remove all quote characters"
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that helps beginner user learn Swedish."},
                {"role": "user", "content": prompt}
            ]
        )
        if response:
            #return response['choices'][0]['message']['content'].strip()
            return response.choices[0].message.content.strip()
        else:
            return "Error"
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return ""

def get_swedish_translation(word):
    try:
        prompt = f"What is translation of this Swedish word '{word}' in English, give short straightforward 1,2 word answer, remove all quote characters"
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that helps beginner user learn Swedish."},
                {"role": "user", "content": prompt}
            ]
        )
        if response:
            #return response['choices'][0]['message']['content'].strip()
            return response.choices[0].message.content.strip()
        else:
            return "Error"
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return ""
        
def verify_swedish_word(word):
    try:
        prompt = f"Use this Swedish word '{word}'  Correct the word if incorrect. Make sure it is grammarly corret in Swedish, print out the word with correct 'ett' or 'en' form without additional context (only 2 words), for example 'ett öga'"
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that helps beginner user learn Swedish."},
                {"role": "user", "content": prompt}
            ]
        )
        if response:
            #return response['choices'][0]['message']['content'].strip()
            return response.choices[0].message.content.strip()
        else:
            return "Error"
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return ""

bot.run(DISCORD_TOKEN)

