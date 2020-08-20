import enum
import queue
import time
from collections import defaultdict


class OrderBook(object):
    def __init__(self):
        """ Orders stored as two default dicts of {price:[orders at price]}
            Orders sent to OrderBook through OrderBook.unprocessed_orders queue
        """
        self.bid_prices = []
        self.bid_sizes = []
        self.offer_prices = []
        self.offer_sizes = []
        self.bids = defaultdict(list)
        self.offers = defaultdict(list)
        self.unprocessed_orders = queue.Queue()
        self.trades = queue.Queue()
        self.order_id = 0
        self.order_offers = defaultdict(list)

    @property
    def max_bid(self):
        if self.bids:
            return max(self.bids.keys())
        else:
            return 0.

    @property
    def min_offer(self):
        if self.offers:
            return min(self.offers.keys())
        else:
            return float('inf')

    def process_order(self, incoming_order):
        """ Main processing function. If incoming_order matches delegate to process_match."""
        if incoming_order.action == 'N':
            print("Creating the new order for order {}".format(incoming_order.orderID))
            if incoming_order.side == 'B':
                if self.offers and incoming_order.price >= self.min_offer:
                    self.process_match(incoming_order)
                else:
                    self.order_offers[int(incoming_order.orderID)].append(incoming_order)
                    self.bids[incoming_order.price].append(incoming_order)
            else:
                if incoming_order.price <= self.max_bid and self.bids:
                    self.process_match(incoming_order)
                else:
                    self.order_offers[int(incoming_order.orderID)].append(incoming_order)
                    self.offers[incoming_order.price].append(incoming_order)
        elif incoming_order.action == 'A':
            print("Need to append the existing order")
            print(self.order_offers)
            for o in self.order_offers:
                if o == incoming_order.orderID:
                    self.order_offers[int(incoming_order.orderID)] = incoming_order
        elif incoming_order.action == 'X':
            print("Cancel an existing order")
            for o in self.order_offers:
                if o == incoming_order.orderID:
                    del self.order_offers[int(incoming_order.orderID)]
        elif incoming_order.action == 'M':
            print("Match the existing orders")
            for o in self.order_offers:
                incoming_order = self.order_offers[o]
                incoming_order.timestamp = incoming_order.timestamp
                incoming_order.order_id = incoming_order.orderID
                if incoming_order.side == 'B':
                    if int(incoming_order.price) >= self.min_offer and self.offers:
                        self.process_match(incoming_order)
                    else:
                        #self.order_offers[int(incoming_order.orderID)].append(incoming_order)
                        self.bids[incoming_order.price].append(incoming_order)
                else:
                    if int(incoming_order.price) <= self.max_bid and self.bids:
                        self.process_match(incoming_order)
                    else:
                        #self.order_offers[int(incoming_order.orderID)].append(incoming_order)
                        self.offers[incoming_order.price].append(incoming_order)

    def process_match(self, incoming_order):
        """ Match an incoming order against orders on the other side of the book, in price-time priority."""
        levels = self.bids if incoming_order.side == 'S' else self.offers
        prices = sorted(levels.keys(), reverse=(incoming_order.side == 'S'))

        def price_doesnt_match(book_price):
            if incoming_order.side == 'B':
                return incoming_order.price < book_price
            else:
                return incoming_order.price > book_price

        for (i, price) in enumerate(prices):
            if (incoming_order.quantity == 0) or (price_doesnt_match(price)):
                break
            orders_at_level = levels[price]
            for (j, book_order) in enumerate(orders_at_level):
                if incoming_order.quantity == 0:
                    break
                print(incoming_order)
                print(book_order)
                trade = self.execute_match(incoming_order, book_order)
                incoming_order.size = max(0, int(incoming_order.quantity) - int(trade.quantity))
                book_order.size = max(0, int(book_order.quantity) - int(trade.quantity))
                self.trades.put(trade)
            levels[price] = [o for o in orders_at_level if o.size > 0]
            if len(levels[price]) == 0:
                levels.pop(price)
        # If the incoming order has not been completely matched, add the remainder to the order book
        if incoming_order.size > 0:
            same_side = self.bids if incoming_order.side == 'B' else self.offers
            same_side[incoming_order.price].append(incoming_order)

    def execute_match(self, incoming_order, book_order):
        trade_size = min(incoming_order.quantity, book_order.quantity)
        return Trade(incoming_order.side, book_order.price, trade_size, incoming_order.order_id, book_order.order_id)

    def book_summary(self):
        self.bid_prices = sorted(self.bids.keys(), reverse=True)
        self.offer_prices = sorted(self.offers.keys())
        self.bid_sizes = [sum(int(o.quantity) for o in self.bids[p]) for p in self.bid_prices]
        self.offer_sizes = [sum(int(o.quantity) for o in self.offers[p]) for p in self.offer_prices]

    def show_book(self):
        self.book_summary()
        print('Sell side:')
        if len(self.offer_prices) == 0:
            print('EMPTY')
        else:
            for i, price in reversed(list(enumerate(self.offer_prices))):
                print('{0}) Price={1}, Total units={2}'.format(i + 1, self.offer_prices[i], self.offer_sizes[i]))
        print('Buy side:')
        if len(self.bid_prices) == 0:
            print('EMPTY')
        for i, price in enumerate(self.bid_prices):
            print('{0}) Price={1}, Total units={2}'.format(i + 1, self.bid_prices[i], self.bid_sizes[i]))
        print()


class Order(object):
    def __init__(self, action=None, orderID=None, timestamp=None, symbol=None, orderType=None, side=None, price=None, quantity=None):
        self.action = action
        self.orderID = orderID
        self.timestamp = timestamp
        self.symbol = symbol
        self.orderType = orderType
        self.side = side
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return '{0} is {1} {2} units at {3}'.format(self.orderID, self.side, self.quantity, self.price)


class Trade(object):
    def __init__(self, incoming_side, incoming_price, trade_size, incoming_order_id, book_order_id):
        self.side = incoming_side
        self.price = incoming_price
        self.quantity = trade_size
        self.incoming_order_id = incoming_order_id
        self.book_order_id = book_order_id

    def __repr__(self):
        return 'Executed: {0} {1} units at {2}'.format(self.side, self.quantity, self.price)


if __name__ == '__main__':
    print('Taking the order from the user')
    order_list = []
    orders = []
    ob = OrderBook()
    n = int(input("Enter the number of orders: "))
    for i in range(n):
        order_list.append(input().split(","))

    for order in order_list:
        if order[0] == 'M':
            orders.append(Order(order[0]))
        else:
            orders.append(Order(order[0], order[1], order[2], order[3], order[4], order[5], int(order[6]), int(order[7])))

    print('We have received these orders:')
    for order in orders:
        print(order)
        ob.unprocessed_orders.put(order)

    while not ob.unprocessed_orders.empty():
        ob.process_order(ob.unprocessed_orders.get())

    print('Resulting order book:')
    ob.show_book()

