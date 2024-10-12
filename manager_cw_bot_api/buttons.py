"""
Module of the create button for the menu and Bot in general.
"""
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from manager_cw_bot_api.handler_db_sub_operations import HandlerDB
from manager_cw_bot_api.handler_email_sender import SenderEmail


class Buttons:
    """
    Class for get the buttons in chats.
    """
    @staticmethod
    async def get_language_privacy_menu() -> InlineKeyboardBuilder:
        """
        builder-button (Inline) of the lang-mode for privacy-menu.

        :return: Builder-buttons.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🇬🇧 ENG", callback_data="eng_privacy_mode")
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🇷🇺 RUS", callback_data="rus_privacy_mode")
        builder.add(var1).row(var2)
        return builder

    @staticmethod
    async def get_email() -> InlineKeyboardBuilder:
        """
        Builder-button (Inline) of the help.

        :return: Builder-buttons.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="👆 Go", url="t.me/aleksandr_work")
        builder.add(var1)
        return builder

    @staticmethod
    async def get_add_new_email() -> InlineKeyboardBuilder:
        """
        Get menu for add a new email for user / admin.

        :return: builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="➕ Add 📧",
            callback_data="add_new_email"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel",
            callback_data="back_on_main"
        )
        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def get_add_new_email_try_again() -> InlineKeyboardBuilder:
        """
        Get menu for add a new email for user / admin again.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔃 Try again 📧",
            callback_data="add_new_email"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel",
            callback_data="back_on_main"
        )
        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def get_add_new_email_or_check_ver_code_try_again() -> InlineKeyboardBuilder:
        """
        Get menu for add a new email for user / admin again or again check the ver. code.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔃 Try again | VERIFY CODE #️⃣",
            callback_data="check_verify_code_again"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔃 Try again | Add EMail 📧",
            callback_data="add_new_email"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel",
            callback_data="back_on_main"
        )
        builder.row(var1).row(var2).row(var3)
        return builder

    @staticmethod
    async def get_var_giga_version(
        message: types.Message | types.CallbackQuery
    ) -> InlineKeyboardBuilder:
        """
        Builder-button (Inline) of the choose version of the GigaChatAI
        for the user.

        :param message: Message.
        :return: Builder-buttons.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        result: bool | tuple = await HandlerDB.check_subscription(message)
        if result[0] is True:
            var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="💡 GigaChatLight", callback_data="gigachat_version_light"
            )
            var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="⚡ GigaChatPRO", callback_data="gigachat_version_pro"
            )
            var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="🔙 Back to AI-Menu", callback_data="ai_two_in_one_main_menu"
            )
            var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="🔙 Main", callback_data="back_on_main"
            )
            builder.row(var1).row(var2).row(var3).row(var4)

        elif result[0] is False:
            var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="💡 GigaChatLight", callback_data="gigachat_version_light"
            )
            var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="⚡ GigaChatPRO", callback_data="get_or_lk_premium"
            )
            var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="🔙 Back to AI-Menu", callback_data="ai_two_in_one_main_menu"
            )
            var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="🔙 Main", callback_data="back_on_main"
            )
            builder.row(var1).row(var2).row(var3).row(var4)

        return builder

    @staticmethod
    async def get_menu_user_tickets() -> InlineKeyboardBuilder:
        """
        Builder-button (Inline) of the Bot Menu
        for the user in "TICKETS".

        :return: Builder-buttons.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💬 Show My tickets", callback_data="show_user_tickets"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💭 Send a new ticket", callback_data="send_new_ticket"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✉ Show the ticket by ID", callback_data="explore_show_ticket_by_id"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🗣 Answer to the admin", callback_data="explore_answer_to_admin"
        )
        var5: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )
        builder.row(var1).row(var2).row(var3).row(var4).row(var5)
        return builder

    @staticmethod
    async def get_menu_user_tickets_again() -> InlineKeyboardBuilder:
        """
        Builder-button (Inline) of the Bot AGAIN-Menu
        for the user in "TICKETS".

        :return: Builder-buttons.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💭 Send a new ticket", callback_data="send_new_ticket"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Tickets Menu", callback_data="explore_user_tickets_menu"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )
        builder.row(var1).row(var2).row(var3)
        return builder

    @staticmethod
    async def get_user_tickets(tg_id: int) -> tuple:
        """
        Builder-button (Inline) of the Bot
        for the user's history of "TICKETS".

        :param tg_id: User's id -- tg_id.

        :return: Tuple with data.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        response: tuple = tuple()

        result: InlineKeyboardBuilder | tuple = await HandlerDB.get_ticket_data(tg_id, builder)

        if type(result) is InlineKeyboardBuilder:
            response = (False, "Not Found. Please, click on the '🔙 Main' / '🔙 TicketSystem' - "
                               "button.")
            builder: InlineKeyboardBuilder = result

        elif (type(result) is tuple) and result[0] is True:
            response = (True, result[1], result[2])
            var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="✅ Allow",
                callback_data="allow_send_email_ticket_data_user"
            )
            var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="❌ No, just show available data",
                callback_data="not_allow_send_email_ticket_data_user"
            )
            var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="🗣 Answer to the admin",
                callback_data="explore_answer_to_admin"
            )
            var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="🔙 TicketSystem",
                callback_data="explore_user_tickets_menu"
            )
            var5: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="🔙 Main",
                callback_data="back_on_main"
            )
            builder.row(var1).row(var2).row(var3).row(var4).row(var5)

        elif (type(result) is tuple) and result[0] is False:
            response = (False, result[1])
            var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="🗣 Answer to the admin",
                callback_data="explore_answer_to_admin"
            )
            var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="🔙 TicketSystem",
                callback_data="explore_user_tickets_menu"
            )
            var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="🔙 Main",
                callback_data="back_on_main"
            )
            builder.row(var1).row(var2).row(var3)

        results: tuple = (response, builder)
        return results

    @staticmethod
    async def get_menu_admin() -> InlineKeyboardBuilder:
        """
        Builder-button (Inline) of the Bot Menu
        for admin.

        :return: Builder-buttons.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🧠 AI | 2 in 1 🖼", callback_data="ai_two_in_one_main_menu"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="👑 MY PREMIUM 🌟", callback_data="get_or_lk_premium"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="ℹ TicketSystem 👨🏻‍💻", callback_data="explore_admin_tickets_menu"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💲 Business and Money 🌐", callback_data="business_and_money"
        )
        builder.row(var1).row(var2).row(var3).row(var4)
        return builder

    @staticmethod
    async def get_ticket_menu_admin() -> InlineKeyboardBuilder:
        """
        Get menu for admin - TicketSystem-Menu (TicketsMenu).

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="📨 Show tickets", callback_data="show_tickets_for_admin_menu"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✉ Show the ticket by ID", callback_data="explore_show_ticket_by_id"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🗣 Answer to the user", callback_data="explore_answer_to_user"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )
        builder.row(var1).row(var2).row(var3).row(var4)
        return builder

    @staticmethod
    async def get_business_and_money_menu_admin() -> InlineKeyboardBuilder:
        """
        Get menu for admin - BusinessAndMoney-Menu.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="📈 Analytic", callback_data="analytic_data"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🧑‍💼 Business Handler", callback_data="business_handler"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="📧 EMail Settings 🔑", callback_data="email_settings_menu"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💱 PROMO 📲", callback_data="show_menu_promo_admin"
        )
        var5: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔃 Refund 💸", callback_data="start_refund"
        )
        var6: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )
        builder.row(var1).row(var2).row(var3).row(var4).row(var5).row(var6)
        return builder

    @staticmethod
    async def get_menu_email_settings(tg_id: int, admin_id: int) -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for menu of Email Settings.

        :param tg_id: TG ID for check and create Builder.
        :param admin_id: ID Admin.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        if tg_id == admin_id:
            data: dict = await SenderEmail.get_email_data_admin()
            if data["ANSWER"][0] is True:
                var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
                    text="👁‍🗨 Show EMail", callback_data="show_email_from_settings_menu"
                )
                var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
                    text="Edit EMAil 💻", callback_data="edit_email_from_settings_menu"
                )
                var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
                    text="🔙 Main", callback_data="back_on_main"
                )
            else:
                var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
                    text="✨ Add Email", callback_data="add_email_from_settings_menu"
                )
                var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
                    text="Support 💻", url="mailto:help@cwr.su"
                )
                var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
                    text="🔙 Main", callback_data="back_on_main"
                )
        else:
            result: tuple = await HandlerDB.get_email_data(tg_id)
            if result[0] is True:
                var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
                    text="👁‍🗨 Show EMail", callback_data="show_email_from_settings_menu"
                )
                var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
                    text="Edit EMail 💻", callback_data="edit_email_from_settings_menu"
                )
                var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
                    text="🔙 Main", callback_data="back_on_main"
                )
            else:
                var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
                    text="✨ Add Email", callback_data="add_email_from_settings_menu"
                )
                var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
                    text="Support 💻", url="mailto:help@cwr.su"
                )
                var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
                    text="🔙 Main", callback_data="back_on_main"
                )

        builder.row(var1).row(var2).row(var3)
        return builder

    @staticmethod
    async def get_menu_confirmation_for_edit_email() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for confirmation to edit email of the user / admin.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ I'm sure 100%, OK",
            callback_data="confirmation_to_edit_email_from_email_settings"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel",
            callback_data="email_settings_menu"
        )
        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def get_menu_back_to_email_settings() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for menu-back to EMailSettings-menu.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Back to EMailSettings", callback_data="email_settings_menu"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )
        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def get_menu_admin_promos() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for main-menu for admin.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🎫 Add a new PROMO data", callback_data="add_new_promo"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Show PROMO datas 🌐", callback_data="show_promo_datas"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🗑️ Delete a PROMO data", callback_data="delete_promo_data"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Back to BusinessAndMoney", callback_data="business_and_money"
        )
        var5: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )

        builder.row(var1).row(var2).row(var3).row(var4).row(var5)
        return builder

    @staticmethod
    async def get_menu_back_to_business_and_money_for_admin() -> InlineKeyboardBuilder:
        """
        Get BACK-MENU for admin, for back to BusinessAndMoney-Menu.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Back to BusinessAndMoney", callback_data="business_and_money"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )
        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def get_users_tickets_for_admin() -> tuple:
        """
        Builder-button (Inline) of the Bot
        for the admin history of "TICKETS" of the users.

        :return: tuple of the tickets and Builder-buttons.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        response: tuple = tuple()

        result: tuple | InlineKeyboardBuilder = await HandlerDB.get_users_tickets_for_admin()

        if type(result) is InlineKeyboardBuilder:
            builder: InlineKeyboardBuilder = result

        elif (type(result) is tuple) and result[0] is True:
            response = (True, result[1], result[2])

        elif (type(result) is tuple) and result[0] is False:
            response = (False, result[1])

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ Allow",
            callback_data="allow_send_email_ticket_data_admin"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ No, just show available data",
            callback_data="not_allow_send_email_ticket_data_admin"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main",
            callback_data="back_on_main"
        )
        builder.row(var1).row(var2).row(var3)

        results: tuple = (response, builder)
        return results

    @staticmethod
    async def get_menu_business_handler() -> InlineKeyboardBuilder:
        """
        Get menu of business handler.

        :return: Builder Buttons.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💫 Thanks", callback_data="handler_thanks_from_users"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Congratulation 🎉", callback_data="handler_congratulation_from_users"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🤖 Problem with bot", callback_data="handler_problem_with_bot_from_users"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Back to BusinessAndMoney", callback_data="business_and_money"
        )
        var5: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )

        builder.row(var1).row(var2).row(var3).row(var4).row(var5)

        return builder

    @staticmethod
    async def get_menu_business_handler_thanks() -> InlineKeyboardBuilder:
        """
        Get menu of business handler - ThanksCommandAnswer.

        :return: Builder Buttons.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💌 Only text", callback_data="only_text_for_thanks_hdl"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Only Sticker 💗", callback_data="only_sticker_for_thanks_hdl"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💞 Both: Message and sticker", callback_data="message_and_sticker_for_thanks_hdl"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Back to BusinessAndMoney", callback_data="business_and_money"
        )
        var5: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )

        builder.row(var1).row(var2).row(var3).row(var4).row(var5)

        return builder

    @staticmethod
    async def get_menu_business_handler_congratulation() -> InlineKeyboardBuilder:
        """
        Get menu of business handler - CongratulationCommandAnswer.

        :return: Builder Buttons.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🎉 Only text", callback_data="only_text_for_congratulation_hdl"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Only Sticker 💗", callback_data="only_sticker_for_congratulation_hdl"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💫 Both: Message and sticker",
            callback_data="message_and_sticker_for_congratulation_hdl"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Back to BusinessAndMoney", callback_data="business_and_money"
        )
        var5: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )

        builder.row(var1).row(var2).row(var3).row(var4).row(var5)

        return builder

    @staticmethod
    async def get_menu_business_handler_problem_with_bot() -> InlineKeyboardBuilder:
        """
        Get menu of business handler - ProblemWithBotCommandAnswer.

        :return: Builder Buttons.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💬 Only text", callback_data="only_text_for_problem_with_bot_hdl"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Only Sticker ♨", callback_data="only_sticker_for_problem_with_bot_hdl"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💫 Both: Message and sticker",
            callback_data="message_and_sticker_for_problem_with_bot_hdl"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Back to BusinessAndMoney", callback_data="business_and_money"
        )
        var5: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )

        builder.row(var1).row(var2).row(var3).row(var4).row(var5)

        return builder

    @staticmethod
    async def sure_refund() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for 'sure' refund by admin.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ I'm sure", callback_data="refund"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel", callback_data="back_on_main"
        )

        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def sure_refund_confirmation() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for 'sure' refund by admin | Confirmation.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ I'm sure 100%", callback_data="refund_confirmation"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel", callback_data="back_on_main"
        )

        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def sure_emergency_refund_confirmation() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for 'sure' emergency refund by admin | Confirmation.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ Emergency Refund | I'm sure!", callback_data="emergency_refund_confirmation"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel", callback_data="back_on_main"
        )

        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def sure_apply_promo() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for 'sure' apply a promo code by user.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ Yes, apply it. I'm sure 100%", callback_data="apply_promo"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel", callback_data="back_on_main"
        )

        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def sure_add_new_promo() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for 'sure' add a promo code by ADMIN | Admin control.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ Yes, add! I'm sure.", callback_data="add_new_promo_confirmation"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel", callback_data="show_menu_promo_admin"
        )

        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def sure_delete_promo() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for 'sure' delete a promo code by ADMIN | Admin control.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ Yes, delete! I'm sure 100%.", callback_data="delete_promo_confirmation"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel", callback_data="show_menu_promo_admin"
        )

        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def try_again_add_new_promo_or_back_on_main() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for attempt add a new promo data or return in PROMO Menu.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔄 Try again", callback_data="try_again_add_new_promo"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Back", callback_data="show_menu_promo_admin"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )
        builder.row(var1).row(var2).row(var3)
        return builder

    @staticmethod
    async def try_again_delete_promo_or_back_on_main() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for attempt delete a promo data or return in PROMO Menu.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔄 Try again", callback_data="try_again_delete_promo"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Back", callback_data="show_menu_promo_admin"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )
        builder.row(var1).row(var2).row(var3)
        return builder

    @staticmethod
    async def back_in_promo_menu() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for return in PROMO menu.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Back", callback_data="show_menu_promo_admin"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )
        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def get_menu_without_premium() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for main-menu for users without CW PREMIUM.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🧠 AI | 2 in 1 🖼", callback_data="ai_two_in_one_main_menu"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Get CW PREMIUM 🔥", callback_data="get_or_lk_premium"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❔ Help | CWR.SU", url="https://cwr.su/"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="ℹ Help | TicketSystem 👨🏻‍💻", callback_data="explore_user_tickets_menu"
        )
        var5: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="📧 EMail Settings 🔑", callback_data="email_settings_menu"
        )
        builder.row(var1).row(var2).row(var3).row(var4).row(var5)
        return builder

    @staticmethod
    async def get_ai_menu() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for main-menu of AI.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✨ Generate IMG 🖼", callback_data="kandinsky_generate"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🧠 Assistance (DIALOG 🆕*)", callback_data="ai_assistance_request"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )
        builder.row(var1).row(var2).row(var3)
        return builder

    @staticmethod
    async def get_menu_with_premium() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for main-menu for users with CW PREMIUM.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🧠 ✨ AI | 2 in 1 🖼", callback_data="ai_two_in_one_main_menu"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="👑 MY PREMIUM 🌟", callback_data="get_or_lk_premium"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❔ Help | CWR.SU", url="https://cwr.su/"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="ℹ Help | TicketSystem 👨🏻‍💻", callback_data="explore_user_tickets_menu"
        )
        var5: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="📧 EMail Settings 🔑", callback_data="email_settings_menu"
        )
        builder.row(var1).row(var2).row(var3).row(var4).row(var5)
        return builder

    @staticmethod
    async def generate_image() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for generate image by GigaChat | V3 | For premium-user.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ I'm sure", callback_data="generate"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel", callback_data="back_on_main"
        )

        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def get_premium() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for get status premium-user and get CW PREMIUM.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Get CW PREMIUM 💥 | -55%", callback_data="continue_subscribe_premium"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="I have a promo code 🎫", callback_data="continue_subscribe_premium_with_promo"
        )

        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def get_premium_process_choosing() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for get status premium-user and get CW PREMIUM | Process choosing.

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💳 ЮKassa | BankCard | FPS (СБП) | PhoneBalance",
            callback_data="continue_subscribe_premium_with_yookassa"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="⭐ Telegram Stars",
            callback_data="continue_subscribe_premium_with_telegram_stars"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔑 Check payment",
            callback_data="check_pay_yookassa"
        )

        builder.row(var1).row(var2).row(var3)
        return builder

    @staticmethod
    async def get_menu_yookassa_payment(url: str) -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for pay with YOOKASSA.

        :param url: URL.
        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💳 Pay", url=url
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Check 🔑", callback_data="check_pay_yookassa"
        )

        builder.row(var1).row(var2)
        return builder

    @staticmethod
    async def back_on_main() -> InlineKeyboardBuilder:
        """
        Get Builder-keyboard for return in main menu (on main).

        :return: Builder.
        """
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        var: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )

        builder.row(var)
        return builder
