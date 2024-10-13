"""
Module of the analytics data from database for admin.
"""
import datetime
import logging

from aiogram import types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB


class Analytic:
    """
    Analytic Class.
    """
    def __init__(self, bot: Bot,
                 call_query: types.CallbackQuery) -> None:
        self.__bot = bot
        self.__call_query: types.CallbackQuery = call_query

    async def analyse(self) -> None:
        """
        Analyse the data for admin.

        :return: None.
        """
        response: tuple = await HandlerDB.get_analytic_datas()

        if len(response) == 0:
            count_of_ai_queries = 0
            count_of_tickets_system = 0
        else:
            count_of_ai_queries: int = response[0][0]
            count_of_tickets_system: int = response[0][1]

        try:
            var: InlineKeyboardBuilder = await (
                Buttons.get_menu_back_to_business_and_money_for_admin()
            )
            await self.__bot.edit_message_text(
                chat_id=self.__call_query.message.chat.id,
                text=f"👑 <b>{self.__call_query.from_user.first_name}</b>, look! Your statistic's "
                     f"below.\n----------------------------------------\n"
                     f"⁉ Count of AI <b>Queries</b> (all): <b>{count_of_ai_queries}</b>.\n\n"
                     f"🎫 Count of <b>Tickets</b> in the System (all): <b>{count_of_tickets_system}"
                     f"</b>.\n\n*<i>The data is current as "
                     f"{str(datetime.datetime.now()).split('.')[0]}.</i>",
                message_id=self.__call_query.message.message_id,
                reply_markup=var.as_markup(),
                parse_mode="HTML"
            )

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")
