import discord
from discord.ext import commands
import texttable
import os
#import openai
from openai import OpenAI
# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
from dotenv import load_dotenv
from gtts import gTTS

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHAT_GPT_API = os.getenv("CHAT_GPT_API")
COMMAND_STRING = os.getenv("COMMAND_STRING")

openai = OpenAI(api_key=CHAT_GPT_API)

# Prefix for bot commands
#bot = commands.Bot(command_prefix='/')
#bot = discord.Client(intents=discord.Intents.default())
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="<" , intents=intents)


# Maximum rows per table
MAX_ROWS_PER_TABLE = int(os.getenv("MAX_ROWS_PER_TABLE"))
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
    # Check if the edited message starts with '/table'
    await process_message(message)

async def process_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the message starts with '/table'
    if message.content.startswith(f'/{COMMAND_STRING}'):
        # Extract the content after '/table'
        content = message.content[len(f'/{COMMAND_STRING}'):].strip()
        print("Message received from " + str(message.author) + ' id='+ str(message.id) + ' channel=' + str(message.guild))
        # Parse the content into rows
        rows = [line.strip().split(':') for line in content.split('\n')]

        # Convert Markdown table to ASCII table
        tables, mp3_files = markdown_to_ascii(rows)
        
        thread = await message.create_thread(name="make_tabler")
        # Reply with the ASCII table
        #await thread.send('```\n' + ascii_table + '```')
        
        try:
            print('Sending tables')
            for table in tables:
                await thread.send('```\n' + table + '```')
            # Send mp3 files
            print('Sending audios')

            for mp3_file in mp3_files:
                try:
                    await thread.send(file=mp3_file)
                except Exception as e:
                    print('fail to send file' + mp3_file.filename + str(e))
                finally:
                    os.remove(mp3_file.filename)

        except Exception as e:
            print("Something went wrong " + str(message.id) + str(e) )
        
    await bot.process_commands(message)

def markdown_to_ascii(rows):
    # Convert Markdown table to ASCII table
    mp3_files = []
    tables = []
    table = texttable.Texttable()
    table.header(["Ord", "Translation", "IPA", "Bestämd", "Plural", "Exampel"])
    table.set_deco(table.HEADER  | table.HLINES)
    for idx, row in enumerate(rows):
        if idx % MAX_ROWS_PER_TABLE == 0:
            # Create a new table for every MAX_ROWS_PER_TABLE rows
            if table._rows:
                s = table.draw()
                #print(s)
                tables.append(s)
                table = texttable.Texttable()
                table.set_deco( table.HEADER  |  table.HLINES)
            #table.header(["Ord", "Translation", "IPA", "Bestämd", "Plural", "Exampel"])
        if row:
            row[0] = verify_swedish_word(row[0].strip())
            # Get the value of the first cell
            first_cell = row[0].strip()
            print(row)
            if len(row) == 1:
                row.append(get_swedish_translation(first_cell))
            row.append(f'/{get_IPA_presentation(first_cell)}/')
            bestamd = get_swedish_bestamd(first_cell)
            row.append(bestamd)
            plural = get_swedish_plural(first_cell)
            row.append(plural)
            sentence = get_swedish_sentence(first_cell)
            row.append(sentence)
            table.add_row([cell.strip() for cell in row])
            
            mp3_files.append(discord.File(create_audio(first_cell, bestamd, plural, sentence.split('.')[0])))
    if table._rows:
        s = table.draw()
        #print(s)
        tables.append(s)
    return tables, mp3_files

def get_swedish_sentence(word):
    try:
        prompt = f"Use this word '{word}' in Swedish,  in a very simple sentence must be less than 20 word. It must be grammarly correct in Swedish. And translate it in parenthesises"
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

def get_swedish_plural(word):
    try:
        prompt = f"What is plural form of the word '{word}' in Swedish, give short straightforward 1,2 word answer, remove all quote characters"
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
        prompt = f"Use this Swedish word '{word}'  Correct the word if there is speeling mistake. it must be grammarly correct in Swedish, if you were to say '1 {word}' in a word, print out the word with correct 'ett' or 'en' form without additional context (only 2 words), for example 'ett öga'. Remove all non-alphanumeric characters. All lowercase"
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

def get_IPA_presentation(word):
    try:
        prompt = f"what is IPA presentatio of this Swedish word '{word}' . Short answer only. Remove all quote characters. All lowercase"
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

def create_audio(word, bestamd, plural, sentence):
    tts_sv = gTTS(word, lang='sv')
    tts_plural = gTTS(plural, lang='sv')
    tts_bestamd = gTTS(bestamd, lang='sv')
    #tts_sv.save(f'{word}.mp3')
    tts_sentence = gTTS(sentence, lang='sv')
    
    with open(f'{word}.mp3', 'wb') as f:
        tts_sv.write_to_fp(f)
        tts_bestamd.write_to_fp(f)
        tts_plural.write_to_fp(f)
        tts_sentence.write_to_fp(f)
    return word+'.mp3'
bot.run(DISCORD_TOKEN)

