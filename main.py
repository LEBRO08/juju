import discord
import asyncio
import random
import os
from flask import Flask
from keep_alive import keep_alive
from settings import (
    is_prize_value_above_threshold,
    is_pool_value_above_threshold,
    is_pool_value_above_threshold_1,
    is_enters_value_at_most_4,
    is_pool_per_enters_above_threshold,
    extract_text_between_parentheses,
)

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
    "tysm",
    "thankss",
]

keep_alive()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

port = os.environ.get('PORT', 8080)  # Default to 8080 if PORT environment variable is not set

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        try:
            if message.author == self.user or message.guild is None:
                return

            # Process raffle ended messages
            for embed in message.embeds:
                if self.user.mentioned_in(message) and "### 🎟️\xa0\xa0Raffle ended!" in embed.description:
                    response = random.choice(responses)
                    await asyncio.sleep(random.randint(2, 4))
                    async with message.channel.typing():
                        await asyncio.sleep(random.randint(2, 4))
                        await message.channel.send(response)

                    # Send a message to a specific channel after processing
                    channel_id = 1252625826109722664
                    channel = self.get_channel(channel_id)
                    if channel:
                        async with message.channel.typing():
                            await asyncio.sleep(random.randint(5, 10))
                            await channel.send("<@740547277164249089> wa rb7t azbi")
            
            # Process airdrop collected messages
            for embed in message.embeds:
                if self.user.mentioned_in(message) and "Airdrop collected" in embed.description:
                    extracted_text = extract_text_between_parentheses(embed.description)
                    if extracted_text:
                        print(f"Extracted text: {extracted_text}")

                    # Send a message to a specific channel after processing
                    channel_id = 1252731072081428500
                    channel = self.get_channel(channel_id)
                    if channel and extracted_text is not None:
                        async with message.channel.typing():
                            await asyncio.sleep(random.randint(5, 10))
                            await channel.send(f"Text between parentheses: {extracted_text}")

            # Process raffle created messages
            for embed in message.embeds:
                if "Raffle created" in embed.description:
                    if is_prize_value_above_threshold(embed.fields):
                        for component in message.components:
                            for child in component.children:
                                if child.label == "Enter":
                                    await asyncio.sleep(random.randint(2, 5))
                                    await child.click()
                    else:
                        print("Prize value is not more than $0.1, skipping entry.")
                        break  # Exit the loop if prize value is not above $0.1
            
            # Process airdrop created messages (Pool > $1 and 4 or less enters)
            for embed in message.embeds:
                if "Airdrop created" in embed.description:
                    if is_pool_value_above_threshold(embed.fields) and is_enters_value_at_most_4(embed.fields):
                        for component in message.components:
                            for child in component.children:
                                if child.label == "Enter":
                                    await child.click()
                    else:
                        print("Pool value is not more than $1 or enters are more than 4, skipping entry.")
                        break  # Exit the loop if pool value is not above $1 or enters are more than 4

            # Process airdrop created messages (Pool > $0.1 per enters)
            for embed in message.embeds:
                if "Airdrop created" in embed.description:
                    if is_pool_per_enters_above_threshold(embed.fields):
                        for component in message.components:
                            for child in component.children:
                                if child.label == "Enter":
                                    await child.click()
                    else:
                        print("Pool value is not more than $0.1 per enters, skipping entry.")
                        break  # Exit the loop if pool value is not above $0.1 per enters

        except Exception as e:
            print(f"An error occurred in on_message: {e}")

client = MyClient()

if __name__ == "__main__":
    client.run(os.environ['TOKEN'])
