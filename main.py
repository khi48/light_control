import RPi.GPIO as GPIO

import tapo

import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

from tapo import ApiClient

env_path = f"{str(Path(__file__).parent.absolute())}/.env"
load_dotenv(dotenv_path=env_path)

device=None
button_pin=26


async def toggle_light():
    global device
    
    device_info = await device.get_device_info()

    if device_info.device_on:
        await device.off()
    else:
        await device.on()

# Setup GPIO16 as input with internal pull-up resistor to hold it HIGH
# until it is pulled down to GND by the connected button: 
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Register an edge detection event on FALLING edge. When this event
# fires, the callback onButton() will be executed. Because of
# bouncetime=20 all edges 20 ms after a first falling edge will be ignored: 
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=toggle_light, bouncetime=20)

async def main(client):
    global device 
    device = await client.l510(ip_address)

    # await device.set_brightness(5)


if __name__ == "__main__":
    tapo_username = os.getenv("TAPO_USERNAME")
    tapo_password = os.getenv("TAPO_PASSWORD")
    ip_address = os.getenv("IP_ADDRESS")

    button_push = True
    client = ApiClient(tapo_username, tapo_password)
    asyncio.run(main(client))