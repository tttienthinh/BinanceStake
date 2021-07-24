import requests, json, pickle, time

URL = "https://www.binance.com/gateway-api/v1/friendly/pos/union?pageSize=50&pageIndex=1&status=ALL"


def binance():
    response = json.loads(requests.get(URL).text)["data"]
    result = []
    for item in response:
        for asset in item["projects"]:
            if not asset["sellOut"]:
                result.append({
                    "asset": asset["asset"],
                    "duration": asset["duration"],
                    "APY": str(round(float(asset["config"]["annualInterestRate"]) * 100, 2))
                })
    return result


def telegram(message):
    bot_token = '1806732732:AAFxtjvhsucDPbOjBYSUzCNztqjntoI4Q-E'
    bot_chatID = '-572290585'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message

    response = requests.get(send_text)
    return response.json()


past_result = []
while True:
    result = binance()
    for data in result:
        if data not in past_result:
            telegram(
                "\n".join([
                    data["asset"],
                    f'{data["duration"]} days',
                    f'{data["APY"]}% APY',
                    time.asctime(),
                ])
            )
    with open('result.pkl', 'wb') as f:
        pickle.dump(result, f)
        f.close()
    time.sleep(3_600 - (time.time() % 3_600)) # Executing every hour

    with open('result.pkl', 'rb') as f:
        past_result = pickle.load(f)
        f.close()


