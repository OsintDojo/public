import discord
from discord import app_commands
from discord.ext import commands
import requests
from config import token, apikey

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Au démarrage
@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot connecté et prêt")

# Commande /lookup
@bot.tree.command(
    name="lookup",
    description="Recherche des informations sur une adresse IP"
)
@app_commands.describe(
    user_input="Entrez une adresse IP"
)
async def lookup(interaction: discord.Interaction, user_input: str):

    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={apikey}&ip={user_input}"

    response = requests.get(url)
    data = response.json()

    ip = data.get("ip", "Inconnue")
    country = data.get("country_name", "Inconnu")
    city = data.get("city", "Inconnue")
    isp = data.get("isp", "Inconnu")

    await interaction.response.send_message(
        f"🌐 IP : {ip}\n"
        f"🏳️ Pays : {country}\n"
        f"🏙️ Ville : {city}\n"
        f"📡 ISP : {isp}",
        ephemeral=True
    )

# Lancement du bot
bot.run(token)
