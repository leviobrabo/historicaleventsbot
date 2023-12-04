from datetime import datetime

import pytz
import requests

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *
from historicalevents.utils.month import *


def get_holidays_of_the_day(CHANNEL):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://pt.wikipedia.org/api/rest_v1/feed/onthisday/holidays/{month}/{day}',
            headers={
                'accept': 'application/json; charset=utf-8; profile="https://www.mediawiki.org/wiki/Specs/onthisday/0.3.3"'
            },
        )

        if response.status_code == 200:
            data = response.json()
            holidays = data.get('holidays', [])

            if len(holidays) > 0:
                holiday_messages = []

                for index, holiday in enumerate(holidays[:5], start=1):
                    name = f"<b>{holiday.get('text', '')}</b>"
                    info = holiday.get('pages', [{}])[0].get(
                        'extract', 'Information not available.'
                    )

                    holiday_message = f'<i>{index}.</i> <b>Name:</b> {name}\n<b>Information:</b> {info}'
                    holiday_messages.append(holiday_message)

                message = f'<b>📆 | Commemorative dates on this day: {day} of {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(holiday_messages)
                message += '\n\n💬 Did you know? Follow @today_in_historys.'

                bot.send_message(CHANNEL, message)
            else:
                logger.info('-' * 50)
                logger.info(
                    'There is no information about worldwide holidays for the current day.'
                )
                logger.info('-' * 50)
        else:
            logger.info('-' * 50)
            logger.warning('Error obtaining information:',
                           response.status_code)
            logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error('Error obtaining information:', str(e))
        logger.info('-' * 50)


def hist_channel_holiday():
    try:
        get_holidays_of_the_day(CHANNEL)
        logger.info('-' * 50)
        logger.success(f'Holidays sent to channel {CHANNEL}')
        logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error('Error sending holidays job:', str(e))
        logger.info('-' * 50)