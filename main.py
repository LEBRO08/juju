import discord
import random
import os
import asyncio
from flask import Flask
from keep_alive import keep_alive

responses = [
    "Thx",
    "Thanks",
    "Ty",
    "thx",
    "ty",
    "thanks",
    "thank you",
    "Thank you",
    "lfg",
    "Thank you",
    "tysm",
    "thankss",
]

keep_alive()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

port = os.environ.get('PORT', 8080)  # Default to 5000 if PORT environment variable is not set

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

client = MyClient()

@client.event
async def on_message(message):
    if message.author.id == 1150448986264698980 and message.channel.id != 1238488488362639364:
        print("Message from bot.")
        for embed in message.embeds:
            if client.user.mentioned_in(message) and "### 🎟️\xa0\xa0Raffle ended!" in embed.description:
                response = random.choice(responses)
                await asyncio.sleep(random.randint(7, 20))
                async with message.channel.typing():
                    await asyncio.sleep(random.randint(2, 4))
                    await message.channel.send(response)
                                    # Send a message to a specific channel after processing
                channel_id = 1252625826109722664
                channel = client.get_channel(channel_id)
                if channel:
                 async with message.channel.typing():
                    await asyncio.sleep(random.randint(5, 10))
                    await channel.send("<@740547277164249089> wa rb7t azbi")
        for embed in message.embeds:
            if "Raffle created" in embed.description:
                for component in message.components:
                    for child in component.children:
                        if child.label == "Enter":
                            await asyncio.sleep(random.randint(10, 30))
                            await child.click()  # Uncomment this line if you want to simulate clicking the "Enter" button
        for embed in message.embeds:
            if "Airdrop created" in embed.description:
                for component in message.components:
                    for child in component.children:
                        if child.label == "Enter":
                            await asyncio.sleep(random.randint(3, 15))
                     #      await child.click()  # Uncomment this line if you want to simulate clicking the "Enter" button

if __name__ == "__main__":
    client.run(os.environ['TOKEN'])
