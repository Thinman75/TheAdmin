#------------------------------------------------------------------------------------------------------------------
#To-do:
# - Add a command to add information to all of the logs such as fixes to the code or corrections (Not super important)
#------------------------------------------------------------------------------------------------------------------
from discord.ext import commands
from time import sleep
import discord
import asyncio
import datetime
import subprocess
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
#Global Variables:
LOGCHANNELID = "382730239698010123"
#LOGCHANNELID = "384482700636979210"

#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
def serverStatus(strChoices : str): #Basically just the status command but able to be used by any other command. Servers to choose from: 1 3 4 5 6 All or All+test

  if(len(strChoices) < 1):
    em = discord.Embed(title='Error', description="No Input recived, please input at least one server", colour=0xFF0000, timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
    return(em)
  elif(len(strChoices) > 5):
    em = discord.Embed(title='Error', description="Too many inputs recived, please only input a max of five", colour=0xFF0000, timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
    return(em)
  else:
    timeStamp = datetime.datetime.strftime(datetime.datetime.now(),"%b-%d-%Y %I:%M:%S:%f %p") #Used in absolute emergencys for logging purposes, down in the major issue hadeling
    teststring = ArkServer("status",strChoices)
    outputstring = " "
    varcolor = 0x008000
    test = teststring.splitlines()
    for line in  test:
      if '---Server-' in line:
        outputstring += line + "\n"
      if '●' in line:
        outputstring += line + "\n"
      if 'Active:' in line:
        if ' active' in line:
          outputstring += line + "\n"
        elif ' failed' in line:
          outputstring += "***" + line + "***\n"
          varcolor = 0xFF0000
        elif '(dead)' in line:
          outputstring += "***" + line + "*** ***...It's dead Jim.***\n"
          varcolor = 0x500090
        else:
          print("MAJOR ISSUE")
          f = open("Log.txt", "a")
          f.write("--------------Status-Error--------------\nCommand Used: status " + ' '.join(strChoices) + "\nA MAJOR UNKNOWN ISSUE HAS OCCURED WITH THE SERVER\nTimeStamp of Use: " + timeStamp + "\n----------------------------------------\n")
          f.close()
          outputstring += "\n\n***A MAJOR UNKNOWN ISSUE HAS OCCURED***\n\n"+ line + "\n"
          varcolor = 0xffff00
      if 'Memory:' in line:
        outputstring += line + "\n"
      if 'CPU:' in line:
        outputstring += line + "\n\n"
    em = discord.Embed(title='Results', description=outputstring, colour=varcolor, timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
    return(em)
#------------------------------------------------------------------------------------------------------------------
def authAdmin(USERID, COMMAND):
  timeStamp = datetime.datetime.strftime(datetime.datetime.now(),"%b-%d-%Y %I:%M:%S:%f %p")
  try:
    f = open("Admin.txt", "rb")
    adminList = f.readlines()
    f.close()
  except IOError:
    print("---------------File-Error---------------")
    print("Admin.txt, Using built in Admin list")
    print("----------------------------------------")
    adminList = ['90587751618981888', '170300974299217920']

  for line in adminList:
    #print("\n\n\n" + str(adminList) + "\n\n\n")
    if(COMMAND == "NoReport"): #Allows for none security related checks of the list
      if str.encode(USERID) in line:
        return(True)
    else:
      if str.encode(USERID) in line:
        PassString = "\n-----------Admin-Command-Used-----------\nCommand Used: " + COMMAND + "\nAuthor of Command: " + USERID + "\nTimeStamp of Use: " + timeStamp + "\n----------------------------------------\n"
        print(PassString)
        f = open("Log.txt", "a")
        f.write(PassString)
        f.close()
        return(True)

  if(COMMAND == "NoReport"):
    return(False)
  FailString = "\n------------Unauthorized-Use------------\nCommand To be Used: " + COMMAND + "\nAuthor of Command: " + USERID + "\nTimeStamp of Attempt: " + timeStamp + "\n----------------------------------------\n"
  print(FailString)
  f = open("Log.txt", "a")
  f.write(FailString)
  f.close()
  return(False)

#------------------------------------------------------------------------------------------------------------------
def authArkAdmin(USERID, COMMAND):
  timeStamp = datetime.datetime.strftime(datetime.datetime.now(),"%b-%d-%Y %I:%M:%S:%f %p")
  try:
    f = open("ArkAdmin.txt", "r")
    adminList = f.readlines()
    f.close()
  except IOError:
    FailString = "---------------File-Error---------------\nArkAdmin.txt, No File in Use\n----------------------------------------"
    print(FailString)
    f = open("Log.txt", "a")
    adminList = []

  for line in adminList:
    if(COMMAND == "NoReport"): #Allows for none security related checks of the list
      if USERID in line: 
        return(True)
    else:
      if USERID in line:
        PassString = "\n---------Ark-Admin-Command-Used---------\nCommand Used: " + COMMAND + "\nAuthor of Command: " + USERID + "\nTimeStamp of Use: " + timeStamp + "\n----------------------------------------\n"
        print(PassString)
        f = open("Log.txt", "a")
        f.write(PassString)
        f.close()
        return(True)
  if(COMMAND == "NoReport"):
    return(False)
  FailString = "\n----------Unauthorized-Attempt----------\nCommand To be Used: " + COMMAND + "\nAuthor of Command: " + USERID + "\nTimeStamp of Attempt: " + timeStamp + "\n----------------------------------------\n"
  print(FailString)
  f = open("Log.txt", "a")
  f.write(FailString)
  f.close()
  return(False)
#------------------------------------------------------------------------------------------------------------------
def fastSSH(HOST,COMMAND):
  if(HOST == '1.1'):
    HOST = "craft@192.168.1.191"
    MAP = "arkhelix_TheIsland.service"
  elif(HOST == '1.2'):
    HOST = "craft@192.168.1.191"
    MAP = "arkhelix_Ragnarok.service"
  elif(HOST == '4'):
    HOST = "craft@192.168.1.194"
    MAP = "arkhelix_ScorchedEarth_P.service"
  elif(HOST == '5'):
    HOST = "craft@192.168.1.195"
    MAP = "arkhelix_TheIslandTest.service"
  elif(HOST == '6'):
    HOST = "craft@192.168.1.196"
    MAP = "arkhelix_TheCenter.service"
  else:
    print("fastSSH Command usage error")
    quit()

  if(COMMAND.lower() == "start"):
    COMMAND = "sudo systemctl start " + MAP
  elif(COMMAND.lower() == "status"):
    COMMAND = "systemctl status " + MAP
  elif(COMMAND.lower() == "stop"):
    COMMAND = "sudo systemctl stop " + MAP
  elif(COMMAND.lower() == "daemon"):
    COMMAND = "sudo systemctl daemon-reload"
  elif(COMMAND.lower() == "arkupdate"):
    COMMAND = "bash /var/share/programs/GameUpdateScript.sh"
  elif(COMMAND.lower() == "arkmodupdate"):
    COMMAND = "bash /var/share/programs/ModUpdateScript.sh"
  else:
    print("fastSSH Command usage error")
    quit()

  ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  return(b''.join(ssh.stdout.readlines()).decode("utf-8"))
#------------------------------------------------------------------------------------------------------------------
def ArkServer(COMMAND,SERVERS : str):
  outputStr = "Output:"

  if(len(SERVERS) < 1):
     print("ERROR")
     outputStr = "No Input Received"
  elif(len(SERVERS) > 5):
    print("MAXERROR")
    outputStr = "Too Many Imputs Received"
  else:
    SERVERS = [x.lower() for x in list(SERVERS)]
    if('all' in SERVERS):
      SERVERS = ["1.1","1.2","4","6"]
    if('all+test' in SERVERS):
      SERVERS = ["1.1","1.2","4","5","6"]
    if('1.1' in SERVERS):
      outputStr = outputStr + "\n\n--------------Server-1.1------------\n\n" + fastSSH("1.1",COMMAND)
    if('1.2' in SERVERS):
      outputStr = outputStr + "\n\n--------------Server-1.2------------\n\n" + fastSSH("1.2",COMMAND)
    if('4' in SERVERS):
      outputStr = outputStr + "\n\n--------------Server-4--------------\n\n" + fastSSH("4",COMMAND)
    if('5' in SERVERS):
      outputStr = outputStr + "\n\n--------------Server-5--------------\n\n" + fastSSH("5",COMMAND)
    if('6' in SERVERS):
      outputStr = outputStr + "\n\n--------------Server-6--------------\n\n" + fastSSH("6",COMMAND)
  return(outputStr)
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
class ArkServers():
    def __init__(self, bot):
        self.bot = bot
#------------------------------------------------------------------------------------------------------------------
    @commands.command(pass_context=True,no_pm=True,description='Servers to choose from: 1.1 1.2 4 5 6 All or All+test')
    async def status(self,ctx,*strChoices : str):
     """Displays server status"""
     if(len(strChoices) < 1):
       em = discord.Embed(title="Error", description="No Input recived, please input at least one server", colour=0xFF0000, timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
       await self.bot.send_message(ctx.message.channel,embed=em)
     elif(len(strChoices) > 5):
       em = discord.Embed(title="Error", description="Too many inputs recived, please only input a max of five", colour=0xFF0000, timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
       await self.bot.send_message(ctx.message.channel,embed=em)
     else:
       timeStamp = datetime.datetime.strftime(datetime.datetime.now(),"%b-%d-%Y %I:%M:%S:%f %p") #Used in absolute emergencys for logging purposes, down in the major issue hadeling
       teststring = ArkServer("status",strChoices)
       outputstring = " "
       varcolor = 0x008000

       test = teststring.splitlines()
       for line in  test:
         if '---Server-' in line:
           outputstring += line + "\n"
         if '●' in line:
           outputstring += line + "\n"
         if 'Active:' in line:
           if 'active' in line:
             outputstring += line + "\n"
           elif 'failed' in line:
             outputstring += "***" + line + "***\n"
             varcolor = 0xFF0000
           elif '(dead)' in line:
             outputstring += "***" + line + "*** ***...It's dead Jim.***\n" #Probably overkill as message simply means the server has never been started
             varcolor = 0x500090
           else:
             print("MAJOR ISSUE")
             f = open("Log.txt", "a")
             f.write("--------------Status-Error--------------\nCommand Used: status " + ' '.join(strChoices) + "\nA MAJOR UNKNOWN ISSUE HAS OCCURED WITH THE SERVER\nTimeStamp of Use: " + timeStamp + "\n----------------------------------------\n")
             f.close()
             outputstring += "\n\n***MAJOR UNKNOWN ISSUE OCCURED***\n\n"+ line + "\n"
             varcolor = 0xffff00
             await self.bot.send_message(discord.Object(id=LOGCHANNELID), "A MAJOR UNKNOWN ISSUE HAS ARISEN")
         if 'Memory:' in line:
           outputstring += line + "\n"
         if 'CPU:' in line:
           outputstring += line + "\n\n"

       em = discord.Embed(title='Results', description=outputstring, colour=varcolor, timestamp = datetime.datetime.now()+ datetime.timedelta(hours=5))
       await self.bot.send_message(ctx.message.channel,embed=em)
#------------------------------------------------------------------------------------------------------------------
    @commands.command(pass_context=True,description='Servers to choose from: 1.1 1.2 4 5 6 All or All+test')
    async def start(self,ctx,*strChoices : str):
       """* Starts the server and reloads the daemon"""
       if(authArkAdmin(ctx.message.author.id, "start " + ' '.join(strChoices))):
         em = discord.Embed(title="Ark Admin Command Used",description="Command Used: start " + ' '.join(strChoices) +  "\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff9933 ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
         ArkServer("daemon",strChoices)
         ArkServer("start",strChoices)
         await self.bot.send_message(ctx.message.channel,embed = serverStatus(strChoices))
       else:
         em = discord.Embed(title="Unauthorized Attempt",description="Command To be Used: start " + ' '.join(strChoices) +"\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff0000,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
         await self.bot.say("You are not Authorized to use this command. This attempt will be logged.")
#------------------------------------------------------------------------------------------------------------------
    @commands.command(pass_context=True,description='Servers to choose from: 1.1 1.2 4 5 6 All or All+test')
    async def stop(self,ctx,*strChoices : str):
       """* KILLS THE SERVER"""
       if(authArkAdmin(ctx.message.author.id, "stop " + ' '.join(strChoices))):
         em = discord.Embed(title="Ark Admin Command Used",description="Command Used: stop " + ' '.join(strChoices) +  "\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff9933 ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
         ArkServer("stop",strChoices)
         await self.bot.send_message(ctx.message.channel,embed = serverStatus(strChoices))
       else:
         em = discord.Embed(title="Unauthorized Attempt",description="Command To be Used: stop " + ' '.join(strChoices) +"\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff0000,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
         await self.bot.say("You are not Authorized to use this command. This attempt will be logged.")
#------------------------------------------------------------------------------------------------------------------
    @commands.command(pass_context=True,description='Servers to choose from: 1.1 1.2 4 5 6 All or All+test')
    async def refresh(self,ctx,*strChoices : str):
       """* Reloads the daemon refreshing the .services"""
       if(authArkAdmin(ctx.message.author.id, "refresh " + ' '.join(strChoices))):
         em = discord.Embed(title="Ark Admin Command Used",description="Command Used: refresh " + ' '.join(strChoices) +  "\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff9933 ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
         ArkServer("daemon",strChoices)
         await self.bot.say("the daemon has been reloaded")
       else:
         em = discord.Embed(title="Unauthorized Attempt",description="Command To be Used: refresh " + ' '.join(strChoices) +"\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff0000,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
         await self.bot.say("You are not Authorized to use this command. This attempt will be logged.")
#------------------------------------------------------------------------------------------------------------------
    @commands.command(pass_context=True, no_pm=True,description='This will affect every single server')
    async def restart(self,ctx):
       """* Stops, updates, and then starts all the servers"""
       if(authArkAdmin(ctx.message.author.id, "restart ")):
         em = discord.Embed(title="Ark Admin Command Used",description="Command Used: restart " + "\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff9933 ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)

         await self.bot.say("This will require some time")
         ArkServer("stop","all+test") #Note This stops test but will never restart it
         await self.bot.say("Server Stopping...\nUpdating the Game...")
         output = fastSSH("1","ArkUpdate")
         #print(output)
         await self.bot.say("Game updated.\nUpdating mods...")
         output = fastSSH("1","ArkModUpdate")
         #print(output)
         ArkServer("start","all")
         await self.bot.say("Server Starting...")
         await self.bot.send_message(ctx.message.channel,embed = serverStatus("all"))
       else:
         em = discord.Embed(title="Unauthorized Attempt",description="Command To be Used: restart " + "\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff0000,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
         await self.bot.say("You are not Authorized to use this command. This attempt will be logged.")
#------------------------------------------------------------------------------------------------------------------
    @commands.command(pass_context=True, no_pm=True,description='Servers to choose from: 1.1 1.2 4 5 6 All or All+test')
    async def quickRestart(self,ctx,*strChoices : str):
       """* Stops and then starts the server again"""
       if(authArkAdmin(ctx.message.author.id, "quickRestart " + ' '.join(strChoices))):
         em = discord.Embed(title="Ark Admin Command Used",description="Command Used:  quickRestart " + ' '.join(strChoices) +  "\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff9933 ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
         await self.bot.say("This will require a moment")
         ArkServer("stop",strChoices)
         await self.bot.say("Server Stopping...")
         sleep(15)
         ArkServer("start",strChoices)
         await self.bot.say("Server Starting...")
         sleep(15)
         await self.bot.send_message(ctx.message.channel,embed = serverStatus(strChoices))
       else:
         em = discord.Embed(title="Unauthorized Attempt",description="Command To be Used: quickRestart " + ' '.join(strChoices) + "\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff0000,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
         await self.bot.say("You are not Authorized to use this command. This attempt will be logged.")
#------------------------------------------------------------------------------------------------------------------
    @commands.command(pass_context=True, no_pm=True,description='Directly updates the mods on the cluster')
    async def updateArkMods(self,ctx):
       """* update the ark mods"""
       if(authArkAdmin(ctx.message.author.id, "updateArkMods")):
         em = discord.Embed(title="Ark Admin Command Used",description="Command Used: updateArkMods" + "\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff9933 ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)

         await self.bot.say("This will require a moment, updating mods...")
         output = fastSSH("1","ArkModUpdate")
         #print(output)
         await self.bot.say("Mods update complete")
       else:
         em = discord.Embed(title="Unauthorized Attempt",description="Command To be Used: updateArkMods" + "\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff0000,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
         await self.bot.say("You are not Authorized to use this command. This attempt will be logged.")

#------------------------------------------------------------------------------------------------------------------
    @commands.command(pass_context=True, no_pm=True,description='Directly updates the game on the cluster')
    async def updateArkGame(self,ctx):
       """* updates the game itself"""
       if(authArkAdmin(ctx.message.author.id, "updateArkGame")):
         em = discord.Embed(title="Ark Admin Command Used",description="Command Used: updateArkGame" + "\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff9933 ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)

         await self.bot.say("This will require a moment, updating the game...")
         output = fastSSH("1","ArkUpdate")
         #print(output)
         await self.bot.say("Game update complete")
       else:
         em = discord.Embed(title="Unauthorized Attempt",description="Command To be Used: updateArkGame"+"\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff0000,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
         await self.bot.say("You are not Authorized to use this command. This attempt will be logged.")

#------------------------------------------------------------------------------------------------------------------
    @commands.command(pass_context=True, no_pm=True,description='Directly updates both the game and the mods on the cluster')
    async def updateArk(self,ctx):
       """* update both the game and the mods"""
       if(authArkAdmin(ctx.message.author.id, "updateArk")):
         em = discord.Embed(title="Ark Admin Command Used",description="Command Used: updateArk" + "\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff9933 ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)

         await self.bot.say("This will require some time, updating mods...")
         output = fastSSH("1","ArkModUpdate")
         #print(output)
         await self.bot.say("Mod update complete, updating the game...")
         output = fastSSH("1","ArkUpdate")
         #print(output)
         await self.bot.say("Game update complete.\nFull update complete.")
       else:
         em = discord.Embed(title="Unauthorized Attempt",description="Command To be Used: updateArk" +"\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff0000,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
         await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
         await self.bot.say("You are not Authorized to use this command. This attempt will be logged.")

#------------------------------------------------------------------------------------------------------------------

    @commands.command(pass_context=True, no_pm=True,description='Use @user to add user to Ark Admin list')
    async def addArkAdmin(self, ctx):
       """** Allows only Admins to add Ark Admins"""
       try:
         if(len(ctx.message.mentions) != 1):
           raise RuntimeError
         else:
           if(authAdmin(str(ctx.message.author.id),"addArkAdmin @" + str(ctx.message.mentions[0]) + "\nUserID: " + str(ctx.message.mentions[0].id))):
             if(authArkAdmin(str(ctx.message.mentions[0].id),"NoReport")): 
               await self.bot.say(str(ctx.message.mentions[0]) + " is already an Ark Admin")
               em = discord.Embed(title="Admin Command Attempted Use",description="File Changed\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id) + "\nUser removed from Ark Admin: " + str(ctx.message.mentions[0]) + "\n - User ID: " + str(ctx.message.mentions[0].id), colour = 0xadd8e6 ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
               await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
             else:
               f = open("ArkAdmin.txt", "a")
               f.write(str(ctx.message.mentions[0].id) + "\n")
               f.close()
               print("--------------File-Changed--------------")
               print("Author of Command: " + str(ctx.message.author))
               print("Author ID: " + str(ctx.message.author.id))
               print("User added to Ark Admin: " + str(ctx.message.mentions[0]))
               print("User ID: " + str(ctx.message.mentions[0].id))
               print("----------------------------------------")
               em = discord.Embed(title="Admin Command Used",description="File Changed\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id) + "\nUser added to Ark Admin: " + str(ctx.message.mentions[0]) + "\n - User ID: " + str(ctx.message.mentions[0].id), colour = 0x0099ff ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
               await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
               await self.bot.say(str(ctx.message.mentions[0]) + " was added to the Ark Admin list")
           else:
             await self.bot.say("You are not Authorized to use this command. This attempt will be logged.")
             print("----------Unauthorized-Attempt----------")
             print("Author of Command: " + str(ctx.message.author))
             print("User to be Ark Admin: " + str(ctx.message.mentions[0]))
             print("----------------------------------------")

       except RuntimeError :
         print("---Add-Command-Usage-Error---")
         await self.bot.say("Please Include a single @user in your message")
#------------------------------------------------------------------------------------------------------------------
    @commands.command(pass_context=True, no_pm=True,description='Use @user to remove user from the Ark Admin list')
    async def removeArkAdmin(self, ctx):
       """** Allows only Admins to remove Ark Admins"""
       try:
         if(len(ctx.message.mentions) != 1):
           raise RuntimeError
         else:
           if(authAdmin(str(ctx.message.author.id),"removeAdmin @" + str(ctx.message.mentions[0]) + "\nUserID: " + str(ctx.message.mentions[0].id))):
             if(authArkAdmin(str(ctx.message.mentions[0].id),"NoReport")):

               checkstring = str(ctx.message.mentions[0].id)

               f = open("ArkAdmin.txt","r")
               lines = f.readlines()
               f.close()
               f = open("ArkAdmin.txt","w")
               for line in lines:
                 if line!=checkstring+"\n":
                   f.write(line)
               f.close()

               print("--------------File-Changed--------------")
               print("Author of Command: " + str(ctx.message.author))
               print("Author ID: " + str(ctx.message.author.id))
               print("User removed from Ark Admin: " + str(ctx.message.mentions[0]))
               print("User ID: " + str(ctx.message.mentions[0].id))
               print("----------------------------------------")
               em = discord.Embed(title="Admin Command Used",description="File Changed\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id) + "\nUser removed from Ark Admin: " + str(ctx.message.mentions[0]) + "\n - User ID: " + str(ctx.message.mentions[0].id), colour = 0x0099ff ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
               await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
               await self.bot.say(str(ctx.message.mentions[0]) + " was removed from the Ark Admin list")

             else:
               await self.bot.say(str(ctx.message.mentions[0]) + " isn't an Ark Admin")
               em = discord.Embed(title="Admin Command Attempted Use",description="File Changed\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id) + "\nUser removed from Ark Admin: " + str(ctx.message.mentions[0]) + "\n - User ID: " + str(ctx.message.mentions[0].id), colour = 0xadd8e6 ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
               await self.bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)

           else:
             await self.bot.say("You are not Authorized to use this command. This attempt will be logged.")
             print("----------Unauthorized-Attempt----------")
             print("Author of Command: " + str(ctx.message.author))
             print("User to be Ark Admin: " + str(ctx.message.mentions[0]))
             print("----------------------------------------")

       except RuntimeError :
         print("---Add-Command-Usage-Error---")
         await self.bot.say("Please Include a single @user in your message")

#------------------------------------------------------------------------------------------------------------------
#    @commands.command(description='test')
#    async def tester(self,*strChoices : str):
#      print("k")
#------------------------------------------------------------------------------------------------------------------
#    @commands.command(pass_context=True, no_pm=True,description='test')
#    async def test(self, ctx, *strChoices : str):
#       """Provides a test command"""
#       await self.bot.send_message(ctx.message.channel,embed = serverStatus(strChoices))
#       timeStamp = datetime.datetime.strftime(datetime.datetime.now(),"%b-%d-%Y %I:%M:%S:%f %p")
#       if(authArkAdmin(ctx.message.author.id, "example " + ' '.join(strChoices))):
#         await self.bot.say("K, Done")
#       else:
#         await self.bot.send_message(discord.Object(id=LOGCHANNELID), "\n----------Unauthorized-Attempt----------\nCommand To be Used: start " + ' '.join(strChoices) +"\nAuthor of Command: " + str(ctx.message.author) + "\nTimeStamp of Attempt: " + timeStamp + "\n----------------------------------------\n")
#         await self.bot.say("You are not Authorized to use this command. This attempt will be logged.")
#------------------------------------------------------------------------------------------------------------------

def setup(bot):
    bot.add_cog(ArkServers(bot))
#------------------------------------------------------------------------------------------------------------------
#Depreciated but useful reference Code
#------------------------------------------------------------------------------------------------------------------
#import subprocess
#import sys
#
#HOST="www.example.org"
## Ports are handled in ~/.ssh/config since we use OpenSSH
#COMMAND="uname -a"
#
#ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
#                       shell=False,
#                       stdout=subprocess.PIPE,
#                       stderr=subprocess.PIPE)
#result = ssh.stdout.readlines()
#if result == []:
#    error = ssh.stderr.readlines()
#    print >>sys.stderr, "ERROR: %s" % error
#else:
#    print result
#------------------------------------------------------------------------------------------------------------------
#    @commands.command(description='For displaying the status of said server')
#    async def simpleStatus(self):
#       """Displays server status"""
#       HOST = "craft@192.168.1.191"
#       COMMAND = "systemctl status arkhelix_TheIsland.service"
#      ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#       output1 = b''.join(ssh.stdout.readlines()).decode("utf-8")
#       await self.bot.say("OUTPUT: \n\n\n" + b''.join(ssh.stdout.readlines()).decode("utf-8"))
#------------------------------------------------------------------------------------------------------------------

