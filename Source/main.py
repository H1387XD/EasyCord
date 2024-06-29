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
  def getBetween(self, message):
    s=" "
    messageCTX=""
    args=[]
    for msg in message:
      if msg in "%ABCDEFGHIJKLMNOPQRSTUVWXYZ": #it is capital
        if msg=="%" and messageCTX=="":
          continue
        elif msg=="%":
          args.append(messageCTX)
          messageCTX=""
          continue
        messageCTX+=msg
      elif msg in " %":
        self.codeOutput.write(s)
        s=""
      elif msg in "abcdefghijklmnopqrstuv":
        s+=msg
    for argtext in args:
      if argtext=="AUTHOR":
        self.codeOutput.write("{ctx.author.mention}")
      if argtext=="MENTION":
        self.codeOutput.write("{member.mention}")
      if argtext=="ARGS":
        self.codeOutput.write("{"+self.args[0].removeprefix("*")+"[0]"+"}")
      if argtext.startswith("RANDOM_"):
        nums=argtext.split("_")[1]
        self.codeOutput.write("{random.randint("+nums+")}'")
  def run(self):
    self.lines=self.code.split('\n')
    self.commandScope=""
    self.commandRequirements=[]
    self.args=[]
    for line in self.lines:
      self.tokens=line.split('=')
      for index,token in enumerate(self.tokens):
        if token=="TOKEN":
          self.codeOutput.write("\nToken="+'"'+self.tokens[index+1]+'"')
          break
        if token=="PREFIX":
          self.codeOutput.write("\nPrefix="+'"'+self.tokens[index+1]+'"')
          break
        if token=="STATUS":
          self.status="discord.CustomActivity(name='"+self.tokens[index+1]+"')"

        if token=="DISCORDBOT_INIT":
          self.codeOutput.write("\nclient=commands.Bot(command_prefix=Prefix, intents=discord.Intents.all())")
          self.codeOutput.write(f"\n@client.event\nasync def on_ready():\n    try:\n        await client.change_presence(activity={self.status})\n    except:\n        pass")
          break

        if token.startswith("COMMAND_"):
          self.commandName=token.removeprefix("COMMAND_")
          self.commandScope=self.commandName
          self.codeOutput.write("\n\n@client.command()")

        if token=="REQUIRE" and self.commandScope!="":
          commandRequirement=self.tokens[index+1]

          if commandRequirement=="DISCORDMEMBER":
            self.commandRequirements.append('member : discord.Member')
        if token=="ARGS" and self.commandScope:
          self.args.append("*"+self.tokens[index+1])
          break
        if token=="ENDREQUIREMENTS":
          self.codeOutput.write("\nasync def "+self.commandName+"(ctx")
          if len(self.commandRequirements)==0:
            pass
          else:
            for req in self.commandRequirements:
              self.codeOutput.write(" ,"+req)
            for arg in self.args:
              self.codeOutput.write(" ,"+arg)
          self.codeOutput.write("):")

        if token=="REPLY":
          message=self.tokens[index+1]
          self.codeOutput.write("\n    await ctx.send(f'")
          self.getBetween(message)
          self.codeOutput.write("')")
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

