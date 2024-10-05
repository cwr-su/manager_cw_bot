"""
Module of the GigaChatAI.
"""
from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.giga_request import pro, light
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB
from manager_cw_bot_api.fsm_handler import ProcessGigaChatAI

router_chat_ai: Router = Router()


class GigaChatAI:
    """
    Class of the helper for the users and admin - GigaChat.
    """
    msg_bot: types.Message = None
    request_user: str = None

    def __init__(
            self,
            bot: Bot,
            call_query: types.CallbackQuery,
            mysql_data: dict,
            admin_id: int
    ) -> None:
        self.__bot: Bot = bot
        self.__call_query: types.CallbackQuery = call_query
        self.__mysql_data: dict = mysql_data
        self.__admin_id: int = admin_id

        router_chat_ai.message.register(
            self.__request,
            ProcessGigaChatAI.request
        )

    async def show_info_edit_text(self, state: FSMContext) -> None:
        """
        Show pre-answer message by editing text.

        :param state: FSM.
        :return: None.
        """
        await state.set_state(ProcessGigaChatAI.request)
        await self.__bot.edit_message_text(
            text="🧠 Enter your request and then choose the AI-Model...",
            chat_id=self.__call_query.message.chat.id,
            message_id=self.__call_query.message.message_id,
        )

    async def __request(self, message: types.Message, state: FSMContext) -> None:
        """
        Request from the user, handler of the buttons and register callback-query.

        :param message: User message.
        :param state: FSM.

        :return: None.
        """
        await state.clear()
        self.__class__.request_user = message.text

        var: InlineKeyboardBuilder = await Buttons.get_var_giga_version(message)
        self.__class__.msg_bot = await self.__bot.send_message(
            chat_id=message.from_user.id,
            text=f"{message.from_user.first_name}, please, "
                 f"select the required 🧠 AI-Model, click below.",
            reply_markup=var.as_markup()
        )
        await self.__bot.set_message_reaction(
            chat_id=message.from_user.id,
            message_id=message.message_id,
            reaction=[types.ReactionTypeEmoji(
                types='emoji',
                emoji='🫡'
            )]
        )

        result: tuple = await HandlerDB.check_subscription(message)
        if result[0] is True:
            router_chat_ai.callback_query.register(
                self.__giga_version_1,
                F.data == "gigachat_version_light"
            )
            router_chat_ai.callback_query.register(
                self.__giga_version_2,
                F.data == "gigachat_version_pro"
            )
            router_chat_ai.callback_query.register(
                self.__say_thanks,
                F.data == "say_thanks"
            )
        else:
            router_chat_ai.callback_query.register(
                self.__giga_version_1,
                F.data == "gigachat_version_light"
            )
            router_chat_ai.callback_query.register(
                self.__say_thanks,
                F.data == "say_thanks"
            )

    async def __giga_version_1(self, call_query: types.CallbackQuery) -> None:
        """
        Handler of the callback query by click on the btn1: LightVersion of GigaChat.

        :param call_query: Query (by click on the button) with callback.
        :return: None.
        """
        await self.__bot.edit_message_text(
            text="💭 Please, waiting... I'm thinking",
            chat_id=call_query.message.chat.id,
            message_id=self.__class__.msg_bot.message_id
        )

        response = await light(self.__class__.request_user)
        var: InlineKeyboardBuilder = await Buttons.say_thanks()

        try:
            await self.__bot.edit_message_text(
                text=response,
                chat_id=call_query.message.chat.id,
                message_id=call_query.message.message_id,
                parse_mode="Markdown",
                reply_markup=var.as_markup()
            )

        except Exception:
            await self.__bot.edit_message_text(
                text=response,
                chat_id=call_query.message.chat.id,
                message_id=call_query.message.message_id,
                reply_markup=var.as_markup()
            )

    async def __giga_version_2(self, call_query: types.CallbackQuery) -> None:
        """
        Handler of the callback query by click on the btn1: PROVersion of GigaChat.

        :param call_query: Query (by click on the button) with callback.
        :return: None.
        """
        await self.__bot.edit_message_text(
            text="💭 Please, waiting... 🧠 I'm thinking",
            chat_id=call_query.message.chat.id,
            message_id=self.__class__.msg_bot.message_id
        )

        response: str = await pro(self.__class__.request_user)
        var: InlineKeyboardBuilder = await Buttons.say_thanks()

        try:
            await self.__bot.edit_message_text(
                text=response,
                chat_id=call_query.message.chat.id,
                message_id=call_query.message.message_id,
                parse_mode="Markdown",
                reply_markup=var.as_markup()
            )
        except Exception:
            await self.__bot.edit_message_text(
                text=response,
                chat_id=call_query.message.chat.id,
                message_id=call_query.message.message_id,
                reply_markup=var.as_markup()
            )

    async def __say_thanks(self, call_query: types.CallbackQuery) -> None:
        """
        Function counter/sender for count_of_thanks_from_users.

        :param call_query: Callback Query.
        :return: None.
        """
        if call_query.from_user.id == self.__admin_id:
            var: InlineKeyboardBuilder = await Buttons.get_menu_admin()
            await self.__bot.send_message(
                chat_id=call_query.from_user.id,
                text=f"👑 <b>{call_query.from_user.first_name}</b>, thank you for your feedback! 💞🙏\n"
                     f"You are in the main menu. Select the desired item below!\n"
                     f"\nUsing the services CWR.SU (CW), you accept all the rules and the agreement. "
                     f"<a href="
                     f"'https://acdn.cwr.su/src/acdn/Agreement_and_Terms_of_Use_for_the_Manager_CW_Bot_Service.pdf'>SEE"
                     f"</a>.",
                reply_markup=var.as_markup(),
                parse_mode="HTML"
            )
        else:
            checked: bool | tuple = await HandlerDB.check_subscription(call_query)
            if checked[0] is False:
                var: InlineKeyboardBuilder = await Buttons.get_menu_without_premium()
                await self.__bot.send_message(
                    chat_id=call_query.from_user.id,
                    text="💡 You are in the main menu. Select the desired item below!, thank you for your feedback! "
                         "💞🙏\n\nUsing the services CWR.SU (CW), you accept all the rules and the agreement. "
                         f"<a href="
                         f"'https://acdn.cwr.su/src/acdn/Agreement_and_Terms_of_Use_for_the_Manager_CW_Bot_Service.pdf'"
                         f">SEE</a>.",
                    reply_markup=var.as_markup(),
                    parse_mode="HTML"
                )
            elif checked[0] is True:
                var: InlineKeyboardBuilder = await Buttons.get_menu_with_premium()
                await self.__bot.send_message(
                    chat_id=call_query.from_user.id,
                    text=f"👑 <b>{call_query.from_user.first_name}</b>, thank you for your feedback! 💞🙏\n"
                         f"You are in the main menu. Select the desired item below!\n"
                         f"\nUsing the services CWR.SU (CW), you accept all the rules and the agreement. "
                         f"<a href="
                         f"'https://acdn.cwr.su/src/acdn/Agreement_and_Terms_of_Use_for_the_Manager_CW_Bot_Service.pdf'"
                         f">SEE</a>.",
                    reply_markup=var.as_markup(),
                    parse_mode="HTML"
                )
        var: InlineKeyboardBuilder = await Buttons.back_on_main()
        await self.__bot.send_message(
            chat_id=self.__admin_id,
            text=f"{call_query.from_user.first_name} thanked you! 💖",
            reply_markup=var.as_markup()
        )

        await HandlerDB.update_analytic_datas()
