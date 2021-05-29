import asyncio
from fastapi_websocket_rpc import RpcMethodsBase, WebSocketRpcClient
import pytest


@pytest.mark.asyncio
async def test_client(uri="ws://localhost:9000/ws", name=123):
    async with WebSocketRpcClient(uri, RpcMethodsBase()) as client:
        response = await client.other.reset_or_create_machine(name=name)
        assert response.result in ['undefined', 'маленькую', 'большую',
                                   'маленькую↦картой', 'большую↦картой',
                                   'маленькую↦картой', 'большую↦наличкой']
        response = await client.other.remove_machine(name=name)
        assert response.result == f'Machine {name} has removed'
        response = await client.other.reset_or_create_machine(name=name)
        assert response.result == 'undefined'
        response = await client.other.update_state(name=name, phrase='большую')
        assert response.result == 'большую'
        response = await client.other.update_state(name=name, phrase='картой')
        assert response.result == 'большую↦картой'
        response = await client.other.update_state(name=name,
                                                   phrase='наличкой')
        assert response.result == 'большую↦наличкой'
        response = await client.other.update_state(name=name,
                                                   phrase='маленькую')
        assert response.result == 'маленькую↦наличкой'
        response = await client.other.update_state(name=name, phrase='картой')
        assert response.result == 'маленькую↦картой'
        response = await client.other.update_state(name=name,
                                                   phrase='наличкой')
        assert response.result == 'маленькую↦наличкой'
