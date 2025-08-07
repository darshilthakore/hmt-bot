import discord
import aiohttp
from bs4 import BeautifulSoup
import asyncio
from datetime import datetime
import os


# get from env
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Get sensitive data from environment variables
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

# watches
watches = {
    "HMT Kohinoor Pink Matte": "https://www.hmtwatches.in/product_details?id=eyJpdiI6IkMwdnFyYUp3L0tMalI1MGQ0NkZ1MGc9PSIsInZhbHVlIjoiOUROWDU1YVQ3K0pjc2hJcG9XcWhZZz09IiwibWFjIjoiZmNmNDZkYmEzZjUyNjk5ODkzMzRlNjNhZjZmMTQ0MmQ3ZGUzN2JkODc3YTNmNzZmMmE4NzE5Zjg2MmFjMjAxZiIsInRhZyI6IiJ9",
    "HMT Rajat Blue": "https://www.hmtwatches.in/product_details?id=eyJpdiI6Im1IODRHdlJ3Z1FidlJMUjJrRkRIV2c9PSIsInZhbHVlIjoiMWZGTGVpYjdnalczUjJRajVjcjdyQT09IiwibWFjIjoiNTc4ZmE2MjlhOTJiYzc2MTA1Y2M3NTE2MDQzODAxMzM5NTRmMTc5NzYyMWJlZWE1MTgwZmVmZjQ2NDE5YzhlOSIsInRhZyI6IiJ9",
    "HMT Rajat Saffron": "https://www.hmtwatches.in/product_details?id=eyJpdiI6IjJIMzkvL2ZoV2JmS01HQlM4dGJyTWc9PSIsInZhbHVlIjoiUXVFUXZURmlKaEdYRlBWc1N4S2Y2dz09IiwibWFjIjoiMzk1YTVhZDk2Nzg3ZGNjMzdjNWZkMTliNTJhZDlmMjdhMjU0NWU2OTZlNDNmNzNlMjAxMDhmNDA4NTExZmNjNCIsInRhZyI6IiJ9",
    "HMT Rajat White": "https://www.hmtwatches.in/product_details?id=eyJpdiI6ImtuRnJuUW55OEljT29lRUEza09QWXc9PSIsInZhbHVlIjoieFlJWVFMY1kyWGpYMmh2TW5vSGlWdz09IiwibWFjIjoiYTY5ODkyZmE0NTgxZDE5ZmM5ZTM4N2RjZWQxMmQ2NmJhMjZjMTA3MzVlYzJjOGVmZDlkMjI5ZWNiMGYxMDBiMyIsInRhZyI6IiJ9",
    "HMT Rajat Black": "https://www.hmtwatches.in/product_details?id=eyJpdiI6IitWUElWeFE3WXB6enZFcTlaZ2g4b0E9PSIsInZhbHVlIjoiV0ZQRURTYWpCMFdSL1pucjlqRG5tdz09IiwibWFjIjoiMDg5NjY2NDEzNWJmZWQ1NjVkMGU5M2U5YzFlZTMzNTNhZDY5NmFlNGY0OWE2MTQ5MTNjZTJmNGEyNjViMDk0YyIsInRhZyI6IiJ9",
    "HMT Rajat Premium Turquoise Blue B": "https://www.hmtwatches.in/product_details?id=eyJpdiI6IlRYdldKcW0wb0hnOTEyWDBPSm1nbEE9PSIsInZhbHVlIjoiaDF2eENoNXFTbXpLR0tlbFJhTXRhQT09IiwibWFjIjoiZjBhN2QwNjIwNWZhYjlkOGFmY2EzOGQ5ODRjNGVkN2FiNGQwNzRjZTczMWQ0YWQ4MDc5ZDUyNDA2OTUzMmNlMyIsInRhZyI6IiJ9",
    "HMT Rajat Premium Saffron B": "https://www.hmtwatches.in/product_details?id=eyJpdiI6IkxQaTdaUEpNVjROd1ZNcUFsc3NjTWc9PSIsInZhbHVlIjoiVDZqbGNmWGo5TUxJNWd4cE1OYTNEdz09IiwibWFjIjoiMDk3ZmI2MmM0NDI0ZWNiN2NhOThiOTIzNWUzZmE0NzIyMzQ5NmQzYTBiZThiZTA5NjA4YWZiYWE1MzEyYjIxNyIsInRhZyI6IiJ9",
    "HMT Rajat Premium White B": "https://www.hmtwatches.in/product_details?id=eyJpdiI6IndIazR0NTlBSG5YL1E5TE1SYlhHZ1E9PSIsInZhbHVlIjoiMC9BM1lMTHBBeEJtQ0U1dHM3WXBuUT09IiwibWFjIjoiNDY2Mjc2M2Q3N2NlNGY2Y2M5Yjg4Mjk2Zjc5YzczNjQzY2NjYzFlMTRhMWIwYjFlN2M5OWFmM2Q3ODE5NWFkMCIsInRhZyI6IiJ9",
    "HMT Kedar Silver": "https://www.hmtwatches.in/product_details?id=eyJpdiI6IjVtSTNNNE5ENzU3cGNOdzNFdWlXZ3c9PSIsInZhbHVlIjoiNEVpUk14ajFxSXpWZVh0SUNNUG9pZz09IiwibWFjIjoiMjQ5MTE0MDNlMDRlYTEyNjU0YmIyZTMwOTBmMGIyNmVlNTQyMDM3NDhkODE4MGIxNjM4MjA2YjAyZjU1ZjEwYyIsInRhZyI6IiJ9",
    "HMT Kedar White": "https://hmtwatches.in/product_details?id=eyJpdiI6IndxZEU3ZkUyaXhBbldkYVVOL1BGQnc9PSIsInZhbHVlIjoiYzY1ckpiZzJBSVJVU3AxVlJjQ3FRZz09IiwibWFjIjoiNjlmN2VlZjZkNDYwOThkN2MxYTNkOGM3NGU3NjVhMzBjZThmMjIwNmI4NWVkNWExNTNkNDM0NTQ2MGQ0ZjRkYyIsInRhZyI6IiJ9",
    "HMT Kedar Blue": "https://hmtwatches.in/product_details?id=eyJpdiI6IlZLakx0VXBTZHptMGg0azFYQ2pxemc9PSIsInZhbHVlIjoicXVBOFN3Z08yd3pYZzV1SVBCYUttZz09IiwibWFjIjoiNjdjZWVhODdjN2UwNmMzNzg1MDVhOTJhN2ZjZTYwYmEwOTMxY2Y4Y2YwZGJlMDIwYjE4ZGRiNDE5OWZmZmJmZSIsInRhZyI6IiJ9",
    "HMT Kedar Grey": "https://hmtwatches.in/product_details?id=eyJpdiI6InpjeFhVckxhTmx5aE9CUlVEZlF0Ymc9PSIsInZhbHVlIjoiSE9zajRZWVdzVytCaXdyS1hSREZTUT09IiwibWFjIjoiYTVkMzBiZWMyNTU5Yzc2YzgwMjAxYjIzZTQzNjRjNWQ2NjY1ZDllNTVlZTEwY2E4MzdmYTIzN2ZkODFkOTZlZSIsInRhZyI6IiJ9"
}

async def check_single_watch(session, name, url, channel):
    try:
        async with session.get(url, timeout=10) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            stock_element = soup.find("p", class_="vote text-danger")
            stock_text = stock_element.get_text(strip=True).lower() if stock_element else "unknown"
            
            print(f"Stock status: {stock_text} for {name} Timestamp: {datetime.now()}")
            
            if stock_text != "out of stock":
                print(f"🛍️ {name} is IN STOCK!\n{url}")
                await channel.send(f"🛍️ **{name} is now IN STOCK!**\n{url}")
    except Exception as e:
        print(f"Error checking {name}: {e}")

async def check_stock(client):
    channel = client.get_channel(CHANNEL_ID)
    async with aiohttp.ClientSession() as session:
        tasks = [
            check_single_watch(session, name, url, channel)
            for name, url in watches.items()
        ]
        await asyncio.gather(*tasks)
    # Exit after one check
    await client.close()

# Configure Discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await check_stock(client)

client.run(TOKEN)