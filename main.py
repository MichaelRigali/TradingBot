import logging

from connectors.binance_futures import BinanceFuturesClient
from connectors.bitmex import BitmexClient

from interface.root_component import Root

logger = logging.getLogger()

logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


if __name__ == '__main__':
    binance = BinanceFuturesClient("3e574effb792bb8bdf3b0460c6fb7ef9326bbc6754a4ddacd5720e083ba0ba40",
                                   "ff20681594618ce5cb1d44de805e2670d20d1d02ea0662866e3620adb406d483",
                                   testnet = True, futures=True)

    bitmex = BitmexClient("uHXdtitZKBe2ET8UgnSjyTJa", "1bN-ILBxWEWVD9yzEbrMRhjGgfWYuxYjVCC-vG0M7Mg3m_q8", True)

    root = Root(binance, bitmex)
    root.geometry("2250x350")
    root.mainloop()