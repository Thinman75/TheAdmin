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
description = '''I control everything... Don't cross me.\n Commands marked with a * are usable by admins only, Unauthroized attempts to use them may result in a ban'''

# this specifies what extensions to load when the bot starts up
startup_extensions = ["ArkServers"]

bot = commands.Bot(command_prefix='!', description=description)
#------------------------------------------------------------------------------------------------------------------
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
      if USERID in line: return(True)
    else:
      if USERID in line:
        PassString = "\n---------Ark-Admin-Command-Used---------\nCommand Used: " + COMMAND + "\nAuthor of Command: " + USERID + "\nTimeStamp of Use: " + timeStamp + "\n----------------------------------------\n"
        print(PassString)
        f = open("Log.txt", "a")
        f.write(PassString)
        f.close()
        return(True)
  if(COMMAND == "NoReport"): return(False)
  FailString = "\n----------Unauthorized-Attempt----------\nCommand To be Used: " + COMMAND + "\nAuthor of Command: " + USERID + "\nTimeStamp of Attempt: " + timeStamp + "\n----------------------------------------\n"
  print(FailString)
  f = open("Log.txt", "a")
  f.write(FailString)
  f.close()
  return(False)
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='with the ban hammer'))
#------------------------------------------------------------------------------------------------------------------
@bot.command(pass_context=True)
async def load(ctx,extension_name : str):
    """** Loads an extension."""
    if(authAdmin(ctx.message.author.id, "start " + extension_name)):
      em = discord.Embed(title="Admin Command Used",description="Command Used: load " + extension_name +  "\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0x0099ff ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
      await bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
      try:
          bot.load_extension(extension_name)
      except (AttributeError, ImportError) as e:
          await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
          return
      await bot.say("{} loaded.".format(extension_name))
    else:
      em = discord.Embed(title="Unauthorized Attempt",description="Command To be Used: load " + extension_name +"\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff0000,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
      await bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
      await bot.say("You are not Authorized to use this command. This attempt will be logged.")
#------------------------------------------------------------------------------------------------------------------
@bot.command(pass_context=True)
async def unload(ctx,extension_name : str):
    """** Unloads an extension."""

    if(authAdmin(ctx.message.author.id, "start " + extension_name)):
      em = discord.Embed(title="Admin Command Used",description="Command Used: unload " + extension_name +  "\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0x0099ff ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
      await bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
      bot.unload_extension(extension_name)
      await bot.say("{} unloaded.".format(extension_name))

    else:
      em = discord.Embed(title="Unauthorized Attempt",description="Command To be Used: unload " + extension_name +"\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff0000,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
      await bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
      await bot.say("You are not Authorized to use this command. This attempt will be logged.")

#------------------------------------------------------------------------------------------------------------------
#@bot.command() #Left for giggles
#async def add(left : int, right : int):
#    """Adds two numbers together."""
#    await bot.say(left + right)
#------------------------------------------------------------------------------------------------------------------
@bot.command()
async def repeat(times : int, content='repeating...'):
    """* Repeats a message multiple times."""
    if(authArkAdmin(ctx.message.author.id, "start " + str(times) + content)):
      em = discord.Embed(title="Ark Admin Command Used",description="Command Used: repeat " + str(times) + content +  "\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff9933 ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
      await bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)

      for i in range(times):
          await bot.say(content)
    else:
      em = discord.Embed(title="Unauthorized Attempt",description="Command To be Used: repeat " + str(times) + content +"\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id), colour = 0xff0000,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
      await bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
      await bot.say("You are not Authorized to use this command. This attempt will be logged.")
#------------------------------------------------------------------------------------------------------------------
@bot.command(description='NULL') #Used to find extensions
async def extensions(self):
   """NULL"""
   cmd = 'find . -name "*.py"'
   result = subprocess.run([cmd], stdout=subprocess.PIPE , shell = True)
   export = "OUTPUT:\n" + result.stdout.decode('utf-8')
   await self.bot.say(export)
#------------------------------------------------------------------------------------------------------------------
@bot.command(pass_context=True, no_pm=True,description='Use @user to add user to Admin list')
async def addAdmin(ctx):
       """** Allows only Admins to add other Admins"""
       try:
         if(len(ctx.message.mentions) != 1):
           raise RuntimeError
         else:
           if(authAdmin(str(ctx.message.author.id),"addAdmin @" + str(ctx.message.mentions[0]) + "\nUserID: " + str(ctx.message.mentions[0].id))):
             if(authAdmin(str(ctx.message.mentions[0].id),"NoReport") and ctx.message.mentions[0].id != "90587751618981888" ):
               await bot.say(str(ctx.message.mentions[0]) + " is already an Admin")
               em = discord.Embed(title="Admin Command Attempted Use",description="File Changed\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id) + "\nUser added to Admin: " + str(ctx.message.mentions[0]) + "\n - User ID: " + str(ctx.message.mentions[0].id), colour = 0xadd8e6 ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
               await bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
             else:
               f = open("Admin.txt", "a")
               f.write(str(ctx.message.mentions[0].id) + "\n")
               f.close()
               print("--------------File-Changed--------------")
               print("Author of Command: " + str(ctx.message.author))
               print("Author ID: " + str(ctx.message.author.id))
               print("User added to Admin: " + str(ctx.message.mentions[0]))
               print("User ID: " + str(ctx.message.mentions[0].id))
               print("----------------------------------------")
               em = discord.Embed(title="Admin Command Used",description="File Changed\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id) + "\nUser added to Admin: " + str(ctx.message.mentions[0]) + "\n - User ID: " + str(ctx.message.mentions[0].id), colour = 0x0099ff ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
               await bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)
               await bot.say(str(ctx.message.mentions[0]) + " was added to the Admin list")
           else:
             await bot.say("You are not Authorized to use this command. This attempt will be logged.")
             print("----------Unauthorized-Attempt----------")
             print("Author of Command: " + str(ctx.message.author))
             print("User to be Admin: " + str(ctx.message.mentions[0]))
             print("----------------------------------------")

       except RuntimeError :
         print("---Add-Command-Usage-Error---")
         await bot.say("Please Include a single @user in your message")
#------------------------------------------------------------------------------------------------------------------
@bot.command(pass_context=True, no_pm=True,description='Use @user to remove user from the Admin list')
async def removeAdmin(ctx):
       """** Allows only Admins to remove other Admins"""
       try:
         if(len(ctx.message.mentions) != 1):
           raise RuntimeError
         else:
           if(authAdmin(str(ctx.message.author.id),"removeAdmin @" + str(ctx.message.mentions[0]) + "\nUserID: " + str(ctx.message.mentions[0].id))):
             if(authAdmin(str(ctx.message.mentions[0].id),"NoReport")):

               checkstring = str(ctx.message.mentions[0].id)

               f = open("Admin.txt","r")
               lines = f.readlines()
               f.close()
               f = open("Admin.txt","w")
               for line in lines:
                 if line!=checkstring+"\n":
                   f.write(line)
               f.close()

               print("--------------File-Changed--------------")
               print("Author of Command: " + str(ctx.message.author))
               print("Author ID: " + str(ctx.message.author.id))
               print("User removed from Admin: " + str(ctx.message.mentions[0]))
               print("User ID: " + str(ctx.message.mentions[0].id))
               print("----------------------------------------")

               em = discord.Embed(title="Admin Command Used",description="File Changed\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id) + "\nUser removed from Admin: " + str(ctx.message.mentions[0]) + "\n - User ID: " + str(ctx.message.mentions[0].id), colour = 0x0099ff ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
               await bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)

               await bot.say(str(ctx.message.mentions[0]) + " was removed from the Admin list")

             else:
               await bot.say(str(ctx.message.mentions[0]) + " isn't an Admin")
               em = discord.Embed(title="Admin Command Attempted Use",description="File Changed\nAuthor of Command: " + str(ctx.message.author) + "\n - Author ID: " + str(ctx.message.author.id) + "\nUser removed from Admin: " + str(ctx.message.mentions[0]) + "\n - User ID: " + str(ctx.message.mentions[0].id), colour = 0xadd8e6 ,timestamp = datetime.datetime.now() + datetime.timedelta(hours=5))
               await bot.send_message(discord.Object(id=LOGCHANNELID),embed = em)

           else:
             await bot.say("You are not Authorized to use this command. This attempt will be logged.")
             print("----------Unauthorized-Attempt----------")
             print("Author of Command: " + str(ctx.message.author))
             print("User to be Admin: " + str(ctx.message.mentions[0]))
             print("----------------------------------------")

       except RuntimeError :
         print("---Add-Command-Usage-Error---")
         await bot.say("Please Include a single @user in your message")
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
#------------------------------------------------------------------------------------------------------------------
    #bot.run('MzY0ODY1OTc1MzU2NDg5NzI5.DOxRMA.RSrhenBsdjvbekTjTPDVWN1dHfU')
    bot.run('MzYzMTQyMzU2NDE0ODg5OTg1.DP-ONQ.1bRPGHFJlTEwVaQ0ClT3XQ5WBT0')

