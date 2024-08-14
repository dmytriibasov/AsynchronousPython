import asyncio


class WeatherServerClient:

    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port

    async def send_message(self, writer: asyncio.StreamWriter, message: str):
        print(f'Sending message: {message}')
        msg_bytes = message.encode()
        writer.write(msg_bytes)
        await writer.drain()

    async def read_response(self, reader: asyncio.StreamReader):
        print('Waiting for response...')
        msg = await reader.readline()
        response = msg.decode()
        print(f'Server responded: {response}')

    async def run_client(self):
        message = "What is the weather today?"
        reader, writer = await asyncio.open_connection(self.host, self.port)
        print('Connected')
        await self.send_message(writer, message)
        await self.read_response(reader)
        writer.close()
        await writer.wait_closed()


asyncio.run(WeatherServerClient().run_client())
