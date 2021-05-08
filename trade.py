import os
import sys
import ccxt


# replace with your key / secret
key =  os.environ.get('ftx_key')
secret =  os.environ.get('ftx_secret')


exchange = ccxt.ftx({
    'apiKey': key,
    'secret': secret
})

# create and execute a scaled order
def scaled_order(symbol, side, total_str, start_price_str, end_price_str, num_orders_str):
    # convert cl args to numbers
    total = float(total_str)
    start_price = float(start_price_str)
    end_price = float(end_price_str)
    num_orders = int(num_orders_str)

    # params for order
    params = {'postOnly': True}

    # size of each order
    order_amount = total/num_orders

    # step size of each order price starting at start_price
    order_inc = (end_price-start_price)/(num_orders - 1)

    # loop to generate orders
    for order_num in range(num_orders):
        # this order price using step size starting from start_price
        order_price = round(start_price + order_inc*order_num, 0)
        # send the order
        exchange.create_order(symbol, "limit", side, order_amount, order_price, params)




# create a simple order
def simple_order(symbol, limit, side,  amount, price):
    params = {'postOnly': True}
    exchange.create_order(symbol, "limit", side, amount, price)



# parse function name and args and call function
def main():
    # name of function to call
    func_name = sys.argv[1]
    # args passed directly to function
    args = sys.argv[2:]
    # call the function
    globals()[func_name](*args)


if __name__ == "__main__":
    main()