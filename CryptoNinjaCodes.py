from hummingbot.strategy.infinity_grid import InfinityGridStrategy

class MyStrategy(InfinityGridStrategy):
    def init(self, **kwargs):
        super().init(**kwargs)

        self.trailing_stop_step_size = 0.001
        self.trailing_stop_min_distance = 0.005
        self.grid_size = 0.001
        self.grid_price_step_size = 0.01
        self.trailing_stop_order_type = "limit"

    def on_order_filled(self, order_filled_event):
        trailing_stop_price = order_filled_event.price - self.spread
        if order_filled_event.order_id == self.trailing_stop_order_id:
            order_filled_event.order.cancel()
        else:
            trailing_stop_price = order_filled_event.price + self.trailing_stop_step_size
            self.trailing_stop_order_id = self.exchange.create_limit_order(
                symbol=self.trading_pair,
                side=order_filled_event.order.side,
                amount=order_filled_event.order.amount,
                price=trailing_stop_price,
            )

    def on_data(self, data):
        if self.market_info.price < trailing_stop_price:
            for order in self.active_orders:
                order.cancel()
            self.restart()


def main():
    strategy = MyStrategy()
    strategy.set_symbol("XAUT-USDT")
    strategy.set_exchange("gate_io")
    strategy.set_trading_pair("XAUT/USDT")
    strategy.set_grid_size(0.001)
    strategy.set_grid_price_step_size(0.01)
    strategy.set_trailing_stop_order_type("limit")
    strategy.start()


if __name__ == "__main__":
    main()
