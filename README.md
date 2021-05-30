# **Async telegram bot**

This is the example of the async telegram bot which offers to order a pizza.<br/>
It uses state machine and remote procedure calls(RPC) with FastAPI endpoint<br/>
States and orders are saved to the MongoDB. (for now to tiny implementation of MongoDB called [montydb](https://github.com/davidlatwe/montydb))

# Reqiurements
- [aiogram](https://github.com/aiogram/aiogram)
- [fastapi_websocket_rpc](https://github.com/authorizon/fastapi_websocket_rpc)
- [transitions](https://github.com/pytransitions/transitions)
- [montydb](https://github.com/davidlatwe/montydb)
- pymongo

# Tests
To run tests you must start the server first:
```
python trans_server.py
```
Then run test(pytest-asyncio must be installed):
```
py.test test_trans_client.py
```
# Run bot locally
First you need to set the environment variable TELETOKEN (It's the token, you can recieve from [@BotFather](https://t.me/botfather))<br/>
Then run the server:
```
python trans_server.py
```
And the client:
```
python telegram_client.py
```
Thats, all! You can find your bot and type /start for make orders and /hist for check the history of your orders.
# Deploy on [heroku](https://www.heroku.com/)
