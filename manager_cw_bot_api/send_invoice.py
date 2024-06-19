"""Module of send invoice to users."""
import telebot


class SendInvoice:
    """Class of the send invoice to users for buy/pay plus-subscription."""
    def __init__(self, bot: telebot.TeleBot,
                 message: telebot.types.Message | telebot.types.CallbackQuery
                 ) -> None:
        self.__bot: telebot.TeleBot = bot
        self.__message: telebot.types.Message = message
        self.__chat_id: int = message.from_user.id

    def send_invoice(self) -> None:
        """
        Send Invoice | First pay.

        :return: None.
        """
        self.__bot.send_invoice(
            chat_id=self.__chat_id,
            title="Manager CW Plus Version",
            description=f"Plus-functions for the user {self.__message.from_user.first_name}.",
            invoice_payload="Invoice",
            provider_token="",
            currency="XTR",
            prices=[telebot.types.LabeledPrice(
                "Plus Manager CW Bot", 2
            )],
            photo_url="https://i.postimg.cc/9MYL5XPq/plus-subs-manager-cw-bot.jpg",
            photo_size=67000,
            photo_width=700,
            photo_height=700,

            reply_markup=telebot.types.InlineKeyboardMarkup().row(telebot.types.InlineKeyboardButton(
                text=f"⭐️ Telegram Stars", pay=True
            ))
        )

    def send_invoice_extend(self) -> None:
        """
        Send invoice | Extend.

        :return: None.
        """
        self.__bot.send_invoice(
            chat_id=self.__chat_id,
            title="Manager CW Plus Version",
            description=f"The subscription renewal. "
                        f"Plus-functions for the user {self.__message.from_user.first_name}.",
            invoice_payload="Invoice",
            provider_token="",
            currency="XTR",
            prices=[telebot.types.LabeledPrice(
                "Plus Manager CW Bot", 1
            )],
            photo_url="https://i.postimg.cc/9MYL5XPq/plus-subs-manager-cw-bot.jpg",
            photo_size=67000,
            photo_width=700,
            photo_height=700,

            reply_markup=telebot.types.InlineKeyboardMarkup().row(telebot.types.InlineKeyboardButton(
                text=f"⭐️ Telegram Stars", pay=True
            ))
        )
