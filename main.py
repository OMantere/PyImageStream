#!/usr/bin/env python3

import functools
import argparse
import os
import io
import asyncio
import websockets
import cv2


parser = argparse.ArgumentParser(description='Start the PyImageStream server.')

parser.add_argument('--port', default=8001, type=int, help='Web server port (default: 8888)')
parser.add_argument('--camera', default=0, type=int, help='Camera index, first camera is 0 (default: 0)')
parser.add_argument('--width', default=640, type=int, help='Width (default: 640)')
parser.add_argument('--height', default=480, type=int, help='Height (default: 480)')
parser.add_argument('--quality', default=70, type=int, help='JPEG Quality 1 (worst) to 100 (best) (default: 70)')
parser.add_argument('--stopdelay', default=7, type=int, help='Delay in seconds before the camera will be stopped after '
                                                             'all clients have disconnected (default: 7)')
args = parser.parse_args()

class Camera:

    def __init__(self, index, width, height, quality, stopdelay):
        print("Initializing camera...")
        self._cap = cv2.VideoCapture(0)
        print("Camera initialized")
        self.is_started = False
        self.stop_requested = False
        self.quality = quality
        self.stopdelay = stopdelay

    def request_start(self):
        if self.stop_requested:
            print("Camera continues to be in use")
            self.stop_requested = False
        if not self.is_started:
            self._start()

    def request_stop(self):
        if self.is_started and not self.stop_requested:
            self.stop_requested = True
            print("Stopping camera in " + str(self.stopdelay) + " seconds...")
            tornado.ioloop.IOLoop.current().call_later(self.stopdelay, self._stop)

    def _start(self):
        print("Starting camera...")
        self._cap.open(0)
        print("Camera started")
        self.is_started = True

    def _stop(self):
        if self.stop_requested:
            print("Stopping camera now...")
            self._cap.release()
            print("Camera stopped")
            self.is_started = False
            self.stop_requested = False

    def get_jpeg_image_bytes(self):
        cam_success, img = self._cap.read()
        if not cam_success:
            print("OpenCV: Camera capture failed")
            return None
        enc_success, buffer = cv2.imencode(".jpg", img)
        if not enc_success:
            print("OpenCV: Image encoding failed")
            return None
        return io.BytesIO(buffer).getvalue()


camera = Camera(args.camera, args.width, args.height, args.quality, args.stopdelay)

async def rpi_server(websocket, path):
    i = 0
    while True:
        data = camera.get_jpeg_image_bytes() 
        if data:
            await websocket.recv()
            await websocket.send(data)
            print("Sent image, len {}".format(len(data)))

start_server = websockets.serve(rpi_server, 'localhost', 8001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

