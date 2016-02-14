import logging
from pytg import Telegram
from pytg.utils import coroutine

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('rename_bot')


TG_BIN = '/home/huiyiqun/bin/telegram-cli'
TG_PUBKEY = '/home/huiyiqun/Source/tg/tg-server.pub'

tg = Telegram(telegram=TG_BIN, pubkey_file=TG_PUBKEY)
self = tg.sender.get_self()['username']


@coroutine
def main_loop():
    while True:
        msg = (yield)
        if msg.event != 'message' or 'text' not in msg:  # Not a text message
            logger.debug("this is not a message")
            continue
        logger.info("Message: %s", msg.text)

        # if msg.own:  # Sent by myself
        #     logger.debug("this message is sent by my self")
        #     continue
        if not msg.text.startswith("/"):  # Not command
            logger.debug("this message is not a command")
            continue

        if " " in msg.text:
            cmd, args = msg.text.split(" ", maxsplit=1)
        else:
            logger.warning("there are no arguments")
            cmd = msg.text
            args = ""

        if "@" in cmd:
            cmd, to = cmd.split("@", maxsplit=1)
            if to != self:  # This command is not for me
                logger.debug("this command is not for me")
                continue

        if cmd[1:] == 'rename':
            logger.debug(msg)
            tg.sender.channel_rename(msg.receiver.name, args)

tg.receiver.start()
tg.receiver.message(main_loop())
