"""Promo-control module."""
import telebot
from telebot import types

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB


class HandlerEP:
    """Class for get plus if user has a promo code."""
    __promo_code: str = ""

    def __init__(self, bot: telebot.TeleBot, admin_id: int) -> None:
        self.__bot: telebot.TeleBot = bot
        self.__admin_id: int = admin_id

    def enter_promo(self, call: types.CallbackQuery) -> None:
        """
        Function for get a promo code from user.

        :param call: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            text="🎫 Enter a promo code...",
            message_id=call.message.message_id
        )
        self.__bot.register_next_step_handler(
            callback=self.__entering_promo_step1,
            message=call.message
        )

    def __entering_promo_step1(self, message: types.Message) -> None:
        """
        Get promo code (text format).

        :param message: A promo code.
        :return: None.
        """
        promo: str = message.text
        checked: bool | tuple = HandlerDB.check_promo_code(promo)
        if checked[0] is False:
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text="❌ *Invalid promo code*.",
                parse_mode="Markdown",
                reply_markup=Buttons.back_on_main()
            )
        elif checked[0] is True:
            type_promo: str = checked[3]

            if type_promo == "plus_month":
                count_days: int = 30
            elif type_promo == "plus_five_days":
                count_days: int = 5
            elif type_promo == "plus_one_week":
                count_days: int = 7
            else:
                count_days: int = 0

            self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"⚠️ Are you sure you want to *apply this promo code* `{promo}`? You'll receive "
                     f"{count_days} days of PLUS.",
                parse_mode="Markdown",
                reply_markup=Buttons.sure_apply_promo()
            )

            self.__class__.__promo_code = promo

            self.__bot.register_callback_query_handler(
                callback=self.__entering_promo_step2,
                func=lambda call: call.data == "apply_promo"
            )

    def __entering_promo_step2(self, call: types.CallbackQuery) -> None:
        """
        Confirmation of apply a promo code.

        :param call: Callback Query.
        :return: None.
        """
        checked_sub: bool | tuple = HandlerDB.sub_promo_code(self.__class__.__promo_code)
        if checked_sub[0] is True:
            count_days: int = 0

            checked: bool | tuple = HandlerDB.check_promo_code(self.__class__.__promo_code)
            if checked[0] is True:
                type_promo: str = checked[3]
                if type_promo == "plus_month":
                    count_days = 30
                elif type_promo == "plus_five_days":
                    count_days = 5
                elif type_promo == "plus_one_week":
                    count_days = 7
                else:
                    count_days = 0
            else:
                pass

            result: bool = HandlerDB.insert_new_record_for_subscribe(
                message=call,
                days=count_days,
                promo=self.__class__.__promo_code
            )
            if result is True:
                self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=f"✅ Successful! Done!\nYour PLUS is *activated*!\n\nNow you can:"
                         f"\n- Use 💥 Kandinsky AI | Generate IMG 🖼\n"
                         f"- 🧠 Use AI-Assistance\n- and more; only MORE!",
                    message_id=call.message.message_id,
                    parse_mode="Markdown",
                    reply_markup=Buttons.back_on_main()
                )

                self.__bot.send_message(
                    chat_id=self.__admin_id,
                    text=f"🆕 Admin, PLUS +1 person! 🔥 | With PROMO: `{self.__class__.__promo_code}` | "
                         f"Days: {count_days}.",
                    parse_mode="Markdown",
                    reply_markup=Buttons.back_on_main()
                )

                if checked_sub[1] == "none":
                    delete: bool = HandlerDB.delete_promo_code(self.__class__.__promo_code)
                    if delete:
                        pass

            else:
                self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=f"❌ Failed!\nYour PLUS *isn't activated*!\n\nNow you should:"
                         f"\n- write on EMail: help@cwr.su.",
                    message_id=call.message.message_id,
                    parse_mode="Markdown"
                )

        elif checked_sub[0] is False:
            self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text=f"❌ Failed!\nYour PLUS *isn't activated*!\n\nNow you should:"
                     f"\n- write on EMail: help@cwr.su.",
                message_id=call.message.message_id,
                parse_mode="Markdown"
            )

    def show_promo_menu_admin(self, call: types.CallbackQuery) -> None:
        """
        Show PROMO Menu. | Control ADMIN.

        :param call: Callback Query.

        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            text=f"*{call.from_user.first_name}*, select the item you need below.\n\n",
            message_id=call.message.message_id,
            reply_markup=Buttons.get_menu_admin_promos(),
            parse_mode="Markdown"
        )

        self.__bot.register_callback_query_handler(
            callback=self.__add_new_promo_code_admin_ctrl,
            func=lambda call_query: call_query.data == "add_new_promo"
        )
        self.__bot.register_callback_query_handler(
            callback=self.__show_promo_datas_admin_ctrl,
            func=lambda call_query: call_query.data == "show_promo_datas"
        )
        self.__bot.register_callback_query_handler(
            callback=self.__delete_promo_data_admin_ctrl,
            func=lambda call_query: call_query.data == "delete_promo_data"
        )

    def __show_promo_datas_admin_ctrl(self, call: types.CallbackQuery) -> None:
        """
        Show PROMO datas. | Control ADMIN.

        :param call: Callback Query.

        :return: None.
        """
        datas: bool | tuple = HandlerDB.show_promo_datas()
        if datas[0] is True:
            self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text=datas[1],
                message_id=call.message.message_id,
                parse_mode="HTML",
                reply_markup=Buttons.back_in_promo_menu()
            )
        elif datas[0] is False:
            self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text=f"🌐 Promo codes *have not been added*.",
                message_id=call.message.message_id,
                parse_mode="Markdown",
                reply_markup=Buttons.back_in_promo_menu()
            )

    def __add_new_promo_code_admin_ctrl(self, call: types.CallbackQuery) -> None:
        """
        Add a new promo. | Control ADMIN. | Confirmation.

        :param call: Callback Query.

        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            text=f"⚠️ Are you sure you want to *add a new promo code*?",
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=Buttons.sure_add_new_promo()
        )

        self.__bot.register_callback_query_handler(
            callback=self.__add_new_promo_admin_ctrl_step1,
            func=lambda call_query: call_query.data == "add_new_promo_confirmation"
        )

    def __add_new_promo_admin_ctrl_step1(self, call: types.CallbackQuery) -> None:
        """
        Add a new promo. | Control ADMIN. | Step 1.

        :param call: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            text=f"👌🏻 *{call.from_user.first_name}*, OK. Create a new promo-data explore this format:\n\n"
                 f"*FORMAT*:\n"
                 f"```Example NEW_PROMO_CODE ~ NUM_USES ~ TYPE_PROMO```\n\n"
                 f"Types of promo codes:\n"
                 f"1. `plus_one_week`;\n"
                 f"2. `plus_five_days`;\n"
                 f"3. `plus_month`;\n",
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )
        self.__bot.register_next_step_handler(
            message=call.message,
            callback=self.__add_new_promo_admin_ctrl_step2
        )

    def __add_new_promo_admin_ctrl_step2(self, message: types.Message) -> None:
        """
        Add a new promo. | Control ADMIN. | Step 2.

        :param message: Message from the admin with PROMO-data.
        :return: None.
        """
        if len(message.text.split(" ~ ")) == 3:
            promo, num_uses, type_promo = message.text.split(" ~ ")
            if int(num_uses) > 0 and len(promo) >= 3:
                checked: bool | tuple = HandlerDB.add_new_promo_code(promo, num_uses, type_promo)
                if checked[0] is True:
                    self.__bot.send_message(
                        chat_id=message.from_user.id,
                        text=f"✅ *Successful*! Done!\n\n{message.from_user.first_name}, *the promo data has been "
                             f"added*!",
                        parse_mode="Markdown",
                        reply_markup=Buttons.back_in_promo_menu()
                    )
                elif checked[0] is False:
                    if checked[1] == "already_exist":
                        self.__bot.send_message(
                            chat_id=message.from_user.id,
                            text=f"❌ *{message.from_user.first_name}*, the promo data *already exists*!",
                            parse_mode="Markdown",
                            reply_markup=Buttons.back_in_promo_menu()
                        )
                    elif checked[1] == "invalid_type":
                        self.__bot.send_message(
                            chat_id=message.from_user.id,
                            text=f"❌ *{message.from_user.first_name}*, the type of promo is *invalid*!",
                            parse_mode="Markdown",
                            reply_markup=Buttons.try_again_add_new_promo_or_back_on_main()
                        )
            else:
                self.__bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"❌ *{message.from_user.first_name}*, sorry. But i can't add your PROMO data!\n\n"
                         f"*Number of uses* must be *>= 1* and *length* of promo code must be *>= 3*!\n",
                    parse_mode="Markdown",
                    reply_markup=Buttons.try_again_add_new_promo_or_back_on_main()
                )

        else:
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"❌ *{message.from_user.first_name}*, sorry. But i can't split your message!\n\n"
                     f"*FORMAT*:\n"
                     f"```Example NEW_PROMO_CODE ~ NUM_USES ~ TYPE_PROMO```\n\n"
                     f"Types of promo codes:\n"
                     f"1. `plus_one_week`;\n"
                     f"2. `plus_five_days`;\n"
                     f"3. `plus_month`;\n",
                parse_mode="Markdown",
                reply_markup=Buttons.try_again_add_new_promo_or_back_on_main()
            )

            self.__bot.register_callback_query_handler(
                callback=self.__add_new_promo_admin_ctrl_step1,
                func=lambda call_query: call_query.data == "try_again_add_new_promo"
            )

    def __delete_promo_data_admin_ctrl(self, call: types.CallbackQuery) -> None:
        """
        Delete promo. | Control ADMIN. | Confirmation.

        :param call: Callback Query.

        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            text=f"⚠️ Are you sure you want to *delete a promo code*?",
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=Buttons.sure_delete_promo()
        )

        self.__bot.register_callback_query_handler(
            callback=self.__delete_promo_data_admin_ctrl_step1,
            func=lambda call_query: call_query.data == "delete_promo_confirmation"
        )

    def __delete_promo_data_admin_ctrl_step1(self, call: types.CallbackQuery) -> None:
        """
        Delete promo. | Control ADMIN. | Step 1.

        :param call: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call.from_user.id,
            text=f"👌🏻 *{call.from_user.first_name}*, OK. Send me the promo code that you want to delete.\n",
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )
        self.__bot.register_next_step_handler(
            message=call.message,
            callback=self.__delete_promo_data_admin_ctrl_step2
        )

    def __delete_promo_data_admin_ctrl_step2(self, message: types.Message) -> None:
        """
        Delete promo. | Control ADMIN. | Step 2.

        :param message: Message from the admin with PROMO-data.
        :return: None.
        """
        promo: str = message.text
        checked: bool = HandlerDB.delete_promo_code(promo)
        if checked is True:
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"✅ *Successful*! Done!\n\n{message.from_user.first_name}, *the promo data has been deleted*!",
                parse_mode="Markdown",
                reply_markup=Buttons.back_in_promo_menu()
            )
        else:
            self.__bot.send_message(
                chat_id=message.from_user.id,
                text=f"❌ *{message.from_user.first_name}*, the promo data *isn't exists*!\n\n"
                     f"Or there was some kind of error when deleting the record. ANSWER: (checked) {checked}.",
                parse_mode="Markdown",
                reply_markup=Buttons.try_again_delete_promo_or_back_on_main()
            )

            self.__bot.register_callback_query_handler(
                callback=self.__delete_promo_data_admin_ctrl_step1,
                func=lambda call_query: call_query.data == "try_again_delete_promo"
            )
