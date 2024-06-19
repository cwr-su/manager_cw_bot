"""
Module of the create button for the menu and Bot in general.
"""
from telebot import types

from manager_cw_bot_api.handler_db_sub_operations import HandlerDB


class Buttons:
    """
    Class for get the buttons in chats.
    """
    @staticmethod
    def get_email() -> types.InlineKeyboardMarkup:
        """
        Markup-button (Inline) of the help.

        :return: Markup-buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="👆 Перейти", url="t.me/aleksandr_work")
        markup.add(btn1)
        return markup

    @staticmethod
    def get_var_giga_version(message: types.Message) -> types.InlineKeyboardMarkup:
        """
        Markup-button (Inline) of the choose version of the GigaChatAI
        for the user.

        :param message: Message.
        :return: Markup-buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        result: bool | tuple = HandlerDB.check_subscription(message)
        if result[0] is True:
            v1: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="💡 GigaChatLight", callback_data="gigachat_version_light"
            )
            v2: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="⚡ GigaChatPRO", callback_data="gigachat_version_pro"
            )
            v3: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="🔙 Main", callback_data="back_on_main"
            )
            markup.row(v1).row(v2).row(v3)

        elif result[0] is False:
            v1: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="💡 GigaChatLight", callback_data="gigachat_version_light"
            )
            v2: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="⚡ GigaChatPRO", callback_data="get_or_lk_plus"
            )
            v3: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text="🔙 Main", callback_data="back_on_main"
            )
            markup.row(v1).row(v2).row(v3)

        return markup

    @staticmethod
    def get_menu_user_tickets() -> types.InlineKeyboardMarkup:
        """
        Markup-button (Inline) of the Bot Menu
        for the user in "TICKETS".

        :return: Markup-buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
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
        markup.row(var1).row(var2).row(var3).row(var4).row(var5)
        return markup

    @staticmethod
    def get_menu_user_tickets_again() -> types.InlineKeyboardMarkup:
        """
        Markup-button (Inline) of the Bot AGAIN-Menu
        for the user in "TICKETS".

        :return: Markup-buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Tickets Menu", callback_data="explore_user_tickets_menu"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💭 Send a new ticket", callback_data="send_new_ticket"
        )
        markup.row(var1).row(var2)
        return markup

    @staticmethod
    def get_user_tickets(username) -> tuple:
        """
        Markup-button (Inline) of the Bot
        for the user's history of "TICKETS".

        :param username: User's name -- username.

        :return: Tuple with data.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        response: str = ""

        result = HandlerDB.get_ticket_data(username, markup)
        if type(result) is types.InlineKeyboardMarkup:
            markup: types.InlineKeyboardMarkup = result
        elif type(result) is str:
            response = result

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Tickets Menu", callback_data="explore_user_tickets_menu"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🗣 Answer to the admin", callback_data="explore_answer_to_admin"
        )
        markup.row(var1).row(var2)

        results: tuple = (response, markup)
        return results

    @staticmethod
    def get_menu_admin() -> types.InlineKeyboardMarkup:
        """
        Markup-button (Inline) of the Bot Menu
        for admin.

        :return: Markup-buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✨ Kandinsky AI | Generate IMG 🖼", callback_data="kandinsky_generate"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="👑 MY PLUS ➕", callback_data="get_or_lk_plus"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🧠 AI Assistance", callback_data="ai_assistance_request"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="📨 Show tickets", callback_data="explore_admin_show_tickets_menu"
        )
        var5: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✉ Show the ticket by ID", callback_data="explore_show_ticket_by_id"
        )
        var6: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🗣 Answer to the user", callback_data="explore_answer_to_user"
        )
        var7: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="📈 Analytic", callback_data="analytic_data"
        )
        var8: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🧑‍💼 Business Handler", callback_data="business_handler"
        )
        var9: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔃 Refund 💸", callback_data="start_refund"
        )
        var10: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💱 PROMO 📲", callback_data="show_menu_promo_admin"
        )
        markup.row(var1).row(var2).row(var3).row(var4).row(var5).row(var6).row(var7).row(var8).row(var9).row(var10)
        return markup

    @staticmethod
    def get_users_tickets_for_admin() -> tuple:
        """
        Markup-button (Inline) of the Bot
        for the admin history of "TICKETS" of the users.

        :return: tuple of the tickets and Markup-buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        response: str = ""

        result = HandlerDB.get_users_tickets_for_admin()
        if type(result) is types.InlineKeyboardMarkup:
            markup: types.InlineKeyboardMarkup = result
        elif type(result) is str:
            response = result

        var: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )
        markup.row(var)

        results: tuple = (response, markup)
        return results

    @staticmethod
    def get_menu_business_handler() -> types.InlineKeyboardMarkup:
        """
        Get menu of business handler.

        :return: Markup Buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

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
            text="🔙 Main Menu", callback_data="back_on_main"
        )

        markup.row(var1).row(var2).row(var3).row(var4)

        return markup

    @staticmethod
    def get_menu_business_handler_thanks() -> types.InlineKeyboardMarkup:
        """
        Get menu of business handler - ThanksCommandAnswer.

        :return: Markup Buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

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
            text="🔙 Main Menu", callback_data="back_on_main"
        )

        markup.row(var1).row(var2).row(var3).row(var4)

        return markup

    @staticmethod
    def get_menu_business_handler_congratulation() -> types.InlineKeyboardMarkup:
        """
        Get menu of business handler - CongratulationCommandAnswer.

        :return: Markup Buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

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
            text="🔙 Main Menu", callback_data="back_on_main"
        )

        markup.row(var1).row(var2).row(var3).row(var4)

        return markup

    @staticmethod
    def get_menu_business_handler_problem_with_bot() -> types.InlineKeyboardMarkup:
        """
        Get menu of business handler - ProblemWithBotCommandAnswer.

        :return: Markup Buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

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
            text="🔙 Main Menu", callback_data="back_on_main"
        )

        markup.row(var1).row(var2).row(var3).row(var4)

        return markup

    @staticmethod
    def say_thanks() -> types.InlineKeyboardMarkup:
        """
        Markup-button (Inline) of the Bot thanks.

        :return: Markup-button.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        var: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Say: Thank you! 💖", callback_data="say_thanks"
        )
        markup.row(var)
        return markup

    @staticmethod
    def sure_refund() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for 'sure' refund by admin.

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ I'm sure", callback_data="refund"
        )
        btn2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel", callback_data="back_on_main"
        )

        markup.row(btn1).row(btn2)
        return markup

    @staticmethod
    def sure_refund_confirmation() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for 'sure' refund by admin | Confirmation.

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ I'm sure 100%", callback_data="refund_confirmation"
        )
        btn2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel", callback_data="back_on_main"
        )

        markup.row(btn1).row(btn2)
        return markup

    @staticmethod
    def sure_emergency_refund_confirmation() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for 'sure' emergency refund by admin | Confirmation.

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ Emergency Refund | I'm sure!", callback_data="emergency_refund_confirmation"
        )
        btn2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel", callback_data="back_on_main"
        )

        markup.row(btn1).row(btn2)
        return markup

    @staticmethod
    def sure_apply_promo() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for 'sure' apply a promo code by user.

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ Yes, apply it. I'm sure 100%", callback_data="apply_promo"
        )
        btn2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel", callback_data="back_on_main"
        )

        markup.row(btn1).row(btn2)
        return markup

    @staticmethod
    def sure_add_new_promo() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for 'sure' add a promo code by ADMIN | Admin control.

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ Yes, add! I'm sure.", callback_data="add_new_promo_confirmation"
        )
        btn2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel", callback_data="show_menu_promo_admin"
        )

        markup.row(btn1).row(btn2)
        return markup

    @staticmethod
    def sure_delete_promo() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for 'sure' delete a promo code by ADMIN | Admin control.

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ Yes, delete! I'm sure 100%.", callback_data="delete_promo_confirmation"
        )
        btn2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel", callback_data="show_menu_promo_admin"
        )

        markup.row(btn1).row(btn2)
        return markup

    @staticmethod
    def try_again_add_new_promo_or_back_on_main() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for attempt add a new promo data or return in PROMO Menu.

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔄 Try again", callback_data="try_again_add_new_promo"
        )

        btn2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Back", callback_data="show_menu_promo_admin"
        )

        markup.row(btn1).row(btn2)
        return markup

    @staticmethod
    def try_again_delete_promo_or_back_on_main() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for attempt delete a promo data or return in PROMO Menu.

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔄 Try again", callback_data="try_again_delete_promo"
        )

        btn2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Back", callback_data="show_menu_promo_admin"
        )

        markup.row(btn1).row(btn2)
        return markup

    @staticmethod
    def back_in_promo_menu() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for return in PROMO menu.

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        btn: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Back", callback_data="show_menu_promo_admin"
        )

        markup.row(btn)
        return markup

    @staticmethod
    def get_menu_without_plus() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for main-menu for users without PLUS.

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✨ Kandinsky AI | Generate IMG 🖼", callback_data="kandinsky_generate"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🧠 AI Assistance", callback_data="ai_assistance_request"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Get PLUS 🔥", callback_data="get_or_lk_plus"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❔ Help | CWR.SU", url="https://cwr.su/"
        )
        var5: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❓ Help | Tickets SYSTEM", callback_data="explore_user_tickets_menu"
        )
        markup.row(var1).row(var2).row(var3).row(var4).row(var5)
        return markup

    @staticmethod
    def get_menu_with_plus() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for main-menu for users with PLUS.

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✨ Kandinsky AI | Generate IMG 🖼", callback_data="kandinsky_generate"
        )
        btn2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🧠 AI Assistance", callback_data="ai_assistance_request"
        )
        btn3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="👑 MY PLUS ➕", callback_data="get_or_lk_plus"
        )
        btn4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❔ Help | CWR.SU", url="https://cwr.su/"
        )
        btn5: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❓ Help | Tickets SYSTEM", callback_data="explore_user_tickets_menu"
        )

        markup.row(btn1).row(btn2).row(btn3).row(btn4).row(btn5)
        return markup

    @staticmethod
    def get_menu_admin_promos() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for main-menu for admin.

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🎫 Add a new PROMO data", callback_data="add_new_promo"
        )
        btn2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Show PROMO datas 🌐", callback_data="show_promo_datas"
        )
        btn3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🗑️ Delete a PROMO data", callback_data="delete_promo_data"
        )
        btn4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Back", callback_data="back_on_main"
        )

        markup.row(btn1).row(btn2).row(btn3).row(btn4)
        return markup

    @staticmethod
    def generate_image() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for generate image by GigaChat | V3 | For plus-user.

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✅ I'm sure", callback_data="generate"
        )
        btn2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❌ Cancel", callback_data="back_on_main"
        )

        markup.row(btn1).row(btn2)
        return markup

    @staticmethod
    def get_plus() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for get status plus-user and get PLUS.

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Get PLUS 💥 | -55%", callback_data="continue_subscribe_plus"
        )
        btn2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="I have a promo code 🎫", callback_data="continue_subscribe_plus_with_promo"
        )

        markup.row(btn1).row(btn2)
        return markup

    @staticmethod
    def back_on_main() -> types.InlineKeyboardMarkup:
        """
        Get markup-keyboard for return in main menu (on main).

        :return: Markup.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        btn: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main", callback_data="back_on_main"
        )

        markup.row(btn)
        return markup


