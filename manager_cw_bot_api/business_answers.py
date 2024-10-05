"""Module of the answers."""
import datetime
import json

from aiogram import types, Bot


class Answers:
    """Answers-Class."""

    def __init__(self, business_connection_id, admin_id):
        self.__business_connection_id: str = business_connection_id
        self.__admin_id: int = admin_id

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
        await bot.send_chat_action(chat_id=chat_id, action=action,
                                   business_connection_id=business_connection_id)

    async def answer_to_user(self, bot: Bot, message: types.Message) -> None:
        """
        Answer to a user from admin-account (as admin).

        :param bot: The Bot Object.
        :param message: Message of a user.
        :return: None.
        """
        chat_id: int = message.chat.id
        action: str = "typing"

        if message.from_user.id != self.__admin_id:

            with open("bot.json", "r", encoding='utf-8') as file:
                data: dict = json.load(file)

            data = data["BUSINESS_HANDLER"]

            thanks_sticker = data["THANKS"]["THANKS_STICKER"]
            congratulation_sticker = data["CONGRATULATION"]["CONGRATULATION_STICKER"]
            problem_with_bot_sticker = data["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_STICKER"]

            thanks_text = data["THANKS"]["THANKS_TEXT"]
            congratulation_text = data["CONGRATULATION"]["CONGRATULATION_TEXT"]
            problem_with_bot_text = data["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"]

            if "пасиб" in message.text.lower() or "thank" in message.text.lower() \
                    or "благодарю" in message.text.lower() or "спасиб" in message.text.lower():
                await Answers.chat_action(
                    bot=bot,
                    chat_id=chat_id,
                    action=action,
                    business_connection_id=self.__business_connection_id
                )
                try:
                    if thanks_text["MSG"] != "NONE":
                        if thanks_text["OFFSET"] != "NONE":
                            await bot.send_message(
                                business_connection_id=self.__business_connection_id,
                                chat_id=chat_id,
                                text=thanks_text["MSG"],
                                entities=[types.MessageEntity(
                                    type='custom_emoji',
                                    offset=thanks_text["OFFSET"],
                                    length=thanks_text["LENGTH"],
                                    custom_emoji_id=thanks_text["C_E_ID"]
                                )]
                            )
                        else:
                            await bot.send_message(
                                business_connection_id=self.__business_connection_id,
                                chat_id=chat_id,
                                text=thanks_text["MSG"]
                            )
                except Exception as ex:
                    await bot.send_message(
                        chat_id=self.__admin_id,
                        text=f"Sorry! The message (THANKS_TEXT) can't send!\n{ex}"
                    )
                    with open("logs.txt", 'a') as logs:
                        logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                                   f"__answer_to_user-function of business.py\n")
                try:
                    if thanks_sticker != "NONE":
                        await bot.send_sticker(
                            business_connection_id=self.__business_connection_id,
                            chat_id=chat_id,
                            sticker=thanks_sticker
                        )
                except Exception as ex:
                    await bot.send_message(
                        chat_id=self.__admin_id,
                        text=f"Sorry! The message (THANKS_STICKER) can't send!\n{ex}"
                    )
                    with open("logs.txt", 'a') as logs:
                        logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                                   f"__answer_to_user-function of business.py\n")

            if "с днём рожден" in message.text.lower() or "happy birthday" in \
                    message.text.lower() or "с праздник" in message.text.lower() or \
                    "с днем рожден" in message.text.lower() or message.text.lower() == "с др":
                await Answers.chat_action(
                    bot=bot,
                    chat_id=chat_id,
                    action=action,
                    business_connection_id=self.__business_connection_id
                )
                try:
                    if congratulation_text["MSG"] != "NONE":
                        if congratulation_text["OFFSET"] != "NONE":
                            await bot.send_message(
                                business_connection_id=self.__business_connection_id,
                                chat_id=chat_id,
                                text=congratulation_text["MSG"],
                                entities=[types.MessageEntity(
                                    type='custom_emoji',
                                    offset=congratulation_text["OFFSET"],
                                    length=congratulation_text["LENGTH"],
                                    custom_emoji_id=congratulation_text["C_E_ID"]
                                )]
                            )
                        else:
                            await bot.send_message(
                                business_connection_id=self.__business_connection_id,
                                chat_id=chat_id,
                                text=congratulation_text["MSG"]
                            )
                except Exception as ex:
                    await bot.send_message(
                        chat_id=self.__admin_id,
                        text=f"Sorry! The message (CONGRATULATION_TEXT) can't send!\n{ex}"
                    )
                    with open("logs.txt", 'a') as logs:
                        logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                                   f"__answer_to_user-function of business.py\n")
                try:
                    if congratulation_sticker != "NONE":
                        await bot.send_sticker(
                            business_connection_id=self.__business_connection_id,
                            chat_id=chat_id,
                            sticker=congratulation_sticker
                        )

                except Exception as ex:
                    await bot.send_message(
                        chat_id=self.__admin_id,
                        text=f"Sorry! The message (CONGRATULATION_STICKER) can't send!\n{ex}"
                    )
                    with open("logs.txt", 'a') as logs:
                        logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                                   f"__answer_to_user-function of business.py\n")

            if ('не работает бот' in message.text.lower() or 'бот не работает' in
                    message.text.lower()):
                await Answers.chat_action(
                    bot=bot,
                    chat_id=chat_id,
                    action=action,
                    business_connection_id=self.__business_connection_id
                )
                try:
                    if problem_with_bot_text["MSG"] != "NONE":
                        if problem_with_bot_text["OFFSET"] != "NONE":
                            await bot.send_message(
                                business_connection_id=self.__business_connection_id,
                                chat_id=chat_id,
                                text=problem_with_bot_text["MSG"],
                                entities=[types.MessageEntity(
                                    type='custom_emoji',
                                    offset=problem_with_bot_text["OFFSET"],
                                    length=problem_with_bot_text["LENGTH"],
                                    custom_emoji_id=problem_with_bot_text["C_E_ID"]
                                )]
                            )
                        else:
                            await bot.send_message(
                                business_connection_id=self.__business_connection_id,
                                chat_id=chat_id,
                                text=problem_with_bot_text["MSG"]
                            )
                except Exception as ex:
                    await bot.send_message(
                        chat_id=self.__admin_id,
                        text=f"Sorry! The message (PROBLEM_WITH_BOT_TEXT) can't send!\n{ex}"
                    )
                    with open("logs.txt", 'a') as logs:
                        logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                                   f"__answer_to_user-function of business.py\n")
                try:
                    if problem_with_bot_sticker != "NONE":
                        await bot.send_sticker(
                            business_connection_id=self.__business_connection_id,
                            chat_id=chat_id,
                            sticker=problem_with_bot_sticker
                        )
                except Exception as ex:
                    await bot.send_message(
                        chat_id=self.__admin_id,
                        text=f"Sorry! The message (PROBLEM_WITH_BOT_STICKER) can't send!\n{ex}"
                    )
                    with open("logs.txt", 'a') as logs:
                        logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                                   f"__answer_to_user-function of business.py\n")
