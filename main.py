import time
import json
from selenium import webdriver
from compare import pixel_compare, dom_compare
from notify import send_telegram

def take_screenshot_and_html(url, out_img="current.png", out_html="current.html"):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)  # ждём загрузки
    driver.save_screenshot(out_img)
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    driver.quit()

if __name__ == "__main__":
    with open("config.json") as f:
        cfg = json.load(f)

    url = cfg["url"]
    print(f"Открываем сайт: {url}")
    take_screenshot_and_html(url, cfg["screenshot"], "current.html")

    # сравнение картинок
    img_ok = pixel_compare(cfg["baseline"], cfg["screenshot"])
    # сравнение DOM
    with open("baseline.html", encoding="utf-8") as f1, open("current.html", encoding="utf-8") as f2:
        dom_ok = dom_compare(f1.read(), f2.read())

    result_msg = []
    if img_ok:
        result_msg.append("✅ Скриншоты совпадают")
    else:
        result_msg.append("❌ Найдены отличия на скриншоте (см. diff.png)")

    if dom_ok:
        result_msg.append("✅ DOM совпадает")
    else:
        result_msg.append("❌ Найдены отличия в DOM (см. dom_diff.txt)")

    final_report = "\n".join(result_msg)
    print(final_report)

    # если настроен Telegram — отправляем
    if cfg.get("telegram_token") and cfg.get("telegram_chat_id"):
        send_telegram(cfg["telegram_token"], cfg["telegram_chat_id"], final_report)
