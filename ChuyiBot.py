import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
@commands.has_permissions(administrator=True)
async def spam(ctx, cantidad: int, *, mensaje: str):
    if cantidad > 1000:
        await ctx.send("Hay un máximo de `1,000` mensajes por canal para evitar bloqueos.")
        return

    tareas = []

    for canal in ctx.guild.text_channels:
        async def enviar_en_canal(canal):
            for _ in range(cantidad):
                try:
                    await canal.send(mensaje)
                    await asyncio.sleep(0)
                except discord.Forbidden:
                    print(f"No tengo permisos para enviar en {canal.name}")
                except Exception as e:
                    print(f"Error en {canal.name}: {e}")

        tareas.append(asyncio.create_task(enviar_en_canal(canal)))

    await asyncio.gather(*tareas)
    await ctx.send(f"Listo, mensaje enviado `{cantidad}` veces en todos los canales de texto.")

@bot.command()
@commands.has_permissions(administrator=True)
async def raid(ctx, cantidad: int, *, nombre_base: str):
    if cantidad > 500:
        await ctx.send("Hay un máximo de `500` canales por comando para evitar bloqueos.")
        return

    creados = 0
    for i in range(1, cantidad + 1):
        nombre = f"{nombre_base}-{i}"
        try:
            await ctx.guild.create_text_channel(name=nombre)
            creados += 1
        except discord.Forbidden:
            await ctx.send(f"No tengo permisos para crear canales.")
            return
        except Exception as e:
            await ctx.send(f"Error al crear `{nombre}`: {e}")

    await ctx.send(f"Listo, se han creado `{creados}` canales con el nombre {nombre_base}.")



@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    await ctx.send("Confirma que quieres borrar **TODOS LOS CANALES** del servidor escribiendo `y` en el chat.")

    def check(m):
        return m.author == ctx.author and m.content == "y"

    try:
        respuesta = await bot.wait_for('message', check=check, timeout=15)
        for canal in ctx.guild.channels:
            try:
                await canal.delete()
            except discord.Forbidden:
                print(f"No tengo permisos para borrar {canal.name}")
            except Exception as e:
                print(f"Error al borrar {canal.name}: {e}")
        await ctx.send("Listo, todos los canales han sido borrados.")
    except asyncio.TimeoutError:
        await ctx.send("Tiempo agotado. No se borró nada.")

@bot.command()
@commands.has_permissions(administrator=True)
async def cn(ctx, *, nuevo_nombre: str):
    try:
        await ctx.guild.edit(name=nuevo_nombre)
        await ctx.send(f"El nombre del servidor ha sido cambiado a: `{nuevo_nombre}`")
    except discord.Forbidden:
        await ctx.send("No tengo permisos para cambiar el nombre del servidor.")
    except Exception as e:
        await ctx.send(f"Error al cambiar el nombre: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def ci(ctx):
    if not ctx.message.attachments:
        await ctx.send("Debes adjuntar una imagen para usar como nuevo icono.")
        return

    imagen = ctx.message.attachments[0]
    try:
        imagen_bytes = await imagen.read()
        await ctx.guild.edit(icon=imagen_bytes)
        await ctx.send("Icono del servidor cambiado correctamente.")
    except discord.Forbidden:
        await ctx.send("No tengo permisos para cambiar el icono del servidor.")
    except Exception as e:
        await ctx.send(f"Error al cambiar el icono: {e}")
        
@bot.command()
@commands.has_permissions(manage_roles=True)
async def cr(ctx, cantidad: int, *, nombre_base: str):
    if cantidad > 100:
        await ctx.send("Hay un máximo de `100` roles por comando para evitar bloqueos.")
        return

    creados = 0
    for i in range(1, cantidad + 1):
        nombre = f"{nombre_base}-{i}"
        try:
            await ctx.guild.create_role(name=nombre)
            creados += 1
            await asyncio.sleep(0.5)
        except discord.Forbidden:
            await ctx.send(f"No tengo permisos para crear el rol `{nombre}`.")
        except Exception as e:
            await ctx.send(f"Error al crear `{nombre}`: {e}")

    await ctx.send(f"Listo, se han creado `{creados}` roles con nombre base `{nombre_base}`.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def ret(ctx, cantidad: int, nombre_base: str, *, mensaje: str):
    if cantidad > 500:
        await ctx.send("Hay un máximo de `500` canales por comando para evitar bloqueos.")
        return

    creados = 0
    for i in range(1, cantidad + 1):
        nombre = f"{nombre_base}-{i}"
        try:
            canal = await ctx.guild.create_text_channel(name=nombre)
            await canal.send(mensaje)
            creados += 1
            await asyncio.sleep(0)
        except Exception as e:
            await ctx.send(f"Error en `{nombre}`: {e}")

    await ctx.send(f"Listo, se han creado `{creados}` canales y enviado el mensaje en cada uno.")

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

@bot.command()
@commands.has_permissions(ban_members=True)
async def bn(ctx):
    miembros = ctx.guild.members
    miembros_que_no_se_banean = [ctx.author, ctx.guild.owner, bot.user]

    miembros_a_banear = [
        miembro for miembro in miembros
        if miembro not in miembros_que_no_se_banean and not miembro.bot
    ]

    baneados = 0
    for usuario in miembros_a_banear:
        try:
            await ctx.guild.ban(usuario, reason="Chuyin Bot.")
            baneados += 1
            await asyncio.sleep(1)
        except discord.Forbidden:
            await ctx.send(f"No tengo permisos para banear a `{usuario}`.")
        except Exception as e:
            await ctx.send(f"Error al banear `{usuario}`: {e}")

    await ctx.send(f"Listo, se han baneado `{baneados}` Personas.")

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

bot.run(os.environ["TOKEN"])