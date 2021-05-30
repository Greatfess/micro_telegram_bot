import os
os.environ["MONTY_ENABLE_BSON"] = "1"
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

# Init the FAST-API app
app = FastAPI()


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
    async def get_saved_machine(self, name: str):
        cur = col.find({'Name': name})
        curs = [c['bin-data'] for c in cur]
        if not curs:
            raise MachineNotFound(name)

        return pickle.loads(curs[0])

    async def reset_or_create_machine(self, name: str):
        try:
            cur = col.find({'Name': name})
            res = next(cur)['bin-data']
            machine = pickle.loads(res)
            await machine.reset()
            thebytes = pickle.dumps(machine)
            col.update_one({'Name': name},
                           {"$set": {'bin-data': Binary(thebytes)}})
        except StopIteration:
            print('StopIteration')
            # if there are no saved machines in db, then create one
            machine = async_nested(states=states,
                                   transitions=transitions,
                                   initial='undefined',
                                   ignore_invalid_triggers=True)
            print('1')
            thebytes = pickle.dumps(machine)
            print('2')
            col.insert_one({'Name': name, 'bin-data': Binary(thebytes)})
            print('3')
        return machine.state

    async def remove_machine(self, name: str):
        try:
            machine = await self.get_saved_machine(name)
        except MachineNotFound:
            await self.reset_or_create_machine(name)
            machine = await self.get_saved_machine(name)
        col.insert_one({'Hist-name': name, 'state': machine.state})
        col.delete_one({'Name': name})
        return f'Machine {name} has removed'

    async def update_state(self, name: str, phrase: str):
        try:
            machine = await self.get_saved_machine(name)
        except MachineNotFound:
            print('MachineNotFound')
            await self.reset_or_create_machine(name)
            machine = await self.get_saved_machine(name)
        if phrase == 'accept':
            # save the order to db
            col.insert_one({'Hist-name': name, 'state': machine.state})
        await machine.dispatch(phrase)
        thebytes = pickle.dumps(machine)
        col.update_one({'Name': name},
                       {"$set": {'bin-data': Binary(thebytes)}})
        return machine.state

    async def get_state(self, name: str):
        try:
            machine = await self.get_saved_machine(name)
        except MachineNotFound:
            await self.reset_or_create_machine(name)
            machine = await self.get_saved_machine(name)
        return machine.state

    async def reset_state(self, name: str):
        try:
            machine = await self.get_saved_machine(name)
        except MachineNotFound:
            await self.reset_or_create_machine(name)
            machine = await self.get_saved_machine(name)
        await machine.reset()
        thebytes = pickle.dumps(machine)
        col.update_one({'Name': name},
                       {"$set": {'bin-data': Binary(thebytes)}})
        return machine.state

    async def get_hist(self, name: str):
        cur = col.find({'Hist-name': name})
        return [doc['state'] for doc in cur]


# Create an endpoint and load it with the methods to expose
endpoint = WebsocketRPCEndpoint(MachineServer())
# add the endpoint to the app
endpoint.register_route(app, "/ws")


def start_server(host="0.0.0.0", port=9000):
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()
