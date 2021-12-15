import discord
import sqlite3

client = discord.Client()
token = 'OTIwNDUxNDg3MjkxODMwMjky.YbkjPw.-PAcIuwG1qfwm2NKNsYllQq3580'

def add_player(message, player):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT Name FROM main WHERE Name = {player}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO main(Name, Wins, Losses) VALUES (?, ?, ?)")
        val = (player, 0, 0)
        cursor.execute(sql, val)
        message.channel.send(f"'{player}' has been added!")
    elif result is not None:
        message.channel.send(f"'{player}' is already in database!")
    db.commit()
    cursor.close()
    db.close()

def add_win(message, player):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT Name FROM main WHERE Name = {player}")
    result = cursor.fetchone()
    if result is None:
        message.channel.send(f"{player} does not exit in database. Win not added.")
    elif result is not None:
        cursor.execute(f"SELECT Wins FROM main WHERE Name = {player}")
        wins = int(cursor.fetchone())
        wins = wins + 1
        cursor.execute(f"SELECT Name FROM main WHERE Name = {player}")
        sql = ("UPDATE main SET Wins = ? WHERE Name = ?")
        val = (wins, player)
        message.channel.send(f"'{player}''s wins increased to '{wins}'.")
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('-hello'):
        await message.channel.send('Hello!')
    if message.content.startswith("-new"):
        player = message.content.split("-new ", 1)[1]
        add_player(message, player)
client.run(token)
