import requests

def send_telegram(token, chat_id, text, timeout=10):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        response = requests.post(
            url,
            json={"chat_id": chat_id, "text": text},
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        return {"ok": False, "error": str(error)}
