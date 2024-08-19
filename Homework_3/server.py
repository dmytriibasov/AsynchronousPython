import asyncio
from random import randint


class BroadcastWeatherServer:

    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.clients = set()

    async def handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.clients.add(writer)

        try:
            while True:
                await asyncio.sleep(1)

        except asyncio.CancelledError:
            pass
        finally:
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()

    async def broadcast_weather(self):
        while True:
            await asyncio.sleep(10)
            message = f"temp = {randint(-10, 40)} Celsius degree\n"
            print(message)
            for client in list(self.clients):

                try:
                    client.write(message.encode())
                    await client.drain()

                except Exception as e:
                    print(f'Failed to send to the client')
                    self.clients.remove(client)

    async def start_server(self):
        server = await asyncio.start_server(self.handler, self.host, self.port)
        async with server:
            await asyncio.gather(
                server.serve_forever(),
                self.broadcast_weather()
            )


asyncio.run(BroadcastWeatherServer().start_server())
