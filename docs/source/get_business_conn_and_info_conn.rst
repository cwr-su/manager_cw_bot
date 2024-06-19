Get business connection and info conn
=====================================

Get business connection and data from that (by requests)
--------------------------------------------------------
HOW TO GET THE BUSINESS_CONNECTION:

.. attention::
   1. Make sure that all bots have business mode TURNED OFF (in `@BotFather <https://t.me/BotFather>`_ [1]_).

   2. Then, turn on business mode in the desired bot.

   3. Update the api key (preferably).

   4. Go to the Telegram Business tab in Telegram and go to the CHATBOT section.

   5. In the (ChatBot) section, add a bot, in which to turn on Business Mode, wait ~ 3 seconds.

   6. Write any message to the bot, And write to the account of the bot owner (your own) from any other Telegram account (you can ask your friend, or from your second account, or in any other way, but so that the sender is a human account).

   7. Launch main.py , which contains the first template code from the section "Installation lib, configuration and run the bot" (you should have copied it in advance, but if you didn't, do it now: `GO <./installation.html>`_).

   8. Find the business_connection data in the result-response line.

   9. Copy and DO NOT delete this data (ID is the id key in the business_connection key).

   10. IF this section is NOT AVAILABLE, add a new bot or/and follow all the above steps again.

.. important::
   This is just a sample instruction! If you have any questions, please write here: help@cwr.su.

-----

.. automodule:: get_business_conn_and_info_conn
   :members:
   :private-members:

-----

.. [1] @BotFather. The bot that allows you (as an admin) to control
   the bot(s): create/delete
   them, change their settings, etc.