Example of a bot.json file
==========================

Below is a sample code of the ``bot.json`` file.
------------------------------------------------
.. code-block:: python
    :linenos:

    {
        "BOT_TOKEN": "NUM_STR_TYPE",
        "update_id": "INT-FLOAT_TYPE",
        "business_connection": {
            "id": "STR_TYPE",
            "user": {
                "id": "INT-FLOAT_TYPE",
                "is_bot": "BOOL_STR_TYPE",
                "first_name": "STR_TYPE",
                "last_name": "STR_TYPE",
                "username": "STR_TYPE",
                "language_code": "STR_TYPE",
                "is_premium": "BOOL_STR_TYPE"
            },
            "user_chat_id": "INT-FLOAT_TYPE",
            "date": "INT-FLOAT_TYPE",
            "can_reply": "BOOL_STR_TYPE",
            "is_enabled": "BOOL_STR_TYPE"
        },
        "GIGACHAT": {
            "TOKEN": "STR_TYPE",
            "AUTH_TOKEN": "STR_TYPE",
            "ANSWER_SETTING": {
                "TEMPERATURE": "INT-FLOAT_TYPE",
                "TOP_P": "INT-FLOAT_TYPE",
                "N": "INT-FLOAT_TYPE"
            }
        },
        "MYSQL": {
            "HOST": "STR_TYPE",
            "USERNAME": "STR_TYPE",
            "PASSWORD": "STR_TYPE",
            "PORT": "INT-FLOAT_TYPE",
            "DB_NAME": "STR_TYPE"
        },
        "BUSINESS_HANDLER": {
            "THANKS": {
                "THANKS_STICKER": "NONE",
                "THANKS_TEXT": {
                    "MSG": "🙏 thanks",
                    "OFFSET": 0,
                    "LENGTH": 2,
                    "C_E_ID": "5285070644864628879"
                }
            },
            "CONGRATULATION": {
                "CONGRATULATION_STICKER": "NONE",
                "CONGRATULATION_TEXT": {
                    "MSG": "☺️ Спасибо большое! 🙏",
                    "OFFSET": 0,
                    "LENGTH": 2,
                    "C_E_ID": "5427161992811004191"
                }
            },
            "PROBLEM_WITH_BOT": {
                "PROBLEM_WITH_BOT_STICKER": "CAACAgIAAxkBAAEBYCVmP0fUN7Ku4cFsiH8r5ao4G0-7HQACkEMAAt5q0UtcycYGwYpCCTUE",
                "PROBLEM_WITH_BOT_TEXT": {
                    "MSG": "Здравствуйте! Принято. Сейчас начнём устранять проблему 🤖. Для начала, напишите Ваш EMail для связи с Вами и для разработчика (чтобы устранить проблему). Ожидаю.",
                    "OFFSET": 56,
                    "LENGTH": 2,
                    "C_E_ID": "5775888014119015271"
                }
            }
        }
    }