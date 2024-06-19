"""
Module of the GigaChatAI.
"""
import telebot
from telebot import types
<<<<<<< HEAD
import pymysql
import datetime

from manager_cw_bot_api.giga_request import (pro, light)
from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.mysql_connection import Connection
=======

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.giga_request import (pro, light)
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB
>>>>>>> f20ff53 (Updated data manager)


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
<<<<<<< HEAD
            text="Enter your request...",
=======
            text="🧠 Enter your request...",
>>>>>>> f20ff53 (Updated data manager)
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
<<<<<<< HEAD
        chooses_buttons: types.InlineKeyboardMarkup = Buttons.get_var_giga_version()
=======
        chooses_buttons: types.InlineKeyboardMarkup = Buttons.get_var_giga_version(message)
>>>>>>> f20ff53 (Updated data manager)

        self.__class__.msg_bot = self.__bot.send_message(
            chat_id=message.from_user.id,
            text=f"{message.from_user.first_name}, please, "
<<<<<<< HEAD
                 f"select the required 🧠 AI-Model, click below",
            reply_markup=chooses_buttons
        )

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
=======
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
>>>>>>> f20ff53 (Updated data manager)

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
<<<<<<< HEAD
        except Exception as ex:
            try:
                self.__bot.edit_message_text(
                    text=self.response,
                    chat_id=call_query.message.chat.id,
                    message_id=self.__class__.msg_bot.message_id,
                    reply_markup=Buttons.say_thanks()
                )

            except Exception:
                pass
            with open("../logs.txt", 'a') as logs:
                logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                           f"__giga_version_1-function of "
                           f"gigachatai.py. Get Response from GigaChatAPI "
                           f"and edit message | LIGHT V.\n")
            print(f"The error (ex): {ex} | Get Response from GigaChatAPI and edit message | "
                  f"LIGHT V.")
=======

        except Exception:
            self.__bot.edit_message_text(
                text=self.response,
                chat_id=call_query.message.chat.id,
                message_id=self.__class__.msg_bot.message_id,
                reply_markup=Buttons.say_thanks()
            )
>>>>>>> f20ff53 (Updated data manager)

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
<<<<<<< HEAD
        except Exception as ex:
            try:
                self.__bot.edit_message_text(
                    text=self.response,
                    chat_id=call_query.message.chat.id,
                    message_id=self.__class__.msg_bot.message_id,
                    reply_markup=Buttons.say_thanks()
                )
            except Exception:
                pass
            with open("../logs.txt", 'a') as logs:
                logs.write(f"{datetime.datetime.now()} | {ex} | "
                           f"The error in __giga_version_2-function of "
                           f"gigachatai.py. Get Response from "
                           f"GigaChatAPI and edit message | PRO V.\n")
            print(f"The error (ex): {ex} | Get Response from GigaChatAPI and edit message | "
                  f"PRO V.")
=======
        except Exception:
            self.__bot.edit_message_text(
                text=self.response,
                chat_id=call_query.message.chat.id,
                message_id=self.__class__.msg_bot.message_id,
                reply_markup=Buttons.say_thanks()
            )
>>>>>>> f20ff53 (Updated data manager)

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

<<<<<<< HEAD
        connection: pymysql.connections.Connection | str = Connection.get_connection(
            self.__mysql_data
        )
        cursor = connection.cursor()

        query: str = "SELECT count_of_thanks_from_users FROM analytics"
        cursor.execute(query)
        count_of_thanks_from_users = cursor.fetchall()

        if len(count_of_thanks_from_users) == 0:
            query: str = f"""INSERT INTO analytics (count_of_thanks_from_users)
                    VALUES ({1});
                    """
            cursor.execute(query)
        else:
            query: str = f"""UPDATE analytics SET 
                         count_of_thanks_from_users = {count_of_thanks_from_users[0][0] + 1}
                         """
            cursor.execute(query)

        connection.commit()
        connection.close()
=======
        HandlerDB.update_analytic_datas()
>>>>>>> f20ff53 (Updated data manager)
