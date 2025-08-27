from PIL import Image, ImageChops
from bs4 import BeautifulSoup
import difflib

def pixel_compare(baseline_path, current_path, diff_path="diff.png"):
    baseline = Image.open(baseline_path)
    current = Image.open(current_path)

    diff = ImageChops.difference(baseline, current)

    if diff.getbbox():
        diff.save(diff_path)
        return False
    return True

def dom_compare(baseline_html, current_html, report_path="dom_diff.txt"):
    """
    Сравнивает DOM двух страниц.
    baseline_html и current_html — строки с HTML-кодом.
    """
    soup1 = BeautifulSoup(baseline_html, "html.parser")
    soup2 = BeautifulSoup(current_html, "html.parser")

    # Очищаем от лишнего (скрипты, стили)
    for s in soup1(["script", "style"]): s.extract()
    for s in soup2(["script", "style"]): s.extract()

    text1 = soup1.prettify()
    text2 = soup2.prettify()

    diff = difflib.unified_diff(
        text1.splitlines(),
        text2.splitlines(),
        fromfile="baseline",
        tofile="current",
        lineterm=""
    )

    diff_list = list(diff)
    if diff_list:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(diff_list))
        return False
    return True
