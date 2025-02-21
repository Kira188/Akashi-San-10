import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()
Bye_words = ["bye","Bye"]

bad_words = ["fuck", "bitch", "whore", "bastard", "pussy", "slut", "dick"]

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing", "tired"]

starter_encouragements = [
  "Gambatekudasai!",
  "Hang in there.",
  "Omae honto baka desu.",
  "It's ok everything will be fine senpai."
]

if "respond" not in db.keys():
  db["respond"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = '"' + json_data[0]['q'] + '"' + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content.lower().replace(" ", "")
  

  if msg.startswith('/hitmeup'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["respond"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("/new"):
    encouraging_message = msg.split("/new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("/del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("/del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("/list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("/respond"):
    value = msg.split("/respond ",1)[1]

    if value.lower() == "true":
      db["respond"] = True
      await message.channel.send("Responding is on.")
    else:
      db["respond"] = False
      await message.channel.send("Responding is off.")
    
  if any(word in msg for word in bad_words):
    
     await message.delete()

  if msg.startswith("?help"):
    await message.channel.send("""
     Use '/' before every message senpai
    hitmeup  I will send you a quote.
    new <>   I will add an encouraging message.
    del <>   I will delete the encouraging message.
    list     I will show the encouraging messages.
    respond  I will stop or start responding.
    ?help    I will show this page.
    """)    
  if any(word in msg for word in Bye_words):
    await message.channel.send('See you soon senpai')

keep_alive()
client.run(os.getenv('TOKEN'))