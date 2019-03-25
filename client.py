#!/usr/bin/env python

import asyncio
import websockets
import time

async def hello():
    i = 0
    prev_time = time.time()
    async with websockets.connect(
            'ws://localhost:8001') as websocket:
        while True:
            await websocket.send('')
            data = await websocket.recv()
            # print("Received image, len {}".format(len(data)))
            with open('img_{}.jpg'.format(i), 'wb') as f:
                f.write(data)
                i += 1
                if i % 10 == 0:
                    new_time = time.time()
                    fps = 1.0/(new_time - prev_time) * 10
                    prev_time = new_time
                    print("*** FPS: {0:.2f} ***".format(fps))

asyncio.get_event_loop().run_until_complete(hello())
