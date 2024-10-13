"""Module of the answers."""
import json
import abc
import logging

from aiogram import types, Bot


class ChatAction:
    """The class for set some action for message."""

    @staticmethod
    async def chat_action(bot: Bot, chat_id: int | str, action: str,
                          business_connection_id: str) -> None:
        """
        Send chat action.

        :param bot: The Bot Object.
        :param chat_id: Chat ID.
        :param action: Action.
        :param business_connection_id: Business connection ID.

        :return: None.
        """
        await bot.send_chat_action(
            chat_id=chat_id, action=action,
            business_connection_id=business_connection_id
        )


class Answers:
    """Answers-Class."""

    def __init__(self, business_connection_id, admin_id):
        self.__business_connection_id: str = business_connection_id
        self.__admin_id: int = admin_id

    async def answer_to_user(self, bot: Bot, message: types.Message) -> None:
        """
        Answer to a user from admin-account (as admin).

        :param bot: The Bot Object.
        :param message: Message of a user.
        :return: None.
        """
        chat_id: int = message.from_user.id
        action: str = "typing"

        if message.from_user.id != self.__admin_id:

            with open("bot.json", "r", encoding='utf-8') as file:
                data: dict = json.load(file)

            data: dict = data["BUSINESS_HANDLER"]

            thanks_sticker: str = data["THANKS"]["THANKS_STICKER"]
            congratulation_sticker: str = data["CONGRATULATION"]["CONGRATULATION_STICKER"]
            problem_with_bot_sticker: str = data["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_STICKER"]

            thanks_text: dict = data["THANKS"]["THANKS_TEXT"]
            congratulation_text: dict = data["CONGRATULATION"]["CONGRATULATION_TEXT"]
            problem_with_bot_text: dict = data["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"]

            if "пасиб" in message.text.lower() or "thank" in message.text.lower() \
                    or "благодарю" in message.text.lower() or "спасиб" in message.text.lower():
                thanks_func_sector: FunctionBusinessAnswerThanksSector = (
                    FunctionBusinessAnswerThanksSector(
                        bot,
                        chat_id,
                        action,
                        self.__business_connection_id,
                        thanks_text,
                        thanks_sticker,
                        self.__admin_id
                    )
                )
                await thanks_func_sector.pattern()

            if "с днём рожден" in message.text.lower() or "happy birthday" in \
                    message.text.lower() or "с праздник" in message.text.lower() or \
                    "с днем рожден" in message.text.lower() or message.text.lower() == "с др":
                congratulation_func_sector: FunctionBusinessAnswerCongratulationSector = \
                    FunctionBusinessAnswerCongratulationSector(
                        bot,
                        chat_id,
                        action,
                        self.__business_connection_id,
                        congratulation_text,
                        congratulation_sticker,
                        self.__admin_id
                    )
                await congratulation_func_sector.pattern()

            if ('не работает бот' in message.text.lower() or 'бот не работает' in
                    message.text.lower() or "bot doesn't work" in message.text.lower() or
                    "bot doesnt work" in message.text.lower()):
                bot_doesnt_work_func_sector: FunctionBusinessAnswerBotDoesntWorkSector = \
                    FunctionBusinessAnswerBotDoesntWorkSector(
                        bot,
                        chat_id,
                        action,
                        self.__business_connection_id,
                        problem_with_bot_text,
                        problem_with_bot_sticker,
                        self.__admin_id
                    )
                await bot_doesnt_work_func_sector.pattern()


class BaseFunctionBusinessAnswerSector(abc.ABC):
    """
    The basic class-sector of function business answer (by some patterns).
    """

    def __init__(
            self,
            bot: Bot,
            chat_id: int | str,
            action: str,
            b_c_id: str,
            text_pattern: dict,
            sticker_pattern: str,
            admin_id: int
    ) -> None:
        self._bot: Bot = bot
        self._chat_id: int | str = chat_id
        self._action: str = action
        self._business_connection_id: str = b_c_id
        self._text_pattern: dict = text_pattern
        self._sticker_pattern: str = sticker_pattern
        self._admin_id: int = admin_id

    @abc.abstractmethod
    async def pattern(self) -> None:
        """
        Pattern-function for business answers.

        :return: None.
        """


class FunctionBusinessAnswerThanksSector(BaseFunctionBusinessAnswerSector):
    """
    The class-sector of function business answer (by pattern "thanks").
    """

    async def pattern(self) -> None:
        """
        Pattern-function for business answers by phrases-type: "thanks".

        :return: None.
        """
        await ChatAction.chat_action(
            bot=self._bot,
            chat_id=self._chat_id,
            action=self._action,
            business_connection_id=self._business_connection_id
        )
        try:
            if self._text_pattern["MSG"] != "NONE":
                if self._text_pattern["OFFSET"] != "NONE":
                    await self._bot.send_message(
                        business_connection_id=self._business_connection_id,
                        chat_id=self._chat_id,
                        text=self._text_pattern["MSG"],
                        entities=[types.MessageEntity(
                            type='custom_emoji',
                            offset=self._text_pattern["OFFSET"],
                            length=self._text_pattern["LENGTH"],
                            custom_emoji_id=self._text_pattern["C_E_ID"]
                        )]
                    )
                else:
                    await self._bot.send_message(
                        business_connection_id=self._business_connection_id,
                        chat_id=self._chat_id,
                        text=self._text_pattern["MSG"]
                    )
        except Exception as ex:
            await self._bot.send_message(
                chat_id=self._admin_id,
                text=f"Sorry! The message (THANKS_TEXT) can't send!\n{ex}"
            )
            logging.warning(f"The exception has arisen: {ex}.")
        try:
            if self._sticker_pattern != "NONE":
                await self._bot.send_sticker(
                    business_connection_id=self._business_connection_id,
                    chat_id=self._chat_id,
                    sticker=self._sticker_pattern
                )
        except Exception as ex:
            await self._bot.send_message(
                chat_id=self._admin_id,
                text=f"Sorry! The message (THANKS_STICKER) can't send!\n{ex}"
            )
            logging.warning(f"The exception has arisen: {ex}.")


class FunctionBusinessAnswerCongratulationSector(BaseFunctionBusinessAnswerSector):
    """
    The class-sector of function business answer (by pattern "congratulation").
    """

    async def pattern(self) -> None:
        """
        Pattern-function for business answers by phrases-type: "congratulation".

        :return: None.
        """
        await ChatAction.chat_action(
            bot=self._bot,
            chat_id=self._chat_id,
            action=self._action,
            business_connection_id=self._business_connection_id
        )
        try:
            if self._text_pattern["MSG"] != "NONE":
                if self._text_pattern["OFFSET"] != "NONE":
                    await self._bot.send_message(
                        business_connection_id=self._business_connection_id,
                        chat_id=self._chat_id,
                        text=self._text_pattern["MSG"],
                        entities=[types.MessageEntity(
                            type='custom_emoji',
                            offset=self._text_pattern["OFFSET"],
                            length=self._text_pattern["LENGTH"],
                            custom_emoji_id=self._text_pattern["C_E_ID"]
                        )]
                    )
                else:
                    await self._bot.send_message(
                        business_connection_id=self._business_connection_id,
                        chat_id=self._chat_id,
                        text=self._text_pattern["MSG"]
                    )
        except Exception as ex:
            await self._bot.send_message(
                chat_id=self._admin_id,
                text=f"Sorry! The message (CONGRATULATION_TEXT) can't send!\n{ex}"
            )
            logging.warning(f"The exception has arisen: {ex}.")
        try:
            if self._sticker_pattern != "NONE":
                await self._bot.send_sticker(
                    business_connection_id=self._business_connection_id,
                    chat_id=self._chat_id,
                    sticker=self._sticker_pattern
                )

        except Exception as ex:
            await self._bot.send_message(
                chat_id=self._admin_id,
                text=f"Sorry! The message (CONGRATULATION_STICKER) can't send!\n{ex}"
            )
            logging.warning(f"The exception has arisen: {ex}.")


class FunctionBusinessAnswerBotDoesntWorkSector(BaseFunctionBusinessAnswerSector):
    """
    The class-sector of function business answer (by pattern "bot doesn't work").
    """

    async def pattern(self) -> None:
        """
        Pattern-function for business answers by phrases-type: "bot doesn't work".

        :return: None.
        """
        await ChatAction.chat_action(
            bot=self._bot,
            chat_id=self._chat_id,
            action=self._action,
            business_connection_id=self._business_connection_id
        )
        try:
            if self._text_pattern["MSG"] != "NONE":
                if self._text_pattern["OFFSET"] != "NONE":
                    await self._bot.send_message(
                        business_connection_id=self._business_connection_id,
                        chat_id=self._chat_id,
                        text=self._text_pattern["MSG"],
                        entities=[types.MessageEntity(
                            type='custom_emoji',
                            offset=self._text_pattern["OFFSET"],
                            length=self._text_pattern["LENGTH"],
                            custom_emoji_id=self._text_pattern["C_E_ID"]
                        )]
                    )
                else:
                    await self._bot.send_message(
                        business_connection_id=self._business_connection_id,
                        chat_id=self._chat_id,
                        text=self._text_pattern["MSG"]
                    )
        except Exception as ex:
            await self._bot.send_message(
                chat_id=self._admin_id,
                text=f"Sorry! The message (PROBLEM_WITH_BOT_TEXT) can't send!\n{ex}"
            )
            logging.warning(f"The exception has arisen: {ex}.")
        try:
            if self._sticker_pattern != "NONE":
                await self._bot.send_sticker(
                    business_connection_id=self._business_connection_id,
                    chat_id=self._chat_id,
                    sticker=self._sticker_pattern
                )
        except Exception as ex:
            await self._bot.send_message(
                chat_id=self._admin_id,
                text=f"Sorry! The message (PROBLEM_WITH_BOT_STICKER) can't send!\n{ex}"
            )
            logging.warning(f"The exception has arisen: {ex}.")
