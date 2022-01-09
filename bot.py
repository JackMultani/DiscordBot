import discord
import sqlite3
from keepalive import keep_alive

client = discord.Client()
//token has been removed for code from privacy purposes

def add_player(player):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT Name FROM main WHERE Name =?", [player])
    result = cursor.fetchone()
    if (len(player) > 20):
        return False
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
        cursor.execute("UPDATE main SET Wins = ? WHERE Name = ?", (wins, player))
        db.commit()
        cursor.close()
        db.close()
        return True

def set_loss(player, losses):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT Name FROM main WHERE Name =?", [player])
    result = cursor.fetchone()
    if result is None:
        return False
    elif result is not None:
        cursor.execute("SELECT Losses FROM main WHERE Name =?", [player])
        cursor.execute("UPDATE main SET Losses = ? WHERE Name = ?", (losses, player))
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
def list_wins():
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM main ORDER BY Wins DESC")
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('5v5 | -help'))
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #Says hello
    if message.content.startswith('-hello'):
        await message.channel.send('i love league')
    #Adds player to database
    if message.content.startswith("-add"):
        test = message.content.split("-add ")
        if(len(test)== 1):
            return
        player = message.content.split("-add ", 1)[1]
        result = add_player(player)
        if (result == True):
            await message.channel.send(f"{player} has been added!")
        elif (result == False):
            if(len(player) > 20):
                await message.channel.send(f"{player} exceeds **20 characters**! {player} not added.")
            else:
                await message.channel.send(f"{player} is already in database!")
    #Incrementing win for a player
    if message.content.startswith("-win"):
        test = message.content.split("-win ")
        if(len(test)== 1):
            return
        player = message.content.split("-win ", 1)[1]
        result = add_win(player)
        if (result == True):
            await message.channel.send(f"{player}'s wins have been incremented.")
        elif (result == False):
            await message.channel.send(f"{player} does not exist in database! Create a player using `-add (player)`.")
    #Incrementing loss for a player
    if message.content.startswith("-loss"):
        test = message.content.split("-loss ")
        if(len(test)== 1):
            return
        player = message.content.split("-loss ", 1)[1]
        result = add_loss(player)
        if (result == True):
            await message.channel.send(f"{player}'s losses have been incremented :(")
        elif (result == False):
            await message.channel.send(f"{player} does not exist in database! Create a player using `-add (player)`.")
    #Setting wins for a player
    if message.content.startswith("-setwin"):
        test = message.content.split("-setwin ")
        if(len(test)== 1):
            return
        player = message.content.split()[1]
        wins = message.content.split()[2]
        result = set_win(player, wins)
        if (result == True):
            await message.channel.send(f"{player}'s win total has been set to {wins}")
        elif (result == False):
            await message.channel.send(f"{player} does not exist in database! Create a player using `-add (player)`.")
    #Setting losses for a player
    if message.content.startswith("-setloss"):
        test = message.content.split("-setloss ")
        if(len(test)== 1):
            return
        player = message.content.split()[1]
        losses = message.content.split()[2]
        result = set_loss(player, losses)
        if (result == True):
            await message.channel.send(f"{player}'s loss total has been set to {losses}")
        elif (result == False):
            await message.channel.send(f"{player} does not exist in database! Create a player using `-add (player)`.")
    #Reset stats for a player
    if message.content.startswith("-reset"):
        test = message.content.split("-reset ")
        if(len(test)== 1):
            return
        player = message.content.split("-reset ", 1)[1]
        result = reset(player)
        if (result == True):
            await message.channel.send(f"{player}'s stats have been reset.")
        elif (result == False):
            await message.channel.send(f"{player} does not exist in database! Create a player using `-add (player)`.")
    #Delete a player
    if message.content.startswith("-delete"):
        test = message.content.split("-delete ")
        if(len(test)== 1):
            return
        player = message.content.split("-delete ", 1)[1]
        result = delete(player)
        if (result == True):
            await message.channel.send(f"{player}'s stats has been deleted.")
        elif (result == False):
            await message.channel.send(f"{player} does not exist.")
    #List sorted by wins
    if message.content.startswith("-ranks"):
        result = list_wins()
        if result is not None:
            count = 0
            for x in result:
                count = count + 1
            if (count == 0):
                await message.channel.send(f"No players exist in database. Create a player using `-add (player)`.")
            elif (count != 0):
                place = 1
                string = ""
                for x in result:
                    name = x[0]
                    wins = x[1]
                    losses = x[2]
                    games = wins + losses
                    if(games == 0):
                        winrate = "N/A"
                    else:
                        winrate = (wins/games)*100
                        winrate = int(winrate)
                    winrate = str(winrate)
                
                    wins = str(wins)
                    losses = str(losses)
                    name = str(name)
                    win_spaces = 25 - len(name)
            
                    loss_spaces = 15
                    winrate_spaces = 18
                    if(place == 1):
                        string = string + ' **#' + str(place) + '** `' + name + (' '*win_spaces) + wins + (' '*loss_spaces) + losses + (' '*winrate_spaces) + winrate + '`\n'
                    else:
                        string = string + '**#' + str(place) + '** `' + name + (' '*win_spaces) + wins + (' '*loss_spaces) + losses + (' '*winrate_spaces) + winrate + '`\n'

                    place = place + 1
                await message.channel.send('**Rankings**\n\n' + '      Player                                      Wins                      Losses                       Winrate (%)' + '\n' + '-'*90 + '\n' + string)
    #Team win
    if message.content.startswith("-teamwin"):
        totalplayers = message.content.split(',')
        firstplayer = totalplayers[0]
        firstplayer = firstplayer.split()
        count = 0
        error_check = 0
        if(len(firstplayer) == 1):
            return
        result = add_win(firstplayer[1])
        if (result == False):
                await message.channel.send(f"{firstplayer[1]} does not exist in database! Win not added for {firstplayer[1]}. Create a player using `-add (player)`.")
                error_check = error_check + 1
                if(len(totalplayers) == 1):
                    return
        for x in totalplayers:
            if (count == 0):
                count = count + 1
                continue
            result = add_win(x)
            if (result == False):
                error_check = error_check + 1
                await message.channel.send(f"{x} does not exist in database! Win not added for {x}. Create a player using `-add (player)`.")
        if (error_check == 0):
            await message.channel.send(f"Wins added for all inputted players! GG!")
            final_list = list_wins()
            place = 1
            string = ""
            for x in final_list:
                    name = x[0]
                    wins = x[1]
                    losses = x[2]
                    games = wins + losses
                    if(games == 0):
                        winrate = "N/A"
                    else:
                        winrate = (wins/games)*100
                        winrate = int(winrate)
                    winrate = str(winrate)
                
                    wins = str(wins)
                    losses = str(losses)
                    name = str(name)
                    win_spaces = 25 - len(name)
            
                    loss_spaces = 15
                    winrate_spaces = 18
                    if(place == 1):
                        string = string + ' **#' + str(place) + '** `' + name + (' '*win_spaces) + wins + (' '*loss_spaces) + losses + (' '*winrate_spaces) + winrate + '`\n'
                    else:
                        string = string + '**#' + str(place) + '** `' + name + (' '*win_spaces) + wins + (' '*loss_spaces) + losses + (' '*winrate_spaces) + winrate + '`\n'

                    place = place + 1
            await message.channel.send('**\nUpdated Rankings**\n\n' + '      Player                                      Wins                      Losses                       Winrate (%)' + '\n' + '-'*90 + '\n' + string)
        else:
            await message.channel.send(f"Wins added for __existing__ inputted players! GG!")
            final_list = list_wins()
            place = 1
            string = ""
            for x in final_list:
                    name = x[0]
                    wins = x[1]
                    losses = x[2]
                    games = wins + losses
                    if(games == 0):
                        winrate = "N/A"
                    else:
                        winrate = (wins/games)*100
                        winrate = int(winrate)
                    winrate = str(winrate)
                
                    wins = str(wins)
                    losses = str(losses)
                    name = str(name)
                    win_spaces = 25 - len(name)
            
                    loss_spaces = 15
                    winrate_spaces = 18
                    if(place == 1):
                        string = string + ' **#' + str(place) + '** `' + name + (' '*win_spaces) + wins + (' '*loss_spaces) + losses + (' '*winrate_spaces) + winrate + '`\n'
                    else:
                        string = string + '**#' + str(place) + '** `' + name + (' '*win_spaces) + wins + (' '*loss_spaces) + losses + (' '*winrate_spaces) + winrate + '`\n'

                    place = place + 1
            await message.channel.send('**\nUpdated Rankings**\n\n' + '      Player                                      Wins                      Losses                       Winrate (%)' + '\n' + '-'*90 + '\n' + string)

    #Team loss
    if message.content.startswith("-teamloss"):
        totalplayers = message.content.split(',')
        firstplayer = totalplayers[0]
        firstplayer = firstplayer.split()
        count = 0
        error_check = 0
        if(len(firstplayer) == 1):
            return
        result = add_loss(firstplayer[1])
        if (result == False):
                await message.channel.send(f"{firstplayer[1]} does not exist in database! Loss not added for {firstplayer[1]}. Create a player using `-add (player)`.")
                error_check = error_check + 1
                if(len(totalplayers) == 1):
                    return
        for x in totalplayers:
            if (count == 0):
                count = count + 1
                continue
            result = add_loss(x)
            if (result == False):
                error_check = error_check + 1
                await message.channel.send(f"{x} does not exist in database! Loss not added for {x}. Create a player using `-add (player)`.")
        if (error_check == 0):
            await message.channel.send(f"Losses added for all inputted players! :(")
            final_list = list_wins()
            place = 1
            string = ""
            for x in final_list:
                    name = x[0]
                    wins = x[1]
                    losses = x[2]
                    games = wins + losses
                    if(games == 0):
                        winrate = "N/A"
                    else:
                        winrate = (wins/games)*100
                        winrate = int(winrate)
                    winrate = str(winrate)
                
                    wins = str(wins)
                    losses = str(losses)
                    name = str(name)
                    win_spaces = 25 - len(name)
            
                    loss_spaces = 15
                    winrate_spaces = 18
                    if(place == 1):
                        string = string + ' **#' + str(place) + '** `' + name + (' '*win_spaces) + wins + (' '*loss_spaces) + losses + (' '*winrate_spaces) + winrate + '`\n'
                    else:
                        string = string + '**#' + str(place) + '** `' + name + (' '*win_spaces) + wins + (' '*loss_spaces) + losses + (' '*winrate_spaces) + winrate + '`\n'

                    place = place + 1
            await message.channel.send('**\nUpdated Rankings**\n\n' + '      Player                                      Wins                      Losses                       Winrate (%)' + '\n' + '-'*90 + '\n' + string)
        else:
            await message.channel.send(f"Losses added for __existing__ inputted players! :(")
            final_list = list_wins()
            place = 1
            string = ""
            for x in final_list:
                    name = x[0]
                    wins = x[1]
                    losses = x[2]
                    games = wins + losses
                    if(games == 0):
                        winrate = "N/A"
                    else:
                        winrate = (wins/games)*100
                        winrate = int(winrate)
                    winrate = str(winrate)
                
                    wins = str(wins)
                    losses = str(losses)
                    name = str(name)
                    win_spaces = 25 - len(name)
            
                    loss_spaces = 15
                    winrate_spaces = 18
                    if(place == 1):
                        string = string + ' **#' + str(place) + '** `' + name + (' '*win_spaces) + wins + (' '*loss_spaces) + losses + (' '*winrate_spaces) + winrate + '`\n'
                    else:
                        string = string + '**#' + str(place) + '** `' + name + (' '*win_spaces) + wins + (' '*loss_spaces) + losses + (' '*winrate_spaces) + winrate + '`\n'

                    place = place + 1
            await message.channel.send('**\nUpdated Rankings**\n\n' + '      Player                                      Wins                      Losses                       Winrate (%)' + '\n' + '-'*90 + '\n' + string)
    #Help page
    if message.content.startswith("-help"):
        typehelp = message.content.split('-help ')
        if(len(typehelp) == 1):
            await message.channel.send('''The usable commands are listed below. **All commands** must begin with a `-`\n
            `add`    `delete`    `win`    `loss`    `ranks`\n
            `setwin`    `setloss`    `teamwin`    `teamloss`\n\n**For more information** on how to use each command, type `-help (command)`.''')
        elif(len(typehelp) == 2):
            if(typehelp[1] == 'add'):
                await message.channel.send('`-add (player)`\n\nAdds a player to database with their wins and losses set to 0. Player names must be **unique** and cannot be longer than **20 characters**.\n\n\tEx:  `-add Bob`')
            elif(typehelp[1] == 'delete'):
                await message.channel.send('`-delete (player)`\n\nDeletes an existing player from the database.\n\n\tEx:  `-delete Bob`')
            elif(typehelp[1] == 'win'):
                await message.channel.send("`-win (player)`\n\nAdds 1 win to a player's win total.\n\n\tEx:  `-win Bob`")
            elif(typehelp[1] == 'loss'):
                await message.channel.send("`-loss (player)`\n\nAdds 1 loss to a player's loss total.\n\n\tEx: `-loss Bob`")
            elif(typehelp[1] == 'setwin'):
                await message.channel.send("`-setwin (player) (value)`\n\nSets a player's win total to a specified value\n\n\tEx: `-setwin Bob 10`\n\tBob now has a win total of **10**")
            elif(typehelp[1] == 'setloss'):
                await message.channel.send("`-setloss (player) (value)`\n\nSets a player's loss total to a specified value\n\n\tEx: `-setloss Bob 15`\n\tBob now has a loss total of **15**")
            elif(typehelp[1] == 'teamwin'):
                await message.channel.send("`-teamwin (player1),(player2),(player3),etc.`\n\nAdds 1 win to each specified player. Players must be **separated by a comma without spaces**.\n\n\tEx: `-teamwin Bob,Tom,Ron`")
            elif(typehelp[1] == 'teamloss'):
                await message.channel.send("`-teamloss (player1),(player2),(player3),etc.`\n\nAdds 1 loss to each specified player. Players must be **separated by a comma without spaces**.\n\n\tEx: `-teamloss Bob,Tom,Ron`")
            elif(typehelp[1] == 'ranks'):
                await message.channel.send('`-ranks`\n\nDisplays the rankings of each player in the database by wins.')
            elif(typehelp[1] == 'help'):
                await message.channel.send('`-help`\n\nDisplays a page with usable commands.')
keep_alive()
client.run(token)
