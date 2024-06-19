"""
Module of the analytics data from database for admin.
"""
import datetime

<<<<<<< HEAD
import telebot
from telebot import types
import pymysql

from manager_cw_bot_api.mysql_connection import Connection
from manager_cw_bot_api.buttons import Buttons
=======
import pymysql
import telebot
from telebot import types

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.mysql_connection import Connection
>>>>>>> f20ff53 (Updated data manager)


class Analytic:
    """
    Analytic Class.
    """
    def __init__(self, bot: telebot.TeleBot, mysql_data: dict,
                 call_query: types.CallbackQuery) -> None:
        self.__bot = bot
        self.__mysql_data: dict = mysql_data
        self.__call_query: types.CallbackQuery = call_query

    def analyse(self) -> None:
        """
        Analyse the data for admin.

        :return: None.
        """
        connection: pymysql.connections.Connection | str = Connection.get_connection(
            self.__mysql_data
        )
        cursor = connection.cursor()

        query: str = "SELECT * FROM analytics;"
        cursor.execute(query)
        response: tuple = cursor.fetchall()

        if len(response) == 0:
            count_of_ai_queries = 0
            count_of_tickets_system = 0
            count_of_thanks_from_users = 0
        else:
            count_of_ai_queries: int = response[0][0]
            count_of_tickets_system: int = response[0][1]
            count_of_thanks_from_users: int = response[0][2]

        try:
            self.__bot.edit_message_text(
                chat_id=self.__call_query.message.chat.id,
                text=f"⁉ Count of AI Queries (all): {count_of_ai_queries}\n\n"
                     f"🎫 Count of Tickets in the System (all): {count_of_tickets_system}\n\n"
                     f"🙏🏻 Count of THANKS for admin {count_of_thanks_from_users}\n\n"
                     f"The data is current as {datetime.datetime.now()}",
                message_id=self.__call_query.message.message_id,
<<<<<<< HEAD
                reply_markup=Buttons.get_menu_on_back_or_main(),
=======
                reply_markup=Buttons.back_on_main(),
>>>>>>> f20ff53 (Updated data manager)
                parse_mode="Markdown"
            )

        except Exception(BaseException) as ex:
            with open("logs.txt", 'a') as logs:
                logs.write(f"\n{datetime.datetime.now()} | {ex} | The error in run-function of "
                           f"business.py.\n")
            print(f"The Error (ex-run-func): {ex}")

        connection.close()
