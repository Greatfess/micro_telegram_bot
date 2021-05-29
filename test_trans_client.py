import asyncio
from fastapi_websocket_rpc import RpcMethodsBase, WebSocketRpcClient


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


async def run_client(uri, name):
    async with WebSocketRpcClient(uri, RpcMethodsBase(), default_response_timeout=10) as client:
        response = await client.other.find_or_create_machine(name=name)
        assert response.result in ['undefined', 'small', 'big',
                                   'small↦card', 'big↦card',
                                   'small↦cash', 'big↦cash']
        print(response.result)
        response = await client.other.remove_machine(name=name)
        assert response.result == f'Machine {name} has removed'
        print(response.result)
        response = await client.other.find_or_create_machine(name=name)
        assert response.result == 'undefined'
        print(response.result)
        response = await client.other.update_state(name=name, phrase='Большую')
        assert response.result == 'big'
        print(response.result)
        response = await client.other.update_state(name=name, phrase='Картой')
        print(response.result)
        assert response.result == 'big↦card'
        response = await client.other.update_state(name=name, phrase='Наличкой')
        assert response.result == 'big↦cash'
        print(response.result)
        response = await client.other.update_state(name=name, phrase='Маленькую')
        assert response.result == 'small'
        print(response.result)
        response = await client.other.update_state(name=name, phrase='Картой')
        assert response.result == 'small↦card'
        print(response.result)
        response = await client.other.update_state(name=name, phrase='Наличкой')
        assert response.result == 'small↦cash'
        print(response.result)



if __name__ == "__main__":
    # run the client until it completes interaction with server
    asyncio.get_event_loop().run_until_complete(
        run_client("ws://localhost:9000/ws", name='John')
    )
