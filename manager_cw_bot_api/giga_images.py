import os
from io import BytesIO

import telebot
from PIL import Image
from telebot import types

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.giga_request import create


class GigaCreator:
    """Class of create image for plus-user."""
    __query: str = ""

    def __init__(self, bot: telebot.TeleBot) -> None:
        self.__bot: telebot.TeleBot = bot

    def get_query(self, call: types.CallbackQuery) -> None:
        """
        Func of get query from plus-user for create image.

        :param call: Callback Query.
        :return: None.
        """
        self.__bot.edit_message_text(
            chat_id=call.message.chat.id,
            text="📸 Enter your query...",
            message_id=call.message.message_id
        )
        self.__bot.register_next_step_handler(
            call.message, self.__check_generate_or_cancel
        )

    def __check_generate_or_cancel(self, message: types.Message) -> None:
        """
        Check generation.

        :param message: Query from user.
        :return: None
        """
        self.__class__.__query = message.text
        self.__bot.send_message(
            chat_id=message.chat.id,
            text=f"{message.from_user.first_name}, are you want to *generate image*? Are you sure?",
            reply_markup=Buttons.generate_image(),
            parse_mode="Markdown"
        )

        self.__bot.register_callback_query_handler(
            callback=self.__handler_query,
            func=lambda call: call.data == "generate"
        )

    def __handler_query(self, call: types.CallbackQuery) -> None:
        """
        Manage of query from plus-user for create image.

        :param call: Call-Query.
        :return: None.
        """
        query: str = self.__class__.__query

        try:
            self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text="💫 Please, wait! I'm generating... ⏳",
                message_id=call.message.message_id
            )
        except Exception:
            self.__bot.send_message(
                chat_id=call.from_user.id,
                text="💫 Please, wait! I'm generating... ⏳",
            )

        image_data: bytes | str = create(query)
        try:
            if image_data == "👌🏻 Sorry! I updated the data. Please, repeat your request :)":
                self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=image_data,
                    message_id=call.message.message_id,
                    reply_markup=Buttons.back_on_main()
                )
            else:
                image: Image = Image.open(BytesIO(image_data))
                temp_image: str = 'AI_Photo_Generate_By_Kandinsky_Manager_PLUS_Version.jpg'
                image.save(temp_image, 'JPEG')

                self.__bot.send_document(
                    chat_id=call.from_user.id,
                    document=open(temp_image, 'rb'),
                    caption=f"<b>{call.from_user.first_name}</b>, the new photo has been generated according to your "
                            f"request: <blockquote>{self.__class__.__query}</blockquote>\n\n"
                            f"✨ There are still generations left: ♾.\n\nThe photo is attached to the message as a "
                            f"file. Download it by clicking on the button above.\n\n"
                            f"#AI_Photo\nDeveloper: @aleksandr_twitt.",
                    parse_mode="HTML",
                    message_effect_id='5104841245755180586'
                )

                os.remove(temp_image)

                self.__bot.send_message(
                    chat_id=call.from_user.id,
                    text="Return to main-menu:",
                    reply_markup=Buttons.back_on_main()
                )

                self.__bot.delete_message(
                    chat_id=call.from_user.id,
                    message_id=call.message.message_id
                )

        except Exception as ex:
            print(ex)
            if "cannot identify image file" in str(ex) or "bytes-like object is required, not 'str'" in str(ex):
                self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=image_data,
                    reply_markup=Buttons.back_on_main(),
                    message_id=call.message.message_id
                )
            else:
                self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text="🤔 Oh, something wrong! 👌🏻 Please, don't worry! Write here: "
                         "@aleksandr_twitt or EMail: help@cwr.su.",
                    reply_markup=Buttons.back_on_main(),
                    message_id=call.message.message_id
                )
