"""
Module of the Manager-Business-Helper Bot.
"""
import datetime
import json

import pymysql
import telebot
from telebot import types

from manager_cw_bot_api.analytics import Analytic
from manager_cw_bot_api.business_answers import Answers
from manager_cw_bot_api.business_handler import BusinessHandler
from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.create_table import CreateTable
from manager_cw_bot_api.giga_images import GigaCreator
from manager_cw_bot_api.gigachatai import GigaChatAI
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB, SubOperations
from manager_cw_bot_api.handler_promo import HandlerEP
from manager_cw_bot_api.handler_successful_payment import HandlerSP
from manager_cw_bot_api.mysql_connection import Connection
from manager_cw_bot_api.refund import Refund
from manager_cw_bot_api.send_invoice import SendInvoice
from manager_cw_bot_api.tickets import TicketAnswersToUsers, TicketAnswersToAdmin
from manager_cw_bot_api.tickets import (TicketUserView, TicketAdminView)


class Manager(telebot.TeleBot):
    """
    Manager of the Alex's Account and helper 'AI'.
    """
    def __init__(self, bot_token: str, business_conn_id: str, admin_id: int,
                 mysql_data: dict, gigachat_data: dict) -> None:
        super().__init__(bot_token)
        self.__business_connection_id: str = business_conn_id
        self.__admin_id: int = admin_id
        self.__mysql_data: dict = mysql_data
        self.__gigachat_data: dict = gigachat_data
        try:
            connection: pymysql.Connection = Connection.get_connection(mysql_data)
            cursor = connection.cursor()
            creator_mysql = CreateTable(connection, cursor)
            # creator_mysql.create()
            # creator_mysql.create_analytics()
            # creator_mysql.create_plus_users()
            creator_mysql.create_plus_promo_codes()

        except Exception as e:
            with open("logs.txt", 'a') as logs:
                logs.write(f"{datetime.datetime.now()} | {e} | "
                           f"The error of database in __init__ of "
                           f"business.py of Manager-Class.\n")

    def __standard_message(self, message: types.Message) -> None:
        """
        Answer to the users and admin.

        :param message: Message.
        :return: None.
        """
        self.send_message(
            chat_id=message.from_user.id,
            text=f"⚡ *{message.from_user.first_name}*, click on the button below to *go to the main menu*.",
            parse_mode="Markdown",
            reply_markup=Buttons.back_on_main()
        )

    def __answer_to_user(self, message: types.Message) -> None:
        """
        Answer to a user from admin-account (as admin).

        :param message: Message of a user.
        :return: None.
        """
        answers: Answers = Answers(
            business_connection_id=self.__business_connection_id,
            admin_id=self.__admin_id
        )
        answers.answer_to_user(
            self, message
        )

    def __explore_show_users_ticket(self, call_query: types.CallbackQuery) -> None:
        """
        Explore to show user's ticket by id.

        :param call_query: Callback Query.
        :return: None.
        """
        self.edit_message_text(
            text=f"⚠ Please, tell me <b>ID Ticket</b>, which you want to look at.",
            chat_id=call_query.message.chat.id,
            message_id=call_query.message.message_id,
            parse_mode="HTML"
        )
        self.register_next_step_handler(call_query.message, self.__get_id_ticket_for_show)

    def __get_id_ticket_for_show(self, message: types.Message) -> None:
        """
        Get id ticket for admin answer/view or user view.

        :param message: Message (ID ticket) from admin/the user.
        :return: None.
        """
        connection: pymysql.connections.Connection | str = Connection.get_connection(
            self.__mysql_data
        )
        cursor = connection.cursor()

        id_ticket: str = message.text
        if len(id_ticket) == 5:
            query: str = f"""SELECT username, tg_id_sender, ticket_data, create_at, status, 
            subject FROM users WHERE id_ticket = %s;"""
            cursor.execute(query, (id_ticket,))
            result: tuple = cursor.fetchall()
            if len(result) == 0:
                self.send_message(
                    chat_id=message.from_user.id,
                    text=f"Sorry! Data is none!\n"
                         f"Your message: {message.text}",
                    reply_markup=Buttons.back_on_main()
                )
            else:
                response: tuple = result[0]

                username: str = response[0]
                id_user_tg: int = int(response[1])
                content_ticket_data: str = response[2]
                create_at: str = response[3]
                status: str = response[4]
                subject: str = response[5]

                self.send_message(
                    chat_id=message.from_user.id,
                    text=f"👤 Sender: @{username}\n"
                         f"#️⃣ ID Sender: {id_user_tg}\n\n"
                         f"#️⃣ ID Ticket: {id_ticket}\n"
                         f"⌚ Create at {create_at}\n"
                         f"🌐 STATUS: {status}\n"
                         f"✉ Subject: {subject}\n"
                         f"📩 Content: \n\n      {content_ticket_data}",
                    reply_markup=Buttons.back_on_main()
                )

        else:
            self.send_message(
                chat_id=message.from_user.id,
                text=f"Sorry! It's not ID Ticket, because length of your message isn't 5 symbols!\n"
                     f"Your message: {message.text}",
                reply_markup=Buttons.back_on_main()
            )

        connection.close()

    def __explore_answer_users_ticket(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (call-handler) for get id ticket for answer to user.

        :param call_query: Callback Query.
        :return: None.
        """
        ticket_answer: TicketAnswersToUsers = TicketAnswersToUsers(
            self, self.__admin_id, self.__mysql_data
        )
        ticket_answer.explore_answer_users_ticket(call_query)

    def __explore_answer_admin_by_ticket(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (call-handler) for get id ticket for answer to admin.

        :param call_query: Callback Query.
        :return: None.
        """
        ticket_answer: TicketAnswersToAdmin = TicketAnswersToAdmin(
            self, self.__admin_id, self.__mysql_data
        )
        ticket_answer.explore_answer_admin_by_ticket(
            call_query
        )

    def __ai_assistance(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (callback-handler) for go to the AI-Menu.

        :param call_query: Callback Query.
        :return: None.
        """
        giga_chat_ai_helper: GigaChatAI = (
            GigaChatAI(
                self, call_query,
                self.__mysql_data,
                self.__admin_id
            )
        )
        giga_chat_ai_helper.show_info_edit_text()
        self.register_next_step_handler(call_query.message, giga_chat_ai_helper.request)

    def __user_menu_tickets(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (callback-handler) for go to the Tickets-Menu.

        :param call_query: Callback Query.
        :return: None.
        """
        ticket: TicketUserView = TicketUserView(
            self,
            self.__mysql_data
        )
        ticket.show_user_menu(call_query)

    def __admin_menu_tickets(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (callback-handler) for show tickets to admin.

        :param call_query: Callback Query.
        :return: None.
        """
        ticket: TicketAdminView = TicketAdminView(
            self,
            self.__mysql_data
        )
        ticket.show_admin_users_tickets(call_query)

    def __analytic_data(self, call_query: types.CallbackQuery) -> None:
        """
        Handler of the analytic-menu (UI) for admin.

        :param call_query: Callback Query.
        :return: None.
        """
        analytic: Analytic = Analytic(
            self,
            self.__mysql_data,
            call_query
        )
        analytic.analyse()

    def __business_handler(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (call-query) for admin (with business) - start main handler.

        :param call_query: Callback Query.
        :return: None.
        """
        handler: BusinessHandler = BusinessHandler(
            self, call_query
        )
        handler.run()

    def __get_or_lk_plus(self, call: types.CallbackQuery) -> None:
        """
        Get Plus or view (look at) "MY PLUS".

        :param call: Callback Query.
        :return: None.
        """
        checked: tuple = HandlerDB.check_subscription(call)
        if checked[0] is False:
            self.edit_message_text(
                chat_id=call.from_user.id,
                text=f"💡 To *get a subscription with an invitation discount*, *click on the button* below. If you have "
                     f"any questions or would like to clarify something, write to us: @aleksandr\\_twitt.\n\n"
                     f"ℹ If you want to _test_ the PLUS (_5 days is a trial period_), please, "
                     f"write to the admin about it (@aleksandr\\_twitt | help@cwr.su).\n"
                     f"_By registering the PLUS, you agree to the terms of use of the service._\n\n"
                     f"#️⃣ My ID: `{call.from_user.id}`",
                message_id=call.message.message_id,
                reply_markup=Buttons.get_plus(),
                parse_mode="Markdown"
            )
        elif checked[0] is True:
            remains = round(SubOperations.sec_to_days(checked[1]))
            d = "days"

            if remains > 1:
                d = "days"
            elif remains == 1:
                d = "day"

            refund_token: str | bool = HandlerDB.check_refund_token(call)
            if refund_token:
                self.edit_message_text(
                    chat_id=call.from_user.id,
                    text=f"🔥 {call.from_user.first_name}, the subscription is still active *{remains} {d}*.\n\n"
                         f"💡 My REFUND Token: `{refund_token}`.\n"
                         f"#️⃣ My ID: `{call.from_user.id}`",
                    message_id=call.message.message_id,
                    parse_mode="Markdown",
                    reply_markup=Buttons.back_on_main()
                )
            else:
                self.edit_message_text(
                    chat_id=call.from_user.id,
                    text=f"🔥 {call.from_user.first_name}, the subscription is still active *{remains} {d}*.\n\n"
                         f"💡 Ask the admin for your token.\n"
                         f"#️⃣ My ID: `{call.from_user.id}`",
                    message_id=call.message.message_id,
                    parse_mode="Markdown",
                    reply_markup=Buttons.back_on_main()
                )

    def __send_invoice(self, message: types.Message) -> None:
        checked: tuple = HandlerDB.check_subscription(message)
        if checked[1] == "ex_sub":
            invoice_extend: SendInvoice = SendInvoice(
                self, message
            )
            invoice_extend.send_invoice_extend()
        else:
            invoice: SendInvoice = SendInvoice(
                self, message
            )
            invoice.send_invoice()

    def __show_promo_menu_admin_ctrl(self, call: types.CallbackQuery) -> None:
        """
        Show PROMO Menu. | Control ADMIN.

        :param call: Callback Query.
        :return: None.
        """
        promo: HandlerEP = HandlerEP(
            self, self.__admin_id
        )
        promo.show_promo_menu_admin(call)

    def __enter_promo_code(self, call: types.CallbackQuery) -> None:
        """
        Func 'ENTER' a promo code from user. | Step 1.

        :param call: CallbackQuery.
        :return: None.
        """
        checked: tuple = HandlerDB.check_subscription(call)
        if checked[1] == "ex_sub":
            self.edit_message_text(
                chat_id=call.from_user.id,
                text=f"💖 {call.from_user.first_name}, you have already been a PLUS subscriber ➕.\n"
                     f"💡 The *promo* code is only *for those users who have never used promo* codes in our system.",
                message_id=call.message.message_id,
                reply_markup=Buttons.back_on_main(),
                parse_mode="Markdown"
            )
        else:
            promo: HandlerEP = HandlerEP(
                self, self.__admin_id
            )
            promo.enter_promo(call)

    def __pre_checkout_query(self, pre_checkout_query: types.PreCheckoutQuery) -> None:
        self.answer_pre_checkout_query(
            pre_checkout_query_id=int(pre_checkout_query.id), ok=True
        )

    def __successful_payment(self, message: types.Message) -> None:
        """
        Handler for successful payment.

        :param message: Message from user.
        :return: None.
        """
        HandlerSP.add_new_record(
            self,
            message,
            self.__admin_id
        )

    def __refund(self, call: types.CallbackQuery) -> None:
        """
        Refund-menu for admin use / control.

        :param call: Callback Query.
        :return: None.
        """
        self.edit_message_text(
            chat_id=call.from_user.id,
            text=f"⚠️ {call.from_user.first_name}, are you sure?"
                 f"\n\nAfter the star(s) are returned, the *subscription will be disabled*!\n"
                 f"But *user can resume* it at any other time by clicking on *Get PLUS* in main menu.",
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=Buttons.sure_refund()
        )

    def __refunding_step1(self, call: types.CallbackQuery) -> None:
        """
        Call-Handler for refund stars | Step 1.

        :param call: Callback Query.

        :return: None.
        """
        refund: Refund = Refund(self)
        refund.refunding_step1_confirmation(call)

    def __generate_image_for_plus_user(self, call: types.CallbackQuery) -> None:
        """
        Generate image for plus-user.

        :param call: Callback Query.
        :return: None.
        """
        checked: bool | tuple = HandlerDB.check_subscription(call)
        if checked[0] is False:
            self.answer_callback_query(
                callback_query_id=call.id,
                text=f"{call.from_user.first_name}, if you want to use this feature 🔥, subscribe to Manager Plus ➕!",
                show_alert=True
            )
        elif checked[0] is True:
            creator: GigaCreator = GigaCreator(
                bot=self
            )
            creator.get_query(call)

    def __back_on_main(self, call: types.CallbackQuery) -> None:
        """
        Handler for return to main-menu.

        :param call: Callback Query.
        :return: None.
        """
        if call.from_user.id == self.__admin_id:
            self.edit_message_text(
                chat_id=call.from_user.id,
                text=f"👑 *{call.from_user.first_name}*,\nYou are in the main menu. Select the desired item below!\n"
                     f"\nUsing the services CWR.SU (CW), you accept all the rules and the agreement. [SEE]("
                     f"https://acdn.cwr.su/src/acdn/Agreement_and_Terms_of_Use_for_the_Manager_CW_Bot_Service.pdf)."
                     f"",
                message_id=call.message.message_id,
                reply_markup=Buttons.get_menu_admin(),
                parse_mode="Markdown"
            )
        else:
            checked: bool | tuple = HandlerDB.check_subscription(call)
            if checked[0] is False:
                self.edit_message_text(
                    chat_id=call.from_user.id,
                    text="💡 You are in the main menu. Select the desired item below!\n"
                         f"\nUsing the services CWR.SU (CW), you accept all the rules and the agreement. [SEE]("
                         f"https://acdn.cwr.su/src/acdn/Agreement_and_Terms_of_Use_for_the_Manager_CW_Bot_Service.pdf)."
                         f"",
                    message_id=call.message.message_id,
                    reply_markup=Buttons.get_menu_without_plus()
                )
            elif checked[0] is True:
                self.edit_message_text(
                    chat_id=call.from_user.id,
                    text=f"👑 *{call.from_user.first_name}*,\n"
                         f"You are in the main menu. Select the desired item below!\n"
                         f"\nUsing the services CWR.SU (CW), you accept all the rules and the agreement. [SEE]("
                         f"https://acdn.cwr.su/src/acdn/Agreement_and_Terms_of_Use_for_the_Manager_CW_Bot_Service.pdf)."
                         f"",
                    message_id=call.message.message_id,
                    reply_markup=Buttons.get_menu_with_plus(),
                    parse_mode="Markdown"
                )

    def __get_main_menu(self, message: types.Message) -> None:
        """
        Handler for go to main-menu.

        :param message: Message.
        :return: None.
        """
        if message.from_user.id == self.__admin_id:
            self.send_message(
                chat_id=message.from_user.id,
                text=f"👑 *{message.from_user.first_name}*,\nYou are in the main menu. Select the desired item below!\n"
                     f"\nUsing the services CWR.SU (CW), you accept all the rules and the agreement. [SEE]("
                     f"https://acdn.cwr.su/src/acdn/Agreement_and_Terms_of_Use_for_the_Manager_CW_Bot_Service.pdf)."
                     f"",
                reply_markup=Buttons.get_menu_admin(),
                parse_mode="Markdown"
            )
        else:
            checked: bool | tuple = HandlerDB.check_subscription(message)
            if checked[0] is False:
                self.send_message(
                    chat_id=message.from_user.id,
                    text="💡 You are in the main menu. Select the desired item below!\n"
                         f"\nUsing the services CWR.SU (CW), you accept all the rules and the agreement. [SEE]("
                         f"https://acdn.cwr.su/src/acdn/Agreement_and_Terms_of_Use_for_the_Manager_CW_Bot_Service.pdf)."
                         f"",
                    reply_markup=Buttons.get_menu_without_plus()
                )
            elif checked[0] is True:
                self.send_message(
                    chat_id=message.from_user.id,
                    text=f"👑 *{message.from_user.first_name}*,\n"
                         f"You are in the main menu. Select the desired item below!\n"
                         f"\nUsing the services CWR.SU (CW), you accept all the rules and the agreement. [SEE]("
                         f"https://acdn.cwr.su/src/acdn/Agreement_and_Terms_of_Use_for_the_Manager_CW_Bot_Service.pdf)."
                         f"",
                    reply_markup=Buttons.get_menu_with_plus(),
                    parse_mode="Markdown"
                )

    def run(self) -> None:
        """
        Run-function Bot.
        """
        self.register_business_message_handler(
            callback=self.__answer_to_user
        )

        self.register_callback_query_handler(
            callback=self.__ai_assistance,
            func=lambda call: call.data == "ai_assistance_request"
        )
        self.register_callback_query_handler(
            callback=self.__user_menu_tickets,
            func=lambda call: call.data == "explore_user_tickets_menu"
        )
        self.register_callback_query_handler(
            callback=self.__admin_menu_tickets,
            func=lambda call: call.data == "explore_admin_show_tickets_menu"
        )
        self.register_callback_query_handler(
            callback=self.__explore_answer_users_ticket,
            func=lambda call: call.data == "explore_answer_to_user"
        )
        self.register_callback_query_handler(
            callback=self.__explore_answer_admin_by_ticket,
            func=lambda call: call.data == "explore_answer_to_admin"
        )
        self.register_callback_query_handler(
            callback=self.__explore_show_users_ticket,
            func=lambda call: call.data == "explore_show_ticket_by_id"
        )
        self.register_callback_query_handler(
            callback=self.__explore_show_users_ticket,
            func=lambda call: call.data == "explore_show_ticket_by_id"
        )
        self.register_callback_query_handler(
            callback=self.__analytic_data,
            func=lambda call: call.data == "analytic_data"
        )
        self.register_callback_query_handler(
            callback=self.__business_handler,
            func=lambda call: call.data == "business_handler"
        )
        self.register_callback_query_handler(
            callback=self.__refund,
            func=lambda call: call.data == "start_refund"
        )
        self.register_callback_query_handler(
            callback=self.__refunding_step1,
            func=lambda call: call.data == "refund"
        )
        self.register_callback_query_handler(
            callback=self.__generate_image_for_plus_user,
            func=lambda call: call.data == "kandinsky_generate"
        )
        self.register_callback_query_handler(
            callback=self.__get_or_lk_plus,
            func=lambda call: call.data == "get_or_lk_plus"
        )

        self.register_callback_query_handler(
            callback=self.__show_promo_menu_admin_ctrl,
            func=lambda call: call.data == "show_menu_promo_admin"
        )

        self.register_callback_query_handler(
            callback=self.__send_invoice,
            func=lambda call: call.data == "continue_subscribe_plus"
        )
        self.register_callback_query_handler(
            callback=self.__enter_promo_code,
            func=lambda call: call.data == "continue_subscribe_plus_with_promo"
        )
        self.register_callback_query_handler(
            callback=self.__back_on_main,
            func=lambda call: call.data == "back_on_main"
        )

        self.register_message_handler(
            callback=self.__get_main_menu, commands=["main", "start"]
        )

        self.register_pre_checkout_query_handler(
            callback=self.__pre_checkout_query,
            func=lambda query: True
        )
        self.register_message_handler(
            callback=self.__successful_payment,
            content_types=['successful_payment']
        )
        self.register_message_handler(
            callback=self.__standard_message, content_types=["text"]
        )

        self.polling(
            non_stop=True,
            interval=0
        )


def get_data(file_path="bot.json") -> dict:
    """
    Get data of the Alex's Manager Bot.

    :param file_path: File Path of JSON-API-keys for Bot.

    :return: Dict with data.
    """
    with open(file_path, "r", encoding='utf-8') as file:
        data: dict = json.load(file)

        dct = dict()
        dct["BOT_TOKEN"] = data["BOT_TOKEN"]
        dct["business_connection_id"] = data["business_connection"]["id"]
        dct["business_connection_is_enabled"] = data["business_connection"]["is_enabled"]
        dct["ADMIN"] = data["business_connection"]["user"]["id"]

        dct["MYSQL"] = data["MYSQL"]

        dct["GIGACHAT"] = data["GIGACHAT"]

        dct["BUSINESS_HANDLER"] = data["BUSINESS_HANDLER"]

        return dct


def run() -> None:
    """
    Run Function of the main-file.

    :return: None.
    """
    try:
        data: dict = get_data()
        if data["business_connection_is_enabled"] == "True":
            bot: Manager = Manager(data["BOT_TOKEN"], data["business_connection_id"],
                                   data["ADMIN"], data["MYSQL"], data["GIGACHAT"])
            bot.run()

        else:
            print("Business Connection isn't enabled!")
    except Exception as ex:
        with open("logs.txt", 'a') as logs:
            logs.write(f"\n{datetime.datetime.now()} | {ex} | The error in run-function of "
                       f"business.py.\n")
        print(f"The Error (ex-run-func): {ex}")
