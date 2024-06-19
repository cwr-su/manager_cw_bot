"""
Module of the business handler.
"""
<<<<<<< HEAD
import telebot
import json
=======
import json

import telebot
>>>>>>> f20ff53 (Updated data manager)
from telebot import types

from manager_cw_bot_api.buttons import Buttons


class BusinessHandler:
    """
    Class of the business handler for admin.
    """
    message: types.Message = None

    def __init__(self, bot, call_query) -> None:
        self.__bot: telebot.TeleBot = bot
        self.__call_query: types.CallbackQuery = call_query

        self.__bot.register_callback_query_handler(
            callback=self.__handler_thanks_from_users,
            func=lambda call: call.data == "handler_thanks_from_users"
        )
        self.__bot.register_callback_query_handler(
            callback=self.__handler_congratulation_from_users,
            func=lambda call: call.data == "handler_congratulation_from_users"
        )
        self.__bot.register_callback_query_handler(
            callback=self.__handler_problem_with_bot_from_users,
            func=lambda call: call.data == "handler_problem_with_bot_from_users"
        )

    def run(self) -> None:
        """
        Run-func for the class.
        """
        self.__bot.edit_message_text(
            chat_id=self.__call_query.message.chat.id,
            text=f"{self.__call_query.from_user.first_name}, you can manage your bot here. "
                 f"You should know:\n  1. <b>Now</b> available only 3 type of message (you can "
                 f"see that below).\n  2. <b>Don't use the bot like spam-bot</b> otherwise "
                 f"we'll ban you!\n\n<i>Thanks for understanding!\n       - Developer of the "
                 f"bot</i>",
            message_id=self.__call_query.message.message_id,
            reply_markup=Buttons.get_menu_business_handler(),
            parse_mode="HTML"
        )

    def __handler_thanks_from_users(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (call-query) for admin (with business).

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"Please, select below:",
            message_id=call_query.message.message_id,
            reply_markup=Buttons.get_menu_business_handler_thanks()
        )

        thanks: Thanks = Thanks(self.__bot)

        self.__bot.register_callback_query_handler(
            callback=thanks.only_text_for_thanks_hdl,
            func=lambda call: call.data == "only_text_for_thanks_hdl"
        )
        self.__bot.register_callback_query_handler(
            callback=thanks.only_sticker_for_thanks_hdl,
            func=lambda call: call.data == "only_sticker_for_thanks_hdl"
        )
        self.__bot.register_callback_query_handler(
            callback=thanks.message_and_sticker_for_thanks_hdl,
            func=lambda call: call.data == "message_and_sticker_for_thanks_hdl"
        )

    def __handler_congratulation_from_users(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (call-query) for admin (with business).

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"Please, select below:",
            message_id=call_query.message.message_id,
            reply_markup=Buttons.get_menu_business_handler_congratulation()
        )

        congratulation: Congratulation = Congratulation(self.__bot)

        self.__bot.register_callback_query_handler(
            callback=congratulation.only_text_for_congratulation_hdl,
            func=lambda call: call.data == "only_text_for_congratulation_hdl"
        )
        self.__bot.register_callback_query_handler(
            callback=congratulation.only_sticker_for_congratulation_hdl,
            func=lambda call: call.data == "only_sticker_for_congratulation_hdl"
        )
        self.__bot.register_callback_query_handler(
            callback=congratulation.message_and_sticker_for_congratulation_hdl,
            func=lambda call: call.data == "message_and_sticker_for_congratulation_hdl"
        )

    def __handler_problem_with_bot_from_users(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (call-query) for admin (with business).

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"Please, select below:",
            message_id=call_query.message.message_id,
            reply_markup=Buttons.get_menu_business_handler_problem_with_bot()
        )

        problem_with_bot: ProblemWithBot = ProblemWithBot(self.__bot)

        self.__bot.register_callback_query_handler(
            callback=problem_with_bot.only_text_for_problem_with_bot_hdl,
            func=lambda call: call.data == "only_text_for_problem_with_bot_hdl"
        )
        self.__bot.register_callback_query_handler(
            callback=problem_with_bot.only_sticker_for_problem_with_bot_hdl,
            func=lambda call: call.data == "only_sticker_for_problem_with_bot_hdl"
        )
        self.__bot.register_callback_query_handler(
            callback=problem_with_bot.message_and_sticker_for_problem_with_bot_hdl,
            func=lambda call: call.data == "message_and_sticker_for_problem_with_bot_hdl"
        )


class Thanks:
    """
    Class of the Thanks-command for the manager bot.
    """
    message: types.Message = None

    def __init__(self, bot: telebot.TeleBot) -> None:
        self.__bot: telebot.TeleBot = bot

    def only_text_for_thanks_hdl(self, call_query: types.CallbackQuery) -> None:
        """
        Handler function of manage THANKS-command by only text.

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"Please, write your message (only text!)",
            message_id=call_query.message.message_id
        )
        self.__bot.register_next_step_handler(
            call_query.message,
            self.__manage_thanks_from_users_only_text
        )

    def only_sticker_for_thanks_hdl(self, call_query: types.CallbackQuery) -> None:
        """
        Handler function of manage THANKS-command by only sticker.

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"Please, send a sticker (only sticker!)",
            message_id=call_query.message.message_id
        )
        self.__bot.register_next_step_handler(
            call_query.message,
            self.__manage_thanks_from_users_only_sticker
        )

    def message_and_sticker_for_thanks_hdl(self, call_query: types.CallbackQuery) -> None:
        """
        Handler function of manage THANKS-command by text and sticker. Step 1.
        Get call-query.

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"Please, write your message now (only text!)",
            message_id=call_query.message.message_id
        )
        self.__bot.register_next_step_handler(
            call_query.message,
            self.__message_and_sticker_for_thanks_hdl_step2
        )

    def __message_and_sticker_for_thanks_hdl_step2(self, message: types.Message) -> None:
        """
        Handler function of manage THANKS-command by text and sticker. Step 2.
        Get message.

        :param message: Message - text.
        :return: None.
        """
        if message.content_type == "text":
            self.__class__.message = message
            self.__bot.send_message(
                chat_id=message.chat.id,
                text=f"Please, send a sticker (only sticker!)",
            )
            self.__bot.register_next_step_handler(
                message,
                self.__manage_thanks_from_users_text_and_sticker
            )
        else:
            self.__bot.send_message(
                chat_id=message.chat.id,
                text=f"❌ FAIL! It's not TEXT-type! Please, try again (or repeat later)",
<<<<<<< HEAD
                reply_markup=Buttons.get_menu_on_back_or_main()
=======
                reply_markup=Buttons.back_on_main()
>>>>>>> f20ff53 (Updated data manager)
            )

    def __manage_thanks_from_users_only_text(self, message: types.Message) -> None:
        """
        Manage THANKS-command by only text. Edit configurate-file by user settings.

        :param message: Message of the user.
        :return: None.
        """
        if message.content_type == 'text':
            with open("bot.json", "r", encoding='utf-8') as file:
                data: dict = json.load(file)

            data["BUSINESS_HANDLER"]["THANKS"]["THANKS_STICKER"] = "NONE"
            data["BUSINESS_HANDLER"]["THANKS"]["THANKS_TEXT"]["MSG"] = message.text
            if message.entities:
                data["BUSINESS_HANDLER"]["THANKS"]["THANKS_TEXT"]["OFFSET"] = (message.entities[0].
                                                                               offset)
                data["BUSINESS_HANDLER"]["THANKS"]["THANKS_TEXT"]["LENGTH"] = (message.entities[0].
                                                                               length)
                data["BUSINESS_HANDLER"]["THANKS"]["THANKS_TEXT"]["C_E_ID"] = (message.entities[0].
                                                                               custom_emoji_id)

            with open("bot.json", "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
<<<<<<< HEAD
                reply_markup=Buttons.get_menu_on_back_or_main()
=======
                reply_markup=Buttons.back_on_main()
>>>>>>> f20ff53 (Updated data manager)
            )

        else:
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )

    def __manage_thanks_from_users_only_sticker(self, message: types.Message) -> None:
        """
        Manage THANKS-command by only sticker. Edit configurate-file by user settings.

        :param message: Message of the user.
        :return: None.
        """
        if message.content_type == 'sticker':
            with open("bot.json", "r", encoding='utf-8') as file:
                data: dict = json.load(file)

            data["BUSINESS_HANDLER"]["THANKS"]["THANKS_STICKER"] = message.sticker.file_id
            data["BUSINESS_HANDLER"]["THANKS"]["THANKS_TEXT"]["MSG"] = "NONE"
            data["BUSINESS_HANDLER"]["THANKS"]["THANKS_TEXT"]["OFFSET"] = "NONE"
            data["BUSINESS_HANDLER"]["THANKS"]["THANKS_TEXT"]["LENGTH"] = "NONE"
            data["BUSINESS_HANDLER"]["THANKS"]["THANKS_TEXT"]["C_E_ID"] = "NONE"

            with open("bot.json", "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
<<<<<<< HEAD
                reply_markup=Buttons.get_menu_on_back_or_main()
=======
                reply_markup=Buttons.back_on_main()
>>>>>>> f20ff53 (Updated data manager)
            )

        else:
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )

    def __manage_thanks_from_users_text_and_sticker(self, message: types.Message) -> None:
        """
        Manage THANKS-command by text and sticker. Edit configurate-file by user settings.

        :param message: Message of the user.
        :return: None.
        """
        if message.content_type == 'sticker':
            with open("bot.json", "r", encoding='utf-8') as file:
                data: dict = json.load(file)

            print(self.__class__.message)
            print(message.sticker)
            print(message)
            print(message.sticker.file_id)

            data["BUSINESS_HANDLER"]["THANKS"]["THANKS_STICKER"] = message.sticker.file_id
            data["BUSINESS_HANDLER"]["THANKS"]["THANKS_TEXT"]["MSG"] = self.__class__.message.text
            if self.__class__.message.entities:
                data["BUSINESS_HANDLER"]["THANKS"]["THANKS_TEXT"]["OFFSET"] = (
                    self.__class__.message.entities[0].offset
                )
                data["BUSINESS_HANDLER"]["THANKS"]["THANKS_TEXT"]["LENGTH"] = (
                    self.__class__.message.entities[0].length
                )
                data["BUSINESS_HANDLER"]["THANKS"]["THANKS_TEXT"]["C_E_ID"] = (
                    self.__class__.message.entities[0].custom_emoji_id
                )

            with open("bot.json", "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
<<<<<<< HEAD
                reply_markup=Buttons.get_menu_on_back_or_main()
=======
                reply_markup=Buttons.back_on_main()
>>>>>>> f20ff53 (Updated data manager)
            )

        else:
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )


class Congratulation:
    """
    Class of the Congratulation-command for the manager bot.
    """
    message: types.Message = None

    def __init__(self, bot: telebot.TeleBot) -> None:
        self.__bot: telebot.TeleBot = bot

    def only_text_for_congratulation_hdl(self, call_query: types.CallbackQuery) -> None:
        """
        Handler function of manage CONGRATULATION-command by only text.

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"Please, write your message (only text!)",
            message_id=call_query.message.message_id
        )
        self.__bot.register_next_step_handler(
            call_query.message,
            self.__manage_congratulation_from_users_only_text
        )

    def only_sticker_for_congratulation_hdl(self, call_query: types.CallbackQuery) -> None:
        """
        Handler function of manage CONGRATULATION-command by only sticker.

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"Please, send a sticker (only sticker!)",
            message_id=call_query.message.message_id
        )
        self.__bot.register_next_step_handler(
            call_query.message,
            self.__manage_congratulation_from_users_only_sticker
        )

    def message_and_sticker_for_congratulation_hdl(self, call_query: types.CallbackQuery) -> None:
        """
        Handler function of manage CONGRATULATION-command by text and sticker. Step 1.
        Get call-query.

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"Please, write your message now (only text!)",
            message_id=call_query.message.message_id
        )
        self.__bot.register_next_step_handler(
            call_query.message,
            self.__message_and_sticker_for_congratulation_hdl_step2
        )

    def __message_and_sticker_for_congratulation_hdl_step2(self, message: types.Message) -> None:
        """
        Handler function of manage THANKS-command by text and sticker. Step 2.
        Get message.

        :param message: Message - text.
        :return: None.
        """
        if message.content_type == "text":
            self.__class__.message = message
            self.__bot.send_message(
                chat_id=message.chat.id,
                text=f"Please, send a sticker (only sticker!)",
            )
            self.__bot.register_next_step_handler(
                message,
                self.__manage_congratulation_from_users_text_and_sticker
            )
        else:
            self.__bot.send_message(
                chat_id=message.chat.id,
                text=f"❌ FAIL! It's not TEXT-type! Please, try again (or repeat later)",
<<<<<<< HEAD
                reply_markup=Buttons.get_menu_on_back_or_main()
=======
                reply_markup=Buttons.back_on_main()
>>>>>>> f20ff53 (Updated data manager)
            )

    def __manage_congratulation_from_users_only_text(self, message: types.Message) -> None:
        """
        Manage CONGRATULATION-command by only text. Edit configurate-file by user settings.

        :param message: Message of the user.
        :return: None.
        """
        if message.content_type == 'text':
            with open("bot.json", "r", encoding='utf-8') as file:
                data: dict = json.load(file)

            data["BUSINESS_HANDLER"]["CONGRATULATION"]["CONGRATULATION_STICKER"] = "NONE"
            data["BUSINESS_HANDLER"]["CONGRATULATION"]["CONGRATULATION_TEXT"]["MSG"] = message.text
            if message.entities:
                data["BUSINESS_HANDLER"]["CONGRATULATION"]["CONGRATULATION_TEXT"]["OFFSET"] = \
                    message.entities[0].offset
                data["BUSINESS_HANDLER"]["CONGRATULATION"]["CONGRATULATION_TEXT"]["LENGTH"] = \
                    message.entities[0].length
                data["BUSINESS_HANDLER"]["CONGRATULATION"]["CONGRATULATION_TEXT"]["C_E_ID"] = (
                    message.entities[0].
                    custom_emoji_id)

            with open("bot.json", "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
<<<<<<< HEAD
                reply_markup=Buttons.get_menu_on_back_or_main()
=======
                reply_markup=Buttons.back_on_main()
>>>>>>> f20ff53 (Updated data manager)
            )

        else:
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )

    def __manage_congratulation_from_users_only_sticker(self, message: types.Message) -> None:
        """
        Manage THANKS-command by only sticker. Edit configurate-file by user settings.

        :param message: Message of the user.
        :return: None.
        """
        if message.content_type == 'sticker':
            with open("bot.json", "r", encoding='utf-8') as file:
                data: dict = json.load(file)

            data["BUSINESS_HANDLER"]["CONGRATULATION"][
                "CONGRATULATION_STICKER"] = message.sticker.file_id
            data["BUSINESS_HANDLER"]["CONGRATULATION"]["CONGRATULATION_TEXT"]["MSG"] = "NONE"
            data["BUSINESS_HANDLER"]["CONGRATULATION"]["CONGRATULATION_TEXT"]["OFFSET"] = "NONE"
            data["BUSINESS_HANDLER"]["CONGRATULATION"]["CONGRATULATION_TEXT"]["LENGTH"] = "NONE"
            data["BUSINESS_HANDLER"]["CONGRATULATION"]["CONGRATULATION_TEXT"]["C_E_ID"] = "NONE"

            with open("bot.json", "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
<<<<<<< HEAD
                reply_markup=Buttons.get_menu_on_back_or_main()
=======
                reply_markup=Buttons.back_on_main()
>>>>>>> f20ff53 (Updated data manager)
            )

        else:
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )

    def __manage_congratulation_from_users_text_and_sticker(self, message: types.Message) -> None:
        """
        Manage THANKS-command text and sticker. Edit configurate-file by user settings.

        :param message: Message of the user.
        :return: None.
        """
        if message.content_type == 'sticker':
            with open("bot.json", "r", encoding='utf-8') as file:
                data: dict = json.load(file)

            data["BUSINESS_HANDLER"]["CONGRATULATION"][
                "CONGRATULATION_STICKER"] = message.sticker.file_id
            data["BUSINESS_HANDLER"]["CONGRATULATION"]["CONGRATULATION_TEXT"][
                "MSG"] = self.__class__.message.text
            if self.__class__.message.entities:
                data["BUSINESS_HANDLER"]["CONGRATULATION"]["CONGRATULATION_TEXT"]["OFFSET"] = (
                    self.__class__.message.entities[0].offset
                )
                data["BUSINESS_HANDLER"]["CONGRATULATION"]["CONGRATULATION_TEXT"]["LENGTH"] = (
                    self.__class__.message.entities[0].length
                )
                data["BUSINESS_HANDLER"]["CONGRATULATION"]["CONGRATULATION_TEXT"]["C_E_ID"] = (
                    self.__class__.message.entities[0].custom_emoji_id
                )

            with open("bot.json", "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
<<<<<<< HEAD
                reply_markup=Buttons.get_menu_on_back_or_main()
=======
                reply_markup=Buttons.back_on_main()
>>>>>>> f20ff53 (Updated data manager)
            )

        else:
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )


class ProblemWithBot:
    """
    Class of the ProblemWithBot-command for the manager bot.
    """
    message: types.Message = None

    def __init__(self, bot: telebot.TeleBot) -> None:
        self.__bot: telebot.TeleBot = bot

    def only_text_for_problem_with_bot_hdl(self, call_query: types.CallbackQuery) -> None:
        """
        Handler function of manage ProblemWithBot-command by only text.

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"Please, write your message (only text!)",
            message_id=call_query.message.message_id
        )
        self.__bot.register_next_step_handler(
            call_query.message,
            self.__manage_problem_with_bot_from_users_only_text
        )

    def only_sticker_for_problem_with_bot_hdl(self, call_query: types.CallbackQuery) -> None:
        """
        Handler function of manage ProblemWithBot-command by only sticker.

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"Please, send a sticker (only sticker!)",
            message_id=call_query.message.message_id
        )
        self.__bot.register_next_step_handler(
            call_query.message,
            self.__manage_problem_with_bot_from_users_only_sticker
        )

    def message_and_sticker_for_problem_with_bot_hdl(self, call_query: types.CallbackQuery) -> None:
        """
        Handler function of manage ProblemWithBot-command by text and sticker. Step 1.
        Get call-query.

        :param call_query: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"Please, write your message now (only text!)",
            message_id=call_query.message.message_id
        )
        self.__bot.register_next_step_handler(
            call_query.message,
            self.__message_and_sticker_for_problem_with_bot_hdl_step2
        )

    def __message_and_sticker_for_problem_with_bot_hdl_step2(self, message: types.Message) -> None:
        """
        Handler function of manage THANKS-command by text and sticker. Step 2.
        Get message.

        :param message: Message - text.
        :return: None.
        """
        if message.content_type == "text":
            self.__class__.message = message
            self.__bot.send_message(
                chat_id=message.chat.id,
                text=f"Please, send a sticker (only sticker!)",
            )
            self.__bot.register_next_step_handler(
                message,
                self.__manage_problem_with_bot_from_users_text_and_sticker
            )
        else:
            self.__bot.send_message(
                chat_id=message.chat.id,
                text=f"❌ FAIL! It's not TEXT-type! Please, try again (or repeat later)",
<<<<<<< HEAD
                reply_markup=Buttons.get_menu_on_back_or_main()
=======
                reply_markup=Buttons.back_on_main()
>>>>>>> f20ff53 (Updated data manager)
            )

    def __manage_problem_with_bot_from_users_only_text(self, message: types.Message) -> None:
        """
        Manage ProblemWithBot-command by only text. Edit configurate-file by user settings.

        :param message: Message of the user.
        :return: None.
        """
        if message.content_type == "text":
            with open("bot.json", "r", encoding='utf-8') as file:
                data: dict = json.load(file)

            data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_STICKER"] = "NONE"
            data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"][
                "MSG"] = message.text

            if message.entities:
                data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"][
                    "OFFSET"] = message.entities[0].offset
                data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"][
                    "LENGTH"] = message.entities[0].length
                data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"][
                    "C_E_ID"] = message.entities[0].custom_emoji_id

            with open("bot.json", "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
<<<<<<< HEAD
                reply_markup=Buttons.get_menu_on_back_or_main()
=======
                reply_markup=Buttons.back_on_main()
>>>>>>> f20ff53 (Updated data manager)
            )

        else:
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )

    def __manage_problem_with_bot_from_users_only_sticker(self, message: types.Message) -> None:
        """
        Manage ProblemWithBot-command by only sticker. Edit configurate-file by user settings.

        :param message: Message of the user.
        :return: None.
        """
        if message.content_type == 'sticker':
            with open("bot.json", "r", encoding='utf-8') as file:
                data: dict = json.load(file)

            data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"][
                "PROBLEM_WITH_BOT_STICKER"] = message.sticker.file_id
            data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"]["MSG"] = "NONE"
            data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"]["OFFSET"] = "NONE"
            data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"]["LENGTH"] = "NONE"
            data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"]["C_E_ID"] = "NONE"

            with open("bot.json", "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
<<<<<<< HEAD
                reply_markup=Buttons.get_menu_on_back_or_main()
=======
                reply_markup=Buttons.back_on_main()
>>>>>>> f20ff53 (Updated data manager)
            )

        else:
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )

    def __manage_problem_with_bot_from_users_text_and_sticker(self, message: types.Message) -> None:
        """
        Manage THANKS-command text and sticker. Edit configurate-file by user settings.

        :param message: Message of the user.
        :return: None.
        """
        if message.content_type == 'sticker':
            with open("bot.json", "r", encoding='utf-8') as file:
                data: dict = json.load(file)

            data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"][
                "PROBLEM_WITH_BOT_STICKER"] = message.sticker.file_id
            data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"][
                "MSG"] = self.__class__.message.text
            if self.__class__.message.entities:
                data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"]["OFFSET"] = (
                    self.__class__.message.entities[0].offset
                )
                data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"]["LENGTH"] = (
                    self.__class__.message.entities[0].length
                )
                data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"]["C_E_ID"] = (
                    self.__class__.message.entities[0].custom_emoji_id
                )

            with open("bot.json", "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
<<<<<<< HEAD
                reply_markup=Buttons.get_menu_on_back_or_main()
=======
                reply_markup=Buttons.back_on_main()
>>>>>>> f20ff53 (Updated data manager)
            )

        else:
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )
