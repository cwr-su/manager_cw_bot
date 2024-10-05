"""Module for handler operations of EMail-DB."""
import json
import re
import random

from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.fsm_handler import ProcessEditingEmailAfterConfirmation, ProcessAddNewEmail, \
    ProcessEnterTheCodeForAddNewEMailForVerifyEmail
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB
from manager_cw_bot_api.handler_email_sender import SenderEmail

router_handler_em: Router = Router()


class HandlerEM:
    """Class for manage EMail (add / delete / edit)."""
    __email: str = ""

    def __init__(
            self,
            bot: Bot,
            admin_id: int
    ):
        self.__bot: Bot = bot
        self.__admin_id: int = admin_id

        router_handler_em.message.register(
            self.__editing_email_process_step_after_confirmation,
            ProcessEditingEmailAfterConfirmation.new_email
        )
        router_handler_em.message.register(
            self.__add_new_email_to_db,
            ProcessAddNewEmail.new_email
        )
        router_handler_em.message.register(
            self.__add_new_email_to_db_enter_the_code,
            ProcessEnterTheCodeForAddNewEMailForVerifyEmail.code
        )

    @staticmethod
    async def valid_email(email: str) -> bool:
        """
        Valid EMail.

        :param email: EMail for valid.
        :return: Result.
        """
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, email):
            return True
        else:
            return False

    async def __generate_code(self) -> str:
        """Func for generate temp code for verification email (user / admin)."""
        lst = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'b', 'a', 'q']
        result: str = ""
        for _ in range(7):
            result += lst[random.randint(0, 12)]

        router_handler_em.callback_query.register(
            self.__add_new_email_to_db,
            F.data == "check_verify_code_again"
        )
        return result

    async def __get_data_email(self, id_user) -> str:
        """
        Get EMail.

        :param id_user: User ID.
        :return: None.
        """
        if id_user != self.__admin_id:
            res: tuple = await HandlerDB.get_email_data(id_user)
            email: str = res[1][0]
        else:
            res: dict = await SenderEmail.get_email_data_admin()
            email: str = res["ADMIN_EMAIL"]

        return email

    async def show_email_settings_menu(self, call: types.CallbackQuery) -> None:
        """
        Show EMail settings menu.

        :param call: Callback Query.

        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.get_menu_email_settings(call.from_user.id, self.__admin_id)
        await self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            text=f"⚡ <b>{call.from_user.first_name}</b>, you are in the EmailSettings menu! Please, select the "
                 f"item you need below.",
            message_id=call.message.message_id,
            parse_mode="HTML",
            reply_markup=var.as_markup()
        )

        router_handler_em.callback_query.register(
            self.add_new_email,
            F.data == "add_email_from_settings_menu"
        )
        router_handler_em.callback_query.register(
            self.__show_email_from_settings_menu,
            F.data == "show_email_from_settings_menu"
        )
        router_handler_em.callback_query.register(
            self.__edit_email_from_settings_menu,
            F.data == "edit_email_from_settings_menu"
        )

    async def __show_email_from_settings_menu(self, call: types.CallbackQuery) -> None:
        """
        Show EMail-data from DB / File (for admin) bot.json.

        :param call: Callback Query.
        :return: None.
        """
        email: str = await self.__get_data_email(call.from_user.id)
        var: InlineKeyboardBuilder = await Buttons.get_menu_back_to_email_settings()

        await self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=f"🔥 <b>{call.from_user.first_name}</b>, You can see your EMail 📧 below.\n\n"
                 f"📧 <b>{email} | 👤 {call.from_user.first_name}</b>.",
            reply_markup=var.as_markup(),
            parse_mode="HTML"
        )

    async def __edit_email_from_settings_menu(self, call: types.CallbackQuery) -> None:
        """
        Edit EMail-data from DB / File (for admin) bot.json.

        :param call: Callback Query.
        :return: None.
        """
        email: str = await self.__get_data_email(call.from_user.id)
        var: InlineKeyboardBuilder = await Buttons.get_menu_confirmation_for_edit_email()

        await self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=f"🔥 <b>{call.from_user.first_name}</b>, You can EDIT your EMail 📧 below.\n\n"
                 f"📧 <b>{email} | 👤 {call.from_user.first_name}</b>.\n\nEdit?",
            reply_markup=var.as_markup(),
            parse_mode="HTML"
        )
        router_handler_em.callback_query.register(
            self.__confirmation_to_edit_email_from_email_settings,
            F.data == "confirmation_to_edit_email_from_email_settings"
        )

    async def __confirmation_to_edit_email_from_email_settings(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Edit EMail-data from DB / File (for admin) bot.json. | Confirmation-Step.

        :param call: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(ProcessEditingEmailAfterConfirmation.new_email)
        await self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=f"👌🏻 OK! Please, enter your new EMail..."
        )

    async def __editing_email_process_step_after_confirmation(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Get new EMail from the user / admin.

        :param message: Message - New EMail.
        :param state: FSM.

        :return: None.
        """
        await state.clear()
        new_email: str = message.text
        email: str = await self.__get_data_email(message.from_user.id)

        if email == new_email:
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"❌ <b>{message.from_user.first_name}</b>, sorry! But this EMail Address is the same as yours.",
                parse_mode="HTML"
            )
        else:
            await self.__add_new_email_to_db(message, state, "ON", new_email)

    async def add_new_email(self, call: types.CallbackQuery, state: FSMContext) -> None:
        """
        Add a new EMail. | Step 1. | Enter a new EMail.

        :param call: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(ProcessAddNewEmail.new_email)
        await self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            text="👌🏻 Ok! Please, enter you EMail... 📧",
            message_id=call.message.message_id
        )

    async def __add_new_email_to_db(
            self,
            message: types.Message | types.CallbackQuery,
            state: FSMContext,
            email_edit_mode="OFF",
            new_email_from_edit_set="None"
    ) -> None:
        """
        Add a new EMail. | Step 2. | Adding a new EMail to DB.

        :param message: EMail.
        :param state: FSM.
        :param email_edit_mode: Edit-Mode (OFF/ON).
        :param new_email_from_edit_set: None, if the mode is OFF.

        :return: None.
        """
        await state.clear()
        if type(message) is types.Message:
            if email_edit_mode == "OFF":
                self.__class__.__email = message.text
            elif email_edit_mode == "ON":
                self.__class__.__email = new_email_from_edit_set

            var: InlineKeyboardBuilder = await Buttons.get_add_new_email_try_again()
            valid: bool = await HandlerEM.valid_email(self.__class__.__email)

            if valid:
                result: tuple = await HandlerDB.get_email_data(message.from_user.id)
                if result[0] is False or email_edit_mode == "ON":
                    code: str = await self.__generate_code()
                    result: tuple = await HandlerDB.update_temp_code_for_check_email(
                        message.from_user.id,
                        code,
                        message.from_user.first_name,
                        message.from_user.username,
                        "add",
                        self.__admin_id
                    )
                    if result[0] is True:
                        await state.set_state(ProcessEnterTheCodeForAddNewEMailForVerifyEmail.code)
                        await SenderEmail.send_check_email_temp_code(
                            self.__class__.__email,
                            "#️⃣ Verification your EMail | CWR.SU INFO SYS",
                            message.from_user.first_name,
                            code
                        )
                        await self.__bot.send_message(
                            text=f"👌🏻 Please, {message.from_user.first_name}, enter the verification code. I sent it to"
                                 f" your EMail (*{self.__class__.__email}*)",
                            chat_id=message.from_user.id,
                            parse_mode="Markdown"
                        )
                    else:
                        await self.__bot.send_message(
                            text=f"❌ {message.from_user.first_name}, *Fail*! I can't add the verification code! "
                                 f"Try again 🔃",
                            chat_id=message.from_user.id,
                            parse_mode="Markdown",
                            reply_markup=var.as_markup()
                        )
                else:
                    await self.__bot.send_message(
                        text=f"❌ {message.from_user.first_name}, *Fail*! I can't send the verification code! "
                             f"Try again 🔃",
                        chat_id=message.from_user.id,
                        parse_mode="Markdown",
                        reply_markup=var.as_markup()
                    )
            else:
                await self.__bot.send_message(
                    text=f"❌ {message.from_user.first_name}, *Fail*! Your EMail: {self.__class__.__email} is invalid! "
                         f"Try again 🔃",
                    chat_id=message.from_user.id,
                    parse_mode="Markdown",
                    reply_markup=var.as_markup()
                )

        elif type(message) is types.CallbackQuery:
            if email_edit_mode == "ON":
                self.__class__.__email = new_email_from_edit_set
            valid: bool = await HandlerEM.valid_email(self.__class__.__email)
            if valid:
                result: tuple = await HandlerDB.get_email_data(message.from_user.id)
                if result[0] is False or email_edit_mode == "ON":
                    await state.set_state(ProcessEnterTheCodeForAddNewEMailForVerifyEmail.code)
                    await self.__bot.edit_message_text(
                        text=f"👌🏻 Please, {message.from_user.first_name}, enter the verification code. I sent it to"
                             f" your EMail (*{self.__class__.__email}*)",
                        message_id=message.message.message_id,
                        chat_id=message.from_user.id,
                        parse_mode="Markdown"
                    )
                else:
                    await self.__bot.edit_message_text(
                        text=f"❌ {message.from_user.first_name}, *Fail*! I can't send the verification code! "
                             f"Try again 🔃",
                        message_id=message.message.message_id,
                        chat_id=message.from_user.id,
                        parse_mode="Markdown"
                    )
            else:
                await self.__bot.edit_message_text(
                    text=f"❌ {message.from_user.first_name}, *Fail*! Your EMail: {self.__class__.__email} is invalid! "
                         f"Try again 🔃",
                    message_id=message.message.message_id,
                    chat_id=message.from_user.id,
                    parse_mode="Markdown"
                )

    async def __add_new_email_to_db_enter_the_code(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Add a new EMail. | Step 3. | Adding a new EMail to DB.

        :param message: Code from user (from EMail for check / valid).
        :param state: FSM.

        :return: None.
        """
        await state.clear()
        true_code: tuple = await HandlerDB.get_temp_code_for_check_email(
            message.from_user.id
        )
        if true_code[0] is True:
            if message.text == true_code[1][0]:
                if message.from_user.id != self.__admin_id:
                    result: bool = await HandlerDB.add_new_email(
                        self.__class__.__email,
                        message.from_user.id,
                        message.from_user.username,
                        message.from_user.first_name
                    )
                    var: InlineKeyboardBuilder = await Buttons.get_add_new_email_try_again()
                    if result:
                        await self.__bot.send_message(
                            text=f"✅ {message.from_user.first_name}, <b>Successfully</b>! Your EMail: "
                                 f"<b>{self.__class__.__email}</b> "
                                 f"has been added!",
                            chat_id=message.chat.id,
                            parse_mode="HTML",
                            reply_markup=var.as_markup()
                        )
                        await HandlerDB.update_temp_code_for_check_email(
                            message.from_user.id, "code", message.from_user.first_name,
                            message.from_user.username, "del"
                        )
                    else:
                        await self.__bot.send_message(
                            text=f"❌ {message.from_user.first_name}, <b>Fail</b>! Your EMail: "
                                 f"<b>{self.__class__.__email}</b> "
                                 f"hasn't been added!",
                            chat_id=message.chat.id,
                            parse_mode="HTML",
                            reply_markup=var.as_markup()
                        )
                else:
                    with open("bot.json", encoding='utf-8') as f:
                        dt: dict = json.load(f)

                    dt["EMAIL_DATA"]["ADMIN_EMAIL"] = self.__class__.__email

                    with open("bot.json", 'w', encoding='utf-8') as fl:
                        json.dump(dt, fl, ensure_ascii=False, indent=4)

                    var: InlineKeyboardBuilder = await Buttons.back_on_main()
                    await self.__bot.send_message(
                        text=f"✅ {message.from_user.first_name}, <b>Successfully</b>! Your EMail: "
                             f"<b>{self.__class__.__email}</b> "
                             f"has been added!",
                        chat_id=message.chat.id,
                        parse_mode="HTML",
                        reply_markup=var.as_markup()
                    )
                    await HandlerDB.update_temp_code_for_check_email(
                        message.from_user.id, "code", message.from_user.first_name,
                        message.from_user.username, "del", self.__admin_id
                    )

            else:
                var: InlineKeyboardBuilder = await Buttons.get_add_new_email_or_check_ver_code_try_again()

                await self.__bot.send_message(
                    text=f"❌ {message.from_user.first_name}, <b>Fail</b>! Code is invalid! Please, try again.",
                    chat_id=message.chat.id,
                    parse_mode="HTML",
                    reply_markup=var.as_markup()
                )
        else:
            var: InlineKeyboardBuilder = await Buttons.get_add_new_email_try_again()

            await self.__bot.send_message(
                text=f"❌ {message.from_user.first_name}, <b>Fail</b>! Verification code isn't exists"
                     f" (💡 Please, write to ADMIN)!",
                chat_id=message.chat.id,
                parse_mode="HTML",
                reply_markup=var.as_markup()
            )
