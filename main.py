import aiohttp
import asyncio
async def test_ssl():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://discord.com") as response:
            print(response.status)
asyncio.run(test_ssl())

import os
from dotenv import load_dotenv
load_dotenv()  # Carica le variabili d'ambiente dal file .env
TOKEN = os.getenv("DISCORD_TOKEN")  # Recupera il token dal file .env

import discord
from discord.ext import commands

# Imports usati nelle funzioni.
import random

# Set-up del bot con gli Intents necessari.
intents = discord.Intents.default()
# Attiva la possibilita' che ha il bot di leggere messaggi.
intents.message_content = True

# Define the bot, with "!" as the command prefix
bot = commands.Bot(command_prefix=".", intents=intents)

# La parte iniziale "ctx" si riferisce al contesto (context) in cui il bot viene richiamato.

# Quando il bot e' pronto, invia questo messaggio sul terminale.
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def clear(ctx):
    await ctx.channel.purge(limit=10);
    # La funzione serve ad eliminare dei messaggi dalla chat.
    # @limit è il numero massimo di messaggi eliminabili dalla funzione.

@bot.command()
@commands.has_permissions(manage_channels=True)
async def ticket(ctx):
    # @user e' l'utente che ha avviato il comando.
    user = ctx.author
    role = discord.utils.get(ctx.guild.roles, name="testing")
    ticketName = "ticket-" + f"{user.name}"
    duplic = discord.utils.get(ctx.guild.channels, name=ticketName)
    # Check della presenza di canali testuali con lo stesso nome.
    if duplic:
        # @duplic vera nel caso in cui esiste gia' un canale con lo stesso nome.
        await ctx.send(f"`{ctx.author}` ha già un ticket aperto.")
    else:
        permissions = {
        # Nascondi il canale a @everyone.
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        # Permessi per il ruolo scelto.
        role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        # Permessi per l'utente che ha avviato il comando.
        user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        # Creazione del canale testuale con il nome pre-assegnato.
        ticket = await ctx.guild.create_text_channel(ticketName, overwrites=permissions)
        await ctx.send(f"E' stato aperto il ticket #`{ticketName}`")

# Avvio del bot tramite TOKEN.
bot.run(TOKEN)