import asyncio
from fastapi_websocket_rpc import RpcMethodsBase, WebSocketRpcClient


async def create(uri, name):
    async with WebSocketRpcClient(uri, RpcMethodsBase(),
                                  default_response_timeout=10) as client:
        response = await client.other.find_or_create_machine(name=name)
        return response


async def update(uri, name, phrase):
    async with WebSocketRpcClient(uri, RpcMethodsBase(),
                                  default_response_timeout=10) as client:
        response = await client.other.update_state(name=name, phrase=phrase)
        return response


async def reset(uri, name):
    async with WebSocketRpcClient(uri, RpcMethodsBase(),
                                  default_response_timeout=10) as client:
        response = await client.other.reset_state(name=name)
        return response


async def get_state(uri, name):
    async with WebSocketRpcClient(uri, RpcMethodsBase(),
                                  default_response_timeout=10) as client:
        response = await client.other.get_state(name=name)
        return response


async def get_hist(uri, name):
    async with WebSocketRpcClient(uri, RpcMethodsBase(),
                                  default_response_timeout=10) as client:
        response = await client.other.get_hist(name=name)
        return response


if __name__ == "__main__":
    # run the client until it completes interaction with server
    asyncio.get_event_loop().run_until_complete(
        create("ws://localhost:9000/ws", name='John')
    )
