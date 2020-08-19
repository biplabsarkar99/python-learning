from collections import deque


class Order:
    def __init__(self, action, orderID, timestamp, symbol, orderType, side, price, quantity):
        self.action = action
        self.orderID = orderID
        self.timestamp = timestamp
        self.symbol = symbol
        self.orderType = orderType
        self.side = side
        self.price = price
        self.quantity = quantity
        self.next_order = None
        self.prev_order = None
        self.parent_limit = None


class Limit:
    def __str__(self):
        left = 'None' if self.left_child is None else str(self.left_child.price)
        right = 'None' if self.right_child is None else str(self.right_child.price)
        return left + '--' + str(self.price) + '--' + right

    def __init__(self, price):
        self.price = price
        self.size = 0
        self.total_volume = 0
        self.height = 1
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.head_order = None
        self.tail_order = None

    def add(self, order):
        if not self.head_order:
            self.head_order = order
            self.tail_order = order
        else:
            self.tail_order.next_order = order
            order.prev_order = self.tail_order
            self.tail_order = order
        self.size += 1
        self.total_volume += int(order.quantity)


class LimitTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, limit):
        if not self.root:
            self.root = limit
        else:
            ptr = self.root
            while True:
                if limit.price < ptr.price:
                    if ptr.left_child is None:
                        ptr.left_child = limit
                        ptr.left_child.parent = ptr
                        new = ptr.left_child
                        break
                    else:
                        ptr = ptr.left_child
                        continue
                else:
                    if ptr.right_child is None:
                        ptr.right_child = limit
                        ptr.right_child.parent = ptr
                        new = ptr.right_child
                        break
                    else:
                        ptr = ptr.right_child
                        continue
            self.update_height(new)  # update heights of nodes up the path to the root
            x = y = z = new
            while x is not None:
                if abs(self.height(x.left_child) - self.height(x.right_child)) <= 1:
                    z = y
                    y = x
                    x = x.parent
                else:
                    break
            if x is not None:
                self.rebalance(x, y, z)

    def rebalance(self, x, y, z):
        """
        http://www.mathcs.emory.edu/~cheung/Courses/323/Syllabus/Trees/AVL-insert.html
        """
        z_is_left_child = z is y.left_child
        y_is_left_child = y is x.left_child
        if z_is_left_child and y_is_left_child:
            a = z
            b = y
            c = x
            t0 = z.left_child
            t1 = z.right_child
            t2 = y.right_child
            t3 = x.right_child
        elif not z_is_left_child and y_is_left_child:
            a = y
            b = z
            c = x
            t0 = y.left_child
            t1 = z.left_child
            t2 = z.right_child
            t3 = x.right_child
        elif z_is_left_child and not y_is_left_child:
            a = x
            b = z
            c = y
            t0 = x.left_child
            t1 = z.left_child
            t2 = z.right_child
            t3 = y.right_child
        else:
            a = x
            b = y
            c = z
            t0 = x.left_child
            t1 = y.left_child
            t2 = z.left_child
            t3 = z.right_child

        if x is self.root:
            self.root = b
            self.root.parent = None
        else:
            x_parent = x.parent
            if x is x_parent.left_child:
                b.parent = x_parent
                x_parent.left_child = b
            else:
                b.parent = x_parent
                x_parent.right_child = b
        b.left_child = a
        a.parent = b
        b.right_child = c
        c.parent = b

        a.left_child = t0
        if t0 is not None:
            t0.parent = a
        a.right_child = t1
        if t1 is not None:
            t1.parent = a

        c.left_child = t2
        if t2 is not None:
            t2.parent = c
        c.right_child = t3
        if t3 is not None:
            t3.parent = c
        self.update_height(a)
        self.update_height(c)

    def update_height(self, node):
        """
        http://www.mathcs.emory.edu/~cheung/Courses/323/Syllabus/Trees/AVL-insert.html#tri-node
        """
        while node is not None:
            node.height = 1 + max(self.height(node.left_child), self.height(node.right_child))
            node = node.parent

    def height(self, node):
        """
        https://stackoverflow.com/questions/575772/the-best-way-to-calculate-the-height-in-a-binary-search-tree-balancing-an-avl
        """
        if node is None:
            return 0
        else:
            return node.height

    def successor(self, node):
        """Returns the inorder successor of the node
        :param node: Limit instance
        :return: In-order successor of input if it exists or None otherwise
        """
        if node is None:
            return None
        if node.right_child is not None:
            succ = node.right_child
            while succ.left_child is not None:
                succ = succ.left_child
            return succ
        else:
            p = node.parent
            while p is not None:
                if node is not p.right_child:
                    break
                node = p
                p = p.parent
            return p

    def predecessor(self, node):
        """Returns the inorder predecessor of the node
        :param node: Limit instance
        :return: In-order predecessor of input if its exists or None otherwise
        """
        if node is None:
            return None
        if node.left_child is not None:
            pred = node.left_child
            while pred.right_child is not None:
                pred = pred.right_child
            return pred
        else:
            p = node.parent
            while p is not None:
                if node is not p.left_child:
                    break
                node = p
                p = p.parent
            return p


class Book:
    buy_tree = LimitTree()
    sell_tree = LimitTree()
    lowest_sell = None
    highest_buy = None
    buy_map = {}
    sell_map = {}
    buy_levels = {}
    sell_levels = {}

    def update_book(self):
        """Update the order book, executing any trades that are now possible
        :param:
        :return:
        """
        while self.lowest_sell is not None and self.highest_buy is not None and self.lowest_sell <= self.highest_buy:
            sell = self.sell_levels[self.lowest_sell].head_order
            buy = self.buy_levels[self.highest_buy].head_order
            self.execute_trade(sell, buy)

    def add_order(self, order):
        """Add an order to the correct tree at the correct Limit level
        :param order: Order instance
        :return:
        """
        print(order.__dict__)
        if order.side == 'B':
            print("{} in BUY LEVELS.".format(self.buy_levels))
            if order.price in self.buy_levels:
                limit = self.buy_levels[order.price]
                if limit.size == 0:
                    self.buy_tree.size += 1
                limit.add(order)
                self.buy_map[order.orderID] = order
                order.parent_limit = limit
            else:
                limit = Limit(order.price)
                limit.add(order)
                self.buy_map[order.orderID] = order
                self.buy_tree.insert(limit)
                self.buy_tree.size += 1
                self.buy_levels[order.price] = limit
                order.parent_limit = self.buy_levels[order.price]
            if self.highest_buy is None or order.price > self.highest_buy:
                self.highest_buy = order.price
        else:
            if order.price in self.sell_levels:
                print("{} in SELL LEVELS.".format(self.sell_levels))
                limit = self.sell_levels[order.price]
                if limit.size == 0:
                    self.sell_tree.size += 1
                limit.add(order)
                self.sell_map[order.uid] = order
                order.parent_limit = self.sell_levels[order.price]
            else:
                limit = Limit(order.price)
                limit.add(order)
                self.sell_map[order.uid] = order
                self.sell_tree.insert(limit)
                self.sell_tree.size += 1
                self.sell_levels[order.price] = limit
                order.parent_limit = self.sell_levels[order.price]
            if self.lowest_sell is None or order.price < self.lowest_sell:
                self.lowest_sell = order.price
        self.update_book()


# Main function to start the test
if __name__ == '__main__':
    '''
    The input command will have the following components
    Action : N,A,X,M,Q
    OrderID: An integer value
    Timestamp: An integer value 
    Symbol :Varying length string containing only alphabets
    OrderType : M,L,I
    Side: Buy(B) or Sell(S)
    Price: A float value 0.99 if order type is M, the price is given exactly to the two places of decimal 
    Quantity: An integer value

    ###
    Action,OrderID,Timestamp,Symbol,OrderType,Side,Price,Quantity
    ###
    '''
    order_list = []
    order_temp_buy = []
    order_temp_sell = []
    orders = {}
    orderBook = Book()
    count = 1
    print(orderBook.__dict__)
    n = int(input("Enter the number of orders: "))
    for i in range(n):
        order_list.append(input().split(","))

    for order in order_list:
        if order[0] == 'N':
            if int(order[1]) in orders:
                print("{} - AmendReject  - 303 - Invalid order details".format(order[1]))
            else:
                print("{} - Accept".format(order[1]))
                orders[int(order[1])] = {"OrderId": order[1],
                                         "Timestamp": order[2],
                                         "Symbol": order[3],
                                         "OrderType": order[4],
                                         "Side": order[5],
                                         "Price": order[6],
                                         "Quantity": order[7]}
                order = Order(order[0], order[1], order[2], order[3], order[4], order[5], order[6], order[7])
                print(order.__dict__)
                orderBook.add_order(order)

        elif order[0] == 'A':
            if int(order[1]) not in orders:
                print("{} - AmendReject  - 404 - Order does not exist".format(order[0]))
            else:
                if orders[int(order[1])]["Side"] != order[5]:
                    print("{} - AmendReject  - 101 - Invalid amendment details".format(order[0]))
                else:
                    print("{} - AmendAccept".format(order[0]))
                    orders[int(order[1])] = {"OrderId": order[1],
                                             "Timestamp": order[2],
                                             "Symbol": order[3],
                                             "OrderType": order[4],
                                             "Price": order[6],
                                             "Quantity": order[7]}

        elif order[0] == 'X':
            if int(order[1]) not in orders:
                print("{} - CancelReject  - 404 - Order does not exist".format(order[1]))
            else:
                print("{} - CancelAccept".format(order[1]))
                book.reduce_order(fields[2], int(fields[3]))
            # del orders[int(order[1])]

        elif order[0] == 'M':
            for order in orders:
                # print(order)
                # print(orders[order]['Side'])
                # print(orders[order])
                if orders[order]['Side'] == 'B':
                    order_temp_buy.append(orders[order])
                elif orders[order]['Side'] == 'S':
                    order_temp_sell.append(orders[order])
                else:
                    print("Invalid Option.")

        # print("###########################################################")
        # print(order_temp_sell)
        # print(order_temp_buy)
        # print("###########################################################")
        for order_buy in order_temp_buy:
            for order_sell in order_temp_sell:
                if order_buy['Symbol'] == order_sell['Symbol'] and order_buy['Price'] == order_sell['Price']:
                    print("{}|{},{},{},{}|{},{},{},{}".format(order_buy['Symbol'],
                                                              order_buy['OrderId'],
                                                              order_buy['OrderType'],
                                                              order_buy['Quantity'],
                                                              order_buy['Price'],
                                                              order_sell['Price'],
                                                              order_sell['Quantity'],
                                                              order_sell['OrderType'],
                                                              order_sell['OrderId']
                                                              ))
                else:
                    pass
    count += 1

    print(order.__dict__)
    print(orderBook.__dict__)











