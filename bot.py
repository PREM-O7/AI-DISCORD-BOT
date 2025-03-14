import discord
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Free AI APIs
CHAT_API_URL = "https://chatbot.vercel.app/api"
IMAGE_API_URL = "https://api.pexels.com/v1/search"

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents, description="OXTA AI Bot")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ask(ctx, *, question):
    """Ask the AI a question"""
    response = requests.get(CHAT_API_URL, params={"text": question})
    if response.status_code == 200:
        answer = response.json().get("text", "I couldn't understand that.")
        await ctx.send(answer)
    else:
        await ctx.send("Error: AI service is unavailable.")

@bot.command()
async def image(ctx, *, prompt):
    """Generate an AI image"""
    headers = {"Authorization": os.getenv("PEXELS_API_KEY")}
    params = {"query": prompt, "per_page": 1}
    response = requests.get(IMAGE_API_URL, headers=headers, params=params)
    if response.status_code == 200 and response.json().get("photos"):
        img_url = response.json()["photos"][0]["src"]["large"]
        await ctx.send(img_url)
    else:
        await ctx.send("Error: Couldn't generate an image.")

@bot.command()
async def ping(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)  # Convert to ms
    await ctx.send(f'Pong! 🏓 {latency}ms')

# Run bot
bot.run(DISCORD_TOKEN)
