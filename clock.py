#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import os
import logging
import epd2in13_V3
import time
import json
import random
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13_V3 datetime and message of the day")

    epd = epd2in13_V3.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)

    # Drawing on the image
    font52 = ImageFont.truetype('TREBUCBD.ttf', 52)
    font24 = ImageFont.truetype('trebuc.ttf', 24)
    fontIT = ImageFont.truetype('trebucit.ttf', 20)

    clock_refresh_interval = 4  # 4 seconds
    motd_refresh_interval = 60  # 1 minute in seconds

    logging.info("Reading message of the day from JSON file...")
    with open('motd.json', 'r') as file:
        motd_data = json.load(file)

    logging.info("Showing time, date, and message of the day...")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    date_draw = ImageDraw.Draw(time_image)
    motd_draw = ImageDraw.Draw(time_image)
    previous_clock_time = ''
    previous_date = ''
    previous_motd_update = 0

    while True:
        current_time = time.strftime('%l:%M %p').lstrip().lower()
        if current_time != previous_clock_time:
            # Update time display
            time_draw.rectangle((0, 0, 250, 61), fill=255)
            time_draw.text((0, 0), current_time, font=font52, fill=0)
            rotated_time_image = time_image.rotate(180)
            epd.displayPartial(epd.getbuffer(rotated_time_image))
            previous_clock_time = current_time

        current_date = time.strftime('%A, %b %d, \'%y')
        if current_date != previous_date:
            # Update date display
            date_draw.rectangle((0, 61, 250, 86), fill=255)
            date_draw.text((0, 61), current_date, font=font24, fill=0)
            rotated_date_image = time_image.rotate(180)
            epd.displayPartial(epd.getbuffer(rotated_date_image))
            previous_date = current_date

        if time.time() - previous_motd_update >= motd_refresh_interval:
            # Choose a random line from motd_data
            random_motd = random.choice(motd_data)

            # Update motd display
            motd_draw.rectangle((0, 90, 250, 122), fill=255)
            motd_draw.text((0, 90), random_motd, font=fontIT, fill=0)
            rotated_motd_image = time_image.rotate(180)
            epd.displayPartial(epd.getbuffer(rotated_motd_image))

            previous_motd_update = time.time()

        time.sleep(clock_refresh_interval)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V3.epdconfig.module_exit()
    exit()
