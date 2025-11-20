import os
import discord
from discord.ext import commands
from discord import app_commands
import json

# Load token from environment variable
TOKEN = os.getenv("TOKEN")  # Railway should have this variable set

# Intents
intents = discord.Intents.default()
intents.message_content = True

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Load diddify/oilup/kill counts from file
counts_file = "diddify_counts.json"
if os.path.exists(counts_file):
    with open(counts_file, "r") as f:
        counts = json.load(f)
else:
    counts = {}

# -----------------------------
#        UTILITY FUNCTION
# -----------------------------
async def do_action(interaction: discord.Interaction, user: discord.User, action: str):
    user_id = str(user.id)
    if user_id not in counts:
        counts[user_id] = {"diddify": 0, "oilup": 0, "kill": 0}
    counts[user_id][action] += 1

    # Save counts
    with open(counts_file, "w") as f:
        json.dump(counts, f)

    await interaction.response.send_message(
        f"{interaction.user.mention} {action}ed {user.mention}! Total {action}ed: {counts[user_id][action]}"
    )

# -----------------------------
#        EVENTS
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
#        SLASH COMMANDS
# -----------------------------

# /diddify
@bot.tree.command(name="diddify", description="diddify someone")
@app_commands.describe(user="Who do you want to diddify?")
async def diddify(interaction: discord.Interaction, user: discord.User = None):
    if user is None:
        user = interaction.user
    await do_action(interaction, user, "diddify")

# /oilup
@bot.tree.command(name="oilup", description="oil someone up")
@app_commands.describe(user="Who do you want to oil up?")
async def oilup(interaction: discord.Interaction, user: discord.User = None):
    if user is None:
        user = interaction.user
    await do_action(interaction, user, "oilup")

# /kill
@bot.tree.command(name="kill", description="kill someone (funny command)")
@app_commands.describe(user="Who do you want to kill?")
async def kill(interaction: discord.Interaction, user: discord.User = None):
    if user is None:
        user = interaction.user
    await do_action(interaction, user, "kill")

# -----------------------------

bot.run(TOKEN)
