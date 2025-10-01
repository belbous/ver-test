import json
import os
from compare import pixel_compare, dom_compare
from notify import send_telegram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def take_screenshot_and_html(url, screenshot_path, html_path):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1366,768")

    # Try common chromium/chrome locations in CI environments
    chromium_paths = [
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
    ]
    for path in chromium_paths:
        if os.path.exists(path):
            options.binary_location = path
            break

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    driver.save_screenshot(screenshot_path)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    driver.quit()


if __name__ == "__main__":
    with open("config.json", encoding="utf-8") as f:
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
        result_msg.append("Упс... Найдены отличия на скриншоте (diff.png)")

    if dom_ok:
        result_msg.append("✅ DOM совпадает")
    else:
        result_msg.append("Упс... Найдены отличия в DOM (dom_diff.txt)")

    final_report = "\n".join(result_msg)
    print(final_report)

    # если настроен Telegram — отправляем
    if cfg.get("telegram_token") and cfg.get("telegram_chat_id"):
        send_telegram(cfg["telegram_token"], cfg["telegram_chat_id"], final_report)

