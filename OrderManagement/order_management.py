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
        self.pending_bids = []
        self.traded_bids = []
        self.offer_prices = []
        self.offer_sizes = []
        self.pending_offers = []
        self.traded_offers = []
        self.bids = defaultdict(list)
        self.offers = defaultdict(list)
        self.unprocessed_orders = queue.Queue()
        self.trades = queue.Queue()
        self.order_id = 0
        self.order_offers = defaultdict(list)
        self.book_entry = []

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

    def validate_new_order(self, incoming_order):
        try:
            int(incoming_order.orderID)
            int(incoming_order.timestamp)
            float(incoming_order.price)
            int(incoming_order.quantity)
            (incoming_order.symbol).isalpha()
            return True
        except Exception as e:
            return False

    def process_order(self, incoming_order):
        """ Main processing function. If incoming_order matches delegate to process_match."""
        if incoming_order.action == 'N':
            print("Creating the new order for order {}".format(incoming_order.orderID))
            if not self.validate_new_order(incoming_order):
                self.book_entry.append("{} - Reject  - 303 - Invalid order details".format(incoming_order.orderID))
                return
            else:
                self.book_entry.append(("{} - Accept".format(incoming_order.orderID)))
            if incoming_order.side == 'B':
                if self.offers and incoming_order.price >= self.min_offer:
                    self.process_match(incoming_order)
                else:
                    self.order_offers[int(incoming_order.orderID)].append(incoming_order)
                    self.bids[incoming_order.price].append(incoming_order)
            else:
                if self.bids and incoming_order.price <= self.max_bid:
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
        print("Levels : \n {}".format(levels))
        prices = sorted(levels.keys(), reverse=(incoming_order.side == 'S'))
        print("Prices : \n {} ".format(prices))
        def price_doesnt_match(book_price):
            if incoming_order.side == 'B':
                return incoming_order.price < book_price
            else:
                return incoming_order.price > book_price

        for (i, price) in enumerate(prices):
            if (incoming_order.quantity == 0) or (price_doesnt_match(price)):
                break
            orders_at_level = levels[price]
            print("Orders at level: \n {}".format(orders_at_level))
            for (j, book_order) in enumerate(orders_at_level):
                if incoming_order.quantity == 0:
                    break
                print("Book_order: {}".format(book_order))
                print("Incoming_order: {}".format(incoming_order))
                trade = self.execute_match(incoming_order, book_order)
                self.book_entry.append(trade)
                print(int(incoming_order.quantity) - int(trade.quantity))
                incoming_order.size = max(0, abs(int(incoming_order.quantity) - int(trade.quantity)))
                print("1: {}".format(incoming_order.size))
                book_order.size = max(0, abs(int(book_order.quantity) - int(trade.quantity)))
                print("2: {}".format(book_order.size))
                self.trades.put(trade)
                print(self.trades)
            levels[price] = [o for o in orders_at_level if o.size > 0]
            if len(levels[price]) == 0:
                levels.pop(price)

        # If the incoming order has not been completely matched, add the remainder to the order book
        if incoming_order.size > 0:
            incoming_order.pending = incoming_order.quantity - incoming_order.size
            incoming_order.traded = incoming_order.size
            if incoming_order.side == 'B':
                same_side = self.bids
                same_side[incoming_order.price].append(incoming_order)
                for p in self.offers:
                    for o in self.offers[p]:
                        o.traded = o.traded + trade.quantity
                        o.pending = o.quantity - o.traded
            else:
                same_side = self.offers
                same_side[incoming_order.price].append(incoming_order)
                for p in self.bids:
                    if p == incoming_order.price:
                        for o in self.bids[p]:
                            o.traded = o.traded + trade.quantity
                            o.pending = o.quantity - o.traded

        elif incoming_order.size == 0:
            incoming_order.traded = trade.quantity
            if incoming_order.side == 'B':
                same_side = self.bids
                same_side[incoming_order.price].append(incoming_order)
                for p in self.offers:
                    for o in self.offers[p]:
                        o.traded = o.traded + trade.quantity
                        o.pending = o.quantity - o.traded
            else:
                same_side = self.offers
                same_side[incoming_order.price].append(incoming_order)
                for p in self.bids:
                    if p == incoming_order.price:
                        for o in self.bids[p]:
                            o.traded = o.traded + trade.quantity
                            o.pending = o.quantity - o.traded


    def execute_match(self, incoming_order, book_order):
        trade_size = min(incoming_order.quantity, book_order.quantity)
        print("Trade Size: {}".format(trade_size))
        return Trade(incoming_order.side, book_order.price, trade_size, incoming_order.orderID, book_order.orderID)

    def book_summary(self):
        self.bid_prices = sorted(self.bids.keys(), reverse=True)
        self.offer_prices = sorted(self.offers.keys())
        self.bid_sizes = [sum(int(o.quantity) for o in self.bids[p]) for p in self.bid_prices]
        self.pending_bids = [sum(int(o.pending) for o in self.bids[p]) for p in self.bid_prices]
        self.traded_bids = [sum(int(o.traded) for o in self.bids[p]) for p in self.bid_prices]
        self.offer_sizes = [sum(int(o.quantity) for o in self.offers[p]) for p in self.offer_prices]
        self.pending_offers = [sum(int(o.pending) for o in self.offers[p]) for p in self.offer_prices]
        self.traded_offers = [sum(int(o.traded)  for o in self.offers[p])for p in self.offer_prices]

    def show_book(self):
        self.book_summary()
        print('Sell side:')
        if len(self.offer_prices) == 0:
            print('EMPTY')
        else:
            for i, price in reversed(list(enumerate(self.offer_prices))):
                print('{0}) Price={1}, Total units={2}, Traded={3}, Pending= {4}'.format(i + 1, self.offer_prices[i],
                                                                                         self.offer_sizes[i],
                                                                                         self.traded_offers[i],
                                                                                         self.pending_offers[i]))
        print('Buy side:')
        if len(self.bid_prices) == 0:
            print('EMPTY')
        for i, price in enumerate(self.bid_prices):
            print('{0}) Price={1}, Total units={2}, Traded={3}, Pending= {4}'.format(i + 1, self.bid_prices[i],
                                                                                     self.bid_sizes[i],
                                                                                     self.traded_bids[i],
                                                                                     self.pending_bids[i]))

    def show_transactions(self):
        for entry in self.book_entry:
            print(entry)

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
        self.traded = 0
        self.pending = 0

    def __repr__(self):
        return 'Order Id {0} is {1} {2} units at {3}'.format(self.orderID, self.side, self.quantity, self.price)


class Trade(object):
    def __init__(self, incoming_side, incoming_price, trade_size, incoming_order_id, book_order_id):
        self.side = incoming_side
        self.price = incoming_price
        self.quantity = trade_size
        self.incoming_order_id = incoming_order_id
        self.book_order_id = book_order_id

    def __repr__(self):
        return 'Executed: {0} {1} units at {2} for order {3}'.format(self.side, self.quantity, self.price, self.incoming_order_id)


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
            orders.append(Order(order[0], order[1], order[2], order[3], order[4], order[5], float(order[6]), int(order[7])))

    print('We have received these orders:')
    for order in orders:
        print(order)
        ob.unprocessed_orders.put(order)

    while not ob.unprocessed_orders.empty():
        ob.process_order(ob.unprocessed_orders.get())
        ob.show_book()

    print("####################################################")
    print('Final transactions:')
    ob.show_transactions()
    print("####################################################")
    print("Final Order Book:")
    ob.show_book()
    print("####################################################")

