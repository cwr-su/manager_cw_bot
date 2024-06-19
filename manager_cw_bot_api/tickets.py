"""
Module of the ticket-system with work in DB MySQL.
"""
import datetime
import random
import string

import pymysql
import telebot
from telebot import types

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.mysql_connection import Connection


class TicketUserView:
    """
    Class of the ticket system UI for users.
    """

    def __init__(self, bot: telebot.TeleBot, mysql_data: dict) -> None:
        self.__bot: telebot.TeleBot = bot
        self.__mysql_data: dict = mysql_data

    def show_user_menu(self, call_query: types.CallbackQuery) -> None:
        """
        Function of the show user's menu.

        :param call_query: Callback Query by click on the button.
        :return: None.
        """
        self.__bot.edit_message_text(
            text="🔹 You're in the TicketSystem Menu (USER)",
            chat_id=call_query.message.chat.id,
            message_id=call_query.message.message_id,
            reply_markup=Buttons.get_menu_user_tickets()
        )

        self.__bot.register_callback_query_handler(
            callback=self.__show_user_tickets,
            func=lambda call: call.data == "show_user_tickets"
        )
        self.__bot.register_callback_query_handler(
            callback=self.__send_new_ticket,
            func=lambda call: call.data == "send_new_ticket"
        )

    def __show_user_tickets(self, call_query: types.CallbackQuery) -> None:
        """
        Show user's tickets in the Menu with mini-UI.

        :param call_query: Callback Query.
        :return: None.
        """
        response: tuple = Buttons.get_user_tickets(
            call_query.from_user.username
        )
        self.__bot.edit_message_text(
            text=f"💫 Here your ID tickets and Subjects\n\n{response[0]}",
            chat_id=call_query.message.chat.id,
            message_id=call_query.message.message_id,
            reply_markup=response[1],
            parse_mode="HTML"
        )

    def __send_new_ticket(self, call_query: types.CallbackQuery) -> None:
        """
        Send ticket to admin via Manager Bot in the Menu with mini-UI.

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            text="⚠ Please, tell me ID Ticket, your message and new status of the ticket, "
                 "which you want to answer. System use special "
                 "parse-mode here!\n\n"
                 "FORMAT your message: ``` ID_TICKET ~ MESSAGE```\n"
                 "1. IF YOU WANT *TO ATTACH THE PHOTO use this free website* (we checked "
                 "it!): "
                 "https://imgbly.com/;\n"
                 "2. IF YOU WANT *TO ATTACH THE DOCUMENT-FILE use this free website* (we "
                 "checked it!): https://www.file.io/;\n"
                 "3. IF YOU WANT *TO USE THE SYMBOL*: ```'``` - *USE THIS* (backquote): ```` "
                 "```"
                 "4. IF YOU WANT *TO USE THE SYMBOL*: ```\\``` - *USE THIS* (double slash): "
                 "```\\\\```"
                 "But when you'll send, you agree with rules of "
                 "'SENDER'.\n\n_1. Please, don't send spam or other ticket as spam\n"
                 "2. Don't use TicketSystem like personal messenger!_",
            chat_id=call_query.message.chat.id,
            message_id=call_query.message.message_id,
            parse_mode="Markdown"
        )
        self.__bot.register_next_step_handler(call_query.message, self.__sending_ticket)

    def __sending_ticket(self, message: types.Message) -> None:
        """
        Sending the ticket from the user to admin and save data of ticket in the DB (MySQL).

        :param message: Message (data ticket) of the user.
        :return: None.
        """
        if message.content_type != "text":
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"{message.from_user.first_name}, it isn't only text-format (type)! Please, "
                     f"explore the rules and tips given above, if you want to send a ticket.",
                reply_markup=Buttons.get_menu_user_tickets_again()
            )
        else:
            if not (25 <= len(message.text) <= 2500):
                self.__bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"{message.from_user.first_name}, your message doesn't have "
                         f"25<=symbols<=2500! "
                         f"Please, explore the rules and tips given above, "
                         f"if you want to send a ticket.",
                    reply_markup=Buttons.get_menu_user_tickets_again()
                )
            else:
                try:
                    connection: pymysql.connections.Connection | str = Connection.get_connection(
                        self.__mysql_data
                    )
                    cursor = connection.cursor()

                    id_ticket = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
                    subject = message.text[:24]
                    username: str = message.from_user.username
                    tg_id_sender: int = message.from_user.id
                    ticket_data: str = f"--User: {message.text}"
                    create_at: str = (
                        datetime.datetime.
                        now(datetime.timezone(datetime.timedelta(hours=3))).
                        strftime('%d.%m.%Y | %H:%M:%S MSK+3')
                    )

                    query = f"""INSERT INTO users (id_ticket, username, tg_id_sender, 
                    ticket_data, create_at, subject) VALUES('{id_ticket}', '{username}', 
                    '{tg_id_sender}', '{ticket_data}', '{create_at}', 
                    '{subject}');"""
                    cursor.execute(query)

                    query_select_1step = "SELECT count_of_tickets_system FROM analytics;"
                    cursor.execute(query_select_1step)
                    result = cursor.fetchall()

                    if len(result) == 0:
                        query_update_2step = f"""INSERT INTO analytics ( count_of_tickets_system )
                        VALUES ( {1} );"""
                        cursor.execute(query_update_2step)
                    else:
                        query_update_2step = f"""UPDATE analytics SET count_of_tickets_system = 
                        {result[0][0] + 1};"""
                        cursor.execute(query_update_2step)

                    connection.commit()

                    self.__bot.send_message(
                        chat_id=message.from_user.id,
                        text=f"✅ Successful! {message.from_user.first_name}, your ticket added and "
                             f"sent.",
                        reply_markup=Buttons.get_menu_user_tickets_again()
                    )

                    connection.close()

                except Exception as ex:
                    with open("logs.txt", 'a') as logs:
                        logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                                   f"__sending_ticket-function of tickets.py\n")
                    print(ex)
                    self.__bot.send_message(
                        chat_id=message.from_user.id,
                        text=f"❌ We have a problem! {message.from_user.first_name}, your ticket "
                             f"didn't add and didn't send. Please, repeat later.",
                        reply_markup=Buttons.get_menu_user_tickets_again()
                    )


class TicketAdminView:
    """
    Class of the ticket system UI for admin.
    """

    def __init__(self, bot: telebot.TeleBot, mysql_data: dict) -> None:
        self.__bot: telebot.TeleBot = bot
        self.__mysql_data: dict = mysql_data

    def show_admin_users_tickets(self, call_query: types.CallbackQuery) -> None:
        """
        Function of the show tickets to admin.

        :param call_query: Callback Query by click on the button.
        :return: None.
        """

        response: tuple = Buttons.get_users_tickets_for_admin()
        self.__bot.edit_message_text(
            text=f"🔹 Tickets (ADMIN)\n\n{response[0]}",
            chat_id=call_query.message.chat.id,
            message_id=call_query.message.message_id,
            reply_markup=response[1],
            parse_mode="HTML"
        )


class TicketAnswersToUsers:
    """Class for manage answers to users by ticket-system."""

    def __init__(self, bot: telebot.TeleBot, admin_id: int, mysql_data: dict) -> None:
        self.__bot: telebot.TeleBot = bot
        self.__admin_id: int = admin_id
        self.__mysql_data: dict = mysql_data

    def explore_answer_users_ticket(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (call-handler) for get id ticket for answer to user.

        :param call_query: Callback Query.
        :return: None.
        """
        if call_query.from_user.id == self.__admin_id:
            self.__bot.edit_message_text(
                text=f"⚠ Please, tell me ID Ticket, your message and new status of the ticket, "
                     f"which you want to answer. System use special "
                     f"parse-mode here!\n\n"
                     f"FORMAT your message: ``` ID_TICKET ~ MESSAGE ~ "
                     f"NEW_STATUS```\n"
                     f"1. IF YOU WANT *TO ATTACH THE PHOTO use this free website* (we checked "
                     f"it!): "
                     f"https://imgbly.com/;\n"
                     f"2. IF YOU WANT *TO ATTACH THE DOCUMENT-FILE use this free website* (we "
                     f"checked it!): https://www.file.io/;\n"
                     f"3. IF YOU WANT *TO USE THE SYMBOL*: ```'``` - *USE THIS* (backquote): ```` "
                     f"```"
                     f"4. IF YOU WANT *TO USE THE SYMBOL*: ```\\``` - *USE THIS* (double slash): "
                     f"```\\\\```"
                     f"But when you'll send, you agree with rules of "
                     f"'SENDER'.\n\n_1. Please, don't send spam or other ticket as spam\n"
                     f"2. Don't use TicketSystem like personal messenger!_",
                chat_id=call_query.message.chat.id,
                message_id=call_query.message.message_id,
                parse_mode="Markdown"
            )
            self.__bot.register_next_step_handler(call_query.message, self.__get_id_ticket_for_answer)

    def __get_id_ticket_for_answer(self, message: types.Message) -> None:
        """
        Get id ticket for answer to user and sending answer to the user.

        :param message: Message of the user.
        :return: None.
        """
        try:
            connection: pymysql.connections.Connection | str = Connection.get_connection(
                self.__mysql_data
            )
            cursor = connection.cursor()

            id_ticket: str = message.text.split(' ~ ')[0]
            message_for_ticket: str = message.text.split(' ~ ')[1]
            new_status: str = message.text.split(' ~ ')[2]

            if len(id_ticket) == 5:
                query: str = f"""SELECT tg_id_sender, ticket_data, subject
                             FROM users WHERE id_ticket = %s;"""
                cursor.execute(query, (id_ticket,))
                result: tuple = cursor.fetchall()
                if len(result) == 0:
                    self.__bot.reply_to(
                        message=message,
                        text=f"Sorry! Data is none!\n"
                             f"Your message: {message.text}"
                    )
                else:
                    response: tuple = result[0]

                    tg_id_sender: int = int(response[0])
                    content_ticket_data: str = response[1]
                    subject: str = response[2]

                    self.__bot.send_message(
                        chat_id=tg_id_sender,
                        text=f"👤 ADMIN ANSWER\n\n"
                             f"#️⃣ ID Ticket: {id_ticket}\n"
                             f"🌐 STATUS: {new_status}\n"
                             f"✉ Subject: {subject}\n"
                             f"📩 Content of message: \n\n      {message_for_ticket}",
                        reply_markup=Buttons.back_on_main()
                    )
                    msg: types.Message = self.__bot.send_message(
                        chat_id=message.from_user.id,
                        text=f"✅ SUCCESSFUL! Your message has been delivered!"
                    )
                    if (len(content_ticket_data) + len(message_for_ticket)) <= 3800:
                        new_content_data: str = (f"{content_ticket_data}\n"
                                                 f"--Admin: {message_for_ticket}")
                    else:
                        new_content_data: str = f"{message_for_ticket}"

                    query: str = f"""UPDATE users SET ticket_data = '{new_content_data}', 
                                 status = '{new_status}' WHERE id_ticket = %s;"""
                    cursor.execute(query, (id_ticket,))
                    connection.commit()
                    self.__bot.edit_message_text(
                        chat_id=message.from_user.id,
                        message_id=msg.message_id,
                        text=f"✅ SUCCESSFUL! Updated DB-data for ID: {id_ticket}!",
                        reply_markup=Buttons.back_on_main()
                    )

            else:
                self.__bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"Sorry! It's not ID Ticket, because length of your message isn't 5 "
                         f"symbols!\nYour message: {message.text}",
                    reply_markup=Buttons.back_on_main()
                )

            connection.close()

        except Exception as ex:
            with open("logs.txt", 'a') as logs:
                logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                           f"__get_id_ticket_for_answer-function of business.py\n")
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"❌ FAIL!",
                reply_markup=Buttons.back_on_main()
            )


class TicketAnswersToAdmin:
    """Class for manage answers to admin by ticket-system."""

    def __init__(self, bot: telebot.TeleBot, admin_id: int, mysql_data: dict) -> None:
        self.__bot: telebot.TeleBot = bot
        self.__admin_id: int = admin_id
        self.__mysql_data: dict = mysql_data

    def explore_answer_admin_by_ticket(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (call-handler) for get id ticket for answer to admin.

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            text=f"⚠ Please, tell me ID Ticket, your message and new status of the ticket, "
                 f"which you want to answer. System use special "
                 f"parse-mode here!\n\n"
                 f"FORMAT your message: ``` ID_TICKET ~ MESSAGE```\n"
                 f"1. IF YOU WANT *TO ATTACH THE PHOTO use this free website* (we checked "
                 f"it!): "
                 f"https://imgbly.com/;\n"
                 f"2. IF YOU WANT *TO ATTACH THE DOCUMENT-FILE use this free website* (we "
                 f"checked it!): https://www.file.io/;\n"
                 f"3. IF YOU WANT *TO USE THE SYMBOL*: ```'``` - *USE THIS* (backquote): ```` ```"
                 f"4. IF YOU WANT *TO USE THE SYMBOL*: ```\\``` - *USE THIS* (double slash): "
                 f"```\\\\```"
                 f"But when you'll send, you agree with rules of "
                 f"'SENDER'.\n\n_1. Please, don't send spam or other ticket as spam\n"
                 f"2. Don't use TicketSystem like personal messenger!_",
            chat_id=call_query.message.chat.id,
            message_id=call_query.message.message_id,
            parse_mode="Markdown"
        )
        self.__bot.register_next_step_handler(call_query.message,
                                              self.__get_id_ticket_for_answer_for_admin)

    def __get_id_ticket_for_answer_for_admin(self, message: types.Message) -> None:
        """
        Get id ticket for answer to user and sending answer to admin.

        :param message: Message of the user.
        :return: None.
        """
        try:
            connection: pymysql.connections.Connection | str = Connection.get_connection(
                self.__mysql_data
            )
            cursor = connection.cursor()
            id_ticket: str = message.text.split(' ~ ')[0]
            message_for_ticket: str = message.text.split(' ~ ')[1]

            if len(id_ticket) == 5:
                query: str = f"""SELECT tg_id_sender, ticket_data, status, subject
                             FROM users WHERE id_ticket = %s;"""
                cursor.execute(query, (id_ticket,))
                result: tuple = cursor.fetchall()

                if len(result) == 0:
                    self.__bot.reply_to(
                        message=message,
                        text=f"Sorry! Data is none!\n"
                             f"Your message: {message.text}"
                    )
                else:
                    response: tuple = result[0]

                    tg_id_sender: int = int(response[0])
                    content_ticket_data: str = response[1]
                    status: str = response[2]
                    subject: str = response[3]

                    if tg_id_sender == message.from_user.id:
                        self.__bot.send_message(
                            chat_id=self.__admin_id,
                            text=f"👤 USER ANSWER\n\n"
                                 f"#️⃣ ID Ticket: {id_ticket}\n"
                                 f"🌐 STATUS: {status}\n"
                                 f"✉ Subject: {subject}\n"
                                 f"📩 Content of message: \n\n      {message_for_ticket}",
                            reply_markup=Buttons.back_on_main()
                        )

                        msg: types.Message = self.__bot.send_message(
                            chat_id=message.from_user.id,
                            text=f"✅ SUCCESSFUL! Your message has been delivered!"
                        )
                        if (len(content_ticket_data) + len(message_for_ticket)) <= 3800:
                            new_content_data: str = (f"{content_ticket_data}\n"
                                                     f"--User: {message_for_ticket}")
                        else:
                            new_content_data: str = f"{message_for_ticket}"

                        query: str = f"""
                                     UPDATE users SET ticket_data = '{new_content_data}' 
                                     WHERE id_ticket = %s;
                                     """
                        cursor.execute(query, (id_ticket,))
                        connection.commit()
                        self.__bot.edit_message_text(
                            chat_id=message.from_user.id,
                            message_id=msg.message_id,
                            text=f"✅ SUCCESSFUL! Updated DB-data for ID: {id_ticket}!",
                            reply_markup=Buttons.back_on_main()
                        )
                    else:
                        self.__bot.send_message(
                            chat_id=tg_id_sender,
                            text=f"🚫 ERROR 43! {message.from_user.first_name}, forbidden!",
                            parse_mode="Markdown",
                            reply_markup=Buttons.back_on_main()
                        )

            else:
                self.__bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"Sorry! It's not ID Ticket, because length of your message isn't 5 "
                         f"symbols!\nYour message: {message.text}",
                    reply_markup=Buttons.back_on_main()
                )

            connection.close()

        except Exception as ex:
            with open("logs.txt", 'a') as logs:
                logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                           f"__get_id_ticket_for_answer-function of business.py\n")
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"❌ FAIL! {ex}",
                reply_markup=Buttons.back_on_main()
            )
