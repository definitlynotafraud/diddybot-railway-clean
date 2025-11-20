import os
import json
import discord
from discord.ext import commands
from discord import app_commands

# -----------------------------
# Load token from environment
# -----------------------------
TOKEN = os.getenv("TOKEN")

# -----------------------------
# Intents and Bot Setup
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------------
# Load / Initialize Counters
# -----------------------------
COUNTERS_FILE = "diddify_counters.json"

try:
    with open(COUNTERS_FILE, "r") as f:
        counts = json.load(f)
except FileNotFoundError:
    counts = {}  # empty dictionary if file doesn't exist

def save_counts():
    with open(COUNTERS_FILE, "w") as f:
        json.dump(counts, f, indent=4)

# -----------------------------
# Bot Ready Event
# -----------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Commands synced! ({len(synced)})")
    except Exception as e:
        print(e)

# -----------------------------
# Helper to increment counters
# -----------------------------
def increment_counter(user_id, action):
    if str(user_id) not in counts:
        counts[str(user_id)] = {"diddify": 0, "oilup": 0, "kill": 0}
    counts[str(user_id)][action] += 1
    save_counts()
    return counts[str(user_id)][action]

# -----------------------------
# Slash Commands
# -----------------------------

# /diddify
@bot.tree.command(name="diddify", description="diddify someone")
async def diddify(interaction: discord.Interaction):
    user_id = interaction.user.id
    total = increment_counter(user_id, "diddify")
    await interaction.response.send_message(f"{interaction.user.mention} got diddified! Total diddifies: {total}")

# /oilup
@bot.tree.command(name="oilup", description="oil someone up")
async def oilup(interaction: discord.Interaction):
    user_id = interaction.user.id
    total = increment_counter(user_id, "oilup")
    await interaction.response.send_message(f"{interaction.user.mention} got oiled up! Total oil-ups: {total}")

# /kill
@bot.tree.command(name="kill", description="kill someone (funny command)")
@app_commands.describe(user="Who do you want to kill?")
async def kill(interaction: discord.Interaction, user: discord.User = None):
    user_id = interaction.user.id
    total = increment_counter(user_id, "kill")
    if user is None:
        await interaction.response.send_message(f"{interaction.user.mention} killed themselves 💀 Total kills: {total}")
    else:
        await interaction.response.send_message(f"{interaction.user.mention} killed {user.mention} 💀 Total kills: {total}")

# -----------------------------
# Run Bot
# -----------------------------
bot.run(TOKEN)
