"""Refunding module."""
import telebot
from telebot import types

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB, SubOperations


class Refund:
    """Class of a refund."""
    def __init__(self, bot: telebot.TeleBot) -> None:
        self.__bot: telebot.TeleBot = bot
        self.__refund_token: str = ""

    def refunding_step1_confirmation(self, call: types.CallbackQuery) -> None:
        """
        Call-Handler for refund stars | Step 1 - Confirmation.

        :param call: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="#️⃣ Enter the REFUND-token..."
        )
        self.__bot.register_next_step_handler(
            call.message, self.__refunding_step2_confirmation
        )

    def __refunding_step2_confirmation(self, message: types.Message) -> None:
        """
        Refunding star(-s) to user | Step 2 - Confirmation.

        :param message: Token from user.
        :return: None.
        """
        self.__refund_token = message.text

        if self.__refund_token != "PROMO":
            checked: tuple = HandlerDB.check_subscription_by_refund_token(self.__refund_token)
            if checked[0] is False:
                if checked[2] == "none":
                    self.__bot.send_message(
                        chat_id=message.from_user.id,
                        text=f"⚠️ *{message.from_user.first_name}*, are you sure? I could not find this REFUND-"
                             f"Token in the database. It may not have been added in time due to problems on the "
                             f"server side.\n\nIf you see that the token looks like a real one, click the "
                             f"corresponding button below. BUT if you are not sure that this isn't a real token, "
                             f"click '❌ Cancel'!\n\n"
                             f"⚠ This step is registered!",
                        parse_mode="Markdown",
                        reply_markup=Buttons.sure_refund_confirmation()
                    )

                    self.__bot.register_callback_query_handler(
                        callback=self.__refunding_step3,
                        func=lambda call: call.data == "refund_confirmation"
                    )
                elif checked[1] == "ex_sub":
                    self.__bot.send_message(
                        chat_id=message.from_user.id,
                        text=f"⚠️ *{message.from_user.first_name}*, are you sure? I found "
                             f"a user, but his subscription has expired!\n\n"
                             f"⚠ This step is registered!",
                        parse_mode="Markdown",
                        reply_markup=Buttons.sure_refund_confirmation()
                    )

                    self.__bot.register_callback_query_handler(
                        callback=self.__refunding_step3,
                        func=lambda call: call.data == "refund_confirmation"
                    )
            elif checked[0] is True:
                remains = round(SubOperations.sec_to_days(checked[1]))
                d = "days"

                if remains > 1:
                    d = "days"
                elif remains == 1:
                    d = "day"

                self.__bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"⚠️ *{message.from_user.first_name}*, are you sure? The subscription ends after *{remains} "
                         f"{d}*. If necessary, notify the user about this!"
                         f"\n\nAfter the star(s) are returned, the *subscription will be disabled*!\n"
                         f"But *user can resume* it at any other time by clicking on *Get PLUS* in main menu.",
                    parse_mode="Markdown",
                    reply_markup=Buttons.sure_refund_confirmation()
                )

                self.__bot.register_callback_query_handler(
                    callback=self.__refunding_step3,
                    func=lambda call: call.data == "refund_confirmation"
                )
            else:
                self.__bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"🚫 *{message.from_user.first_name}*, sorry. But I can't make a refund. "
                         f"That's a PROMO-REF-Token! (We can't make a refund on it).",
                    parse_mode="Markdown",
                    reply_markup=Buttons.back_on_main()
                )

    def __refunding_step3(self, call: types.CallbackQuery) -> None:
        """
        Refunding. The admin has confirmed the actions.

        :param call: Callback Query.
        :return: None.
        """
        try:
            self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text="⏳ Starting the refund...",
                message_id=call.message.message_id
            )

            check: bool | tuple = HandlerDB.check_subscription_by_refund_token(self.__refund_token)
            if check[2] != "none":
                self.__bot.refund_star_payment(
                    user_id=check[2],
                    telegram_payment_charge_id=self.__refund_token
                )

                deleted: bool | tuple = HandlerDB.delete_record_for_subscribe(self.__refund_token)

                if deleted[0] is True:
                    self.__bot.edit_message_text(
                        chat_id=call.from_user.id,
                        text="✅ Completed the refund ✨",
                        message_id=call.message.message_id,
                        reply_markup=Buttons.back_on_main()
                    )

                    firstname: str = deleted[2]
                    self.__bot.send_message(
                        chat_id=check[2],
                        text=f"ℹ {firstname}, Your star(s) have been returned!",
                        reply_markup=Buttons.back_on_main()
                    )

                else:
                    self.__bot.edit_message_text(
                        chat_id=call.from_user.id,
                        text="⚠ Something wrong! Check your balance.",
                        message_id=call.message.message_id,
                        reply_markup=Buttons.back_on_main()
                    )

            elif check[2] == "none":
                self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=f"⚠️ *{call.from_user.first_name}*, are you sure? I could not find the User ID to return "
                         f"the stars. If you are sure that this is a real REFUND Token, click the corresponding "
                         f"button below. If not, then click on '❌ Cancel'!",
                    parse_mode="Markdown",
                    message_id=call.message.message_id,
                    reply_markup=Buttons.sure_emergency_refund_confirmation()
                )

                self.__bot.register_callback_query_handler(
                    callback=self.__emergency_refunding_step1,
                    func=lambda call_query: call_query.data == "emergency_refund_confirmation"
                )

        except Exception as t_ex:
            if "CHARGE_ALREADY_REFUNDED" in str(t_ex):
                self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=f"🚫 *{call.from_user.first_name}*, sorry. But I can't make a refund by this ("
                         f"`{self.__refund_token}`) "
                         f"token.\n\n❌ Error: There has already been a refund for this token!"
                         f"\n\nPlease, write: help@cwr.su for support.",
                    message_id=call.message.message_id,
                    parse_mode="Markdown",
                    reply_markup=Buttons.back_on_main()
                )
            else:
                self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=f"🚫 *{call.from_user.first_name}*, sorry. But I can't make a refund by this ("
                         f"`{self.__refund_token}`) "
                         f"token.\n\nPlease, write: help@cwr.su for support.",
                    message_id=call.message.message_id,
                    parse_mode="Markdown",
                    reply_markup=Buttons.back_on_main()
                )

    def __emergency_refunding_step1(self, call: types.CallbackQuery) -> None:
        """
        Emergency Refund by admin. | Step 1 | Confirmation.

        :param call: Callback Query.
        :return: None.
        """
        try:
            self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text=f"👌🏻 *{call.from_user.first_name}*, OK. Tell me the 👤 User ID "
                     f"(To confirm the operation).\n\n"
                     f"The user has it (User ID) in the *My PLUS"
                     f" -> My ID section*.",
                message_id=call.message.message_id,
                parse_mode="Markdown"
            )

            self.__bot.register_next_step_handler(
                message=call.message,
                callback=self.__emergency_refunding_step2
            )
        except Exception as ex:
            self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text=f"❌ *{call.from_user.first_name}*, Error! Exception-prog: {ex}.",
                message_id=call.message.message_id,
                parse_mode="Markdown"
            )

    def __emergency_refunding_step2(self, message: types.Message) -> None:
        """
        Emergency Refund by admin. | Step 2 | Confirmation.

        :param message: UserID.
        :return: None.
        """
        try:
            user_id = message.text

            msg: types.Message = self.__bot.send_message(
                chat_id=message.from_user.id,
                text="⏳ Starting the refund...",
            )

            self.__bot.refund_star_payment(
                user_id=int(user_id),
                telegram_payment_charge_id=self.__refund_token
            )

            self.__bot.edit_message_text(
                chat_id=message.from_user.id,
                text="✅ Completed the refund ✨",
                message_id=msg.message_id,
                reply_markup=Buttons.back_on_main()
            )

            self.__bot.send_message(
                chat_id=int(user_id),
                text=f"ℹ [{user_id}] Your star(s) have been returned!",
                reply_markup=Buttons.back_on_main()
            )

        except Exception as ex:
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"❌ *{message.from_user.first_name}*, Error! Exception-prog: {ex}.",
                parse_mode="Markdown"
            )
