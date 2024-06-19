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

   1. Create a file in your project directory: ``bot.json``.

   2. Create a file ``main.py`` (in the same directory) and go to it.

   3. Write the following code in it (replacing YOUR_TOKEN with your bot's token received from `@BotFather <https://t.me/BotFather>`_) (1):

   .. code-block:: python
       :linenos:

       from manager_cw_bot_api import get_business_conn_and_info_conn

       def run() -> None:
           print(get_business_conn_and_info_conn.gets("YOUR_TOKEN"))

       if __name__ == "__main__":
           run()


   4. Before executing the code, read the more detailed instructions here: `Get Business connection and info connection-obj <./get_business_conn_and_info_conn.html>`_.

   5. Next, once you have received the data to insert into the bot.json (`bot.json <./example_bot_json.html>`_) - clear the main.py and enter the following in it (2):

   .. code-block:: python
       :linenos:

       from manager_cw_bot_api import main

       def run() -> None:
           main()

       if __name__ == "__main__":
           run()


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