import discord
import sqlite3

client = discord.Client()
token = 'OTIwNDUxNDg3MjkxODMwMjky.YbkjPw.-PAcIuwG1qfwm2NKNsYllQq3580'

def add_player(player):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT Name FROM main WHERE Name =?", [player])
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO main(Name, Wins, Losses) VALUES (?, ?, ?)")
        val = (player, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        return True
    elif result is not None:
        return False

def add_win(player):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT Name FROM main WHERE Name =?", [player])
    result = cursor.fetchone()
    if result is None:
        return False
    elif result is not None:
        cursor.execute("SELECT Wins FROM main WHERE Name =?", [player])
        cursor.execute("UPDATE main SET Wins = Wins + 1 WHERE Name = ?", [player])
        db.commit()
        cursor.close()
        db.close()
        return True

def add_loss(player):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT Name FROM main WHERE Name =?", [player])
    result = cursor.fetchone()
    if result is None:
        return False
    elif result is not None:
        cursor.execute("SELECT Losses FROM main WHERE Name =?", [player])
        cursor.execute("UPDATE main SET Losses = Losses + 1 WHERE Name = ?", [player])
        db.commit()
        cursor.close()
        db.close()
        return True

def set_win(player, wins):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT Name FROM main WHERE Name =?", [player])
    result = cursor.fetchone()
    if result is None:
        return False
    elif result is not None:
        cursor.execute("SELECT Wins FROM main WHERE Name =?", [player])
        cursor.execute("UPDATE main SET Wins = ? WHERE Name = ?", wins, [player])
        db.commit()
        cursor.close()
        db.close()
        return True
    
def reset(player):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT Name FROM main WHERE Name =?", [player])
    result = cursor.fetchone()
    if result is None:
        return False
    elif result is not None:
        cursor.execute("SELECT Losses FROM main WHERE Name =?", [player])
        cursor.execute("UPDATE main SET Losses = 0 WHERE Name = ?", [player])
        db.commit()
        cursor.execute("SELECT Wins FROM main WHERE Name =?", [player])
        cursor.execute("UPDATE main SET Wins = 0 WHERE Name = ?", [player])
        db.commit()
        cursor.close()
        db.close()
        return True
def delete(player):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT Name FROM main WHERE Name =?", [player])
    result = cursor.fetchone()
    if result is None:
        return False
    elif result is not None:
        cursor.execute("DELETE FROM main WHERE Name =?", [player])
        db.commit()
        cursor.close()
        db.close()
        return True

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #Says hello
    if message.content.startswith('-hello'):
        await message.channel.send('Hello!')
    #Adds player to database
    if message.content.startswith("-add"):
        player = message.content.split("-add ", 1)[1]
        result = add_player(player)
        if (result == True):
            await message.channel.send(f"{player} has been added!")
        elif (result == False):
            await message.channel.send(f"{player} is already in database!")
    #Incrementing win for a player
    if message.content.startswith("-win"):
        player = message.content.split("-win ", 1)[1]
        result = add_win(player)
        if (result == True):
            await message.channel.send(f"{player}'s wins have been incremented.")
        elif (result == False):
            await message.channel.send(f"{player} does not exist in database! Create player using -add (player).")
    #Incrementing loss for a player
    if message.content.startswith("-loss"):
        player = message.content.split("-loss ", 1)[1]
        result = add_loss(player)
        if (result == True):
            await message.channel.send(f"{player}'s losses have been incremented :(")
        elif (result == False):
            await message.channel.send(f"{player} does not exist in database! Create player using -add (player).")
    #Setting wins for a player
    if message.content.startswith("-setwin"):
        player = message.content.split(" ", 1)[1]
        wins = message.content.split(" ", 1)[2]
        result = set_win(player)
        if (result == True):
            await message.channel.send(f"{player}'s wins total has been set to {wins}")
        elif (result == False):
            await message.channel.send(f"{player} does not exist in database! Create player using -add (player).")
    #Reset stats for a player
    if message.content.startswith("-reset"):
        player = message.content.split("-reset ", 1)[1]
        result = reset(player)
        if (result == True):
            await message.channel.send(f"{player}'s stats have been reset.")
        elif (result == False):
            await message.channel.send(f"{player} does not exist in database! Create player using -add (player).")
    #Delete a player
    if message.content.startswith("-delete"):
        player = message.content.split("-delete ", 1)[1]
        result = delete(player)
        if (result == True):
            await message.channel.send(f"{player}'s stats has been deleted.")
        elif (result == False):
            await message.channel.send(f"{player} already does not exist.")
client.run(token)
