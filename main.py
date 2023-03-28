# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from constants import COMPUTER, BASE_URL
from controller.process import Crawling
# Press the green button in the gutter to run the script.
from model.sqlite_dao import Computer
from view.process import draw

if __name__ == '__main__':
    crawl = Crawling(BASE_URL)
    # crawl.get("laptop", COMPUTER["laptop"])
    # crawl.get("gameBook", COMPUTER["gameBook"])
    crawl.get("desktop", COMPUTER["desktop"])
    # crawl.get("server", COMPUTER["server"])

    # for k in COMPUTER.keys():
    #     result = Computer().select(k)
    #     draw.histogram(result, k, "$")
