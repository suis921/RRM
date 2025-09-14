import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
  print(f"RRM is activated.")
  try:
    guild = discord.Object(id=1416633828788666569)
    synced = await client.tree.sync(guild=guild)
    print(f"Synchronized slash commands : {len(synced)}")
  except Exceptions as e:
    print(e)

@client.event
async def on_message(message):
  if message.author.bot:
    return
  if client.user in message.mentions:
    await message.add_reaction("✅")
  
  await client.process_commands(message)

# /check_reactionコマンド
@client.tree.command(name="check_reaction", description="指定したメッセージでリアクションしていないメンションユーザーを確認")
@app_commands.describe(message_id="確認したいメッセージのID", emoji="✅")
async def check_reaction(interaction: discord.Interaction, message_id: str, emoji: str):
  # メッセージ取得
  try:
    message = await interaction.channel.fetch_message(int(message_id))
  except:
    await interaction.response.send_message("メッセージが見つかりませんでした.", ephemeral=True)
    return
  
  # メンションされたユーザーを取得
  mentioned_users = message.mentions
  
  for role in message.role_mentions:
    for member in role.members:
      if not member.bot and member not in mentioned_users:
        mentioned_users.append(member)
        
  if not mentioned_users:
    await interaction.response.send_message("このメッセージにはメンションされたユーザーがいません.", ephemeral=True)
    return
  
  # リアクションを探す
  reaction = discord.utils.get(message.reactions, emoji=emoji)
  reacted_users = []
  if reaction:
    async for user in reaction_users():
      reacted_users.append(user)
  
  # リアクションしていないユーザーを判定
  not_reacted = [u.mention for u in mentioned_users if u not in reacted_users]
  
  if not_reacted:
    await interaction.response.send_message(f"未読のユーザー : {','.join(not_reacted)}.", ephemeral=True)
  else:
    await interaction.response.send_message(f"全員が既読しました.", ephemeral=True)


# 右クリックの「メッセージコマンド」
@client.tree.context_menu(name="既読チェック")
async def check_reaction_ctx(interaction: discord.Interaction, message: discord.Message):
  emoji = "✅"

  mentioned_users = message.mentions
  
  for role in message.role_mentions:
    for member in role.members:
      if not member.bot and member not in mentioned_users:
        mentioned_users.append(member)
        
  if not mentioned_users:
    await interaction.response.send_message("このメッセージにはメンションされたユーザーがいません.", ephemeral=True)
    return

  reaction = discord.utils.get(message.reactions, emoji=emoji)
  reacted_users = []
  if reaction:
    async for user in reaction.users():
      reacted_users.append(user)

  not_reacted = [u.mention for u in mentioned_users if u not in reacted_users]

  if not_reacted:
    await interaction.response.send_message(f"未読のユーザー : {', '.join(not_reacted)}", ephemeral=True)
  else:
    await interaction.response.send_message(f"全員が既読しました.", ephemeral=True)

client.run(DISCORD_TOKEN)