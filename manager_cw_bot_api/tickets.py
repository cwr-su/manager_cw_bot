"""
Module of the ticket-system with work in DB MySQL.
"""
import datetime
import logging
import random
import string
import json

import pymysql
from aiogram import Bot, types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB
from manager_cw_bot_api.mysql_connection import Connection
from manager_cw_bot_api.handler_email_sender import SenderEmail
from manager_cw_bot_api.pdf_generate_data import GenerateTicketDataUniversal
from manager_cw_bot_api.fsm_handler import (
    GetDataForSendNewTicket,
    GetTicketDataForAnswerToUser,
    GetTicketDataForAnswerToAdmin
)

router: Router = Router()


class TicketUserView:
    """
    Class of the ticket system UI for users.
    """
    __response_big: tuple = tuple()

    def __init__(self, bot: Bot, mysql_data: dict) -> None:
        self.__bot: Bot = bot
        self.__mysql_data: dict = mysql_data

        router.message.register(
            self.__sending_ticket,
            GetDataForSendNewTicket.ticket_data
        )

    async def show_user_menu(self, call_query: types.CallbackQuery) -> None:
        """
        Function of the show user's menu.

        :param call_query: Callback Query by click on the button.
        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.get_menu_user_tickets()
        await self.__bot.edit_message_text(
            text="🔹 You're in the TicketSystem Menu (USER UI | CWBot UI).",
            chat_id=call_query.message.chat.id,
            message_id=call_query.message.message_id,
            reply_markup=var.as_markup()
        )
        router.callback_query.register(
            self.__show_user_tickets,
            F.data == "show_user_tickets"
        )
        router.callback_query.register(
            self.__send_new_ticket,
            F.data == "send_new_ticket"
        )

    async def __show_user_tickets(self, call_query: types.CallbackQuery) -> None:
        """
        Show user's tickets in the Menu with mini-UI.

        :param call_query: Callback Query.
        :return: None.
        """

        response: tuple = await Buttons.get_user_tickets(
            call_query.from_user.id
        )
        if response[0][0] is False:
            await self.__bot.edit_message_text(
                text=f"🔹 Tickets (USER UI | CWBot UI)\n----------------------------------------"
                     f"\n{response[0][1]}",
                chat_id=call_query.message.chat.id,
                message_id=call_query.message.message_id,
                reply_markup=response[1].as_markup(),
                parse_mode="HTML"
            )
        elif response[0][0] is True:
            self.__class__.__response_big = response[0][1], response[0][2]

            await self.__bot.edit_message_text(
                text=f"🔹 Tickets (USER UI | CWBot UI)\n----------------------------------------"
                     f"\nI'm sorry, but "
                     f"I can't send the details of all tickets. More characters "
                     f"are required. Will you allow me to send the details of the remaining "
                     f"tickets to your email?\n\n<b>Available Data look after click on the "
                     f"button (which you need)</b>.",
                chat_id=call_query.message.chat.id,
                message_id=call_query.message.message_id,
                reply_markup=response[1].as_markup(),
                parse_mode="HTML"
            )

            router.callback_query.register(
                self.__allow_send_email_ticket_data_user,
                F.data == "allow_send_email_ticket_data_user"
            )
            router.callback_query.register(
                self.__not_allow_send_email_ticket_data_user,
                F.data == "not_allow_send_email_ticket_data_user"
            )

    async def __allow_send_email_ticket_data_user(self, call_query: types.CallbackQuery) -> None:
        """
        Allow to send email for ticket data (big) for user.

        :param call_query: CallbackQuery.
        :return: None.
        """
        try:
            var: InlineKeyboardBuilder = await Buttons.get_menu_user_tickets_again()
            await self.__bot.edit_message_text(
                text=f"🔹 Tickets (USER UI | CWBot UI)\n----------------------------------------\n"
                     f"⚡ <b>Available Data</b>:"
                     f"\n\n{self.__class__.__response_big[0]}",
                chat_id=call_query.message.chat.id,
                message_id=call_query.message.message_id,
                reply_markup=var.as_markup(),
                parse_mode="HTML"
            )

            result: tuple = await HandlerDB.get_email_data(call_query.from_user.id)
            if result[0]:
                file_path: str = await GenerateTicketDataUniversal.generate(
                    result[1][1],
                    self.__class__.__response_big[1]
                )
                await self.__bot.send_document(
                    chat_id=call_query.message.chat.id,
                    document=FSInputFile(file_path),
                    caption=f"✅ {call_query.from_user.first_name}, see TicketData in the "
                            f"attachment below. Also, for convenience, I am sending you an "
                            f"email with the same file, in the official format."
                )
                await SenderEmail.send_others_ticket_data_in_email_format(
                    result[1][0],
                    f"👤 TicketData from Manager CW for {result[1][1]} | CWR.SU",
                    result[1][1],
                    file_path
                )
                msg_temp: types.Message = await self.__bot.send_message(
                    text=f"✅ The data sent!",
                    chat_id=call_query.message.chat.id
                )

                await self.__bot.delete_message(
                    chat_id=msg_temp.chat.id,
                    message_id=msg_temp.message_id
                )

                var: InlineKeyboardBuilder = await Buttons.back_on_main()
                await self.__bot.send_message(
                    text=f"🔐 You've all the data and they're safe. To go to the main, click on "
                         f"the button below.",
                    chat_id=call_query.message.chat.id,
                    reply_markup=var.as_markup(),
                    parse_mode="HTML"
                )

                logging.info(
                    f"Successful! Sent data to user's EMail. "
                    f"User ID: {call_query.from_user.id}"
                )

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")

    async def __not_allow_send_email_ticket_data_user(
            self,
            call_query:
            types.CallbackQuery
    ) -> None:
        """
        Not allow to send email for ticket data (big) for user.

        :param call_query: CallbackQuery.
        :return: None.
        """
        try:
            var: InlineKeyboardBuilder = await Buttons.get_menu_user_tickets_again()
            await self.__bot.edit_message_text(
                text=f"🔹 Tickets (USER UI | CWBot UI)\n----------------------------------------\n"
                     f"⚡ <b>Available Data</b>:"
                     f"\n{self.__class__.__response_big[0]}",
                chat_id=call_query.message.chat.id,
                message_id=call_query.message.message_id,
                reply_markup=var.as_markup(),
                parse_mode="HTML"
            )

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")

    async def __send_new_ticket(self, call_query: types.CallbackQuery, state: FSMContext) -> None:
        """
        Send ticket to admin via Manager Bot in the Menu with mini-UI.

        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(GetDataForSendNewTicket.ticket_data)
        await self.__bot.edit_message_text(
            text="👌🏻 Please, send your message. System use special "
                 "parse-mode here!\n----------------------------------------\n"
                 "1. IF YOU WANT *TO ATTACH THE PHOTO use this free website* (we checked "
                 "it!): "
                 "https://imgbly.com/;\n"
                 "2. IF YOU WANT *TO ATTACH THE DOCUMENT-FILE use this free website* (we "
                 "checked it!): https://www.file.io/;\n"
                 "3. IF YOU WANT *TO USE THE SYMBOL*: ``` '  ``` - *USE THIS* (backquote): ``` `  "
                 "```"
                 "4. IF YOU WANT *TO USE THE SYMBOL*: ``` \\  ``` - *USE THIS* (double slash): "
                 "``` \\\\  ```"
                 "But when you'll send, you agree with rules of "
                 "'SENDER'.\n\n_1. Please, don't send spam or other ticket as spam\n"
                 "2. Don't use TicketSystem like personal messenger!_",
            chat_id=call_query.message.chat.id,
            message_id=call_query.message.message_id,
            parse_mode="Markdown"
        )

    async def __sending_ticket(self, message: types.Message, state: FSMContext) -> None:
        """
        Sending the ticket from the user to admin and save data of ticket in the DB (MySQL).

        :param message: Message (data ticket) of the user.
        :param state: FSM.

        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.get_menu_user_tickets_again()

        if message.content_type != "text":
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"{message.from_user.first_name}, it isn't only text-format (type)! Please, "
                     f"explore the rules and tips given above, if you want to send a ticket.",
                reply_markup=var.as_markup()
            )
            logging.warning(
                f"Unsuccessful adding data to the database. "
                f"Message contains not only text-format. "
                f"User ID: {message.from_user.id}"
            )

        else:
            if not (25 <= len(message.text) <= 2500):
                await self.__bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"❌ {message.from_user.first_name}, your message doesn't have "
                         f"25 <= symbols <= 2500! "
                         f"Please, explore the rules and tips given above, "
                         f"if you want to send a ticket.",
                    reply_markup=var.as_markup()
                )
                logging.warning(
                    f"Unsuccessful adding data to the database. Message of the user doesn't have "
                    f"25 <= symbols <= 2500. "
                    f"User ID: {message.from_user.id}"
                )

            else:
                try:
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

                    await HandlerDB.add_new_ticket_data(
                        id_ticket, 
                        username, 
                        tg_id_sender, 
                        ticket_data,
                        create_at, 
                        subject
                    )

                    await self.__bot.send_message(
                        chat_id=message.from_user.id,
                        text=f"✅ Successful! {message.from_user.first_name}, your ticket added "
                             f"and sent.",
                        reply_markup=var.as_markup()
                    )

                    await HandlerDB.update_analytic_datas_count_tickets_system()

                    logging.info(
                        f"Successful! Updated data in the database. "
                        f"User ID: {message.from_user.id}"
                    )

                except Exception as ex:
                    logging.warning(f"The exception has arisen: {ex}.")

                    await self.__bot.send_message(
                        chat_id=message.from_user.id,
                        text=f"❌ We have a problem! {message.from_user.first_name}, your ticket "
                             f"didn't add and didn't send. Please, repeat later.",
                        reply_markup=var.as_markup()
                    )

        await state.clear()


class TicketAdminView:
    """
    Class of the ticket system UI for admin.
    """
    __response_big: tuple = tuple()

    def __init__(self, bot: Bot, mysql_data: dict) -> None:
        self.__bot: Bot = bot
        self.__mysql_data: dict = mysql_data

    async def show_admin_menu(self, call_query: types.CallbackQuery) -> None:
        """
        Function of the show menu of admin.

        :param call_query: Callback Query by click on the button.
        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.get_ticket_menu_admin()
        await self.__bot.edit_message_text(
            text="🔹 You're in the TicketSystem Menu (ADMIN UI | CWBot UI).",
            chat_id=call_query.message.chat.id,
            message_id=call_query.message.message_id,
            reply_markup=var.as_markup()
        )

        router.callback_query.register(
            self.__show_admin_users_tickets,
            F.data == "show_tickets_for_admin_menu"
        )

    async def __show_admin_users_tickets(self, call_query: types.CallbackQuery) -> None:
        """
        Function of the show tickets to admin.

        :param call_query: Callback Query by click on the button.
        :return: None.
        """
        response: tuple = await Buttons.get_users_tickets_for_admin()
        if len(response[0]) != 0:
            if response[0][0] is False:
                await self.__bot.edit_message_text(
                    text=f"🔹 Tickets (ADMIN UI | CWBot UI)\n"
                         f"----------------------------------------\n{response[0][1]}",
                    chat_id=call_query.message.chat.id,
                    message_id=call_query.message.message_id,
                    reply_markup=response[1].as_markup(),
                    parse_mode="HTML"
                )
            elif response[0][0] is True:
                self.__class__.__response_big = response[0][1], response[0][2]

                await self.__bot.edit_message_text(
                    text=f"🔹 Tickets (ADMIN UI | CWBot UI)\n"
                         f"----------------------------------------\nI'm sorry, but "
                         f"I can't send the details of all tickets. More characters "
                         f"are required. Will you allow me to send the details of the "
                         f"remaining tickets to your email?"
                         f"\n\n<b>Available Data look after click on the button "
                         f"(which you need)</b>.",
                    chat_id=call_query.message.chat.id,
                    message_id=call_query.message.message_id,
                    reply_markup=response[1].as_markup(),
                    parse_mode="HTML"
                )

                router.callback_query.register(
                    self.__allow_send_email_ticket_data_admin,
                    F.data == "allow_send_email_ticket_data_admin"
                )
                router.callback_query.register(
                    self.__not_allow_send_email_ticket_data_admin,
                    F.data == "not_allow_send_email_ticket_data_admin"
                )
        else:
            await self.__bot.edit_message_text(
                    text=f"🔹 Tickets (ADMIN UI | CWBot UI)\n"
                         f"----------------------------------------\n\n"
                         f"It's still empty here!",
                    chat_id=call_query.message.chat.id,
                    message_id=call_query.message.message_id,
                    reply_markup=response[1].as_markup(),
                    parse_mode="HTML"
                )

    async def __allow_send_email_ticket_data_admin(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Allow to send email for ticket data (big) for admin.

        :param call_query: CallbackQuery.
        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.back_on_main()
        try:
            await self.__bot.edit_message_text(
                text=f"🔹 Tickets (ADMIN UI | CWBot UI)\n"
                     f"----------------------------------------\n"
                     f"⚡ <b>Available Data</b>:"
                     f"\n\n{self.__class__.__response_big[0]}",
                chat_id=call_query.message.chat.id,
                message_id=call_query.message.message_id,
                reply_markup=var.as_markup(),
                parse_mode="HTML"
            )

            with open("bot.json", encoding='utf-8') as f:
                data: dict = json.load(f)
                admin_email: str = data["EMAIL_DATA"]["ADMIN_EMAIL"]
                admin_name: str = data["business_connection"]["user"]["first_name"]

            file_path: str = await GenerateTicketDataUniversal.generate(
                admin_name,
                self.__class__.__response_big[1]
            )
            await self.__bot.send_document(
                chat_id=call_query.message.chat.id,
                document=FSInputFile(file_path),
                caption=f"✅ {call_query.from_user.first_name}, see TicketData in the attachment "
                        f"below. Also, for convenience, I am sending you an email with "
                        f"the same file, in the official format."
            )
            await SenderEmail.send_others_ticket_data_in_email_format(
                admin_email,
                "👤 TicketData from Manager CW for ADMIN | CWR.SU",
                admin_name,
                file_path
            )
            msg_temp: types.Message = await self.__bot.send_message(
                text=f"✅ The data sent!",
                chat_id=call_query.message.chat.id
            )

            await self.__bot.delete_message(
                chat_id=msg_temp.chat.id,
                message_id=msg_temp.message_id
            )
            await self.__bot.send_message(
                text=f"🔐 You've all the data and they're safe. "
                     f"To go to the main, click on the button below.",
                chat_id=call_query.message.chat.id,
                reply_markup=var.as_markup(),
                parse_mode="HTML"
            )

            logging.info(
                f"Successful! Sent data to user / admin EMail. "
                f"User ID: {call_query.from_user.id}"
            )

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")

    async def __not_allow_send_email_ticket_data_admin(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Not allow to send email for ticket data (big) for admin.

        :param call_query: CallbackQuery.
        :return: None.
        """
        try:
            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.edit_message_text(
                text=f"🔹 Tickets (ADMIN UI | CWBot UI)\n"
                     f"----------------------------------------\n"
                     f"⚡ <b>Available Data</b>:"
                     f"\n\n{self.__class__.__response_big[0]}",
                chat_id=call_query.message.chat.id,
                message_id=call_query.message.message_id,
                reply_markup=var.as_markup(),
                parse_mode="HTML"
            )

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")


class TicketAnswersToUsers:
    """Class for manage answers to users by ticket-system."""
    def __init__(self, bot: Bot, admin_id: int, mysql_data: dict) -> None:
        self.__bot: Bot = bot
        self.__admin_id: int = admin_id
        self.__mysql_data: dict = mysql_data

        router.message.register(
            self.__get_ticket_data_for_answer,
            GetTicketDataForAnswerToUser.ticket_data
        )

    async def explore_answer_users_ticket(
            self,
            call_query: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Handler (call-handler) for get id ticket for answer to user.

        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(GetTicketDataForAnswerToUser.ticket_data)
        if call_query.from_user.id == self.__admin_id:
            await self.__bot.edit_message_text(
                text=f"👌🏻 Please, tell me ID Ticket, your message and new status of the ticket, "
                     f"which you want to answer. System use special "
                     f"parse-mode here!\n----------------------------------------\n"
                     f"FORMAT your message: ``` ID_TICKET ~ MESSAGE ~ "
                     f"NEW_STATUS  ```\n"
                     f"1. IF YOU WANT *TO ATTACH THE PHOTO use this free website* (we checked "
                     f"it!): "
                     f"https://imgbly.com/;\n"
                     f"2. IF YOU WANT *TO ATTACH THE DOCUMENT-FILE use this free website* (we "
                     f"checked it!): https://www.file.io/;\n"
                     f"3. IF YOU WANT *TO USE THE SYMBOL*: ``` '  ``` - *USE THIS* (backquote): "
                     f"``` `  "
                     f"```"
                     f"4. IF YOU WANT *TO USE THE SYMBOL*: ``` \\  ``` - *USE THIS* "
                     f"(double slash): "
                     f"``` \\\\  ```"
                     f"But when you'll send, you agree with rules of "
                     f"'SENDER'.\n\n_1. Please, don't send spam or other ticket as spam\n"
                     f"2. Don't use TicketSystem like personal messenger!_",
                chat_id=call_query.message.chat.id,
                message_id=call_query.message.message_id,
                parse_mode="Markdown"
            )

    async def __get_ticket_data_for_answer(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Get ticket-data for answer to user and sending answer to the user.

        :param message: Message of the user.
        :param state: FSM.

        :return: None.
        """
        await state.clear()

        var: InlineKeyboardBuilder = await Buttons.back_on_main()
        try:
            connection: pymysql.connections.Connection | str = await Connection.get_connection(
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
                    await message.answer(
                        text=f"Sorry! Data is none!\n"
                             f"Your message: {message.text}"
                    )
                    logging.warning(
                        f"Unsuccessful adding data to the database. Data is none. "
                        f"User ID: {message.from_user.id}"
                    )

                else:
                    response: tuple = result[0]

                    tg_id_sender: int = int(response[0])
                    content_ticket_data: str = response[1]
                    subject: str = response[2]

                    await self.__bot.send_message(
                        chat_id=tg_id_sender,
                        text=f"👤 <b>ANSWER FROM ADMIN</b>\n"
                             f"----------------------------------------\n"
                             f"#️⃣ ID Ticket: <code>{id_ticket}</code>\n"
                             f"🌐 STATUS: <b>{new_status}</b>\n"
                             f"✉ Subject: {subject}\n"
                             f"📩 Content of message: \n\n      {message_for_ticket}",
                        reply_markup=var.as_markup(),
                        parse_mode="HTML"
                    )
                    msg: types.Message = await self.__bot.send_message(
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
                    await self.__bot.edit_message_text(
                        chat_id=message.from_user.id,
                        message_id=msg.message_id,
                        text=f"✅ SUCCESSFUL! Updated DB-data for ID: {id_ticket}!",
                        reply_markup=var.as_markup()
                    )

                    logging.info(
                        f"Successful! Updated data in the database. "
                        f"User ID: {message.from_user.id}"
                    )

            else:
                await self.__bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"Sorry! It's not ID Ticket, because length of your message isn't 5 "
                         f"symbols!\nYour message: {message.text}",
                    reply_markup=var.as_markup()
                )

                logging.error(
                    f"Error: It's not ID Ticket, because length of user's message isn't 5 "
                    f"symbols! {message.text}. UserID: {message.from_user.id}"
                )

            connection.close()

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")

            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"❌ FAIL! Please, follow the rules!",
                reply_markup=var.as_markup()
            )


class TicketAnswersToAdmin:
    """Class for manage answers to admin by ticket-system."""
    def __init__(self, bot: Bot, admin_id: int, mysql_data: dict) -> None:
        self.__bot: Bot = bot
        self.__admin_id: int = admin_id
        self.__mysql_data: dict = mysql_data

        router.message.register(
            self.__get_ticket_data_for_answer_to_admin,
            GetTicketDataForAnswerToAdmin.ticket_data
        )

    async def explore_answer_admin_by_ticket(
            self,
            call_query: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Handler (call-handler) for get id ticket for answer to admin.

        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(GetTicketDataForAnswerToAdmin.ticket_data)
        await self.__bot.edit_message_text(
            text=f"👌🏻 Please, tell me ID Ticket, your message of the ticket, "
                 f"which you want to answer. System use special "
                 f"parse-mode here!\n----------------------------------------\n"
                 f"FORMAT your message: ``` ID_TICKET ~ MESSAGE  ```\n"
                 f"1. IF YOU WANT *TO ATTACH THE PHOTO use this free website* (we checked "
                 f"it!): "
                 f"https://imgbly.com/;\n"
                 f"2. IF YOU WANT *TO ATTACH THE DOCUMENT-FILE use this free website* (we "
                 f"checked it!): https://www.file.io/;\n"
                 f"3. IF YOU WANT *TO USE THE SYMBOL*: ``` '  ``` - *USE THIS* (backquote): "
                 f"``` `  ```"
                 f"4. IF YOU WANT *TO USE THE SYMBOL*: ``` \\  ``` - *USE THIS* (double slash): "
                 f"``` \\\\  ```"
                 f"But when you'll send, you agree with rules of "
                 f"'SENDER'.\n\n_1. Please, don't send spam or other ticket as spam\n"
                 f"2. Don't use TicketSystem like personal messenger!_",
            chat_id=call_query.message.chat.id,
            message_id=call_query.message.message_id,
            parse_mode="Markdown"
        )

    async def __get_ticket_data_for_answer_to_admin(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Get ticket-data for answer to user and sending answer to admin.

        :param message: Message of the user.
        :param state: FSM.

        :return: None.
        """
        await state.clear()

        var: InlineKeyboardBuilder = await Buttons.back_on_main()
        try:
            connection: pymysql.connections.Connection | str = await Connection.get_connection(
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
                    await message.answer(
                        text=f"Sorry! Data is none!\n"
                             f"Your message: {message.text}"
                    )

                    logging.warning(
                        f"Unsuccessful adding data to the database. Data is none."
                        f"User ID: {message.from_user.id}"
                    )

                else:
                    response: tuple = result[0]

                    tg_id_sender: int = int(response[0])
                    content_ticket_data: str = response[1]
                    status: str = response[2]
                    subject: str = response[3]

                    if tg_id_sender == message.from_user.id:
                        await self.__bot.send_message(
                            chat_id=self.__admin_id,
                            text=f"👤 <b>ANSWER FROM USER</b>\n"
                                 f"----------------------------------------\n"
                                 f"#️⃣ ID Ticket: <code>{id_ticket}</code>\n"
                                 f"🌐 STATUS: <b>{status}</b>\n"
                                 f"✉ Subject: {subject}\n"
                                 f"📩 Content of message: \n\n      {message_for_ticket}",
                            reply_markup=var.as_markup(),
                            parse_mode="HTML"
                        )

                        msg: types.Message = await self.__bot.send_message(
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
                        await self.__bot.edit_message_text(
                            chat_id=message.from_user.id,
                            message_id=msg.message_id,
                            text=f"✅ SUCCESSFUL! Updated DB-data for ID: {id_ticket}!",
                            reply_markup=var.as_markup()
                        )

                        logging.info(
                            f"Successful! Updated data in the database. "
                            f"User ID: {message.from_user.id}"
                        )

                    else:
                        await self.__bot.send_message(
                            chat_id=tg_id_sender,
                            text=f"🚫 ERROR 43! {message.from_user.first_name}, forbidden!",
                            parse_mode="Markdown",
                            reply_markup=var.as_markup()
                        )

                        logging.error(
                            f"Error: 43 Forbidden. UserID: {message.from_user.id}"
                        )

            else:
                await self.__bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"Sorry! It's not ID Ticket, because length of your message isn't 5 "
                         f"symbols!\nYour message: {message.text}",
                    reply_markup=var.as_markup()
                )

                logging.error(
                    f"Error: It's not ID Ticket, because length of user's message isn't 5 "
                    f"symbols! {message.text}. UserID: {message.from_user.id}"
                )

            connection.close()

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")

            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"❌ FAIL! Please, follow the rules!",
                reply_markup=var.as_markup()
            )
