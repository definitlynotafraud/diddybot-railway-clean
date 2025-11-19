import discord
from discord import app_commands
from discord.ext import commands
import json
import os

COUNT_FILE = "diddify_counts.json"

# Load counts safely, handle old or corrupted files
if os.path.exists(COUNT_FILE):
    try:
        with open(COUNT_FILE, "r") as f:
            counts = json.load(f)
            # Convert old int counts to new dict format
            for user_id, value in counts.items():
                if isinstance(value, int):
                    counts[user_id] = {"diddify": value, "kill": 0}
    except (json.JSONDecodeError, ValueError):
        counts = {}
else:
    counts = {}

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()
    print("Commands synced!")

def save_counts():
    with open(COUNT_FILE, "w") as f:
        json.dump(counts, f)

async def do_action(interaction: discord.Interaction, target: discord.Member, action: str):
    user_id = str(target.id)
    # Initialize nested dictionary if user not in counts
    if user_id not in counts:
        counts[user_id] = {"diddify": 0, "kill": 0}
    # Increment only the specific action
    counts[user_id][action] += 1
    save_counts()
    await interaction.response.send_message(
        f"🔥 {interaction.user.mention} {action}ed {target.mention}!\n"
        f"📊 They have been {action}ed **{counts[user_id][action]}** time(s)!"
    )

# /diddify command
@bot.tree.command(name="diddify", description="Diddify a user")
@app_commands.describe(user="Choose a user to diddify")
async def diddify(interaction: discord.Interaction, user: discord.Member):
    await do_action(interaction, user, "diddify")

# /kill command
@bot.tree.command(name="kill", description="Kill a user")
@app_commands.describe(user="Choose a user to kill")
async def kill(interaction: discord.Interaction, user: discord.Member):
    await do_action(interaction, user, "kill")

import os
bot.run(os.getenv("TOKEN"))

