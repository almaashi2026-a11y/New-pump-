import os
import telebot
import time
import yfinance as yf
from finvizfinance.screener.overview import Overview

# قراءة المتغيرات من Render
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# التحقق من وجود التوكن لتجنب الخطأ الذي ظهر
if not BOT_TOKEN:
    raise ValueError("لم يتم العثور على TELEGRAM_BOT_TOKEN في المتغيرات!")

bot = telebot.TeleBot(BOT_TOKEN)
