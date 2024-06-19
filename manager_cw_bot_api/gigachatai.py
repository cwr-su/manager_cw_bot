"""
Module of the GigaChatAI.
"""
import telebot
from telebot import types

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.giga_request import (pro, light)
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB


class GigaChatAI:
    """
    Class of the helper for the users and admin - GigaChat.
    """
    msg_bot: types.Message = None
    request_user: str = None

    def __init__(self, bot, call_query: types.CallbackQuery,
                 mysql_data: dict, admin_id: int) -> None:
        self.__bot: telebot.TeleBot = bot
        self.__call_query: types.CallbackQuery = call_query
        self.__mysql_data: dict = mysql_data
        self.__admin_id: int = admin_id

    def show_info_edit_text(self) -> None:
        """
        Show pre-answer message by editing text.

        :return: None.
        """
        self.__bot.edit_message_text(
            text="🧠 Enter your request...",
            chat_id=self.__call_query.message.chat.id,
            message_id=self.__call_query.message.message_id,
        )

    def request(self, message: types.Message) -> None:
        """
        Request from the user, handler of the buttons and register callback-query.

        :param message: User message.
        :return: None.
        """
        self.__class__.request_user = message.text
        chooses_buttons: types.InlineKeyboardMarkup = Buttons.get_var_giga_version(message)

        self.__class__.msg_bot = self.__bot.send_message(
            chat_id=message.from_user.id,
            text=f"{message.from_user.first_name}, please, "
                 f"select the required 🧠 AI-Model, click below.",
            reply_markup=chooses_buttons
        )

        result: bool | tuple = HandlerDB.check_subscription(message)
        if result[0] is True:
            self.__bot.register_callback_query_handler(
                callback=self.__giga_version_1,
                func=lambda call: call.data == "gigachat_version_light"
            )
            self.__bot.register_callback_query_handler(
                callback=self.__giga_version_2,
                func=lambda call: call.data == "gigachat_version_pro"
            )
            self.__bot.register_callback_query_handler(
                callback=self.__say_thanks,
                func=lambda call: call.data == "say_thanks"
            )
        else:
            self.__bot.register_callback_query_handler(
                callback=self.__giga_version_1,
                func=lambda call: call.data == "gigachat_version_light"
            )
            self.__bot.register_callback_query_handler(
                callback=self.__say_thanks,
                func=lambda call: call.data == "say_thanks"
            )

    def __giga_version_1(self, call_query: types.CallbackQuery) -> None:
        """
        Handler of the callback query by click on the btn1: LightVersion of GigaChat.

        :param call_query: Query (by click on the button) with callback.
        :return: None.
        """
        self.__bot.edit_message_text(
            text="💭 Please, waiting... I'm thinking",
            chat_id=call_query.message.chat.id,
            message_id=self.__class__.msg_bot.message_id
        )

        try:
            self.response: str = light(self.__class__.request_user)
            self.__bot.edit_message_text(
                text=self.response,
                chat_id=call_query.message.chat.id,
                message_id=self.__class__.msg_bot.message_id,
                parse_mode="Markdown",
                reply_markup=Buttons.say_thanks()
            )

        except Exception:
            self.__bot.edit_message_text(
                text=self.response,
                chat_id=call_query.message.chat.id,
                message_id=self.__class__.msg_bot.message_id,
                reply_markup=Buttons.say_thanks()
            )

    def __giga_version_2(self, call_query: types.CallbackQuery) -> None:
        """
        Handler of the callback query by click on the btn1: PROVersion of GigaChat.

        :param call_query: Query (by click on the button) with callback.
        :return: None.
        """
        self.__bot.edit_message_text(
            text="💭 Please, waiting... 🧠 I'm thinking",
            chat_id=call_query.message.chat.id,
            message_id=self.__class__.msg_bot.message_id
        )

        try:
            self.response: str = pro(self.__class__.request_user)
            self.__bot.edit_message_text(
                text=self.response,
                chat_id=call_query.message.chat.id,
                message_id=self.__class__.msg_bot.message_id,
                parse_mode="Markdown",
                reply_markup=Buttons.say_thanks()
            )
        except Exception:
            self.__bot.edit_message_text(
                text=self.response,
                chat_id=call_query.message.chat.id,
                message_id=self.__class__.msg_bot.message_id,
                reply_markup=Buttons.say_thanks()
            )

    def __say_thanks(self, call_query: types.CallbackQuery) -> None:
        """
        Function counter/sender for count_of_thanks_from_users.

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.send_message(
            chat_id=call_query.message.chat.id,
            text=f"{call_query.from_user.first_name}, thank you for your feedback! 💞🙏"
        )
        self.__bot.send_message(
            chat_id=self.__admin_id,
            text=f"{call_query.from_user.first_name} thanked you! 💖"
        )

        HandlerDB.update_analytic_datas()