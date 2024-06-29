import sys
import math
import os
if len(sys.argv)==1:
  path="main.ezc"
else:
  path=sys.argv[1]

with open("main.ezc", "r") as f:
  CODE=f.read()

class Intepreter:
  def __init__(self, code):
    self.code=code
    self.codeOutput=open("easycord.py", "w")

    self.codeOutput.write("""import discord
import random
import asyncio

from discord.ext import commands
    """)
  def getMessageAlloc(self, message):
    s=message.split("%")
    middle=math.floor(len(s)/3)
    if s[middle]=="AUTHOR":
      return s[0]+"{ctx.author.mention}"+s[2]
    if s[middle]=="MENTION":
      return s[0]+"{member.mention}"+s[2]
    if s[middle].startswith("RANDOM_"):
      return s[0]+"{random.randint("+s[middle].split('_')[1]+")}"+s[2]
    return message
  def run(self):
    self.lines=self.code.split('\n')
    self.commandScope=""
    self.commandRequirements=[]
    for line in self.lines:
      self.tokens=line.split('=')
      for index,token in enumerate(self.tokens):
        if token=="TOKEN":
          self.codeOutput.write("\nToken="+'"'+self.tokens[index+1]+'"')
          break
        if token=="PREFIX":
          self.codeOutput.write("\nPrefix="+'"'+self.tokens[index+1]+'"')
          break

        if token=="DISCORDBOT_INIT":
          self.codeOutput.write("\nclient=commands.Bot(command_prefix=Prefix, intents=discord.Intents.all())")
          break

        if token.startswith("COMMAND_"):
          self.commandName=token.removeprefix("COMMAND_")
          self.commandScope=self.commandName
          self.codeOutput.write("\n\n@client.command()")

        if token=="REQUIRE" and self.commandScope!="":
          commandRequirement=self.tokens[index+1]

          if commandRequirement=="DISCORDMEMBER":
            self.commandRequirements.append('member : discord.Member')
        
        if token=="ENDREQUIREMENTS":
          self.codeOutput.write("\nasync def "+self.commandName+"(ctx")
          if len(self.commandRequirements)==0:
            pass
          else:
            for req in self.commandRequirements:
              self.codeOutput.write(" ,"+req)
          self.codeOutput.write("):")

        if token=="REPLY":
          message=self.tokens[index+1]
          message=self.getMessageAlloc(message)
          self.codeOutput.write("\n    await ctx.send(f'"+message+"')")
          break
        if token=="BAN":
          self.codeOutput.write("\n    await member.ban()")
          break
        if token=="KICK":
          self.codeOutput.write("\n    await member.kick()")
          break
        if token=="PM_%MENTION%":
          message=self.tokens[index+1]
          message=self.getMessageAlloc(message)
          self.codeOutput.write("\n    await member.send(f'"+message+"')")
          break
        if token=="ENDCOMMAND":
          self.commandName=""
          self.commandRequirements=[]
          self.commandScope=""
          break
    self.codeOutput.write(f"\nclient.run(Token)")   
    self.codeOutput.close()

    os.system('python easycord.py')
          

IP=Intepreter(CODE)
IP.run()

