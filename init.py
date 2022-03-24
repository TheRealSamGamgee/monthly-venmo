from dotenv import load_dotenv
from datetime import datetime
from operator import methodcaller
import calendar

from utils import get_env, env_vars, get_month, Venmo

def main(now):
  """
  The main function which initiates the script.
  """

  load_dotenv()  # take environment variables from .env.
  actualVars = []
  for var in env_vars:
    actualVars.append(get_env(var))

  access_token, request_configs = actualVars

  month = get_month(now)
  venmo = Venmo(access_token)
 # telegram = Telegram(bot_token, chat_id)
  friends = list(map(methodcaller("split", ";"), request_configs.split("|")))
  print(friends)


  successfulRequests = 0
  expectedRequests = len(friends)

  # name = 0, id = 1, purpose = 2, amount = 3, date = 4
  for friend in friends:
    date = int(friend[4])
    last_day_of_month = calendar.monthrange(now.year, now.month)[1]

    if (date == now.day) or (now.day == last_day_of_month and date > last_day_of_month):
      name = friend[0]
      id = friend[1]
      description = friend[2] + " for the month of " + month + " — Sent by Sam's AI Assistant"
      amount = friend[3]
      message = "Successfully requested $" + amount + " from " + name + " for " + description
      success = venmo.request_money(id, float(amount), description, print(message))#, telegram.send_message(message))
      if success:
        successfulRequests+=1
    else:
      print("Not due for " + str(date - now.day) + " more days")
      expectedRequests-=1
      continue

  if successfulRequests == expectedRequests:
    print("✅ Ran script successfully and sent " + str(expectedRequests) + " Venmo requests.")
  else:
    print("❌ Something went wrong. Only sent " + str(successfulRequests) + "/" + str(expectedRequests) + " venmo requests.")

now = datetime.now()
main(now)
