import discord
import asyncio
import random
import os
from flask import Flask
from keep_alive import keep_alive
import re

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

def extract_prize_value(prize_text):
    try:
        # Regular expression to extract value inside parentheses after $
        match = re.search(r'\(\$([\d.]+)\)', prize_text)
        if match:
            value_str = match.group(1)  # Extract the value part as a string
            return float(value_str)  # Convert to float
        else:
            return None  # Return None if no match found
    except ValueError:
        return None  # Handle the case where conversion fails

def is_prize_value_above_threshold(fields):
    for field in fields:
        if field.name.lower() == "prize":
            prize_text = field.value  # Extract prize text from the prize field
            print(f"Checking prize: {prize_text}")
            value = extract_prize_value(prize_text)
            if value is not None:
                return value > 0.1  # Check if the value is more than $0.1
            else:
                return False  # Return False if extraction failed
    return False  # Return False if no prize field found or extraction failed

keep_alive()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

port = os.environ.get('PORT', 8080)  # Default to 8080 if PORT environment variable is not set

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

client = MyClient()

@client.event
async def on_message(message):
    if message.author.id == 1150448986264698980 and message.guild.id == 1239293213525803048:
        print("Message from bot.")
        
        # Processing raffle ended messages
        for embed in message.embeds:
            if client.user.mentioned_in(message) and "### 🎟️\xa0\xa0Raffle ended!" in embed.description:
                response = random.choice(responses)
                await asyncio.sleep(random.randint(2, 4))
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
        
        # Processing raffle created messages
        for embed in message.embeds:
            if "Raffle created" in embed.description:
                for field in embed.fields:
                    if field.name.lower() == "prize":
                        prize_text = field.value  # Extract prize text from the prize field
                        print(f"Checking prize: {prize_text}")
                        if is_prize_value_above_threshold(embed.fields):
                            await asyncio.sleep(random.randint(2, 4))
                            for component in message.components:
                                for child in component.children:
                                    if child.label == "Enter":
                                        await child.click()  # Simulate clicking the "Enter" button
                        else:
                            print("Prize value is not more than $0.1, skipping entry.")
                            break  # Exit the loop if prize value is not above $0.1
        
        # Processing airdrop created messages
        for embed in message.embeds:
            if "Airdrop created" in embed.description:
                for component in message.components:
                    for child in component.children:
                        if child.label == "Enter":
                            await asyncio.sleep(random.randint(3, 15))
                            # await child.click()  # Uncomment this line if you want to simulate clicking the "Enter" button

if __name__ == "__main__":
    client.run(os.environ['TOKEN'])
