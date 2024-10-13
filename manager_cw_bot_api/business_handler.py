"""
Module of the business handler.
"""
import json
import logging

from aiogram import types, Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.fsm_handler import (
    BusinessHandlerThanksFunctions,
    BusinessHandlerCongratulationFunctions,
    BusinessHandlerProblemWithBotFunctions
)

router_business: Router = Router()


class BusinessHandler:
    """
    Class of the business handler for admin.
    """
    message: types.Message = None

    def __init__(
            self,
            bot,
            call_query
    ) -> None:
        self.__bot: Bot = bot
        self.__call_query: types.CallbackQuery = call_query

        router_business.callback_query.register(
            self.__handler_thanks_from_users,
            F.data == "handler_thanks_from_users"
        )
        router_business.callback_query.register(
            self.__handler_congratulation_from_users,
            F.data == "handler_congratulation_from_users"
        )
        router_business.callback_query.register(
            self.__handler_problem_with_bot_from_users,
            F.data == "handler_problem_with_bot_from_users"
        )

    async def run(self) -> None:
        """
        Run-func for the class.
        """
        var: InlineKeyboardBuilder = await Buttons.get_menu_business_handler()
        await self.__bot.edit_message_text(
            chat_id=self.__call_query.message.chat.id,
            text=f"🔥 <b>{self.__call_query.from_user.first_name}</b>, you can manage your bot "
                 f"here. You should know:\n  1. <b>Now</b> available only 3 type of message (you "
                 f"can see that below).\n  2. <b>Don't use the bot like spam-bot</b> otherwise "
                 f"we'll ban you!\n\n<i>Thanks for understanding!\n       - Developer of the "
                 f"bot</i>",
            message_id=self.__call_query.message.message_id,
            reply_markup=var.as_markup(),
            parse_mode="HTML"
        )

    async def __handler_thanks_from_users(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Handler (call-query) for admin (with business).

        :param call_query: Callback Query.
        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.get_menu_business_handler_thanks()
        await self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"👌🏻 Please, select below:",
            message_id=call_query.message.message_id,
            reply_markup=var.as_markup()
        )

        thanks: Thanks = Thanks(self.__bot)

        router_business.callback_query.register(
            thanks.only_text_for_thanks_hdl,
            F.data == "only_text_for_thanks_hdl"
        )
        router_business.callback_query.register(
            thanks.only_sticker_for_thanks_hdl,
            F.data == "only_sticker_for_thanks_hdl"
        )
        router_business.callback_query.register(
            thanks.message_and_sticker_for_thanks_hdl,
            F.data == "message_and_sticker_for_thanks_hdl"
        )

    async def __handler_congratulation_from_users(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Handler (call-query) for admin (with business).

        :param call_query: Callback Query.
        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.get_menu_business_handler_congratulation()
        await self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"👌🏻 Please, select below:",
            message_id=call_query.message.message_id,
            reply_markup=var.as_markup()
        )

        congratulation: Congratulation = Congratulation(self.__bot)

        router_business.callback_query.register(
            congratulation.only_text_for_congratulation_hdl,
            F.data == "only_text_for_congratulation_hdl"
        )
        router_business.callback_query.register(
            congratulation.only_sticker_for_congratulation_hdl,
            F.data == "only_sticker_for_congratulation_hdl"
        )
        router_business.callback_query.register(
            congratulation.message_and_sticker_for_congratulation_hdl,
            F.data == "message_and_sticker_for_congratulation_hdl"
        )

    async def __handler_problem_with_bot_from_users(
            self,
            call_query: types.CallbackQuery
    ) -> None:
        """
        Handler (call-query) for admin (with business).

        :param call_query: Callback Query.
        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.get_menu_business_handler_problem_with_bot()
        await self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"👌🏻 Please, select below:",
            message_id=call_query.message.message_id,
            reply_markup=var.as_markup()
        )

        problem_with_bot: ProblemWithBot = ProblemWithBot(self.__bot)

        router_business.callback_query.register(
            problem_with_bot.only_text_for_problem_with_bot_hdl,
            F.data == "only_text_for_problem_with_bot_hdl"
        )
        router_business.callback_query.register(
            problem_with_bot.only_sticker_for_problem_with_bot_hdl,
            F.data == "only_sticker_for_problem_with_bot_hdl"
        )
        router_business.callback_query.register(
            problem_with_bot.message_and_sticker_for_problem_with_bot_hdl,
            F.data == "message_and_sticker_for_problem_with_bot_hdl"
        )


class Thanks:
    """
    Class of the Thanks-command for the manager bot.
    """
    message: types.Message = None

    def __init__(
            self,
            bot: Bot
    ) -> None:
        self.__bot: Bot = bot

        router_business.message.register(
            self.__manage_thanks_from_users_only_text,
            BusinessHandlerThanksFunctions.only_text
        )
        router_business.message.register(
            self.__manage_thanks_from_users_only_sticker,
            BusinessHandlerThanksFunctions.only_sticker
        )
        router_business.message.register(
            self.__message_and_sticker_for_thanks_hdl_step2,
            BusinessHandlerThanksFunctions.message_and_sticker_step1_message
        )
        router_business.message.register(
            self.__manage_thanks_from_users_text_and_sticker,
            BusinessHandlerThanksFunctions.message_and_sticker_step2_sticker
        )

    async def only_text_for_thanks_hdl(
            self,
            call_query: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Handler function of manage THANKS-command by only text.

        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(BusinessHandlerThanksFunctions.only_text)
        await self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"👌🏻 Please, write your message (only text!)",
            message_id=call_query.message.message_id
        )

    async def only_sticker_for_thanks_hdl(
            self,
            call_query: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Handler function of manage THANKS-command by only sticker.

        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(BusinessHandlerThanksFunctions.only_sticker)
        await self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"👌🏻 Please, send a sticker (only sticker!)",
            message_id=call_query.message.message_id
        )

    async def message_and_sticker_for_thanks_hdl(
            self,
            call_query: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Handler function of manage THANKS-command by text and sticker. Step 1.
        Get call-query.

        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(BusinessHandlerThanksFunctions.message_and_sticker_step1_message)
        await self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"👌🏻 Please, write your message now (only text!)",
            message_id=call_query.message.message_id
        )

    async def __message_and_sticker_for_thanks_hdl_step2(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Handler function of manage THANKS-command by text and sticker. Step 2.
        Get message.

        :param message: Message - text.
        :param state: FSM.

        :return: None.
        """
        if message.content_type == "text":
            await state.set_state(BusinessHandlerThanksFunctions.message_and_sticker_step2_sticker)

            self.__class__.message = message
            await self.__bot.send_message(
                chat_id=message.chat.id,
                text=f"👌🏻 Please, send a sticker (only sticker!)",
            )
        else:           
            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.send_message(
                chat_id=message.chat.id,
                text=f"❌ FAIL! It's not TEXT-type! Please, try again (or repeat later)",
                reply_markup=var.as_markup()
            )

    async def __manage_thanks_from_users_only_text(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Manage THANKS-command by only text. Edit configurate-file by user settings.

        :param message: Message of the user.
        :param state: FSM.

        :return: None.
        """
        await state.clear()
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

            logging.info(
                f"Successfully overwrote configuration file data from the business "
                f"response section"
            )

            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
                reply_markup=var.as_markup()
            )

        else:
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )

    async def __manage_thanks_from_users_only_sticker(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Manage THANKS-command by only sticker. Edit configurate-file by user settings.

        :param message: Message of the user.
        :return: None.
        """
        await state.clear()
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

            logging.info(
                f"Successfully overwrote configuration file data from the business "
                f"response section"
            )

            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
                reply_markup=var.as_markup()
            )

        else:
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )

    async def __manage_thanks_from_users_text_and_sticker(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Manage THANKS-command by text and sticker. Edit configurate-file by user settings.

        :param message: Message of the user.
        :return: None.
        """
        await state.clear()
        if message.content_type == 'sticker':
            with open("bot.json", "r", encoding='utf-8') as file:
                data: dict = json.load(file)

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

            logging.info(
                f"Successfully overwrote configuration file data from the business "
                f"response section"
            )

            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
                reply_markup=var.as_markup()
            )

        else:
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )


class Congratulation:
    """
    Class of the Congratulation-command for the manager bot.
    """
    message: types.Message = None

    def __init__(
            self,
            bot: Bot
    ) -> None:
        self.__bot: Bot = bot

        router_business.message.register(
            self.__manage_congratulation_from_users_only_text,
            BusinessHandlerCongratulationFunctions.only_text
        )
        router_business.message.register(
            self.__manage_congratulation_from_users_only_sticker,
            BusinessHandlerCongratulationFunctions.only_sticker
        )
        router_business.message.register(
            self.__message_and_sticker_for_congratulation_hdl_step2,
            BusinessHandlerCongratulationFunctions.message_and_sticker_step1_message
        )
        router_business.message.register(
            self.__manage_congratulation_from_users_text_and_sticker,
            BusinessHandlerCongratulationFunctions.message_and_sticker_step2_sticker
        )

    async def only_text_for_congratulation_hdl(
        self,
        call_query: types.CallbackQuery,
        state: FSMContext
    ) -> None:
        """
        Handler function of manage CONGRATULATION-command by only text.

        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(BusinessHandlerThanksFunctions.only_text)
        await self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"👌🏻 Please, write your message (only text!)",
            message_id=call_query.message.message_id
        )

    async def only_sticker_for_congratulation_hdl(
            self,
            call_query: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Handler function of manage CONGRATULATION-command by only sticker.

        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(BusinessHandlerThanksFunctions.only_sticker)
        await self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"👌🏻 Please, send a sticker (only sticker!)",
            message_id=call_query.message.message_id
        )

    async def message_and_sticker_for_congratulation_hdl(
            self,
            call_query: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Handler function of manage CONGRATULATION-command by text and sticker. Step 1.
        Get call-query.

        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(BusinessHandlerThanksFunctions.message_and_sticker_step1_message)
        await self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"👌🏻 Please, write your message now (only text!)",
            message_id=call_query.message.message_id
        )

    async def __message_and_sticker_for_congratulation_hdl_step2(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Handler function of manage THANKS-command by text and sticker. Step 2.
        Get message.

        :param message: Message - text.
        :param state: FSM.

        :return: None.
        """
        if message.content_type == "text":
            await state.set_state(
                BusinessHandlerThanksFunctions.message_and_sticker_step2_sticker
            )

            self.__class__.message = message
            await self.__bot.send_message(
                chat_id=message.chat.id,
                text=f"👌🏻 Please, send a sticker (only sticker!)",
            )
        else:           
            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.send_message(
                chat_id=message.chat.id,
                text=f"❌ FAIL! It's not TEXT-type! Please, try again (or repeat later)",
                reply_markup=var.as_markup()
            )

    async def __manage_congratulation_from_users_only_text(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Manage CONGRATULATION-command by only text. Edit configurate-file by user settings.

        :param message: Message of the user.
        :param state: FSM.

        :return: None.
        """
        await state.clear()
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

            logging.info(
                f"Successfully overwrote configuration file data from the business "
                f"response section"
            )

            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
                reply_markup=var.as_markup()
            )

        else:
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )

    async def __manage_congratulation_from_users_only_sticker(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Manage THANKS-command by only sticker. Edit configurate-file by user settings.

        :param message: Message of the user.
        :param state: FSM.

        :return: None.
        """
        await state.clear()
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

            logging.info(
                f"Successfully overwrote configuration file data from the business "
                f"response section"
            )

            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
                reply_markup=var.as_markup()
            )

        else:
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )

    async def __manage_congratulation_from_users_text_and_sticker(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Manage THANKS-command text and sticker. Edit configurate-file by user settings.

        :param message: Message of the user.
        :param state: FSM.

        :return: None.
        """
        await state.clear()
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

            logging.info(
                f"Successfully overwrote configuration file data from the business "
                f"response section"
            )

            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
                reply_markup=var.as_markup()
            )

        else:
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )


class ProblemWithBot:
    """
    Class of the ProblemWithBot-command for the manager bot.
    """
    message: types.Message = None

    def __init__(
            self,
            bot:
            Bot
    ) -> None:
        self.__bot: Bot = bot

        router_business.message.register(
            self.__manage_problem_with_bot_from_users_only_text,
            BusinessHandlerCongratulationFunctions.only_text
        )
        router_business.message.register(
            self.__manage_problem_with_bot_from_users_only_sticker,
            BusinessHandlerCongratulationFunctions.only_sticker
        )
        router_business.message.register(
            self.__message_and_sticker_for_problem_with_bot_hdl_step2,
            BusinessHandlerCongratulationFunctions.message_and_sticker_step1_message
        )
        router_business.message.register(
            self.__manage_problem_with_bot_from_users_text_and_sticker,
            BusinessHandlerCongratulationFunctions.message_and_sticker_step2_sticker
        )

    async def only_text_for_problem_with_bot_hdl(
            self,
            call_query: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Handler function of manage ProblemWithBot-command by only text.

        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(BusinessHandlerProblemWithBotFunctions.only_text)
        await self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"👌🏻 Please, write your message (only text!)",
            message_id=call_query.message.message_id
        )

    async def only_sticker_for_problem_with_bot_hdl(
            self,
            call_query: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Handler function of manage ProblemWithBot-command by only sticker.

        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(BusinessHandlerProblemWithBotFunctions.only_sticker)
        await self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"👌🏻 Please, send a sticker (only sticker!)",
            message_id=call_query.message.message_id
        )

    async def message_and_sticker_for_problem_with_bot_hdl(
            self,
            call_query: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Handler function of manage ProblemWithBot-command by text and sticker. Step 1.
        Get call-query.

        :param call_query: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(
            BusinessHandlerProblemWithBotFunctions.message_and_sticker_step1_message
        )
        await self.__bot.edit_message_text(
            chat_id=call_query.message.chat.id,
            text=f"👌🏻 Please, write your message now (only text!)",
            message_id=call_query.message.message_id
        )

    async def __message_and_sticker_for_problem_with_bot_hdl_step2(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Handler function of manage THANKS-command by text and sticker. Step 2.
        Get message.

        :param message: Message - text.
        :param state: FSM.

        :return: None.
        """
        if message.content_type == "text":
            await state.set_state(
                BusinessHandlerProblemWithBotFunctions.message_and_sticker_step2_sticker
            )

            self.__class__.message = message
            await self.__bot.send_message(
                chat_id=message.chat.id,
                text=f"Please, send a sticker (only sticker!)",
            )
        else:           
            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.send_message(
                chat_id=message.chat.id,
                text=f"❌ FAIL! It's not TEXT-type! Please, try again (or repeat later)",
                reply_markup=var.as_markup()
            )

    async def __manage_problem_with_bot_from_users_only_text(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Manage ProblemWithBot-command by only text. Edit configurate-file by user settings.

        :param message: Message of the user.
        :param state: FSM.

        :return: None.
        """
        await state.clear()
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

            logging.info(
                f"Successfully overwrote configuration file data from the business "
                f"response section"
            )

            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
                reply_markup=var.as_markup()
            )

        else:
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )

    async def __manage_problem_with_bot_from_users_only_sticker(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Manage ProblemWithBot-command by only sticker. Edit configurate-file by user settings.

        :param message: Message of the user.
        :param state: FSM.

        :return: None.
        """
        await state.clear()
        if message.content_type == 'sticker':
            with open("bot.json", "r", encoding='utf-8') as file:
                data: dict = json.load(file)

            data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"][
                "PROBLEM_WITH_BOT_STICKER"] = \
                message.sticker.file_id
            data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"]["MSG"] = \
                "NONE"
            data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"]["OFFSET"] = \
                "NONE"
            data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"]["LENGTH"] = \
                "NONE"
            data["BUSINESS_HANDLER"]["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"]["C_E_ID"] = \
                "NONE"

            with open("bot.json", "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            logging.info(
                f"Successfully overwrote configuration file data from the business "
                f"response section"
            )

            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
                reply_markup=var.as_markup()
            )

        else:
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )

    async def __manage_problem_with_bot_from_users_text_and_sticker(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Manage THANKS-command text and sticker. Edit configurate-file by user settings.

        :param message: Message of the user.
        :param state: FSM.

        :return: None.
        """
        await state.clear()
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

            logging.info(
                f"Successfully overwrote configuration file data from the business "
                f"response section"
            )

            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="✅ SUCCESSFUL! The data updated!",
                reply_markup=var.as_markup()
            )

        else:
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, but this type of message not available!"
            )
