import requests
import os

def get_rates():
    # 使用免費 API (ExchangeRate-API) 獲取匯率數據 (以台幣為基準)
    url = "https://open.er-api.com/v6/latest/TWD"
    response = requests.get(url)
    data = response.json()
    
    if data["result"] == "success":
        rates = data["rates"]
        # 計算 1 外幣 = 多少台幣
        usd = 1 / rates["USD"]
        cny = 1 / rates["CNY"]
        jpy = 1 / rates["JPY"]
        krw = 1 / rates["KRW"]
        eur = 1 / rates["EUR"]
        
        msg = (
            "早安！今日匯率推送 📈\n"
            "--------------------------\n"
            f"🇺🇸 美金 (USD)：{usd:.2f} TWD\n"
            f"🇨🇳 人民幣 (CNY)：{cny:.2f} TWD\n"
            f"🇯🇵 日幣 (JPY)：{jpy:.3f} TWD\n"
            f"🇰🇷 韓元 (KRW)：{krw:.4f} TWD\n"
            f"🇪🇺 歐元 (EUR)：{eur:.2f} TWD\n"
            "--------------------------\n"
            "資料更新時間：" + data["time_last_update_utc"][:16]
        )
        return msg
    return "匯率抓取失敗，請檢查 API 狀態。"

def send_to_server_chan(text):
    sendkey = os.getenv("SERVER_CHAN_SENDKEY")
    if sendkey:
        url = f"https://sctapi.ftqq.com/{sendkey}.send"
        requests.post(url, data={"title": "每日匯率報告", "desp": text})

def send_to_wecom(text):
    webhook_key = os.getenv("WECOM_WEBHOOK")
    if webhook_key:
        url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
        data = {
            "msgtype": "text",
            "text": {"content": text}
        }
        requests.post(url, json=data)

if __name__ == "__main__":
    report = get_rates()
    print(report)
    send_to_server_chan(report)
    send_to_wecom(report)
