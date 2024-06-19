"""Module of the control successful payments."""
import telebot
from telebot import types

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB


class HandlerSP:
    """Class-handler for successful payments."""
    @staticmethod
    def add_new_record(bot: telebot.TeleBot, message: types.Message, admin_id: int) -> None:
        """
        Add a new record in database.

        :param bot: The object of Telegram Bot.
        :param message: Message of the successful payment by Stars.
        :param admin_id: Telegram Admin ID.

        :return: bool.
        """

        try:
            msg: types.Message = bot.send_message(
                chat_id=message.chat.id,
                text=f"💖 Thanks! The asterisk was received!\n\n⚠ Token for refund stars: "
                     f"`{message.successful_payment.telegram_payment_charge_id}`\n\nPlease, wait! I'm activating "
                     f"your subscription...⏳",
                message_effect_id="5046509860389126442",
                parse_mode="Markdown"
            )
            result: bool = HandlerDB.insert_new_record_for_subscribe(
                message=message,
                days=30,
                token_successful_payment=message.successful_payment.telegram_payment_charge_id
            )
            if result is True:
                bot.edit_message_text(
                    chat_id=message.from_user.id,
                    text=f"✅ Successful! Done!\nYour PLUS is *activated*!\n\nNow you can:"
                         f"\n- Use 💥 Kandinsky AI | Generate IMG 🖼\n"
                         f"- 🧠 Use AI-Assistance\n- and more; only MORE!\n"
                         f"Your refund token: `{message.successful_payment.telegram_payment_charge_id}`.",
                    message_id=msg.message_id,
                    parse_mode="Markdown",
                    reply_markup=Buttons.back_on_main()
                )
                bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"✅ Successful! Done!\nYour PLUS is *activated*!\n\nNow you can:"
                         f"\n- Use 💥 Kandinsky AI | Generate IMG 🖼\n"
                         f"- 🧠 Use AI-Assistance\n- and more; only MORE!\n"
                         f"Your refund token: `{message.successful_payment.telegram_payment_charge_id}`.",
                    parse_mode="Markdown",
                    reply_markup=Buttons.back_on_main()
                )
                bot.send_message(
                    chat_id=admin_id,
                    text=f"🆕 Admin, PLUS +1 person! 🔥",
                    reply_markup=Buttons.back_on_main()
                )

            else:
                bot.edit_message_text(
                    chat_id=message.from_user.id,
                    text=f"❌ Failed!\nYour PLUS *isn't activated*!\n\nNow you should:"
                         f"\n- write on EMail: help@cwr.su\n"
                         f"Your refund token: `{message.successful_payment.telegram_payment_charge_id}`.",
                    message_id=msg.message_id,
                    parse_mode="Markdown"
                )

                bot.refund_star_payment(
                    user_id=message.from_user.id,
                    telegram_payment_charge_id=message.successful_payment.telegram_payment_charge_id
                )

                bot.edit_message_text(
                    chat_id=msg.from_user.id,
                    text=f"✨ {message.from_user.first_name}, you already have a PLUS subscription. "
                         f"💞 We have returned the stars back to your account.",
                    message_id=msg.message_id,
                    reply_markup=Buttons.back_on_main()
                )
        except Exception as ex:
            bot.send_message(
                chat_id=admin_id,
                text=f"Admin, we have a problem with successful payment! Error (exception): {ex}.",
                reply_markup=Buttons.back_on_main()
            )
