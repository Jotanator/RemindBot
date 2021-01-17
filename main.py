import discord
#import os
from datetime import tzinfo, timedelta, datetime
from pytz import timezone
from threading import Timer
import time as time_funcs
from Notification import Notification
from notificationDict import notificationDict


client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  fmt = "%H:%M:%S %m/%d/%Y"
  if message.author == client.user: #client.user is remindbot.
    return  #avoid infinite loop.
  #$remind time date
  #time 00:00-23:59
  #date MM/DD/YYYY
  if message.content.startswith('$help'):
    await message.channel.send('Syntax: \n $remind Hour:Min Month/Date/Year Meeting_Title')
    await message.channel.send('All times are in PST, and Hours are recorded from 0 to 24. React to RemindBot\'s reply to sign up for the event.')
  if message.content.startswith('$remind'):
    splitStr = []
    splitStr = message.content.split(" ")
    #print(splitStr)
    time = splitStr[1].split(":") # Get Time divided into a list 0:Hours 1:Min
    date = splitStr[2].split("/") # Get Date divided into a list 0:Months 1:Day 2:Year
    if int(time[0]) > 23 or int(time[0]) < 0 or int(time[1]) < 0 or int(time[1]) > 59 or int(date[0]) > 12 or int(date[0]) < 1:
      await message.channel.send('Bad format')
      return
    time_object_current = datetime.now(timezone('US/Pacific'))
    time_object_current_new = time_object_current#.replace(second = 0)
    current_time = time_object_current_new.strftime(fmt)
    print("Current time: ", current_time)
    #splitStr[1] += ":00" + splitStr[2]
    #print(splitStr[1])
    print(time)
    print(date)
    time_object_user = datetime(int(date[2]), int(date[0]), int(date[1]), hour=int(time[0]), minute=int(time[1]), tzinfo=timezone('US/Pacific'))
    user_time = time_object_user.strftime(fmt)
    print("User Time: ", user_time)
    time = (time_object_user - time_object_current_new).total_seconds()+420
    print(time)
    #t = #Timer(time, #method_name_here)#
    #t.start()
    title = " "
    s=title.join(splitStr[3:])
    bot = await message.channel.send(" ***" + s + "*** " + ' Meeting scheduled at: ' + user_time)
    await bot.add_reaction("\N{THUMBS UP SIGN}")
    #time_funcs.sleep(5)
    print("TITLE:", s)
    print(bot.id)
    print(message.id)
    noti = Notification(s, time, [], bot)
    notificationDict[bot.id] = noti
    print(notificationDict)
    await noti.mention_ping()

@client.event
async def on_reaction_add(reaction, user):
  id = reaction.message.id
  print("MESSAGE ID: ", id)
  if user != client.user:
    print(user.id)
    try:
      noti = notificationDict[id]
      noti.addPeople(user.id) 
      #print(noti.getPeople())
    except:
      print("YOU GOT CAUGHT")



@client.event
async def on_raw_reaction_remove(payload):
  print("test")
  print("MESSAGE ID: ", payload.user_id)
  id = payload.message_id
  print(id)
  if payload.user_id != client.user.id:
    print(payload.user_id)
    try:
      noti = notificationDict[id]
      noti.removePeople(payload.user_id)
    except: 
      print("BRRRRRREEEHHHHHH Y U DO DIS")
    #print(noti.getPeople())

    


client.run("ODAwMTEyODgyMzU2MTkxMjcy.YANZMA.p3xR2v66g1C0FtLr7CUQ5VlMhsQ")
#client.run(os.getenv('TOKEN'))