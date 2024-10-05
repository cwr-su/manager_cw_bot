"""Module of the control successful payments."""
import datetime

from aiogram import types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.input_file import FSInputFile

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB
from manager_cw_bot_api.handler_email_sender import SenderEmail
from manager_cw_bot_api.pdf_generate_data import GenerateReceiptForUser


class HandlerSP:
    """Class-handler for successful payments."""
    @staticmethod
    async def add_new_record(
            bot: Bot,
            message: types.Message | types.CallbackQuery,
            admin_id: int,
            mode="TGStar",
            yookassa_ref_token="yookassa"
    ) -> None:
        """
        Add a new record in database.

        :param bot: The object of Telegram Bot.
        :param message: Message of the successful payment by Stars.
        :param admin_id: Telegram Admin ID.
        :param mode: Mode of process successful payment.
        :param yookassa_ref_token: Yookassa refund-token.

        :return: bool.
        """
        time = (datetime.datetime.
                now(datetime.timezone(datetime.timedelta(hours=3))).
                strftime('%d.%m.%Y | %H:%M:%S'))

        var: InlineKeyboardBuilder = await Buttons.back_on_main()
        try:
            if mode == "TGStar":
                ref_token: str = message.successful_payment.telegram_payment_charge_id
                method: str = "Telegram Stars (XTR)"
            else:
                ref_token: str = yookassa_ref_token
                method: str = "YooKassa"

            msg: types.Message = await bot.send_photo(
                photo="https://telegra.ph/file/4279f8aec9f71db459a7e.jpg",
                chat_id=message.from_user.id,
                caption=f"💖 Thanks! I received the payment!\n\n🔐 Token for refund stars / money: "
                        f"<code>{ref_token}</code>\n\nPlease, wait! I'm activating "
                        f"your subscription...⏳",
                message_effect_id="5046509860389126442",
                parse_mode="HTML"
            )
            result: tuple = await HandlerDB.insert_new_record_for_subscribe(
                message=message,
                days=30,
                token_successful_payment=ref_token,
            )
            res: bool = result[0]
            des: str = result[1]

            if res is True:
                await HandlerDB.yookassa_delete_record_conf_id(message.from_user.id)
                await bot.edit_message_caption(
                    chat_id=message.from_user.id,
                    caption=f"✅ <b>Successful! Done!</b>\nYour CW PREMIUM is <b>activated</b>!\n\nNow you can:\n"
                            f"- Use 💥 AI-Generate IMG 🖼\n"
                            f"- 🧠 Use AI-Assistance (👑 PRO-Mode)\n"
                            f"- and more functions: ⚡ See the card 😉!\n\n"
                            f"🔐 Your refund token:\n<code>{ref_token}</code>.",
                    message_id=msg.message_id,
                    parse_mode="HTML",
                    reply_markup=var.as_markup()
                )
                await bot.send_message(
                    chat_id=admin_id,
                    text=f"🆕 Admin, CW PREMIUM +1 person! 🔥",
                    reply_markup=var.as_markup(),
                    message_effect_id="5046509860389126442",
                )

                receipt_data = (f"<tr>"
                                f"  <td align='center'><code>{ref_token}</code></td>"
                                f"  <td align='center'>@{message.from_user.username}</td>"
                                f"  <td align='center'>CW PREMIUM</td>"
                                f"  <td align='center'>{time} (UTC+3)</td>"
                                f"  <td align='center'>{method}</td>"
                                f"</tr>")

                result: tuple = await HandlerDB.get_email_data(message.from_user.id)
                if result[0]:
                    file_path: str = await GenerateReceiptForUser.generate(
                        result[1][1],
                        receipt_data
                    )
                    await bot.send_document(
                        chat_id=message.from_user.id,
                        document=FSInputFile(file_path),
                        caption=f"👑 {message.from_user.first_name}, there is the payment receipt attached below. It'll "
                                f"also send to you by email! ⚡"
                    )
                    await SenderEmail.send_receipt_to_user_in_email_format(
                        result[1][0],
                        f"🧾📨 Payment Receipt from Manager CW for {result[1][1]} | CWR.SU",
                        result[1][1],
                        file_path
                    )

                    msg_temp: types.Message = await bot.send_message(
                        text=f"✅ The data sent!",
                        chat_id=message.from_user.id
                    )

                    await bot.delete_message(
                        chat_id=msg_temp.chat.id,
                        message_id=msg_temp.message_id
                    )

                    var: InlineKeyboardBuilder = await Buttons.back_on_main()
                    await bot.send_message(
                        text=f"🔐 You've all the data and they're safe. To go to the main, click on the button below.",
                        chat_id=message.from_user.id,
                        reply_markup=var.as_markup(),
                        parse_mode="HTML"
                    )

            else:
                await bot.edit_message_text(
                    chat_id=message.from_user.id,
                    text=f"❌ <b>Failed!</b>\nYour CW PREMIUM <b>isn't activated</b>!\n\nNow you should:\n"
                         f"- write on EMail: help@cwr.su\n\n"
                         f"🔐 Your refund token:\n<code>{ref_token}</code>.",
                    message_id=msg.message_id,
                    parse_mode="HTML"
                )

                if des == "error":
                    await bot.refund_star_payment(
                        user_id=message.from_user.id,
                        telegram_payment_charge_id=ref_token
                    )

                    await bot.edit_message_text(
                        chat_id=message.from_user.id,
                        text=f"✨ <b>{message.from_user.first_name}</b>, you already have a CW PREMIUM subscription. "
                             f"💞 We have <b>returned</b> the stars back to your account.",
                        message_id=msg.message_id,
                        reply_markup=var.as_markup(),
                        parse_mode="HTML"
                    )
        except Exception as ex:
            await bot.send_message(
                chat_id=admin_id,
                text=f"❕ Admin, we have a problem with successful payment! Error (exception): {ex}.",
                reply_markup=var.as_markup()
            )
            print(ex)
