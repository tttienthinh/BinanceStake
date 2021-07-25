import requests, json, pickle, time
import os
from keep_alive import keep_alive

URL = os.getenv("URL")
bot_token = os.getenv("bot_token")
bot_chatID = os.getenv("bot_chatID")


def binance():
    response = json.loads(requests.get(URL).text)["data"]
    result = []
    for item in response:
        for asset in item["projects"]:
            if not asset["sellOut"]:
                result.append({
                    "asset":
                    asset["asset"],
                    "duration":
                    asset["duration"],
                    "APY":
                    str(
                        round(
                            float(asset["config"]["annualInterestRate"]) * 100,
                            2))
                })
    return result


def telegram(bot_message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response.json()


keep_alive()
past_result = []
while True:
    print(time.asctime())
    result = binance()
    message = ""
    for data in result:
        if data not in past_result:
            message += " ".join([
                data["asset"],
                f'{data["duration"]} days',
                f'{data["APY"]}% APY',
            ]) + "\n"
    if message != "":
        message += "\n" + time.asctime()
        print(message)
        telegram(message)
    with open('result.pkl', 'wb') as f:
        pickle.dump(result, f)
        f.close()
    time.sleep(60 - (time.time() % 60))  # Executing every hour

    with open('result.pkl', 'rb') as f:
        past_result = pickle.load(f)
        f.close()

