import discord
import os
import time 
discord_key = os.environ['discord_key']
from selenium import webdriver
import subprocess
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import urllib.parse
from discord.ext import commands

# keep running
from keep_alive import keep_alive
keep_alive()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("–lang= ja")

driver = webdriver.Chrome(options=chrome_options)

def generateMessage(message, language):

  if language == "en":
    driver.get(f"https://www.deepl.com/en/translator#ja/en/{message}")
  elif language == "ja" or "jp":
    driver.get(f"https://www.deepl.com/en/translator#en/ja/{message}")
    
  try:
      time.sleep(5)
      text = driver.find_element(By.XPATH, "//*[@id=\"target-dummydiv\"]").get_attribute("textContent")

      return text
  except Exception as e:
      print(e)
      pass 


intents = discord.Intents.all()

bot = commands.Bot(command_prefix="-", intents=intents)
@bot.event
async def on_ready():
  print('Started!')

@bot.command()
async def t(ctx, *args):
  print(args)
  if args[0] == "en" or args[0] == "jp":
    message = ' '.join(args[1:])
    print(f"Message Content: {message}")
    filtered_message = urllib.parse.quote(message, safe='').replace("%2F", "%5C%2F")
    print(f"Filtered Message Content: {filtered_message}")
    payload = generateMessage(filtered_message, args[0])
    print(f"After translation: {payload}")
    await ctx.reply(payload, mention_author=False)
    
@t.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Wrong formating')
bot.run(discord_key)
