"""Refunding module."""
import datetime
import logging

from aiogram import types, Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.input_file import FSInputFile

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.fsm_handler import (
    ProcessRefundingGetREFTokenST1,
    ProcessEmergencyRefundingGetREFTokenST1
)
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB, SubOperations
from manager_cw_bot_api.handler_email_sender import SenderEmail
from manager_cw_bot_api.pdf_generate_data import GenerateReceiptRefundForUser

router_refund: Router = Router()


class Refund:
    """Class of a refund."""
    __refund_token: str = ""

    def __init__(self, bot: Bot) -> None:
        self.__bot: Bot = bot

        router_refund.message.register(
            self.__refunding_step2_confirmation,
            ProcessRefundingGetREFTokenST1.token
        )
        router_refund.message.register(
            self.__emergency_refunding_step2,
            ProcessEmergencyRefundingGetREFTokenST1.user_id
        )

    async def refunding_step1_confirmation(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Call-Handler for refund stars | Step 1 - Confirmation.

        :param call: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(ProcessRefundingGetREFTokenST1.token)
        await self.__bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='Important! If the payment was made through the YooKassa system (as a payment '
                 'method), then a refund (in this case) is possible only through a personal '
                 'account on the site https://yookassa.ru / in the "Refunds" section.\n\n'
                 '🔐 Enter the *REFUND-token... (*only for Telegram Stars as a payment method)'
        )

    async def __refunding_step2_confirmation(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Refunding star(-s) to user | Step 2 - Confirmation.

        :param message: Token from user.
        :param state: FSM.

        :return: None.
        """
        await state.clear()

        var: InlineKeyboardBuilder = await Buttons.sure_refund_confirmation()
        self.__class__.__refund_token = message.text

        checked_promo: tuple = await HandlerDB.check_promo_code(
            self.__class__.__refund_token
        )

        if checked_promo[0] is False:
            checked: tuple = await HandlerDB.check_subscription_by_refund_token(
                self.__class__.__refund_token
            )
            if checked[0] is False:
                if checked[2] == "none":
                    await self.__bot.send_message(
                        chat_id=message.from_user.id,
                        text=f"⚠️ *{message.from_user.first_name}*, are you sure? I could not "
                             f"find this REFUND-Token in the database. It may not have been "
                             f"added in time due to problems on the server side.\n\nIf you see "
                             f"that the token looks like a real one, click the corresponding "
                             f"button below. BUT if you are not sure that this isn't a real "
                             f"token, click '❌ Cancel'!\n\n"
                             f"⚠ This step is registered!",
                        parse_mode="Markdown",
                        reply_markup=var.as_markup()
                    )

                    router_refund.callback_query.register(
                        self.__refunding_step3,
                        F.data == "refund_confirmation"
                    )
                elif checked[1] == "ex_sub":
                    await self.__bot.send_message(
                        chat_id=message.from_user.id,
                        text=f"⚠️ *{message.from_user.first_name}*, are you sure? I found "
                             f"a user, but his subscription has expired!\n\n"
                             f"⚠ This step is registered!",
                        parse_mode="Markdown",
                        reply_markup=var.as_markup()
                    )

                    router_refund.callback_query.register(
                        self.__refunding_step3,
                        F.data == "refund_confirmation"
                    )
            elif checked[0] is True:
                remains = round(await SubOperations.sec_to_days(checked[1]))
                d = "days"

                if remains > 1:
                    d = "days"
                elif remains == 1:
                    d = "day"

                await self.__bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"⚠️ *{message.from_user.first_name}*, are you sure? The subscription "
                         f"ends after *{remains} {d}*. If necessary, notify the user about this!"
                         f"\n\nAfter the star(s) are returned, the *subscription will be "
                         f"disabled*!\nBut *user can resume* it at any other time by "
                         f"clicking on *Get CW PREMIUM* in main menu.",
                    parse_mode="Markdown",
                    reply_markup=var.as_markup()
                )

                router_refund.callback_query.register(
                    self.__refunding_step3,
                    F.data == "refund_confirmation"
                )
        else:
            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"🚫 *{message.from_user.first_name}*, sorry. But I can't make a refund. "
                     f"That's a PROMO-REF-Token! (We can't make a refund on it).",
                parse_mode="Markdown",
                reply_markup=var.as_markup()
            )

            logging.warning(
                f"Rejection of TGStars return on PROMO token."
            )

    async def __refunding_step3(self, call: types.CallbackQuery) -> None:
        """
        Refunding. The admin has confirmed the actions.

        :param call: Callback Query.
        :return: None.
        """
        try:
            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text="⏳ Starting the refund...",
                message_id=call.message.message_id
            )

            check: tuple = await HandlerDB.check_subscription_by_refund_token(
                self.__class__.__refund_token
            )

            if check[2] != "none":
                user_id: int = int(check[2])
                await self.__bot.refund_star_payment(
                    user_id=user_id,
                    telegram_payment_charge_id=self.__class__.__refund_token
                )

                result: tuple = await HandlerDB.get_email_data(user_id)

                deleted: tuple = await HandlerDB.delete_record_for_subscribe(
                    self.__class__.__refund_token
                )
                if deleted[0] is True:
                    await self.__bot.edit_message_text(
                        chat_id=call.from_user.id,
                        text="✅ The refund is completed ✨",
                        message_id=call.message.message_id,
                        reply_markup=var.as_markup()
                    )

                    firstname: str = deleted[2]
                    await self.__bot.send_message(
                        chat_id=user_id,
                        text=f"ℹ {firstname}, Your star(s) have been returned!",
                        reply_markup=var.as_markup()
                    )

                    if result[0]:
                        time = (datetime.datetime.
                                now(datetime.timezone(datetime.timedelta(hours=3))).
                                strftime('%d.%m.%Y | %H:%M:%S'))

                        receipt_data = (f"<tr>"
                                        f"  <td align='center'><code>"
                                        f"{self.__class__.__refund_token}"
                                        f"</code></td>"
                                        f"  <td align='center'>@{call.from_user.username}</td>"
                                        f"  <td align='center'>15 XTR</td>"
                                        f"  <td align='center'>{time} (UTC+3)</td>"
                                        f"  <td align='center'>Telegram Stars (XTR)</td>"
                                        f"</tr>")

                        file_path: str = await GenerateReceiptRefundForUser.generate(
                            result[1][1],
                            receipt_data
                        )
                        await self.__bot.send_document(
                            chat_id=user_id,
                            document=FSInputFile(file_path),
                            caption=f"👑 {call.from_user.first_name}, there is the payment "
                                    f"receipt attached below. It'll also send to you by email! ⚡"
                        )
                        await SenderEmail.send_receipt_refund_to_user_in_email_format(
                            result[1][0],
                            f"🧾📨 Receipt for the refund of funds from the Manager "
                            f"CW for {result[1][1]} | CWR.SU",
                            result[1][1],
                            file_path
                        )

                        msg_temp: types.Message = await self.__bot.send_message(
                            text=f"✅ The data sent!",
                            chat_id=user_id
                        )

                        await self.__bot.delete_message(
                            chat_id=msg_temp.chat.id,
                            message_id=msg_temp.message_id
                        )

                        var: InlineKeyboardBuilder = await Buttons.back_on_main()
                        await self.__bot.send_message(
                            text=f"🔐 You've all the data and they're safe. To go to the main, "
                                 f"click on the button below.",
                            chat_id=user_id,
                            reply_markup=var.as_markup(),
                            parse_mode="HTML"
                        )

                        logging.info(
                            f"Successful return of stars to the user's balance and sending the "
                            f"receipt (EMail: {result[1][0]}). User ID: {user_id}"
                        )

                else:
                    await self.__bot.edit_message_text(
                        chat_id=call.from_user.id,
                        text="⚠ Something wrong! Check your balance.",
                        message_id=call.message.message_id,
                        reply_markup=var.as_markup()
                    )

                    logging.warning(
                        f"SMTH wrong about returning of stars to the user's balance and sending "
                        f"the receipt (EMail: {result[1][0]}). User ID: {user_id}"
                    )

            elif check[2] == "none":
                var: InlineKeyboardBuilder = await Buttons.sure_emergency_refund_confirmation()
                await self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=f"⚠️ *{call.from_user.first_name}*, are you sure? I could not find the "
                         f"User ID to return the stars. If you are sure that this is a "
                         f"real REFUND Token, click the corresponding "
                         f"button below. If not, then click on '❌ Cancel'!",
                    parse_mode="Markdown",
                    message_id=call.message.message_id,
                    reply_markup=var.as_markup()
                )

                router_refund.callback_query.register(
                    self.__emergency_refunding_step1,
                    F.data == "emergency_refund_confirmation"
                )

                logging.warning("Registered emergency refund (stars)")

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")

            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            if "CHARGE_ALREADY_REFUNDED" in str(ex):
                await self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=f"🚫 *{call.from_user.first_name}*, sorry. But I can't make a refund "
                         f"by this (`{self.__class__.__refund_token}`) "
                         f"token.\n\n❌ Error: There has already been a refund for this token!"
                         f"\n\nPlease, write: help@cwr.su for support.",
                    message_id=call.message.message_id,
                    parse_mode="Markdown",
                    reply_markup=var.as_markup()
                )

                logging.warning(
                    f"Rejection on the return of the stars. Cause: There has already been a "
                    f"refund for this token ({self.__class__.__refund_token}). User ID: "
                    f"{call.from_user.id}"
                )
            else:
                await self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=f"🚫 *{call.from_user.first_name}*, sorry. But I can't make a refund "
                         f"by this (`{self.__class__.__refund_token}`) "
                         f"token.\n\nPlease, write: help@cwr.su for support.",
                    message_id=call.message.message_id,
                    parse_mode="Markdown",
                    reply_markup=var.as_markup()
                )
                logging.warning(
                    f"Rejection on the return of the stars. "
                    f"REF-Token: {self.__class__.__refund_token}. User ID: {call.from_user.id}"
                )

    async def __emergency_refunding_step1(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ) -> None:
        """
        Emergency Refund by admin. | Step 1 | Confirmation.

        :param call: Callback Query.
        :param state: FSM.

        :return: None.
        """
        try:
            await state.set_state(ProcessEmergencyRefundingGetREFTokenST1.user_id)
            await self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text=f"👌🏻 *{call.from_user.first_name}*, OK. Tell me the 👤 User ID "
                     f"(To confirm the operation).\n\n"
                     f"The user has it (User ID) in the *My CW PREMIUM"
                     f" -> My ID section*.",
                message_id=call.message.message_id,
                parse_mode="Markdown"
            )

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")

            await self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text=f"❌<b>{call.from_user.first_name}</b>, Error! Exception-prog: {ex}.\n"
                     f"REF-TOKEN: {self.__class__.__refund_token}",
                message_id=call.message.message_id,
                parse_mode="HTML"
            )

    async def __emergency_refunding_step2(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """
        Emergency Refund by admin. | Step 2 | Confirmation.

        :param message: UserID.
        :param state: FSM.

        :return: None.
        """
        try:
            await state.clear()

            if message.text.isdigit():
                user_id: int = int(message.text)

                msg: types.Message = await self.__bot.send_message(
                    chat_id=message.from_user.id,
                    text="⏳ Starting the refund...",
                )

                await self.__bot.refund_star_payment(
                    user_id=int(user_id),
                    telegram_payment_charge_id=self.__class__.__refund_token
                )

                self.__class__.__refund_token = ""
                var: InlineKeyboardBuilder = await Buttons.back_on_main()

                await self.__bot.edit_message_text(
                    chat_id=message.from_user.id,
                    text="✅ The refund is completed ✨.",
                    message_id=msg.message_id,
                    reply_markup=var.as_markup()
                )

                await self.__bot.send_message(
                    chat_id=int(user_id),
                    text=f"ℹ [{user_id}] Your star(s) have been returned!\n",
                    reply_markup=var.as_markup()
                )

                logging.info(
                    f"Successful return of stars to the user's balance User ID: {user_id}"
                )

                result: tuple = await HandlerDB.get_email_data(user_id)

                if result[0]:
                    firstname: str = result[1][1]
                    time = (datetime.datetime.
                            now(datetime.timezone(datetime.timedelta(hours=3))).
                            strftime('%d.%m.%Y | %H:%M:%S'))

                    receipt_data = (f"<tr>"
                                    f"  <td align='center'><code>"
                                    f"{self.__class__.__refund_token}"
                                    f"</code></td>"
                                    f"  <td align='center'>[ID]: {user_id}</td>"
                                    f"  <td align='center'>15 XTR</td>"
                                    f"  <td align='center'>{time} (UTC+3)</td>"
                                    f"  <td align='center'>Telegram Stars (XTR)</td>"
                                    f"</tr>")

                    file_path: str = await GenerateReceiptRefundForUser.generate(
                        firstname,
                        receipt_data
                    )
                    await self.__bot.send_document(
                        chat_id=user_id,
                        document=FSInputFile(file_path),
                        caption=f"👑 {firstname}, there is the payment "
                                f"receipt attached below. It'll also send to you by email! ⚡"
                    )
                    await SenderEmail.send_receipt_refund_to_user_in_email_format(
                        result[1][0],
                        f"🧾📨 Receipt for the refund of funds from the Manager "
                        f"CW for {firstname} | CWR.SU",
                        firstname,
                        file_path
                    )

                    msg_temp: types.Message = await self.__bot.send_message(
                        text=f"✅ The data sent!",
                        chat_id=user_id
                    )

                    await self.__bot.delete_message(
                        chat_id=msg_temp.chat.id,
                        message_id=msg_temp.message_id
                    )

                    var: InlineKeyboardBuilder = await Buttons.back_on_main()
                    await self.__bot.send_message(
                        text=f"🔐 You've all the data and they're safe. To go to the main, "
                             f"click on the button below.",
                        chat_id=user_id,
                        reply_markup=var.as_markup(),
                        parse_mode="HTML"
                    )

                    logging.info(
                        f"Successful sending the receipt (EMail: {result[1][0]}). "
                        f"User ID: {user_id}"
                    )
                else:
                    await self.__bot.send_message(
                        chat_id=int(user_id),
                        text=f"ℹ [{user_id}], stars-refund receipt will not be delivered to your "
                             f"EMail! Check the history of pay in your Telegram Account.",
                        reply_markup=var.as_markup()
                    )

            else:
                logging.warning(f"User ID {message.text} must be integer-type!")

                await self.__bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"❌ <b>{message.from_user.first_name}</b>, Error! "
                         f"User ID {message.text} must be integer-type!",
                    parse_mode="HTML"
                )

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")

            await self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"❌ <b>{message.from_user.first_name}</b>, Error! Exception-prog: {ex}.\n"
                     f"REF-TOKEN: {self.__class__.__refund_token}",
                parse_mode="HTML"
            )
