import aiohttp
import asyncio
async def test_ssl():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://discord.com") as response:
            print(response.status)
asyncio.run(test_ssl())
import random
import os
from dotenv import load_dotenv
load_dotenv()  # Carica le variabili d'ambiente dal file .env
TOKEN = os.getenv("DISCORD_TOKEN")  # Recupera il token dal file .env
import discord
from discord.ext import commands

# Set-up permessi del bot.
intents = discord.Intents.default()
intents.message_content = True

# Definiamo il prefisso per i comandi del bot.
bot = commands.Bot(command_prefix=".", intents=intents)

# Quando il bot e' pronto, invia questo messaggio sul terminale.
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def clear(ctx):
    await ctx.channel.purge(limit=20);
    # @limit è il numero massimo di messaggi eliminabili dalla funzione.

@bot.command()
@commands.has_permissions(manage_channels=True)
async def ticket(ctx):
    user = ctx.author
    role = discord.utils.get(ctx.guild.roles, name="testing")
    ticketName = "ticket-" + f"{user.name}"
    duplic = discord.utils.get(ctx.guild.channels, name=ticketName)
    if duplic:
        # @duplic vera nel caso in cui esiste gia' un canale con lo stesso nome.
        await ctx.send(f"{ctx.author} ha già un ticket aperto.")
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
        await ctx.send(f"E' stato aperto il ticket `{ticketName}`")
        try:
            ticketContext = discord.utils.get(ctx.guild.channels, name=ticketName)
            await ticketContext.send(f"Il tuo ticket e' stato aperto!\nLo Staff risponderà il prima possibile alla tua richiesta di supporto.\n\nSe desideri chiudere il ticket, invia il comandio " + ".close\n@here")
        except discord.errors.NotFound:
            print(f"{bot.user} non e' riuscito a trovare il canale in cui inviare il messaggio.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def close(ctx):
    user = ctx.author
    # Compongo l'eventuale nome del canale "ticket-username" per verificarne l'esistenza.
    ticketName = "ticket-" + f"{user.name}"
    # Assegno ad existing il canale che potrebbe trovare/esistere con il nome composto prima.
    existing = discord.utils.get(ctx.guild.channels, name=ticketName)
    if existing: await existing.delete(reason="Chiusura del ticket.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def take(ctx):
    user = ctx.author
    await ctx.channel.edit(topic=f"{user}")
    await ctx.send(f"{user} ha preso il ticket in carico.\n@here")

# Per far funzionare i comandi .wl e .removewl bisogna scegliere il nome di un ruolo esistente da assegnare/rimuovere.
# Per fare cio' basta cambiare il nome del ruolo in @role.
@bot.command()
@commands.has_permissions(manage_roles=True)
async def wl(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Whitelist")
    await member.add_roles(role)
    await ctx.send(f"{member.mention} ha RICEVUTO la sua whitelist.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removewl(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Whitelist")
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} ha PERSO la sua whitelist.")

# Avvio del bot tramite TOKEN.
bot.run(TOKEN)