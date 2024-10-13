"""
Module of the Manager-Business-Helper Bot.
"""
import json
import pymysql
import logging

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.types import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from manager_cw_bot_api.analytics import Analytic
from manager_cw_bot_api.business_answers import Answers
from manager_cw_bot_api.business_handler import BusinessHandler, router_business
from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.create_table import CreateTable
from manager_cw_bot_api.fsm_handler import GetTicketDataByIDTCK
from manager_cw_bot_api.giga_images import GigaCreator, router_ai_img
from manager_cw_bot_api.gigachatai import GigaChatAI, router_chat_ai
from manager_cw_bot_api.handler_db_sub_operations import SubOperations, HandlerDB
from manager_cw_bot_api.handler_email import HandlerEM, router_handler_em
from manager_cw_bot_api.handler_promo import HandlerEP, router_promo
from manager_cw_bot_api.handler_successful_payment import HandlerSP
from manager_cw_bot_api.mysql_connection import Connection
from manager_cw_bot_api.refund import Refund, router_refund
from manager_cw_bot_api.send_invoice import ChooseMethodOfPayment, router_send_invoice
from manager_cw_bot_api.tickets import (
    TicketAnswersToUsers,
    TicketAnswersToAdmin,
    TicketUserView,
    TicketAdminView,
    router
)


class PrivacyMessagesSector:
    """
    Sender-class of privacy messages.
    """

    @staticmethod
    async def privacy(
            bot: Bot,
            message: types.Message
    ) -> None:
        """
        Privacy for the users.

        :param bot: The bot object
        :param message: Message / Command Privacy.

        :return: None.
        """
        await bot.set_message_reaction(
            chat_id=message.from_user.id,
            message_id=message.message_id,
            reaction=[types.ReactionTypeEmoji(
                types='emoji',
                emoji='💯'
            )]
        )
        var: InlineKeyboardBuilder = await Buttons.get_language_privacy_menu()
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"Choose your language:",
            reply_markup=var.as_markup()
        )

    @staticmethod
    async def eng_privacy(
            bot: Bot,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Explore to show ENG Privacy.

        :param bot: The bot object
        :param call_query: Callback Query.

        :return: None.
        """
        await bot.edit_message_text(
            message_id=call_query.message.message_id,
            chat_id=call_query.from_user.id,
            text=f"🇬🇧 ENG: https://acdn.cwr.su/src/acdn/new_user_agreement_manager_cw_bot.pdf "
                 f"🗣 <b>{call_query.from_user.first_name}</b>, you must follow these rules, "
                 f"which are indicated in the attached document. It also indicates what we "
                 f"charge, what data we transfer to the server for data processing / analysis, "
                 f"and the like.\nYou also <b>automatically</b> accept the user agreement "
                 f"specified in the attachment.\n\n👑 The rules for signing up for a CW PREMIUM "
                 f"➕ subscription are listed <a href='https://acdn.cwr.su/src/acdn/Agreement_and_"
                 f"Terms_of_Use_for_the_Manager_CW_Bot_Service.pdf'>here</a>.\n\n🔥 The paid CW "
                 f"PREMIUM ➕subscription period is 30 days.\nCW PREMIUM's price:\n"
                 f"⭐ 15 XTR (TGStar);\n"
                 f"💳 5 RUB - Different payment options are available.\n\n"
                 f"#UserAgreement #privacy_manager_cw_bot_and_include_api\n"
                 f"#privacy_bot #privacy",
            parse_mode="HTML"
        )

    @staticmethod
    async def rus_privacy(
            bot: Bot,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Explore to show RUS Privacy.

        :param bot: The bot object
        :param call_query: Callback Query.

        :return: None.
        """
        await bot.edit_message_text(
            chat_id=call_query.from_user.id,
            message_id=call_query.message.message_id,
            text=f"🇷🇺 RUS: https://acdn.cwr.su/src/acdn/new_user_agreement_manager_cw_bot.pdf "
                 f"🗣 <b>{call_query.from_user.first_name}</b>, вы должны соблюдать эти правила, "
                 f"которые указаны в прикреплённом док-те. Там также указано какие данные мы "
                 f"собираем и передаем на сервер для обработки / анализа и т.п.\n"
                 f"Вы также автоматически принимаете пользовательское соглашение, указанное во "
                 f"вложении.\n\n👑 Смотрите перечисленные правила оформления подписки CW PREMIUM "
                 f"➕ <a href='https://acdn.cwr.su/src/acdn/Agreement_and_Terms_of_Use_for_the_"
                 f"Manager_CW_Bot_Service.pdf'>здесь</a>.\n\n🔥 Срок действия платной подписки CW "
                 f"PREMIUM ➕ составляет 30 дней.\nПРАЙС CW PREMIUM'а:\n⭐ 15 XTR (TGStar);\n"
                 f"💳 5 RUB - Доступны различные варианты оплаты.\n\n"
                 f"#UserAgreement #privacy_manager_cw_bot_and_include_api\n"
                 f"#privacy_bot #privacy",
            parse_mode="HTML"
        )


class TicketsSector:
    """
    Ticket-Manage Class.
    """

    @staticmethod
    async def explore_show_users_ticket(
            bot: Bot,
            call_query: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Explore to show user's ticket by id.

        :param bot: The Bot-object.
        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(GetTicketDataByIDTCK.id_ticket)
        await bot.edit_message_text(
            text=f"👌🏻 Please, tell me <b>ID Ticket</b>, which you want to look at.",
            chat_id=call_query.from_user.id,
            message_id=call_query.message.message_id,
            parse_mode="HTML"
        )

    @staticmethod
    async def get_id_ticket_for_show(
            bot: Bot,
            message: types.Message,
            state: FSMContext,
            mysql_data: dict
    ) -> None:
        """
        Get id ticket for admin answer/view or user view.

        :param bot: The Bot-object.
        :param message: Message (ID ticket) from admin/the user.
        :param state: FSM.
        :param mysql_data: MySQL (Database) data.

        :return: None.
        """
        connection: pymysql.connections.Connection | str = await Connection.get_connection(
            mysql_data
        )
        cursor = connection.cursor()
        await state.clear()
        id_ticket = message.text

        var: InlineKeyboardBuilder = await Buttons.back_on_main()
        if len(id_ticket) == 5:
            query: str = f"""SELECT username, tg_id_sender, ticket_data, create_at, status, 
            subject FROM users WHERE id_ticket = %s;"""
            cursor.execute(query, (id_ticket,))
            result: tuple = cursor.fetchall()
            if len(result) == 0:
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"Sorry! Data is none!\n"
                         f"Your message: {message.text}",
                    reply_markup=var.as_markup()
                )
            else:
                response: tuple = result[0]

                username: str = response[0]
                id_user_tg: int = int(response[1])
                content_ticket_data: str = response[2]
                create_at: str = response[3]
                status: str = response[4]
                subject: str = response[5]

                await bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"👤 Sender: @{username}\n"
                         f"#️⃣ ID Sender: {id_user_tg}\n\n"
                         f"#️⃣ ID Ticket: {id_ticket}\n"
                         f"⌚ Create at {create_at}\n"
                         f"🌐 STATUS: {status}\n"
                         f"✉ Subject: {subject}\n"
                         f"📩 Content: \n\n      {content_ticket_data}",
                    reply_markup=var.as_markup()
                )

        else:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"Sorry! It's not ID Ticket, because length of your message isn't 5 symbols!"
                     f"\nYour message: {message.text}",
                reply_markup=var.as_markup()
            )

        connection.close()

    @staticmethod
    async def explore_answer_users_ticket(
            bot: Bot,
            call_query: types.CallbackQuery,
            state: FSMContext,
            admin_id: int,
            mysql_data: dict
    ) -> None:
        """
        Handler (call-handler) for get id ticket for answer to user.

        :param bot: The Bot-object.
        :param call_query: Callback Query.
        :param state: FSM.
        :param admin_id: Admin ID (telegram ID).
        :param mysql_data: MySQL (Database) data.

        :return: None.
        """
        ticket_answer: TicketAnswersToUsers = TicketAnswersToUsers(
            bot,
            admin_id,
            mysql_data
        )
        await ticket_answer.explore_answer_users_ticket(
            call_query,
            state
        )

    @staticmethod
    async def explore_answer_admin_by_ticket(
            bot: Bot,
            call_query: types.CallbackQuery,
            state: FSMContext,
            admin_id: int,
            mysql_data: dict
    ) -> None:
        """
        Handler (call-handler) for get id ticket for answer to admin.

        :param bot: The Bot-object.
        :param call_query: Callback Query.
        :param state: FSM.
        :param admin_id: Admin ID (telegram ID).
        :param mysql_data: MySQL (Database) data.

        :return: None.
        """
        ticket_answer: TicketAnswersToAdmin = TicketAnswersToAdmin(
            bot,
            admin_id,
            mysql_data
        )
        await ticket_answer.explore_answer_admin_by_ticket(
            call_query,
            state
        )

    @staticmethod
    async def user_menu_tickets(
            bot: Bot,
            call_query: types.CallbackQuery,
            mysql_data: dict
    ) -> None:
        """
        Handler (callback-handler) for go to the Tickets-Menu.

        :param bot: The Bot-object.
        :param call_query: Callback Query.
        :param mysql_data: MySQL (Database) data.

        :return: None.
        """
        result: tuple = await HandlerDB.get_email_data(call_query.from_user.id)
        if result[0] is True:
            ticket: TicketUserView = TicketUserView(
                bot,
                mysql_data
            )
            await ticket.show_user_menu(call_query)
        else:
            var: InlineKeyboardBuilder = await Buttons.get_add_new_email()
            await bot.edit_message_text(
                text=f"🤔 <b>{call_query.from_user.first_name}</b>, sorry! But your email address "
                     f"is not in the system.\n<em>Add your email address to manage TicketSystem "
                     f"in <b>CWBot UI</b>, click on the button below!</em>.",
                message_id=call_query.message.message_id,
                chat_id=call_query.from_user.id,
                parse_mode="HTML",
                reply_markup=var.as_markup()
            )

    @staticmethod
    async def admin_menu_tickets(
            bot: Bot,
            call_query: types.CallbackQuery,
            mysql_data: dict
    ) -> None:
        """
        Handler (callback-handler) for show tickets to admin.

        :param bot: The Bot-object.
        :param call_query: Callback Query.
        :param mysql_data: MySQL (Database) data.

        :return: None.
        """
        ticket: TicketAdminView = TicketAdminView(
            bot,
            mysql_data
        )
        await ticket.show_admin_menu(call_query)


class PremiumFunctionsSector:
    """
    Class for manage Premium functions
    """

    @staticmethod
    async def business_handler(
            bot: Bot,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Handler (call-query) for admin (with business) - start main handler.

        :param bot: The Bot-object.
        :param call_query: Callback Query.
        :return: None.
        """
        handler: BusinessHandler = BusinessHandler(
            bot, call_query
        )
        await handler.run()

    @staticmethod
    async def get_or_lk_premium(
            bot: Bot,
            call_query: types.CallbackQuery,
            admin_id: int,
            admin_username: str
    ) -> None:
        """
        Get CW PREMIUM or view (look at) "MY PREMIUM".

        :param bot: The Bot-object.
        :param call_query: Callback Query.
        :param admin_id: Admin ID (telegram ID).
        :param admin_username: Admin USERNAME (telegram USERNAME).

        :return: None.
        """
        try:
            result: tuple = await HandlerDB.get_email_data(call_query.from_user.id)
            if result[0] is True or call_query.from_user.id == admin_id:
                checked: tuple = await HandlerDB.check_subscription(call_query)
                if checked[0] is False:
                    var: InlineKeyboardBuilder = await Buttons.get_premium()
                    await bot.edit_message_text(
                        chat_id=call_query.from_user.id,
                        text=f"💡 To <b>get a subscription with an invitation discount</b>, "
                             f"<b>click on the button</b> below. If you have "
                             f"any questions or would like to clarify something, write to us: "
                             f"@{admin_username}.\n\nℹ If you want to <i>test</i> the CW Premium "
                             f"(<i>5 days is a trial period</i>), please, write to the admin "
                             f"about it (@{admin_username} | help@cwr.su).\n<i>By registering the "
                             f"CW Premium, you agree to the terms of use of the service.</i>\n\n"
                             f"#️⃣ My ID: <code>{call_query.from_user.id}</code>",
                        message_id=call_query.message.message_id,
                        reply_markup=var.as_markup(),
                        parse_mode="HTML"
                    )
                elif checked[0] is True:
                    var: InlineKeyboardBuilder = await Buttons.back_on_main()

                    remains = round(await SubOperations.sec_to_days(checked[1]))
                    d = "days"

                    if remains > 1:
                        d = "days"
                    elif remains == 1:
                        d = "day"

                    refund_token: str | bool = await HandlerDB.check_refund_token(call_query)
                    if refund_token:
                        await bot.edit_message_text(
                            chat_id=call_query.from_user.id,
                            text=f"🔥 <b>{call_query.from_user.first_name}</b>, the subscription "
                                 f"is still active <b>{remains} {d}</b>.\n\n"
                                 f"🔐 My REFUND Token: <code>{refund_token}</code>.\n"
                                 f"#️⃣ My ID: <code>{call_query.from_user.id}</code>",
                            message_id=call_query.message.message_id,
                            parse_mode="HTML",
                            reply_markup=var.as_markup()
                        )
                    else:
                        await bot.edit_message_text(
                            chat_id=call_query.from_user.id,
                            text=f"🔥 <b>{call_query.from_user.first_name}</b>, the subscription "
                                 f"is still active <b>{remains} {d}</b>.\n\n"
                                 f"💡 Ask the admin for your token.\n"
                                 f"#️⃣ My ID: <code>{call_query.from_user.id}</code>",
                            message_id=call_query.message.message_id,
                            parse_mode="HTML",
                            reply_markup=var.as_markup()
                        )
            else:
                var: InlineKeyboardBuilder = await Buttons.get_add_new_email()
                await bot.edit_message_text(
                    text=f"🤔 <b>{call_query.from_user.first_name}</b>, sorry! But your email "
                         f"address is not in the system.\n"
                         f"<em>Add your email address to manage your CW PREMIUM in <b>CWBot UI</b>"
                         f", click on the button below!</em>.",
                    message_id=call_query.message.message_id,
                    chat_id=call_query.from_user.id,
                    parse_mode="HTML",
                    reply_markup=var.as_markup()
                )
        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")

    @staticmethod
    async def continue_subscribe_premium(
            bot: Bot,
            call_query: types.CallbackQuery,
            admin_id: int
    ) -> None:
        """
        Continue to subscribe CW PREMIUM. Choose method of payment.

        :param bot: The Bot-object.
        :param call_query: Callback Query.
        :param admin_id: Admin ID (telegram ID).

        :return: None.
        """
        choose: ChooseMethodOfPayment = ChooseMethodOfPayment(
            bot, admin_id
        )
        await choose.choose_step1(call_query)

    @staticmethod
    async def show_promo_menu_admin(
            bot: Bot,
            call_query: types.CallbackQuery,
            admin_id: int
    ) -> None:
        """
        Show PROMO Menu. | Control ADMIN.

        :param bot: The Bot-object.
        :param call_query: Callback Query.
        :param admin_id: Admin ID (telegram ID).

        :return: None.
        """
        promo: HandlerEP = HandlerEP(
            bot, admin_id
        )
        await promo.show_promo_menu_admin(call_query)

    @staticmethod
    async def business_and_money(
            bot: Bot,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Handler (callback-handler) for explore to BusinessAndMoney-menu.

        :param bot: The Bot-object.
        :param call_query: Callback Query.
        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.get_business_and_money_menu_admin()
        await bot.edit_message_text(
            chat_id=call_query.from_user.id,
            message_id=call_query.message.message_id,
            text=f"🔥 <b>{call_query.from_user.first_name}</b>, you are in the main menu of the "
                 f"your Business functionality and money (and promo-datas).\n"
                 f"⚡ Please select the appropriate item for you to fulfill your task / desire.",
            reply_markup=var.as_markup(),
            parse_mode="HTML"
        )


class PromoFunctionsSector:
    """
    The class of Promo functions.
    """

    @staticmethod
    async def show_promo_menu_admin(
            bot: Bot,
            call_query: types.CallbackQuery,
            admin_id: int
    ) -> None:
        """
        Show PROMO Menu. | Control ADMIN.

        :param bot: The Bot-object.
        :param call_query: Callback Query.
        :param admin_id: Admin ID (telegram ID).

        :return: None.
        """
        promo: HandlerEP = HandlerEP(
            bot, admin_id
        )
        await promo.show_promo_menu_admin(call_query)

    @staticmethod
    async def enter_promo_code(
            bot: Bot,
            call: types.CallbackQuery,
            state: FSMContext,
            admin_id: int
    ) -> None:
        """
        Func 'ENTER' a promo code from user. | Step 1.

        :param bot: The Bot-object.
        :param call: CallbackQuery.
        :param state: FSM.
        :param admin_id: Admin ID (telegram ID).

        :return: None.
        """
        checked: tuple = await HandlerDB.check_subscription(call)
        if checked[1] == "ex_sub":
            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await bot.edit_message_text(
                chat_id=call.from_user.id,
                text=f"💖 {call.from_user.first_name}, you have already been a CW PREMIUM "
                     f"subscriber ➕.\n💡 The *promo* code is only *for those users who have "
                     f"never used promo* codes in our system.",
                message_id=call.message.message_id,
                reply_markup=var.as_markup(),
                parse_mode="Markdown"
            )
        else:
            promo: HandlerEP = HandlerEP(
                bot, admin_id
            )
            await promo.enter_promo(call, state)


class FinanceSector:
    """
    Finance sector-class.
    """

    @staticmethod
    async def pre_checkout_query(
            bot: Bot,
            pre_checkout_query: types.PreCheckoutQuery
    ) -> None:
        """
        Pre-Checkout TelegramPay Function.

        :param bot: The Bot-object.
        :param pre_checkout_query: Pre-Checkout-query.

        :return: None.
        """
        await bot.answer_pre_checkout_query(
            pre_checkout_query_id=pre_checkout_query.id, ok=True
        )

    @staticmethod
    async def successful_payment(
            bot: Bot,
            message: types.Message,
            admin_id: int
    ) -> None:
        """
        Handler for successful payment.

        :param bot: The Bot-object.
        :param message: Message from user.
        :param admin_id: Admin ID (telegram ID).

        :return: None.
        """
        await HandlerSP.add_new_record(
            bot,
            message,
            admin_id
        )

    @staticmethod
    async def refund(
            bot: Bot,
            call: types.CallbackQuery
    ) -> None:
        """
        Refund-menu for admin use / control.

        :param bot: The Bot-object.
        :param call: Callback Query.
        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.sure_refund()
        await bot.edit_message_text(
            chat_id=call.from_user.id,
            text=f"⚠️ {call.from_user.first_name}, are you sure?"
                 f"\n\nAfter the star(s) are returned, the *subscription will be disabled*!\n"
                 f"But *user can resume* it at any other time by clicking on *Get CW PREMIUM* "
                 f"in main menu.",
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=var.as_markup()
        )

    @staticmethod
    async def refunding_step1(
            bot: Bot,
            call: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Call-Handler for refund stars | Step 1.

        :param bot: The Bot-object.
        :param call: Callback Query.
        :param state: FSM.

        :return: None.
        """
        refund: Refund = Refund(bot)
        await refund.refunding_step1_confirmation(
            call,
            state
        )


class AISector:
    """
    AI Sector-class.
    """

    @staticmethod
    async def ai_assistance(
            bot: Bot,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Handler (callback-handler) for go to the AI-Menu.

        :param bot: The Bot-object.
        :param call_query: Callback Query.

        :return: None.
        """
        giga_chat_ai_helper: GigaChatAI = (
            GigaChatAI(
                bot,
                call_query
            )
        )
        await giga_chat_ai_helper.choosing_ai_model()

    @staticmethod
    async def generate_image_for_premium_user(
            bot: Bot,
            call: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Generate image for premium-user.

        :param bot: The Bot-object.
        :param call: Callback Query.
        :param state: FSM.

        :return: None.
        """
        checked: bool | tuple = await HandlerDB.check_subscription(call)
        if checked[0] is False:
            await bot.answer_callback_query(
                callback_query_id=call.id,
                text=f"{call.from_user.first_name}, if you want to use this feature 🔥, subscribe "
                     f"to CW PREMIUM!",
                show_alert=True
            )
        elif checked[0] is True:
            creator: GigaCreator = GigaCreator(
                bot
            )
            await creator.get_query(
                call,
                state
            )

    @staticmethod
    async def ai_two_in_one_main_menu(
            bot: Bot,
            call_query: types.CallbackQuery,
            admin_id: int
    ) -> None:
        """
        Handler (callback-handler) for explore to AI-menu.

        :param bot: The Bot-object.
        :param call_query: Callback Query.
        :param admin_id: Admin ID (telegram ID).

        :return: None.
        """
        result: tuple = await HandlerDB.get_email_data(call_query.from_user.id)
        if result[0] is True or call_query.from_user.id == admin_id:
            var: InlineKeyboardBuilder = await Buttons.get_ai_menu()
            await bot.edit_message_text(
                chat_id=call_query.from_user.id,
                message_id=call_query.message.message_id,
                text=f"🔥 <b>{call_query.from_user.first_name}</b>, you are in the main menu of "
                     f"the AI functionality.\n⚡ Please select the appropriate item for you to "
                     f"fulfill your task / desire.",
                reply_markup=var.as_markup(),
                parse_mode="HTML"
            )
        else:
            var: InlineKeyboardBuilder = await Buttons.get_add_new_email()
            await bot.edit_message_text(
                text=f"🤔 <b>{call_query.from_user.first_name}</b>, sorry! But your email "
                     f"address is not in the system.\n"
                     f"<em>Add your email address to manage your AI-Functions in <b>CWBot UI</b>, "
                     f"click on the button "
                     f"below!</em>.",
                message_id=call_query.message.message_id,
                chat_id=call_query.from_user.id,
                parse_mode="HTML",
                reply_markup=var.as_markup()
            )


class EmailSector:
    """
    Email sector-class.
    """

    @staticmethod
    async def add_new_email(
            bot,
            call_query: types.CallbackQuery,
            state: FSMContext,
            admin_id: int
    ) -> None:
        """
        Handler (callback-handler) for add a new EMail.

        :param bot: The Bot-object.
        :param call_query: Callback Query.
        :param state: FSM.
        :param admin_id: Admin ID (telegram ID).

        :return: None.
        """
        try:
            email: HandlerEM = HandlerEM(bot, admin_id)
            await email.add_new_email(call_query, state)

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")

    @staticmethod
    async def email_settings_menu(
            bot,
            call_query: types.CallbackQuery,
            admin_id: int
    ) -> None:
        """
        Menu of EMail Settings for any users and admin.

        :param bot: The Bot-object.
        :param call_query: Callback Query.
        :param admin_id: Admin ID (telegram ID).

        :return: None.
        """
        result: tuple = await HandlerDB.get_email_data(call_query.from_user.id)
        if result[0] is True or call_query.from_user.id == admin_id:
            email: HandlerEM = HandlerEM(bot, admin_id)
            await email.show_email_settings_menu(call_query)
        else:
            var: InlineKeyboardBuilder = await Buttons.get_add_new_email()
            await bot.edit_message_text(
                text=f"🤔 <b>{call_query.from_user.first_name}</b>, sorry! But your email "
                     f"address is not in the system.\n"
                     f"<em>Add your email address to manage your AI-Functions in <b>CWBot UI</b>, "
                     f"click on the button below!</em>.",
                message_id=call_query.message.message_id,
                chat_id=call_query.from_user.id,
                parse_mode="HTML",
                reply_markup=var.as_markup()
            )


class MenuSector:
    """
    The class-sector of manage MENU-functions.
    """

    @staticmethod
    async def back_on_main(
            bot: Bot,
            call: types.CallbackQuery,
            admin_id: int
    ) -> None:
        """
        Handler for return to main-menu.

        :param bot: The Bot-object.
        :param call: Callback Query.
        :param admin_id: Admin ID (telegram ID).

        :return: None.
        """
        if call.from_user.id == admin_id:
            var: InlineKeyboardBuilder = await Buttons.get_menu_admin()
            await bot.edit_message_text(
                chat_id=call.from_user.id,
                text=f"👑 *{call.from_user.first_name}*,\nYou are in the main menu. Select the "
                     f"desired item below!\n\nUsing the services CWR.SU (CW), you accept all the "
                     f"rules and the agreement. [SEE](https://acdn.cwr.su/src/acdn/Agreement_and_"
                     f"Terms_of_Use_for_the_Manager_CW_Bot_Service.pdf).",
                message_id=call.message.message_id,
                reply_markup=var.as_markup(),
                parse_mode="Markdown"
            )
        else:
            var: InlineKeyboardBuilder = await Buttons.get_menu_without_premium()
            checked: bool | tuple = await HandlerDB.check_subscription(call)
            if checked[0] is False:
                await bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text="💡 You are in the main menu. Select the desired item below!\n"
                         f"\nUsing the services CWR.SU (CW), you accept all the rules and the "
                         f"agreement. [SEE](https://acdn.cwr.su/src/acdn/Agreement_and_Terms_of_"
                         f"Use_for_the_Manager_CW_Bot_Service.pdf).",
                    message_id=call.message.message_id,
                    reply_markup=var.as_markup(),
                    parse_mode="Markdown"
                )
            elif checked[0] is True:
                var: InlineKeyboardBuilder = await Buttons.get_menu_with_premium()
                await bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=f"👑 *{call.from_user.first_name}*,\n"
                         f"You are in the main menu. Select the desired item below!\n"
                         f"\nUsing the services CWR.SU (CW), you accept all the rules and the "
                         f"agreement. [SEE](https://acdn.cwr.su/src/acdn/Agreement_and_Terms_of_"
                         f"Use_for_the_Manager_CW_Bot_Service.pdf).",
                    message_id=call.message.message_id,
                    reply_markup=var.as_markup(),
                    parse_mode="Markdown"
                )

    @staticmethod
    async def get_main_menu(
            bot: Bot,
            message: types.Message,
            admin_id: int
    ) -> None:
        """
        Handler for go to main-menu.

        :param bot: The Bot-object.
        :param message: Message.
        :param admin_id: Admin ID (telegram ID).

        :return: None.
        """
        await bot.set_message_reaction(
            chat_id=message.from_user.id,
            message_id=message.message_id,
            reaction=[types.ReactionTypeEmoji(
                types='emoji',
                emoji='⚡'
            )]
        )
        if message.from_user.id == admin_id:
            var: InlineKeyboardBuilder = await Buttons.get_menu_admin()
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"👑 *{message.from_user.first_name}*,\nYou are in the main menu. Select "
                     f"the desired item below!\n\nUsing the services CWR.SU (CW), you accept all "
                     f"the rules and the agreement. [SEE](https://acdn.cwr.su/src/acdn/new_user_"
                     f"agreement_manager_cw_bot.pdf).",
                reply_markup=var.as_markup(),
                parse_mode="Markdown"
            )
        else:
            checked: bool | tuple = await HandlerDB.check_subscription(message)
            if checked[0] is False:
                var: InlineKeyboardBuilder = await Buttons.get_menu_without_premium()
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text="💡 You are in the main menu. Select the desired item below!\n"
                         f"\nUsing the services CWR.SU (CW), you accept all the rules and the "
                         f"agreement. [SEE](https://acdn.cwr.su/src/acdn/new_user_agreement_"
                         f"manager_cw_bot.pdf).",
                    reply_markup=var.as_markup(),
                    parse_mode="Markdown"
                )
            elif checked[0] is True:
                var: InlineKeyboardBuilder = await Buttons.get_menu_with_premium()
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"👑 *{message.from_user.first_name}*,\n"
                         f"You are in the main menu. Select the desired item below!\n"
                         f"\nUsing the services CWR.SU (CW), you accept all the rules and the "
                         f"agreement. [SEE](https://acdn.cwr.su/src/acdn/new_user_agreement_"
                         f"manager_cw_bot.pdf).",
                    reply_markup=var.as_markup(),
                    parse_mode="Markdown"
                )


class Manager(Bot):
    """
    Manager of the Admin Account and helper 'AI'.
    """
    def __init__(
            self,
            bot_token: str,
            business_conn_id: str,
            admin_id: int,
            mysql_data: dict,
            gigachat_data: dict,
            admin_username: str
    ) -> None:
        super().__init__(bot_token)
        self.__dp = Dispatcher()
        self.router = Router()

        self.router.message.register(
            self.__get_id_ticket_for_show,
            GetTicketDataByIDTCK.id_ticket
        )

        self.__business_connection_id: str = business_conn_id
        self.__admin_id: int = admin_id
        self.__mysql_data: dict = mysql_data
        self.__gigachat_data: dict = gigachat_data
        self.__admin_username: str = admin_username

    async def __privacy(self, message: types.Message) -> None:
        """
        Privacy for the users.

        :param message: Message / Command Privacy.
        :return: None.
        """
        await PrivacyMessagesSector.privacy(
            self, message
        )

    async def __eng_privacy(self, call_query: types.CallbackQuery) -> None:
        """
        Explore to show ENG Privacy.

        :param call_query: Callback Query.

        :return: None.
        """
        await PrivacyMessagesSector.eng_privacy(
            self, call_query
        )

    async def __rus_privacy(self, call_query: types.CallbackQuery) -> None:
        """
        Explore to show RUS Privacy.

        :param call_query: Callback Query.

        :return: None.
        """
        await PrivacyMessagesSector.rus_privacy(
            self, call_query
        )

    async def __standard_message(self, message: types.Message) -> None:
        """
        Answer to the users and admin.

        :param message: Message.
        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.back_on_main()
        await self.send_message(
            chat_id=message.from_user.id,
            text=f"⚡ *{message.from_user.first_name}*, click on the button below to *go to the "
                 f"main menu*.",
            parse_mode="Markdown",
            reply_markup=var.as_markup()
        )

    async def __answer_to_user(self, message: types.Message) -> None:
        """
        Answer to a user from admin-account (as admin).

        :param message: Message of a user.
        :return: None.
        """
        answers: Answers = Answers(
            business_connection_id=self.__business_connection_id,
            admin_id=self.__admin_id
        )
        await answers.answer_to_user(
            self, message
        )

    async def __explore_show_users_ticket(
            self,
            call_query: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Explore to show user's ticket by id.

        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await TicketsSector.explore_show_users_ticket(
            self, call_query, state
        )

    async def __get_id_ticket_for_show(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Get id ticket for admin answer/view or user view.

        :param message: Message (ID ticket) from admin/the user.
        :param state: FSM.

        :return: None.
        """
        await TicketsSector.get_id_ticket_for_show(
            self, message, state, self.__mysql_data
        )

    async def __explore_answer_users_ticket(
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
        await TicketsSector.explore_answer_users_ticket(
            self, call_query, state, self.__admin_id, self.__mysql_data
        )

    async def __explore_answer_admin_by_ticket(
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
        await TicketsSector.explore_answer_admin_by_ticket(
            self, call_query, state, self.__admin_id, self.__mysql_data
        )

    async def __user_menu_tickets(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Handler (callback-handler) for go to the Tickets-Menu.

        :param call_query: Callback Query.
        :return: None.
        """
        await TicketsSector.user_menu_tickets(
            self, call_query, self.__mysql_data
        )

    async def __admin_menu_tickets(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Handler (callback-handler) for show tickets to admin.

        :param call_query: Callback Query.
        :return: None.
        """
        await TicketsSector.admin_menu_tickets(
            self, call_query, self.__mysql_data
        )

    async def __analytic_data(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Handler of the analytic-menu (UI) for admin.

        :param call_query: Callback Query.
        :return: None.
        """
        analytic: Analytic = Analytic(
            self,
            call_query
        )
        await analytic.analyse()

    async def __business_handler(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Handler (call-query) for admin (with business) - start main handler.

        :param call_query: Callback Query.
        :return: None.
        """
        await PremiumFunctionsSector.business_handler(
            self, call_query
        )

    async def __get_or_lk_premium(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Get CW PREMIUM or view (look at) "MY PREMIUM".

        :param call_query: Callback Query.
        :return: None.
        """
        await PremiumFunctionsSector.get_or_lk_premium(
            self, call_query, self.__admin_id, self.__admin_username
        )

    async def __continue_subscribe_premium(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Continue to subscribe CW PREMIUM. Choose method of payment.

        :param call_query: Callback Query.
        :return: None.
        """
        await PremiumFunctionsSector.continue_subscribe_premium(
            self, call_query, self.__admin_id
        )

    async def __business_and_money(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Handler (callback-handler) for explore to BusinessAndMoney-menu.

        :param call_query: Callback Query.
        :return: None.
        """
        await PremiumFunctionsSector.business_and_money(
            self, call_query
        )

    async def __show_promo_menu_admin(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Show PROMO Menu. | Control ADMIN.

        :param call_query: Callback Query.
        :return: None.
        """
        await PromoFunctionsSector.show_promo_menu_admin(
            self, call_query, self.__admin_id
        )

    async def __enter_promo_code(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Func 'ENTER' a promo code from user. | Step 1.

        :param call: CallbackQuery.
        :param state: FSM.

        :return: None.
        """
        await PromoFunctionsSector.enter_promo_code(
            self, call, state, self.__admin_id
        )

    async def __pre_checkout_query(
            self,
            pre_checkout_query: types.PreCheckoutQuery
    ) -> None:
        """
        Pre-Checkout TelegramPay Function.

        :param pre_checkout_query: Pre-Checkout-query.
        :return: None.
        """
        await FinanceSector.pre_checkout_query(
            self, pre_checkout_query
        )

    async def __successful_payment(
            self,
            message: types.Message
    ) -> None:
        """
        Handler for successful payment.

        :param message: Message from user.
        :return: None.
        """
        await FinanceSector.successful_payment(
            self, message, self.__admin_id
        )

    async def __refund(
            self,
            call: types.CallbackQuery
    ) -> None:
        """
        Refund-menu for admin use / control.

        :param call: Callback Query.
        :return: None.
        """
        await FinanceSector.refund(
            self, call
        )

    async def __refunding_step1(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Call-Handler for refund stars | Step 1.

        :param call: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await FinanceSector.refunding_step1(
            self, call, state
        )

    async def __ai_assistance(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Handler (callback-handler) for go to the AI-Menu.

        :param call_query: Callback Query.
        :return: None.
        """
        await AISector.ai_assistance(
            self, call_query
        )

    async def __generate_image_for_premium_user(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Generate image for premium-user.

        :param call: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await AISector.generate_image_for_premium_user(
            self, call, state
        )

    async def __ai_two_in_one_main_menu(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Handler (callback-handler) for explore to AI-menu.

        :param call_query: Callback Query.
        :return: None.
        """
        await AISector.ai_two_in_one_main_menu(
            self, call_query, self.__admin_id
        )

    async def __back_on_main(
            self,
            call: types.CallbackQuery
    ) -> None:
        """
        Handler for return to main-menu.

        :param call: Callback Query.
        :return: None.
        """
        await MenuSector.back_on_main(
            self, call, self.__admin_id
        )

    async def __get_main_menu(
            self,
            message: types.Message
    ) -> None:
        """
        Handler for go to main-menu.

        :param message: Message.
        :return: None.
        """
        await MenuSector.get_main_menu(
            self, message, self.__admin_id
        )

    async def __add_new_email(
            self,
            call_query: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Handler (callback-handler) for add a new EMail.

        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await EmailSector.add_new_email(
            self, call_query, state, self.__admin_id
        )

    async def __email_settings_menu(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Menu of EMail Settings for any users and admin.

        :param call_query: Callback Query.
        :return: None.
        """
        await EmailSector.email_settings_menu(
            self, call_query, self.__admin_id
        )

    async def run(self) -> None:
        """
        Run-function Bot.
        """
        try:
            connection: pymysql.Connection = await Connection.get_connection(self.__mysql_data)
            cursor = connection.cursor()
            creator_mysql = CreateTable(connection, cursor)
            creator_mysql.create()

        except Exception as ex:
            logging.error(f"The error of database of business.py Manager class: {ex}.")

        self.router.message.register(
            self.__get_main_menu, Command(commands=["main", "start"])
        )
        self.router.message.register(
            self.__privacy, Command("privacy")
        )
        self.router.callback_query.register(
            self.__eng_privacy,
            F.data == "eng_privacy_mode"
        )
        self.router.callback_query.register(
            self.__rus_privacy,
            F.data == "rus_privacy_mode"
        )

        self.router.business_message.register(
            self.__answer_to_user,
            F.content_type == ContentType.TEXT
        )

        self.router.callback_query.register(
            self.__ai_assistance,
            F.data == "ai_assistance_request"
        )
        self.router.callback_query.register(
            self.__generate_image_for_premium_user,
            F.data == "kandinsky_generate"
        )
        self.router.callback_query.register(
            self.__ai_two_in_one_main_menu,
            F.data == "ai_two_in_one_main_menu"
        )
        self.router.callback_query.register(
            self.__admin_menu_tickets,
            F.data == "explore_admin_tickets_menu"
        )
        self.router.callback_query.register(
            self.__user_menu_tickets,
            F.data == "explore_user_tickets_menu"
        )

        self.router.callback_query.register(
            self.__explore_answer_users_ticket,
            F.data == "explore_answer_to_user"
        )
        self.router.callback_query.register(
            self.__explore_answer_admin_by_ticket,
            F.data == "explore_answer_to_admin"
        )

        self.router.callback_query.register(
            self.__explore_show_users_ticket,
            F.data == "explore_show_ticket_by_id"
        )

        self.router.callback_query.register(
            self.__business_and_money,
            F.data == "business_and_money"
        )
        self.router.callback_query.register(
            self.__analytic_data,
            F.data == "analytic_data"
        )
        self.router.callback_query.register(
            self.__business_handler,
            F.data == "business_handler"
        )
        self.router.callback_query.register(
            self.__email_settings_menu,
            F.data == "email_settings_menu"
        )
        self.router.callback_query.register(
            self.__refund,
            F.data == "start_refund"
        )
        self.router.callback_query.register(
            self.__refunding_step1,
            F.data == "refund"
        )
        self.router.callback_query.register(
            self.__show_promo_menu_admin,
            F.data == "show_menu_promo_admin"
        )

        self.router.callback_query.register(
            self.__get_or_lk_premium,
            F.data == "get_or_lk_premium"
        )
        self.router.callback_query.register(
            self.__continue_subscribe_premium,
            F.data == "continue_subscribe_premium"
        )
        self.router.callback_query.register(
            self.__enter_promo_code,
            F.data == "continue_subscribe_premium_with_promo"
        )

        self.router.callback_query.register(
            self.__back_on_main,
            F.data == "back_on_main"
        )

        self.router.callback_query.register(
            self.__add_new_email,
            F.data == "add_new_email"
        )

        self.router.pre_checkout_query.register(
            self.__pre_checkout_query,
            F.func(lambda query: True)
        )
        self.router.message.register(
            self.__successful_payment,
            F.content_type == ContentType.SUCCESSFUL_PAYMENT
        )
        self.router.message.register(
            self.__standard_message,
            F.content_type == ContentType.TEXT
        )

        self.__dp.include_routers(
            router,
            router_ai_img,
            router_business,
            router_chat_ai,
            router_handler_em,
            router_refund,
            router_promo,
            router_send_invoice,
            self.router
        )

        logging.info("Handlers and routers from other modules successfully registered")

        await self.__dp.start_polling(self)


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
        dct["ADMIN_ID"] = data["business_connection"]["user"]["id"]
        dct["ADMIN_USERNAME"] = data["business_connection"]["user"]["username"]
        dct["ADMIN_EMAIL_FOR_CHECK"] = data["EMAIL_DATA"]["ADMIN_EMAIL"]

        dct["MYSQL"] = data["MYSQL"]

        dct["GIGACHAT"] = data["GIGACHAT"]

        dct["BUSINESS_HANDLER"] = data["BUSINESS_HANDLER"]

        logging.info("Data unloaded (received) from configuration file")
        return dct


async def run() -> None:
    """
    Run Function of the main-file.

    :return: None.
    """
    try:
        data: dict = get_data()
        if (data["business_connection_is_enabled"] == "True" and
                len(data["ADMIN_EMAIL_FOR_CHECK"]) >= 7):
            bot: Manager = Manager(
                data["BOT_TOKEN"],
                data["business_connection_id"],
                data["ADMIN_ID"],
                data["MYSQL"],
                data["GIGACHAT"],
                data["ADMIN_USERNAME"]
            )
            await bot.run()

        else:
            logging.error("Business connection is unavailable or the length of your EMail "
                          "is incorrect!")
            raise ValueError("Business connection is unavailable or the length of your EMail "
                             "is incorrect!")
    except Exception as ex:
        logging.warning(f"The exception has arisen: {ex}.")
