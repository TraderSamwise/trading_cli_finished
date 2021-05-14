import sys
import ccxt
import os
from pprint import pprint

# replace with your key / secret
key =  os.environ.get('ftx_key')
secret =  os.environ.get('ftx_secret')

exchange = ccxt.ftx({
    'apiKey': key,
    'secret': secret
})
exchange.load_markets()


# cancel all open orders for symbol
def cancel_all(symbol):
    res = exchange.cancel_all_orders(symbol)
    pprint(res)


# create and execute a scaled order
def scaled_order(symbol, side, total, start_price, end_price, num_orders):
    # cast command line args to proper types for math
    total = float(total)
    start_price = float(start_price)
    end_price = float(end_price)
    num_orders = int(num_orders)

    # params for the order
    params = {'postOnly': True}

    # size of each order
    order_amount = total / num_orders

    # step size of each order price starting from start_price
    step_size = (end_price-start_price)/(num_orders-1)

    # loop to generate orders
    for order_num in range(num_orders):
        # the price of this order, using step_size to calculate offset
        order_price = start_price + step_size*order_num
        # send the order
        res = exchange.create_order(symbol, "limit", side, order_amount, order_price, params)
        pprint(res)


# create and execute a basic order
def simple_order(symbol, side, amount, price):
    # params for the order
    params = {'postOnly': True}
    # send the order
    res = exchange.create_order(symbol, "limit", side, amount, price, params)
    pprint(res)


# parse function name and args and call function
def main():
    # name of function
    func_name = sys.argv[1]
    # args passed to function
    args = sys.argv[2:]
    # calling the function
    globals()[func_name](*args)




if __name__ == "__main__":
    main()