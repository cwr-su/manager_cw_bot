import logging
import os
from io import BytesIO

from PIL import Image
from aiogram import types, Bot, Router, F
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.giga_request import VersionAIImagePro
from manager_cw_bot_api.fsm_handler import GigaImage
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB

router_ai_img: Router = Router()


class GigaCreator:
    """Class of create image for premium-user."""
    __query: str = ""

    def __init__(self, bot: Bot) -> None:
        self.__bot: Bot = bot

        router_ai_img.message.register(
            self.__check_generate_or_cancel,
            GigaImage.request
        )

    async def get_query(self, call: types.CallbackQuery, state: FSMContext) -> None:
        """
        Func of get query from premium-user for create image.

        :param call: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(GigaImage.request)
        await self.__bot.edit_message_text(
            chat_id=call.message.chat.id,
            text="📸 Enter your query...",
            message_id=call.message.message_id
        )

    async def __check_generate_or_cancel(self, message: types.Message, state: FSMContext) -> None:
        """
        Check generation.

        :param message: Query from user.
        :param state: FSM.

        :return: None
        """
        await state.clear()
        var: InlineKeyboardBuilder = await Buttons.generate_image()
        self.__class__.__query = message.text
        await self.__bot.send_message(
            chat_id=message.chat.id,
            text=f"{message.from_user.first_name}, are you want to *generate image*? "
                 f"Are you sure?",
            reply_markup=var.as_markup(),
            parse_mode="Markdown"
        )
        await self.__bot.set_message_reaction(
            chat_id=message.from_user.id,
            message_id=message.message_id,
            reaction=[types.ReactionTypeEmoji(
                types='emoji',
                emoji='🫡'
            )]
        )
        router_ai_img.callback_query.register(
            self.__handler_query,
            F.data == "generate"
        )

    async def __handler_query(self, call: types.CallbackQuery) -> None:
        """
        Manage of query from premium-user for create image.

        :param call: Call-Query.
        :return: None.
        """
        query: str = self.__class__.__query

        try:
            await self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text="💫 Please, wait! I'm generating... ⏳",
                message_id=call.message.message_id
            )
        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")

            await self.__bot.send_message(
                chat_id=call.from_user.id,
                text="💫 Please, wait! I'm generating... ⏳",
            )

        image_data: str | bytes = await VersionAIImagePro.request(query)
        try:
            if image_data == "Sorry! I updated the data. Please, repeat your request :)":
                var: InlineKeyboardBuilder = await Buttons.back_on_main()
                await self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=image_data,
                    message_id=call.message.message_id,
                    reply_markup=var.as_markup()
                )
            else:
                image: Image = Image.open(BytesIO(image_data))
                temp_image: str = 'AI_Photo_By_CW_PREMIUM_Version.jpg'
                image.save(temp_image, 'JPEG')

                await self.__bot.send_document(
                    chat_id=call.from_user.id,
                    document=FSInputFile(temp_image),
                    caption=f"<b>{call.from_user.first_name}</b>, the new photo has been generated"
                            f" according to your request: <blockquote>{self.__class__.__query}"
                            f"</blockquote>\n\n✨ There are still generations left: ♾.\n\nThe "
                            f"photo is attached to the message as a file. Download it by clicking "
                            f"on the button above.\n\n"
                            f"#AI_Photo\nDeveloper: @aleksandr_twitt.",
                    parse_mode="HTML",
                    message_effect_id='5104841245755180586'
                )

                os.remove(temp_image)

                var: InlineKeyboardBuilder = await Buttons.back_on_main()
                await self.__bot.send_message(
                    chat_id=call.from_user.id,
                    text="Return to main-menu:",
                    reply_markup=var.as_markup()
                )

                await HandlerDB.update_analytic_datas_count_ai_queries()

                await self.__bot.delete_message(
                    chat_id=call.from_user.id,
                    message_id=call.message.message_id
                )

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")

            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            if ("cannot identify image file" in str(ex) or
                    "bytes-like object is required, not 'str'" in str(ex)):
                await self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=image_data,
                    reply_markup=var.as_markup(),
                    message_id=call.message.message_id
                )
            else:
                await self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text="🤔 Oh, something wrong! 👌🏻 Please, don't worry! "
                         "Write ticket or EMail: help@cwr.su.",
                    reply_markup=var.as_markup(),
                    message_id=call.message.message_id
                )
