#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os

picdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "pic"
)
libdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "lib"
)
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import epd2in13_V3
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13_V3 Demo")

    epd = epd2in13_V3.EPD()
    logging.info("init")
    epd.init()
    logging.info("clearing")
    epd.Clear(0xFF)

    # Drawing on the image
    font42 = ImageFont.truetype(
        os.path.join(picdir, "trebucbold.ttf"), 42
    )
    font24 = ImageFont.truetype(
        os.path.join(picdir, "trebuc.ttf"), 24
    )

    logging.info("Now displaying time")
    time_image = Image.new("1", (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    date_draw = ImageDraw.Draw(time_image)
    previous_time = ""
    previous_date = ""

    # While editing the parameters,
    # keep in mind that the resolution of the display is 250 × 122.

    while True:
        current_time = time.strftime("%H:%M:%S")
        if current_time != previous_time:
            time_draw.rectangle((0, 0, 250, 51), fill=255)
            time_draw.text((0, 0), current_time, font=font42, fill=0)
            rotated_time_image = time_image.rotate(180)
            epd.displayPartial(epd.getbuffer(rotated_time_image))
            previous_time = current_time
        current_date = time.strftime("%m/%d/%Y")
        if current_date != previous_date:
            date_draw.rectangle((0, 51, 250, 112), fill=255)
            date_draw.text((0, 51), current_date, font=font24, fill=0)
            rotated_date_image = time_image.rotate(180)
            epd.displayPartial(epd.getbuffer(rotated_date_image))
            previous_date = current_date
        time.sleep(5)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V3.epdconfig.module_exit()
    exit()
