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
    extract_text_between_parentheses
)

emoji_options = ['<a:pepemoney:1236611457047859210>', '<:peepoheart:1236627534523797535>', '🔥']

responses = [
    "thx <a:pepemoney:1236611457047859210>",
    "<:peepoheart:1236627534523797535>",
    "thx",
    "ty <:prayge:1236611465142861834>",
    "<a:pepemoney:1236611457047859210> <a:pepemoney:1236611457047859210> <a:pepemoney:1236611457047859210>",
    "<a:peepoPog2:781015662578499597>",
    "<:Peepo_Happy:1246998990319259658>",
    "thanks <:Peepo_Happy:1246998990319259658> ",
    "thank you",
    "lfg",
    "ty",
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

client = MyClient()

@client.event
async def on_message(message):
    if message.author.id == 1150448986264698980 and message.guild.id != 1102183639791452242:
        print("Message from bot.")

        # Processing raffle ended messages
        for embed in message.embeds:
            if client.user.mentioned_in(message) and "### 🎟️\xa0\xa0Raffle ended!" in embed.description:
                response = random.choice(responses)
                extracted_text = extract_text_between_parentheses(embed.description)

                if extracted_text:
                    print(f"Extracted text: {extracted_text}")
    
                # Send a message to a specific channel after processing
                
                await asyncio.sleep(random.randint(2, 4))
                async with message.channel.typing():
                    await asyncio.sleep(random.randint(2, 4))
                    await message.channel.send(response)
                try:
                    random_emoji = random.choice(emoji_options)
                    await asyncio.sleep(random.randint(5, 8))
                    await message.add_reaction(random_emoji)  # 
                except Exception as e:
                    print(f"Failed to add reaction: {e}")

                # Send a message to a specific channel after processing
                channel_id = 1252625826109722664
                channel = client.get_channel(channel_id)
                
                if extracted_text:
                    print(f"Extracted text: {extracted_text}")
    
                if channel and extracted_text is not None:  # Ensure extracted_text is not None
 #                   async with channel.typing():
                        await asyncio.sleep(random.randint(2, 5))
                        await channel.send(f"<@740547277164249089> hmdlh rb7t {extracted_text}")

            elif client.user.mentioned_in(message) and "Airdrop collected" in embed.description:
                response = random.choice(responses)
                extracted_text = extract_text_between_parentheses(embed.description)
                
                if extracted_text:
                    print(f"Extracted text: {extracted_text}")
    
                # Send a message to a specific channel after processing
                channel_id = 1252731072081428500
                channel = client.get_channel(channel_id)
                
                if channel and extracted_text is not None:  # Ensure extracted_text is not None
                    async with channel.typing():
                        await asyncio.sleep(random.randint(3, 7))
                        await channel.send(f"<@740547277164249089> dit {extracted_text} f airdrop")
                        await asyncio.sleep(random.randint(3, 7))

                  # Typing for response
                    await asyncio.sleep(random.randint(3, 5))
                    async with message.channel.typing():  # Start typing indicator
                        response_length = len(response)
                        min_sleep = 2  # Minimum sleep duration
                        adjusted_sleep = max(min_sleep, response_length // 5)  # Adjusted sleep duration based on response length
                        await asyncio.sleep(adjusted_sleep)
                        await message.channel.send(response)
                    try:
                        random_emoji = random.choice(emoji_options)
                        await asyncio.sleep(random.randint(5, 8))
                        await message.add_reaction(random_emoji)  # 
                    except Exception as e:
                        print(f"Failed to add reaction: {e}")

        # Only joining raffle = or above 0.1$
        for embed in message.embeds:
            if "Raffle created" in embed.description:
                if is_prize_value_above_threshold(embed.fields):
                    for component in message.components:
                        for child in component.children:
                            if child.label == "Enter":
                                await asyncio.sleep(random.randint(2, 4))
                                await child.click()  # Simulate clicking the "Enter" button
                           #     await message.channel.send(response)
                else:
                    print("Prize value is not more than $0.1, skipping entry.")
                    break  # Exit the loop if prize value is not above $0.1

        # Processing airdrop created messages
        for embed in message.embeds:
            response = random.choice(responses)
            if "Airdrop created" in embed.description:
                if is_pool_value_above_threshold(embed.fields):
                    for component in message.components:
                        for child in component.children:
                            if child.label == "Enter":
                                await asyncio.sleep(random.randint(3, 6))
                                await child.click()  # CLICKS THE ENTER BUTTON
                           #     await asyncio.sleep(random.randint(2, 4))
                          #      async with message.channel.typing():
                         #           await asyncio.sleep(random.randint(2, 4))
                        #            await message.channel.send(response)
                    # Exit the loop after processing
                    break

                elif is_pool_value_above_threshold_1(embed.fields) and is_enters_value_at_most_4(embed.fields):
                    for component in message.components:
                        for child in component.children:
                            if child.label == "Enter":
                                await child.click()  # CLICKS THE ENTER BUTTON
                                await asyncio.sleep(random.randint(5, 10))
                                async with message.channel.typing():
                                    await asyncio.sleep(random.randint(3, 6))
                                    await message.channel.send(response)
                    # Exit the loop after processing
                    break

                elif is_pool_per_enters_above_threshold(embed.fields):
                    for component in message.components:
                        for child in component.children:
                            if child.label == "Enter":
                                await asyncio.sleep(random.randint(10, 30))
                                await child.click()  # CLICKS THE ENTER BUTTON
                    #            async with message.channel.typing():
                    #                await asyncio.sleep(random.randint(2, 4))
                    #                await message.channel.send(response)
                    # Exit the loop after processing
                    break

                else:
                    print("Conditions not met for any action, skipping")
                    break  # Exit the loop if no conditions are met

if __name__ == "__main__":
    client.run(os.environ['TOKEN'])
