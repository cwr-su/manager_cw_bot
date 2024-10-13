"""
Module of the GigaChatAI.
"""
import abc
import logging

from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.giga_request import VersionAIPro, VersionAILight
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB
from manager_cw_bot_api.fsm_handler import GetProcessQueryCDLight, GetProcessQueryCDPro

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
            call_query: types.CallbackQuery
    ) -> None:
        self.__bot: Bot = bot
        self.__call_query: types.CallbackQuery = call_query

        router_chat_ai.message.register(
            self.__chat_dialog_light,
            GetProcessQueryCDLight.query
        )

        router_chat_ai.message.register(
            self.__chat_dialog_pro,
            GetProcessQueryCDPro.query
        )

    async def choosing_ai_model(self) -> None:
        """
        Choosing AI-Model (PRO/Light) before Chat-Dialog function.

        :return: None.
        """
        var: InlineKeyboardBuilder = await Buttons.get_var_giga_version(self.__call_query)
        self.__class__.msg_bot = self.__call_query.message

        await self.__bot.edit_message_text(
            chat_id=self.__call_query.from_user.id,
            message_id=self.__call_query.message.message_id,
            text=f"{self.__call_query.from_user.first_name}, please, "
                 f"select the required 🧠 AI-Model, click below.",
            reply_markup=var.as_markup()
        )
        await self.__bot.set_message_reaction(
            chat_id=self.__call_query.from_user.id,
            message_id=self.__call_query.message.message_id,
            reaction=[types.ReactionTypeEmoji(
                types='emoji',
                emoji='🫡'
            )]
        )

        result: tuple = await HandlerDB.check_subscription(self.__call_query)
        if result[0] is True:
            router_chat_ai.callback_query.register(
                self.__giga_version_1,
                F.data == "gigachat_version_light"
            )
            router_chat_ai.callback_query.register(
                self.__giga_version_2,
                F.data == "gigachat_version_pro"
            )
        else:
            router_chat_ai.callback_query.register(
                self.__giga_version_1,
                F.data == "gigachat_version_light"
            )

    async def __giga_version_1(self, call_query: types.CallbackQuery, state: FSMContext) -> None:
        """
        Handler of the callback query by click on the btn1: LightVersion of GigaChat.

        :param call_query: Query (by click on the button) with callback.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(GetProcessQueryCDLight.query)

        await self.__bot.edit_message_text(
            text="Hello! I'm ready to help you! What question are you interested in? 😎\n\n"
                 "_STOP-Command_: `//stop`.",
            chat_id=call_query.message.chat.id,
            message_id=self.__class__.msg_bot.message_id,
            parse_mode="Markdown"
        )

        logging.info(
            "AI dialogue in Light mode - activated!"
        )

    async def __chat_dialog_light(self, message: types.Message, state: FSMContext) -> None:
        """
        GLV Chat-Dialog function.

        :param message: Message of user / query.
        :param state: FSM.

        :return: None.
        """
        cd: ChatDialogGigaVersionLight = ChatDialogGigaVersionLight(self.__bot)
        await cd.chat_dialog(message, state)

    async def __giga_version_2(self, call_query: types.CallbackQuery, state: FSMContext) -> None:
        """
        Handler of the callback query by click on the btn1: PROVersion of GigaChat.

        :param call_query: Query (by click on the button) with callback.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(GetProcessQueryCDPro.query)

        await self.__bot.edit_message_text(
            text="Hello! I'm ready to help you! What question are you interested in? 😎\n\n"
                 "_STOP-Command_: `//stop`.",
            chat_id=call_query.message.chat.id,
            message_id=self.__class__.msg_bot.message_id,
            parse_mode="Markdown"
        )

        logging.info(
            "AI dialogue in PRO mode - activated!"
        )

    async def __chat_dialog_pro(self, message: types.Message, state: FSMContext) -> None:
        """
        GPV Chat-Dialog function.

        :param message: Message of user / query.
        :param state: FSM.

        :return: None.
        """
        cd: ChatDialogGigaVersionPro = ChatDialogGigaVersionPro(self.__bot)
        await cd.chat_dialog(message, state)


class BaseChatDialog(abc.ABC):
    """
    The class for Chat-Dialog function (Base Class-Sector).
    """

    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @abc.abstractmethod
    async def chat_dialog(self, message: types.Message, state: FSMContext) -> None:
        """
        Basic Chat-Dialog function.

        :param message: Message of user / query.
        :param state: FSM.
        
        :return: None.
        """


class ChatDialogGigaVersionLight(BaseChatDialog):
    """
    The class for Chat-Dialog function (GigaLight V. dialog).
    """

    async def chat_dialog(self, message: types.Message, state: FSMContext) -> None:
        """
        GLV Chat-Dialog function.

        :param message: Message of user / query.
        :param state: FSM.

        :return: None.
        """
        if message.text.lower() != "//stop":
            router_chat_ai.message.register(
                ChatDialogGigaVersionLight.chat_dialog,
                GetProcessQueryCDLight.query
            )

            response: str = await VersionAILight.request(message.text)

            await self.bot.send_message(
                text=response,
                chat_id=message.from_user.id,
                parse_mode="Markdown",
            )
            await self.bot.send_message(
                text=f"*If you want to stop this chat, write* `//stop`.\n(Light mode is enabled)",
                chat_id=message.from_user.id,
                parse_mode="Markdown",
            )

            await HandlerDB.update_analytic_datas_count_ai_queries()

            await state.clear()
            new_state: NewFSMContextLight = NewFSMContextLight(self.bot)
            await new_state.set(state)

        else:
            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.bot.send_message(
                text=f"Got it! I have stopped (AI-Chat Dialog).",
                chat_id=message.from_user.id,
                parse_mode="Markdown",
                reply_markup=var.as_markup()
            )

            await state.clear()

            logging.info(
                "AI dialogue in Light mode - deactivated!"
            )


class ChatDialogGigaVersionPro(BaseChatDialog):
    """
    The class for Chat-Dialog function (GigaPro V. dialog).
    """

    async def chat_dialog(self, message: types.Message, state: FSMContext) -> None:
        """
        GLV Chat-Dialog function.

        :param message: Message of user / query.
        :param state: FSM.

        :return: None.
        """
        if message.text.lower() != "//stop":
            router_chat_ai.message.register(
                ChatDialogGigaVersionPro.chat_dialog,
                GetProcessQueryCDPro.query
            )

            response: str = await VersionAIPro.request(message.text)

            await self.bot.send_message(
                text=response,
                chat_id=message.from_user.id,
                parse_mode="Markdown",
            )
            await self.bot.send_message(
                text=f"*If you want to stop this chat, write* `//stop`.\n(Pro mode is enabled)",
                chat_id=message.from_user.id,
                parse_mode="Markdown",
            )

            await HandlerDB.update_analytic_datas_count_ai_queries()

            await state.clear()
            new_state: NewFSMContextPro = NewFSMContextPro(self.bot)
            await new_state.set(state)

        else:
            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            await self.bot.send_message(
                text=f"Got it! I have stopped (AI-Chat Dialog-PRO).",
                chat_id=message.from_user.id,
                parse_mode="Markdown",
                reply_markup=var.as_markup()
            )

            await state.clear()

            logging.info(
                "AI dialogue in PRO mode - deactivated!"
            )


class BaseNewFSMContext(abc.ABC):
    """
    The base-class for create new state (FSM).
    """

    def __init__(self, bot: Bot) -> None:
        self.__bot: Bot = bot

    @abc.abstractmethod
    async def set(self, state: FSMContext) -> None:
        """
        Set state.

        :param state: FSM.
        :return: None.
        """

    @abc.abstractmethod
    async def chat_dialog(self, message: types.Message, state: FSMContext) -> None:
        """
        Chat-Dialog function.

        :param message: Message of user / query.
        :param state: FSM.

        :return: None.
        """


class NewFSMContextLight(BaseNewFSMContext):
    """
    The class for create new state (FSM) - GVL.
    """

    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        router_chat_ai.message.register(
            self.chat_dialog,
            GetProcessQueryCDLight.query
        )

    async def set(self, state: FSMContext) -> None:
        """
        Set state.
        
        :param state: FSM.
        :return: None.
        """
        await state.set_state(GetProcessQueryCDLight.query)

    async def chat_dialog(self, message: types.Message, state: FSMContext) -> None:
        """
        GLV Chat-Dialog function.

        :param message: Message of user / query.
        :param state: FSM.

        :return: None.
        """
        cd: ChatDialogGigaVersionLight = ChatDialogGigaVersionLight(self.__bot)
        await cd.chat_dialog(message, state)


class NewFSMContextPro(BaseNewFSMContext):
    """
    The class for create new state (FSM) - GVL.
    """
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        router_chat_ai.message.register(
            self.chat_dialog,
            GetProcessQueryCDPro.query
        )

    async def set(self, state: FSMContext) -> None:
        """
        Set state.
        
        :param state: FSM.
        :return: None.
        """
        await state.set_state(GetProcessQueryCDPro.query)

    async def chat_dialog(self, message: types.Message, state: FSMContext) -> None:
        """
        GLV Chat-Dialog function.

        :param message: Message of user / query.
        :param state: FSM.

        :return: None.
        """
        cd: ChatDialogGigaVersionPro = ChatDialogGigaVersionPro(self.__bot)
        await cd.chat_dialog(message, state)
