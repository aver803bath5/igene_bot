# -*- coding: utf-8 -*-

from telegram.ext import Updater
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from bs4 import BeautifulSoup
from ConfigParser import RawConfigParser
import logging
import re
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def google(bot, update):
    search = update.message.text
    search = re.sub(r'^(?i)google ','',search)
    logger.info("Google %s" %search)
    r = requests.get('https://www.google.com/search?q='+ search)
    soup = BeautifulSoup(r.text, "html.parser")
    result = soup.find('h3', {'class': 'r'}).find('a').attrs['href'].strip()
    update.message.reply_text(result)

def girlfriend(bot, update):
    logger.info("girlfriend called")
    update.message.reply_text(u"醒醒吧你沒有女友")

def sister(bot, update):
    logger.info("sister called")
    update.message.reply_text(u"醒醒吧你沒有妹妹")
    
def no_money(bot, update):
    logger.info("no money called")
    update.message.reply_sticker(sticker='CAADBQADTgADVRXrCVFQ913jCk08Ag')

def main():
    cfg = RawConfigParser()
    with open('config', 'rb') as fp:
        cfg.readfp(fp, 'config')
    token = cfg.get('auth', 'token')
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(RegexHandler('^(?i)google .*', google))
    dp.add_handler(RegexHandler(u'.*女朋友.*', girlfriend))
    dp.add_handler(RegexHandler(u'.*妹妹.*', sister))
    dp.add_handler(RegexHandler(u'.*沒錢.*', no_money))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()