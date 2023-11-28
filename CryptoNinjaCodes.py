import logging
from decimal import Decimal
from typing import Dict, List

import numpy as np
import pandas as pd

from hummingbot.connector.connector_base import InfinityGridStrategy
from hummingbot.core.data_type.common import OrderType, PriceType, TradeType
from hummingbot.core.data_type.order_candidate import OrderCandidate
from hummingbot.core.event.events import BuyOrderCompletedEvent, OrderFilledEvent, SellOrderCompletedEvent
from hummingbot.core.utils import map_df_to_str
from hummingbot.strategy.infinity_grid import InfinityGridStrategy


class CryptoNinjaCodes(InfinityGridStrategy):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.trailing_stop_step_size = Decimal("0.001")
        self.trailing_stop_min_distance = Decimal("0.005")
        self.grid_size = Decimal("0.001")
        self.grid_price_step_size = Decimal("0.01")
        self.trailing_stop_order_type = "limit"

    def on_order_filled(self, order_filled_event):
        # Изчисляване на текущата цена за проследяващ стоп
        trailing_stop_price = order_filled_event.price - self.spread

        # Проверка дали изпълнената поръчка е поръчката, която е задействала защитния стоп, и ако да, дали е от същата страна
        if order_filled_event.order_id == self.trailing_stop_order_id and order_filled_event.order.side == self.trailing_stop_order_side:
            # Затваряне на поръчката
            order_filled_event.order.cancel()
        else:
            # Изчисляване на новата цена за проследяващ стоп
            trailing_stop_price = order_filled_event.price + self.trailing_stop_step_size

            # Създаване на нова поръчка за проследяващ стоп
            self.trailing_stop_order_id = self.exchange.create_limit_order(
                symbol=self.trading_pair,
                side=order_filled_event.order.side,
                amount=order_filled_event.order.amount,
                price=trailing_stop_price,
            )

    def on_data(self, data):
        # Проверка дали е необходимо да се задейства защитен стоп
        if self.market_info.price < trailing_stop_price:
            # Затваряне на всички активни поръчки
            for order in self.active_orders:
                order.cancel()

            # Рестартиране на стратегията
            self.restart()


def main():
    strategy = CryptoNinjaCodes()
    strategy.set_symbol("XAUT-USDT")
    strategy.set_exchange("gate_io")
    strategy.set_trading_pair("XAUT/USDT")
    strategy.set_grid_size(Decimal("0.001"))
    strategy.set_grid_price_step_size(Decimal("0.01"))
    strategy.set_trailing_stop_order_type("limit")
    strategy.start()


if __name__ == "__main__":
    main()
