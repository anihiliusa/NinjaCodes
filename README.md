# Импортиране на необходимите библиотеки
import hummingbot.strategy.infinity_grid as infinity_grid

# Дефиниране на класа за стратегия
class MyStrategy(infinity_grid.InfinityGridStrategy):

    # Инициализация на класа
    def init(self, **kwargs):
        super().init(**kwargs)

        # Задаване на параметрите за стратегията
        self.trailing_stop_step_size = 0.001
        self.trailing_stop_min_distance = 0.005

        # Задаване на размера на мрежата (количеството XAUT за търговия на поръчка)
        self.grid_size = 0.001

        # Задаване на размера на стъпката на цената на мрежата
        self.grid_price_step_size = 0.01

        # Задаване на типа поръчка за проследяващ стоп
        self.trailing_stop_order_type = "limit"

    # Обработка на изпълнена поръчка
    def on_order_filled(self, order_filled_event):
        # Изчисляване на текущата цена за проследяващ стоп
        trailing_stop_price = order_filled_event.price - self.spread

        # Проверка дали изпълнената поръчка е поръчката, която е задействала проследяващия стоп
        if order_filled_event.order_id == self.trailing_stop_order_id:
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

    # Обработка на нова информация за пазара
    def on_data(self, data):
        # Проверка дали текущата цена е под цената за проследяващ стоп
        if self.market_info.price < trailing_stop_price:
            # Затваряне на всички поръчки
            for order in self.active_orders:
                order.cancel()

            # Рестартиране на стратегията
            self.restart()


# Основен метод
def main():
    # Създаване на стратегия
    strategy = MyStrategy()

    # Конфигуриране на стратегията
    strategy.set_symbol("XAUT-USDT")
    strategy.set_exchange("gate_io")
    strategy.set_trading_pair("XAUT/USDT")
    strategy.set_grid_size(0.001)
    strategy.set_grid_price_step_size(0.01)
    strategy.set_trailing_stop_order_type("limit")

    # Стартиране на стратегията
    strategy.start()


# Проверка дали стартираме от терминала
if name == "main":
    main()
