import os
import discord
import openai
from discord.ext import commands
from keep_alive import keep_alive
import prompts

description = '''Its a vish bot'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?',
                   description=description,
                   intents=intents)

prompt = {
  "base": prompts.BASE,
  "about_vish": prompts.ABOUT_VISH,
  "rounaksingh1694": prompts.BASE_PROMPT_FOR_ROUNAK,
  "Ankur Bagchi": prompts.BASE_PROMPT_FOR_ANKUR,
  "בהבש": prompts.BASE_PROMPT_FOR_BHAVES,
  "newsmoke": prompts.BASE_PROMPT_FOR_NEWSMOKE,
  "Sarthak": prompts.BASE_PROMPT_FOR_SARTHAK,
  "spacedoggo": prompts.BASE_PROMPT_FOR_SPACE,
  "sphinx": prompts.BASE_PROMPT_FOR_SPHINX,
  "vish": prompts.BASE_PROMPT_FOR_VISH,
  "Rishi": prompts.BASE_PROMPT_FOR_RISHI
}

chat_history = {}


@bot.event
async def on_ready():
  print(f'Logged in as {bot.user} (ID: {bot.user.id})')
  print('------')


@bot.event
async def on_message(message):
  print(message.author.name)
  if message.author == bot.user:
    return
  if message.content.startswith('-vish'):
    if (message.author.name) in prompt:
      input = prompt["about_vish"] + prompt[message.author.name]
    else:
      input = prompt["about_vish"] + prompt["base"]

    print(message.author.name)

    fetch_chat_history(message.author.name, input, message.content)

    response = generate_text(chat_history[message.author.name])
    msg = (response.lower())
    print(msg)

    chat_history[message.author.name].append({
      "role": "assistant",
      "content": msg
    })

    await message.reply(msg, mention_author=True)


openai.api_key = os.environ["OPENAI_API_KEY"]


def fetch_chat_history(user, base_prompt, usermsg):
  if user not in chat_history:
    chat_history[user] = []
    chat_history[user].append({"role": "system", "content": base_prompt})
    chat_history[user].append({
      "role":
      "assistant",
      "content":
      "aree haa yarr bore hogya hu sun sun ke, ki mei vish hu. jhingalala hu hu"
    })

    chat_history[user].append({"role": "user", "content": usermsg})
  else:
    chat_history[user].append({"role": "user", "content": usermsg})


def generate_text(message):

  response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                          messages=message,
                                          temperature=0.2,
                                          max_tokens=120,
                                          frequency_penalty=0.9)

  s = response.choices[0].message.content
  return s


keep_alive()

bot.run(os.environ['TOKEN'])
