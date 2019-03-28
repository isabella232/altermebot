from telegram.ext import CommandHandler
from telegram import ParseMode


class OffCommandHandler(CommandHandler):
    """description of class"""

    def __init__(self, db_manager):
        super().__init__('off', self.__handle)
        self._db_manager = db_manager

    def __handle(self, bot, update):
        message = update.message
        chat_id = message.chat_id
        user_id = message.from_user.id

        user = message.from_user
        mention = user.username
        parse_mode = None
        if not mention:
            mention = '[%s](tg://user?id=%d)' % (user.full_name, user_id)
            parse_mode = ParseMode.MARKDOWN
        else:
            mention = "@%s" % mention

        self._db_manager.disable_aliasing(user_id, chat_id)

        bot.send_message(chat_id=chat_id,
                         text="%s, you will not be mentioned by your aliases in this chat from now" % mention,
                         parse_mode=parse_mode)

        self._db_manager.log_command(user_id, chat_id, 'off', 'OK')
