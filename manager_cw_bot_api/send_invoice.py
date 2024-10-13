"""Module of send invoice to users."""
import logging

from aiogram import Bot, types, Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB
from manager_cw_bot_api.handler_yookassa import Yookassa
from manager_cw_bot_api.handler_successful_payment import HandlerSP

router_send_invoice: Router = Router()


class ChooseMethodOfPayment:
    """Class for choose method of payment."""
    def __init__(
            self,
            bot: Bot,
            admin_id: int
    ) -> None:
        self.__bot: Bot = bot
        self.__admin_id: int = admin_id

    async def choose_step1(
            self,
            call: types.CallbackQuery
    ) -> None:
        """
        Choose method of payment. Step 1.

        :param call: Callback Query.
        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.get_premium_process_choosing()
        await self.__bot.edit_message_text(
            text=f"❤ <b>{call.from_user.first_name}</b>, please, choose the method of payment "
                 f"below.",
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=var.as_markup(),
            parse_mode="HTML"
        )
        router_send_invoice.callback_query.register(
            self.__continue_subscribe_premium_with_yookassa,
            F.data == "continue_subscribe_premium_with_yookassa"
        )
        router_send_invoice.callback_query.register(
            self.__continue_subscribe_premium_with_telegram_stars,
            F.data == "continue_subscribe_premium_with_telegram_stars"
        )
        router_send_invoice.callback_query.register(
            self.check_pay_yookassa,
            F.data == "check_pay_yookassa"
        )

    async def __continue_subscribe_premium_with_yookassa(
            self,
            call: types.CallbackQuery
    ) -> None:
        """
        Continue payment. | Yookassa-Method.

        :param call: Callback Query.
        :return: None.
        """
        try:
            if call.from_user.id != self.__admin_id:
                res: tuple = await HandlerDB.get_email_data(call.from_user.id)
                email: str = res[1][0]
            else:
                email: str = await HandlerDB.get_admin_email_from_file()

            payment_data: tuple = await Yookassa.create_payment(email)
            url = payment_data[0]
            confirmation_id: str = payment_data[1]

            await HandlerDB.update_yookassa_data(
                call, confirmation_id, self.__admin_id, email
            )

            var: InlineKeyboardBuilder = await Buttons.get_menu_yookassa_payment(url)
            await self.__bot.edit_message_text(
                text=f"✨ {call.from_user.first_name}, perfect!\n\nClick on the button below "
                     f"(💳 <b>Pay</b>) and then click on the <b>Check </b>🔑.\n\nIf button "
                     f"isn't activated, please, return to the main-menu (/start) and click on "
                     f"the: <b>GET CW PREMIUM</b> 🔥 (or <b>👑 MY CW PREMIUM 🌟</b>) -> "
                     f"<b>Get CW PREMIUM 💥 | -55%</b> -> 🔑 <b>Check payment</b>.\n\n"
                     f"ID: <code>{confirmation_id}</code>",
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                reply_markup=var.as_markup(),
                parse_mode="HTML"
            )
            await self.__bot.send_photo(
                chat_id=call.from_user.id,
                photo="https://telegra.ph/file/024c640166958255f5cab.jpg",
                message_effect_id="5159385139981059251",
                caption=f"⚡ See the invoice for payment above (for one message) 👆🏻."
            )
        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")

    async def check_pay_yookassa(
            self,
            call: types.CallbackQuery
    ) -> None:
        """
        Check pay Yookassa.

        :param call: Callback Query.
        :return: None.
        """
        result: tuple = await HandlerDB.yookassa_get_conf_id(call.from_user.id)
        payment_id: str = result[1]

        if result[0] is True:
            check_payment_obj: tuple = await Yookassa.check_payment(payment_id, call.from_user.id)
            if check_payment_obj[0] is True:
                await self.__bot.delete_message(
                    chat_id=call.from_user.id,
                    message_id=call.message.message_id
                )
                await HandlerSP.add_new_record(
                    self.__bot, call, self.__admin_id, "Yookassa", payment_id
                )

            elif check_payment_obj[0] is False and check_payment_obj[1] == "canceled":
                await self.__bot.answer_callback_query(
                    callback_query_id=call.id,
                    text=f"❌ {call.from_user.first_name}, fail! Payment was canceled by system.\n"
                         f"❕ Please, write to admin.",
                    show_alert=True
                )
                logging.warning(
                    f"Payment verification - unsuccessful as it was canceled by system! User ID: "
                    f"{call.from_user.id}"
                )

            else:
                await self.__bot.answer_callback_query(
                    callback_query_id=call.id,
                    text=f"❌ {call.from_user.first_name}, fail! It looks like you haven't paid "
                         f"the bill! Try again.\n❕ If you are sure that you have paid for "
                         f"it, then write to the admin / TicketSystem.",
                    show_alert=True
                )
                logging.warning(
                    f"Payment verification - unsuccessful as it has not been paid! User ID: "
                    f"{call.from_user.id}"
                )

        elif result[0] is False and result[1] == "None":
            await self.__bot.answer_callback_query(
                callback_query_id=call.id,
                text=f"❌ {call.from_user.first_name}, fail! Payment wasn't created!\n❕ "
                     f"Please, write to admin.",
                show_alert=True
            )
            logging.warning(
                f"Payment verification - unsuccessful as it has not been created! User ID: "
                f"{call.from_user.id}"
            )

        else:
            await self.__bot.answer_callback_query(
                callback_query_id=call.id,
                text=f"❌ {call.from_user.first_name}, fail! Please, try again: return to "
                     f"the main-menu (/start) and click on the: GET PREMIUM "
                     f"🔥 -> 🔑 Check payment.",
                show_alert=True
            )
            logging.warning(
                f"Payment verification - unsuccessful! User ID: "
                f"{call.from_user.id}"
            )

    async def __continue_subscribe_premium_with_telegram_stars(
            self,
            call: types.CallbackQuery
    ) -> None:
        """
        Continue payment. | TelegramStars-Method.

        :param call: Callback Query.
        :return: None.
        """
        checked: tuple = await HandlerDB.check_subscription(call)
        if checked[1] == "ex_sub":
            invoice_extend: SendInvoice = SendInvoice(
                self.__bot, call
            )
            await invoice_extend.send_invoice_extend()
        else:
            invoice: SendInvoice = SendInvoice(
                self.__bot, call
            )
            await invoice.send_invoice()


class SendInvoice:
    """Class of the send invoice to users for buy/pay premium-subscription."""
    def __init__(
            self, 
            bot: Bot,
            message: types.Message | types.CallbackQuery
    ) -> None:
        self.__bot: Bot = bot
        self.__message: types.Message = message
        self.__chat_id: int = message.from_user.id

    async def send_invoice(self) -> None:
        """
        Send Invoice | First pay.

        :return: None.
        """
        await self.__bot.send_invoice(
            chat_id=self.__chat_id,
            title="CW Premium",
            description=f"Premium-functions for the user {self.__message.from_user.first_name}.",
            provider_token="",
            currency="XTR",
            prices=[types.LabeledPrice(
                label="CW Premium",
                amount=15
            )],
            photo_url="https://telegra.ph/file/024c640166958255f5cab.jpg",
            photo_size=80000,
            photo_width=800,
            photo_height=610,
            payload="Invoice",
            reply_markup=InlineKeyboardBuilder().row(types.InlineKeyboardButton(
                text=f"⭐️ Telegram Stars", pay=True
            )).as_markup(),
        )

        logging.info(
            "Successful billing for Telegram XTR currency payment | First payment"
        )

    async def send_invoice_extend(self) -> None:
        """
        Send invoice | Extend.

        :return: None.
        """
        await self.__bot.send_invoice(
            chat_id=self.__chat_id,
            title="CW Premium",
            description=f"The subscription renewal. "
                        f"Premium-functions for the user {self.__message.from_user.first_name}.",
            payload="Invoice",
            provider_token="",
            currency="XTR",
            prices=[types.LabeledPrice(
                label="CW Premium",
                amount=15
            )],
            photo_url="https://telegra.ph/file/024c640166958255f5cab.jpg",
            photo_size=80000,
            photo_width=800,
            photo_height=610,
            reply_markup=InlineKeyboardBuilder().row(types.InlineKeyboardButton(
                text=f"⭐️ Telegram Stars", pay=True
            )).as_markup()
        )

        logging.info(
            "Successful billing for Telegram XTR currency payment | Second payment"
        )
