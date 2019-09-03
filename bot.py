#!/usr/bin/env python3

import os
import argparse
import logging
import datetime

from telegram.ext import Updater, MessageHandler, Filters


def handle_event(update, context):
    doc = update.message.document
    if doc is None:
        return

    username = update.message.chat.username
    logging.info(f'Got file {doc.file_name} from {username}')

    path = os.path.join(os.path.abspath(args.save_dir), username)
    os.makedirs(path, exist_ok=True)

    timestamp = int(datetime.datetime.now().timestamp() * 1e6)

    name = f'{timestamp}_{doc.file_name}'

    file = doc.get_file()
    file_path = os.path.join(path, name)

    file.download(custom_path=file_path)

    logging.info(f'File saved to {file_path}')

    update.message.reply_text(f'👆 {username}/{name}', quote=True)


if __name__ == '__main__':
    logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('--token', required=True, help='Telegram API token')
    parser.add_argument('--save-dir', default='.', help='Directory to save files to')

    args = parser.parse_args()

    updater = Updater(args.token, use_context=True)

    updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_event))

    updater.start_polling()

    logging.info('Started up')

    updater.idle()

