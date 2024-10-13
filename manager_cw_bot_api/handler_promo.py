"""Promo-control module."""
import logging

from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.fsm_handler import (ProcessEnteringPromoST1, ProcessAddNewPromoPromoST2,
                                            ProcessDeletePromoPromoST2)
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB

router_promo: Router = Router()


class HandlerEP:
    """Class for get premium if user has a promo code."""
    __promo_code: str = ""

    def __init__(self, bot: Bot, admin_id: int) -> None:
        self.__bot: Bot = bot
        self.__admin_id: int = admin_id

        router_promo.message.register(
            self.__entering_promo_step1,
            ProcessEnteringPromoST1.promo
        )
        router_promo.message.register(
            self.__add_new_promo_admin_ctrl_step2,
            ProcessAddNewPromoPromoST2.promo
        )
        router_promo.message.register(
            self.__delete_promo_data_admin_ctrl_step2,
            ProcessDeletePromoPromoST2.promo
        )

    async def enter_promo(self, call: types.CallbackQuery, state: FSMContext) -> None:
        """
        Function for get a promo code from user.

        :param call: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(ProcessEnteringPromoST1.promo)
        await self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            text="🎫 Enter a promo code...",
            message_id=call.message.message_id
        )

    async def __entering_promo_step1(self, message: types.Message, state: FSMContext) -> None:
        """
        Get promo code (text format).

        :param message: A promo code.
        :param state: FSM.

        :return: None.
        """
        await state.clear()

        promo: str = message.text
        checked: tuple = await HandlerDB.check_promo_code(promo)
        if checked[0] is False:
            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text="❌ *Invalid promo code*.",
                parse_mode="Markdown",
                reply_markup=var.as_markup()
            )
            logging.warning(
                f"Invalid promo code (which was entering by user to activate). "
                f"User ID: {message.from_user.id}"
            )
        elif checked[0] is True:
            type_promo: str = checked[3]

            if type_promo == "premium_month":
                count_days: int = 30
            elif type_promo == "premium_five_days":
                count_days: int = 5
            elif type_promo == "premium_one_week":
                count_days: int = 7
            else:
                count_days: int = 0

            var: InlineKeyboardBuilder = await Buttons.sure_apply_promo()
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"⚠️ Are you sure you want to *apply this promo code* "
                     f"`{promo}`? You'll receive {count_days} days of CW PREMIUM.",
                parse_mode="Markdown",
                reply_markup=var.as_markup()
            )

            self.__class__.__promo_code = promo

            router_promo.callback_query.register(
                self.__entering_promo_step2,
                F.data == "apply_promo"
            )

    async def __entering_promo_step2(self, call: types.CallbackQuery) -> None:
        """
        Confirmation of apply a promo code.

        :param call: Callback Query.
        :return: None.
        """
        checked_sub: bool | tuple = await HandlerDB.sub_promo_code(self.__class__.__promo_code)
        if checked_sub[0] is True:
            count_days: int = 0

            checked: tuple = await HandlerDB.check_promo_code(self.__class__.__promo_code)
            if checked[0] is True:

                type_promo: str = checked[3]
                if type_promo == "premium_month":
                    count_days = 30
                elif type_promo == "premium_five_days":
                    count_days = 5
                elif type_promo == "premium_one_week":
                    count_days = 7

            res: tuple = await HandlerDB.insert_new_record_for_subscribe(
                message=call,
                days=count_days,
                promo=self.__class__.__promo_code
            )
            result = res[0]
            if result is True:
                var: InlineKeyboardBuilder = await Buttons.back_on_main()
                await self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=f"✅ Successful! Done!\nYour CW PREMIUM is *activated*!\n\nNow you can:"
                         f"\n- Use 💥 Kandinsky AI | Generate IMG 🖼\n"
                         f"- 🧠 Use AI-Assistance\n- and more; only MORE!",
                    message_id=call.message.message_id,
                    parse_mode="Markdown",
                    reply_markup=var.as_markup()
                )

                await self.__bot.send_message(
                    chat_id=self.__admin_id,
                    text=f"🆕 Admin, CW PREMIUM +1 person! 🔥 | With PROMO: "
                         f"`{self.__class__.__promo_code}` | "
                         f"Days: {count_days}.",
                    parse_mode="Markdown",
                    reply_markup=var.as_markup()
                )

                if checked_sub[1] == "none":
                    delete: bool = await HandlerDB.delete_promo_code(self.__class__.__promo_code)
                    if delete:
                        pass

                logging.info(
                    f"Successfully activated promo code: {self.__class__.__promo_code}"
                    f"User ID: {call.from_user.id}"
                )

            else:
                await self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=f"❌ Failed!\nYour CW PREMIUM *isn't activated*!\n\nNow you should:"
                         f"\n- write on EMail: help@cwr.su.",
                    message_id=call.message.message_id,
                    parse_mode="Markdown"
                )

                logging.warning(
                    f"Failed activated promo code: {self.__class__.__promo_code}"
                    f"User ID: {call.from_user.id}"
                )

        elif checked_sub[0] is False:
            await self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text=f"❌ Failed!\nYour CW PREMIUM *isn't activated*!\n\nNow you should:"
                     f"\n- write on EMail: help@cwr.su.",
                message_id=call.message.message_id,
                parse_mode="Markdown"
            )

            logging.warning(
                f"Failed activated promo code: {self.__class__.__promo_code}"
                f"User ID: {call.from_user.id}"
            )

    async def show_promo_menu_admin(self, call_query: types.CallbackQuery) -> None:
        """
        Show PROMO Menu. | Control ADMIN.

        :param call_query: Callback Query.

        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.get_menu_admin_promos()
        await self.__bot.edit_message_text(
            chat_id=call_query.from_user.id,
            text=f"👑 <b>{call_query.from_user.first_name}</b>, "
                 f"select the item you need below.\n\n",
            message_id=call_query.message.message_id,
            reply_markup=var.as_markup(),
            parse_mode="HTML"
        )

        router_promo.callback_query.register(
            self.__add_new_promo_code_admin_ctrl,
            F.data == "add_new_promo"
        )
        router_promo.callback_query.register(
            self.__show_promo_datas_admin_ctrl,
            F.data == "show_promo_datas"
        )
        router_promo.callback_query.register(
            self.__delete_promo_data_admin_ctrl,
            F.data == "delete_promo_data"
        )

    async def __show_promo_datas_admin_ctrl(self, call: types.CallbackQuery) -> None:
        """
        Show PROMO datas. | Control ADMIN.

        :param call: Callback Query.

        :return: None.
        """
        datas: bool | tuple = await HandlerDB.show_promo_datas()
        var: InlineKeyboardBuilder = await Buttons.back_in_promo_menu()

        if datas[0] is True:
            await self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text=datas[1],
                message_id=call.message.message_id,
                parse_mode="HTML",
                reply_markup=var.as_markup()
            )
        elif datas[0] is False:
            await self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text=f"🌐 Promo codes *have not been added*.",
                message_id=call.message.message_id,
                parse_mode="Markdown",
                reply_markup=var.as_markup()
            )

    async def __add_new_promo_code_admin_ctrl(self, call: types.CallbackQuery) -> None:
        """
        Add a new promo. | Control ADMIN. | Confirmation.

        :param call: Callback Query.

        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.sure_add_new_promo()
        await self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            text=f"⚠️ Are you sure you want to *add a new promo code*?",
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=var.as_markup()
        )

        router_promo.callback_query.register(
            self.__add_new_promo_admin_ctrl_step1,
            F.data == "add_new_promo_confirmation"
        )

    async def __add_new_promo_admin_ctrl_step1(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Add a new promo. | Control ADMIN. | Step 1.

        :param call: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(ProcessAddNewPromoPromoST2.promo)
        await self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            text=f"👌🏻 *{call.from_user.first_name}*, OK. Create a new promo-data explore "
                 f"this format:\n\n"
                 f"*FORMAT*:\n"
                 f"```Example NEW_PROMO_CODE ~ NUM_USES ~ TYPE_PROMO```\n\n"
                 f"Types of promo codes:\n"
                 f"1. `premium_one_week`;\n"
                 f"2. `premium_five_days`;\n"
                 f"3. `premium_month`;\n",
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )

    async def __add_new_promo_admin_ctrl_step2(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Add a new promo. | Control ADMIN. | Step 2.

        :param message: Message from the admin with PROMO-data.
        :param state: FSM.

        :return: None.
        """
        await state.clear()

        var: InlineKeyboardBuilder = await Buttons.try_again_add_new_promo_or_back_on_main()
        if len(message.text.split(" ~ ")) == 3:
            promo, num_uses, type_promo = message.text.split(" ~ ")
            if int(num_uses) > 0 and len(promo) >= 3:
                checked: tuple = await HandlerDB.add_new_promo_code(promo, num_uses, type_promo)
                if checked[0] is True:
                    var: InlineKeyboardBuilder = await Buttons.back_in_promo_menu()
                    await self.__bot.send_message(
                        chat_id=message.from_user.id,
                        text=f"✅ *Successful*! Done!\n\n{message.from_user.first_name}, "
                             f"*the promo data has been added*!",
                        parse_mode="Markdown",
                        reply_markup=var.as_markup()
                    )

                    logging.info(
                        f"Successfully has been added promo data "
                        f"({promo}, {num_uses}, {type_promo})"
                    )
                elif checked[0] is False:
                    if checked[1] == "already_exist":
                        var: InlineKeyboardBuilder = await Buttons.back_in_promo_menu()
                        await self.__bot.send_message(
                            chat_id=message.from_user.id,
                            text=f"❌ *{message.from_user.first_name}*, the promo data "
                                 f"*already exists*!",
                            parse_mode="Markdown",
                            reply_markup=var.as_markup()
                        )
                        logging.warning(
                            f"The Promo data hasn't been added "
                            f"({promo}, {num_uses}, {type_promo}); Already Exist!"
                        )
                    elif checked[1] == "invalid_type":
                        await self.__bot.send_message(
                            chat_id=message.from_user.id,
                            text=f"❌ *{message.from_user.first_name}*, the type of promo "
                                 f"is *invalid*!",
                            parse_mode="Markdown",
                            reply_markup=var.as_markup()
                        )
                        logging.warning(
                            f"The Promo data hasn't been added "
                            f"({promo}, {num_uses}, {type_promo}); Invalid Type!"
                        )
            else:
                await self.__bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"❌ *{message.from_user.first_name}*, sorry. But i can't add "
                         f"your PROMO data!\n\n*Number of uses* must be *>= 1* and *length* of "
                         f"promo code must be *>= 3*!\n",
                    parse_mode="Markdown",
                    reply_markup=var.as_markup()
                )
                logging.warning(
                    f"The Promo data hasn't been added "
                    f"({promo}, {num_uses}, {type_promo}); Invalid num_uses/length of promo code!"
                )

        else:
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"❌ *{message.from_user.first_name}*, sorry. But i can't "
                     f"split your message!\n\n"
                     f"*FORMAT*:\n"
                     f"```Example NEW_PROMO_CODE ~ NUM_USES ~ TYPE_PROMO```\n\n"
                     f"Types of promo codes:\n"
                     f"1. `premium_one_week`;\n"
                     f"2. `premium_five_days`;\n"
                     f"3. `premium_month`;\n",
                parse_mode="Markdown",
                reply_markup=var.as_markup()
            )
            logging.warning(
                f"The Promo data hasn't been added;"
                f"Can't split message!"
            )

            router_promo.callback_query.register(
                self.__add_new_promo_admin_ctrl_step1,
                F.data == "try_again_add_new_promo"
            )

    async def __delete_promo_data_admin_ctrl(
            self,
            call: types.CallbackQuery
    ) -> None:
        """
        Delete promo. | Control ADMIN. | Confirmation.

        :param call: Callback Query.

        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.sure_delete_promo()
        await self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            text=f"⚠️ Are you sure you want to *delete a promo code*?",
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=var.as_markup()
        )

        router_promo.callback_query.register(
            self.__delete_promo_data_admin_ctrl_step1,
            F.data == "delete_promo_confirmation"
        )

    async def __delete_promo_data_admin_ctrl_step1(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Delete promo. | Control ADMIN. | Step 1.

        :param call: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(ProcessDeletePromoPromoST2.promo)
        await self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            text=f"👌🏻 *{call.from_user.first_name}*, OK. Send me the promo code that you "
                 f"want to delete.\n",
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )

    async def __delete_promo_data_admin_ctrl_step2(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Delete promo. | Control ADMIN. | Step 2.

        :param message: Message from the admin with PROMO-data.
        :param state: FSM.

        :return: None.
        """
        await state.clear()

        promo: str = message.text
        checked: bool = await HandlerDB.delete_promo_code(promo)
        if checked is True:
            var: InlineKeyboardBuilder = await Buttons.back_in_promo_menu()
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"✅ *Successful*! Done!\n\n{message.from_user.first_name}, *the promo "
                     f"data has been deleted*!",
                parse_mode="Markdown",
                reply_markup=var.as_markup()
            )
            logging.info(
                f"Successfully has been deleted promo data "
                f"(promo-code:{promo})"
            )
        else:
            var: InlineKeyboardBuilder = await Buttons.try_again_delete_promo_or_back_on_main()
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"❌ *{message.from_user.first_name}*, the promo data *doesn't exist*!\n\n"
                     f"Or there was some kind of error when deleting the record. "
                     f"ANSWER: (checked) {checked}.",
                parse_mode="Markdown",
                reply_markup=var.as_markup()
            )
            logging.warning(
                f"The Promo data hasn't been deleted "
                f"(promo-code:{promo}); Maybe this promo code doesn't exist."
            )

            router_promo.callback_query.register(
                self.__delete_promo_data_admin_ctrl_step1,
                F.data == "try_again_delete_promo"
            )
