import sys
import ccxt.async_support as ccxt
import os
import asyncio
import logging
import builtins
from pprint import pprint
from datetime import datetime

# replace with your key / secret
key = os.environ.get('ftx_key')
secret = os.environ.get('ftx_secret')


current_symbol = "BTC-PERP"
exchange = ccxt.ftx({
    'apiKey': key,
    'secret': secret,
    'enableRateLimit': True,
    'rateLimit': 250 # Could be required for functions like scaled_order.
})
    

def tprint(msg):
    print(str(datetime.utcnow()) + " - " + str(msg))

async def help(function_str=None):
    if not function_str:
        builtins.help(globals()[function_str])
    else:
        tprint("You need to specify the function you need information on (example: help cancel_all)!")

async def cancel_all():
    """
        This function cancels all active orders on the current trading symbol.
        
        Usage on CLI:
            "cancel_all"
    """
    res = await exchange.cancel_all_orders(current_symbol)
    tprint(res)

async def scaled_order(side, total, start_price, end_price, num_orders):
    """
        This function places a number of `num_orders` uniformly distributed limit orders of the given `side` between `start_price` and `end_price`, such that the total amount ordere is `total` (base asset), on the current trading symbol.
        
        Usage on CLI:
            "scaled_order sell 0.1 42069 69420 10"
    """
    total = float(total)
    start_price = float(start_price)
    end_price = float(end_price)
    num_orders = int(num_orders)
    order_amount = total / num_orders
    step_size = (end_price-start_price)/(num_orders-1)
    params = {'postOnly': True}

    orders = []
    for order_num in range(num_orders):
        order_price = start_price + step_size * order_num
        orders.append(asyncio.create_task(limit_order(side, order_amount, order_price)))
    await asyncio.wait(orders)

async def limit_order(side, amount, price, post_only=True):
    """
        This function places a postOnly limit order of the given `amount`, with the given `side`, at the given `price`, on the current trading symbol.
        Set the post_only parameter to False to send regular limit orders.
        
        Usage on CLI:
            "limit_order buy 0.1 42069"
            "limit_order sell 0.1 44444 False" (this order could be executed as a market order)
    """
    try:
        params = {'postOnly': False if str(post_only).lower() == "false" else True}
        order = await exchange.create_order(current_symbol, "limit", side, amount, price, params)
        tprint(f"[{order['symbol']}] {order['side'].upper()} {order['amount']} @ {order['price']}")
    except Exception as e:
        tprint(f"Error while placing the following order [{symbol} {side} {amount} @ {price}] - " + str(e)) 

async def symbol(new_symbol):
    """
        This function changes your trading symbol.
        
        Usage on CLI:
            "symbol BTC-PERP"
    """
    global current_symbol
    current_symbol = new_symbol
    tprint(f"Now trading on {current_symbol}")

async def main():
    await exchange.load_markets()

    tprint("Enter 'q' to quit.")
    await symbol(input("> Symbol: "))
    
    while True:
        command = input(f"{current_symbol}> ")
        if command.lower() == 'q': break
        
        arguments = command.split(' ')
        func_name = arguments[0]
        args = arguments[1:]
        
        try:
            await globals()[func_name](*args)
        except KeyError as e:
            tprint(f"Error: function {e} does not exist.")
        except Exception as e:
            tprint(f"Unknown error: {e}")
            
    await exchange.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
