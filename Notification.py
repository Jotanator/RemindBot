from datetime import datetime
from pytz import timezone
from threading import Timer
import discord
import asyncio
from notificationDict import notificationDict

client = discord.Client()

class Notification:
  def __init__(self, title: str , wakeup: int, people: list, message): 
    self.title = title
    self.wakeup = wakeup
    self.people = people
    self.message = message
    #task = asyncio.create_task(self.mention_ping())
    #await self.mention_ping()
    #loop = asyncio.get_event_loop()
    #timer = Timer(4, loop.run_until_complete(task))
    #timer.start()


  def getPeople(self) -> list: 
    return self.people

  def getWakeup(self) -> datetime:
    return self.wakeup
  
  def getTitle(self) -> str:
    return self.title

  def addPeople(self, person: str):
    self.people.append(person)
    
  def removePeople(self, person: str):
    self.people.remove(person)

  def addTitle(self, title: str):
    self.title.append(title)
  
  def isFinished(self, current:datetime) -> bool:
    diff = (self.wakeup - current).total_seconds()+421
    if diff <= 0:
      return True
    return False
  
  def onComplete(self):
    str = ""
    for ppl in self.people:
      str += " @"
      str += ppl
    print(str)

  @client.event
  async def mention_ping(self):
    await asyncio.sleep(self.wakeup)
    string = ""
    myids = self.getPeople()
    for ppl in myids:
      string += "<@{0}> ".format(ppl)
    await self.message.reply(string + " ***" + self.getTitle() + "*** " + ' Get on it!')
    del notificationDict[self.message.id]
    print(notificationDict)
    #loop.run_until_complete(task)