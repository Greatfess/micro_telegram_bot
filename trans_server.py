import os

os.environ["MONTY_ENABLE_BSON"] = "1"
print('MONTY_ENABLE_BSON', os.getenv('MONTY_ENABLE_BSON'))

import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi_websocket_rpc import RpcMethodsBase, WebsocketRPCEndpoint
import pickle
from bson.binary import Binary
from trans_model import states, transitions, async_nested
from montydb import MontyClient

client = MontyClient(":memory:")
col = client.db.test


class MachineNotFound(Exception):
    """Exception raised for errors when Machine is not in database.

    Attributes:
        name -- Name of the machine
        message -- explanation of the error
    """

    def __init__(self, name):
        self.name = name
        self.message = "Machine is not in database"
        super().__init__(self.message)

    def __str__(self):
        return f'{self.name} {self.message}'


# Methods to expose to the clients
class MachineServer(RpcMethodsBase):
    async def find_or_create_machine(self, name: str):
        try:
            cur = col.find({'Name': name})
            res = next(cur)['bin-data']
            machine = pickle.loads(res)
            await machine.reset()
            thebytes = pickle.dumps(machine)
            col.update_one({'Name': name},
                           {"$set": {'bin-data': Binary(thebytes)}})
        except StopIteration:
            machine = async_nested(states=states,
                                   transitions=transitions,
                                   initial='undefined',
                                   ignore_invalid_triggers=True)
            thebytes = pickle.dumps(machine)
            col.insert_one({'Name': name, 'bin-data': Binary(thebytes)})
        return machine.state

    async def remove_machine(self, name: str):
        try:
            cur = col.find({'Name': name})
            res = next(cur)['bin-data']
            machine = pickle.loads(res)
            col.insert_one({'Hist-name': name, 'state': machine.state})
            col.delete_one({'Name': name})
            return f'Machine {name} has removed'
        except StopIteration:
            raise MachineNotFound(name)

    async def update_state(self, name: str, phrase: str):
        try:
            cur = col.find({'Name': name})
            res = next(cur)['bin-data']
            machine = pickle.loads(res)
            if phrase == 'accept':
                col.insert_one({'Hist-name': name, 'state': machine.state})
            await machine.dispatch(phrase)
            thebytes = pickle.dumps(machine)
            col.update_one({'Name': name},
                           {"$set": {'bin-data': Binary(thebytes)}})
            return machine.state
        except StopIteration:
            print('not found')
            raise MachineNotFound(name)

    async def get_state(self, name: str):
        try:
            cur = col.find({'Name': name})
            res = next(cur)['bin-data']
            machine = pickle.loads(res)
            return machine.state
        except StopIteration:
            raise MachineNotFound(name)

    async def reset_state(self, name: str):
        try:
            cur = col.find({'Name': name})
            res = next(cur)['bin-data']
            machine = pickle.loads(res)
            await machine.reset()
            print(machine.state)
            thebytes = pickle.dumps(machine)
            col.update_one({'Name': name},
                           {"$set": {'bin-data': Binary(thebytes)}})
            return machine.state
        except StopIteration:
            raise MachineNotFound(name)

    async def get_hist(self, name: str):
        try:
            cur = col.find({'Hist-name': name})
            return [doc['state'] for doc in cur]
        except StopIteration:
            raise MachineNotFound(name)


# Init the FAST-API app
app = FastAPI()
# Create an endpoint and load it with the methods to expose
endpoint = WebsocketRPCEndpoint(MachineServer())
# add the endpoint to the app
endpoint.register_route(app, "/ws")

# Start the server itself
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
