Installation lib, configuration and run the bot
===============================================

Read the rules / instruction for install lib and run your bot
-------------------------------------------------------------

.. attention::
   If you still haven't installed the library, use the pip command:

   ``pip install manager_cw_bot_api``

.. important::
   Before running the file, make sure that you have received the API key from `@BotFather <https://t.me/BotFather>`_ [1]_,
   data for connecting to MySQL, business_connection_id (after enabling Business mode
   in `@BotFather <https://t.me/BotFather>`_).

   Instructions for connecting the bot [2]_:

   1. Create a file in your project directory: ``bot.json`` (`example here <./example_bot_json.html>`_).

   2. Create a file ``main.py`` (in the same directory) and go to it.

   3. Write the following code in it (replacing YOUR_TOKEN with your bot's token received from `@BotFather <https://t.me/BotFather>`_) (1):

   .. code-block:: python
       :linenos:

       from manager_cw_bot_api import get_business_conn_and_info_conn

       def run() -> None:
           print(get_business_conn_and_info_conn.gets("YOUR_TOKEN"))

       if __name__ == "__main__":
           run()

   4. Add a folder called ``styles`` to the directory with the ``bot.json`` and ``main.py`` . Next, you need to add 5 to it files:

   - 3 files with fonts of REGULAR, BOLD, ITALIC types, ``.ttf`` format.

   - A ``.png`` file with a stamp/seal for CW documents and a ``.png`` logo file. - YOU CAN GET ALL THESE FILES FOR FREE `HERE <https://acdn.cwr.su/src/storage/zip_file_styles/>`_.

   5. Before executing the code, read the more detailed instructions here: `Get Business connection and info connection-obj <./get_business_conn_and_info_conn.html>`_.

   6. To find out the GIGACHAT API (RU / EN) data, you need to visit the website: https://developers.sber.ru/studio/workspaces/ and then their API, in order to get the TOKEN: https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/post-token . The rest of the data (AUTH_TOKEN (for entering into the bot.json file), client_secret and client_id (id is your EMail address that you specified during registration)) you need to get it in your personal account. To do this, FOLLOW the INSTRUCTIONS of the official SBER API: https://developers.sber.ru/docs/ru/gigachat/individuals-quickstart (for phys. persons / self-employed) or https://developers.sber.ru/docs/ru/gigachat/legal-quickstart (for legal entities, sole proprietors, and organizations).

   7. Next, once you have received the data to insert into the bot.json (`bot.json <./example_bot_json.html>`_) - clear the main.py and enter the following in it (2):\

   .. code-block:: python
       :linenos:

       """
       Main Module of the Manager and helper-bot-manager.
       """
       import logging
       import asyncio
       import sys
       from manager_cw_bot_api.business import run


       # Do not break the structure of func-s, classes, and components to make the modules work correctly.
       async def main() -> None:
           """Main Function (run bot)."""
           logging.basicConfig(
               level=logging.INFO,
               stream=sys.stdout,
               format='%(levelname)s: %(asctime)s -- %(funcName)s -- %(message)s',
               datefmt='%d-%m-%Y %H:%M:%S'
           )

           await run()


       if __name__ == '__main__':
           asyncio.run(main())


   Familiarize yourself with this rule to create the configuration
   (in the file) of the bot.

   If you have any questions, please contact us by email: help@cwr.su.

-----

.. [1] @BotFather. The bot that allows you (as an admin) to control
   the bot(s): create/delete
   them, change their settings, etc.

.. [2] Telegram Bot API. API for the telegram bot(s).
   An API key is required for use (both through requests and
   through third-party libraries: pyTelegramBotAPI, aiogram and others)