import nextcord
import yt_dlp as youtube_dl
from nextcord.ext import commands
from datetime import datetime

TOKEN = "qwe"

TARGET_VOICE_CHANNEL_ID = 111

STAFF_CHANNEL_ID = 111

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None:
        activity = member.activity
        if activity and activity.type == nextcord.ActivityType.playing and "Escape from Tarkov" in activity.name:
            target_channel = bot.get_channel(TARGET_VOICE_CHANNEL_ID)
            if target_channel and after.channel.id != TARGET_VOICE_CHANNEL_ID:
                try:
                    await member.move_to(target_channel)
                    print(f"Перемещён {member.display_name} в канал {target_channel.name}")
                except nextcord.Forbidden:
                    print(f"Недостаточно прав для перемещения {member.display_name}")
                except nextcord.HTTPException as e:
                    print(f"Ошибка перемещения {member.display_name}: {e}")


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None:
        activity = member.activity
        if activity and activity.type == nextcord.ActivityType.playing and "S.T.A.L.K.E.R. 2" in activity.name:
            target_channel = bot.get_channel(TARGET_VOICE_CHANNEL_ID)
            if target_channel and after.channel.id != TARGET_VOICE_CHANNEL_ID:
                try:
                    await member.move_to(target_channel)
                    print(f"Перемещён {member.display_name} в канал {target_channel.name}")
                except nextcord.Forbidden:
                    print(f"Недостаточно прав для перемещения {member.display_name}")
                except nextcord.HTTPException as e:
                    print(f"Ошибка перемещения {member.display_name}: {e}")


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None:
        activity = member.activity
        if activity and activity.type == nextcord.ActivityType.playing and "Dota 2" in activity.name:
            target_channel = bot.get_channel(TARGET_VOICE_CHANNEL_ID)
            if target_channel and after.channel.id != TARGET_VOICE_CHANNEL_ID:
                try:
                    await member.move_to(target_channel)
                    print(f"Перемещён {member.display_name} в канал {target_channel.name}")
                except nextcord.Forbidden:
                    print(f"Недостаточно прав для перемещения {member.display_name}")
                except nextcord.HTTPException as e:
                    print(f"Ошибка перемещения {member.display_name}: {e}")


@bot.slash_command(name="time", description="Выводит текущее время в канал #штаб")
async def time(interaction: nextcord.Interaction):
    if interaction.channel.id == STAFF_CHANNEL_ID:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await interaction.response.send_message(f"Текущее время: {current_time}")
    else:
        await interaction.response.send_message("Эту команду можно использовать только в канале #штаб.", ephemeral=True)


@bot.slash_command(name="tarkov", description="Перебрасывает указанных пользователей в канал для Escape from Tarkov")
async def tarkov(interaction: nextcord.Interaction):
    user_tags = ["!"]
    target_channel = bot.get_channel(TARGET_VOICE_CHANNEL_ID)

    if not target_channel:
        await interaction.response.send_message("Не удалось найти канал для Tarkov.", ephemeral=True)
        return

    moved_members = []
    for member in interaction.guild.members:
        if f"{member.name}#{member.discriminator}" in user_tags and member.voice and member.voice.channel:
            try:
                await member.move_to(target_channel)
                moved_members.append(member.display_name)
            except nextcord.Forbidden:
                await interaction.response.send_message(f"Недостаточно прав для перемещения {member.display_name}",
                                                        ephemeral=True)
            except nextcord.HTTPException as e:
                await interaction.response.send_message(f"Ошибка перемещения {member.display_name}: {e}",
                                                        ephemeral=True)

    if moved_members:
        await interaction.response.send_message(
            f"Следующие пользователи были перемещены в канал {target_channel.name}: {', '.join(moved_members)}")
    else:
        await interaction.response.send_message("Ни один из указанных пользователей не был найден в голосовых каналах.",
                                                ephemeral=True)


@bot.slash_command(name="song", description="Включаем музыку")
async def song(interaction: nextcord.Interaction, track: str):
    channel = interaction.user.voice.channel if interaction.user.voice else None
    if not channel:
        await interaction.response.send_message("Вы должны быть в голосовом канале, чтобы использовать эту команду.",
                                                ephemeral=True)
        return

    try:
        vc = await channel.connect()

        ydl_opts = {"format": "bestaudio", "quiet": True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{track}", download=False)["entries"][0]
            url = info["url"]

        vc.play(nextcord.FFmpegPCMAudio(executable="ffmpeg", source=url))
        await interaction.response.send_message(f"Сейчас играет: {info['title']}")

    except nextcord.ClientException:
        await interaction.response.send_message("Бот уже подключён к другому голосовому каналу.", ephemeral=True)
    except FileNotFoundError:
        await interaction.response.send_message("FFmpeg не найден. Проверьте установку и настройки PATH.",
                                                ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Ошибка при воспроизведении трека: {e}", ephemeral=True)


bot.run(TOKEN)
