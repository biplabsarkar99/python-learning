from collections import deque
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
    n = int(input("Enter the number of orders: "))
    for i in range(n):
        order_list.append(input().split(","))


    for order in order_list:
        if order[0] == 'N':
            if int(order[1]) in orders:
                print("{} - AmendReject  - 303 - Invalid order details".format(order[1]))
            else:
                print("{} - Accept".format(order[1]))
                orders[int(order[1])] = {"OrderId" : order[1],
                                         "Timestamp": order[2],
                                         "Symbol": order[3],
                                         "OrderType": order[4],
                                         "Side": order[5],
                                         "Price": order[6],
                                         "Quantity": order[7]}
        elif order[0] == 'A':
            if int(order[1]) not in orders:
                print("{} - AmendReject  - 404 - Order does not exist".format(order[0]))
            else:
                if orders[int(order[1])]["Side"] != order[5]:
                    print("{} - AmendReject  - 101 - Invalid amendment details".format(order[0]))
                else:
                    print("{} - AmendAccept".format(order[0]))
                    orders[int(order[1])] = {"OrderId" : order[1],
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
                del orders[int(order[1])]

        elif order[0] == 'M':
            for order in orders:
                if orders[order]['Side'] == 'B':
                    order_temp_buy.append(orders[order])
                elif orders[order]['Side'] == 'S':
                    order_temp_sell.append(orders[order])
                else:
                    print("Invalid Option.")

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









