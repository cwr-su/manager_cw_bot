"""Module for control the database."""
import json
import time

import pymysql
from telebot import types

from manager_cw_bot_api.mysql_connection import Connection


class HandlerDB:
    """Handler-class for manage database."""
    @staticmethod
    def get_data(file_path="bot.json") -> dict:
        """
        Get data of the Alex's Manager Bot.

        :param file_path: File Path of JSON-API-keys for Bot.

        :return: Dict with data.
        """
        with open(file_path, "r", encoding='utf-8') as file:
            data: dict = json.load(file)

            dct = dict()

            dct["MYSQL"] = data["MYSQL"]

            return dct["MYSQL"]

    @staticmethod
    def update_analytic_datas() -> None:
        """
        Update analytic datas.

        :return: None.
        """
        connection: pymysql.Connection = Connection.get_connection(HandlerDB.get_data())
        cursor = connection.cursor()

        query: str = "SELECT count_of_thanks_from_users FROM analytics"
        cursor.execute(query)
        count_of_thanks_from_users = cursor.fetchall()

        if len(count_of_thanks_from_users) == 0:
            query: str = f"""INSERT INTO analytics (count_of_thanks_from_users)
                         VALUES ({1});"""
            cursor.execute(query)
        else:
            query: str = f"""UPDATE analytics SET 
                         count_of_thanks_from_users = {count_of_thanks_from_users[0][0] + 1}"""
            cursor.execute(query)

        connection.commit()
        connection.close()

    @staticmethod
    def get_ticket_data(username: str, markup: types.InlineKeyboardMarkup) -> types.InlineKeyboardMarkup | str:
        """
        Get ticket data.

        :param username: User's name -- username.
        :param markup: Markup.

        :return: None.
        """
        connection: pymysql.Connection = Connection.get_connection(HandlerDB.get_data())
        cursor = connection.cursor()

        query: str = f"SELECT id_ticket, create_at, subject FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result: tuple = cursor.fetchall()
        response: str = ""
        if len(result) > 0:
            for i in range(len(list(result))):
                response += (f"<b>{i + 1}</b>. ID_TCK: <code>{result[i][0]}</code>| "
                             f"CREATE_AT: {result[i][1]}| "
                             f"Subject: <blockquote>'{result[i][2]}'</blockquote>\n")

                connection.close()
                return response
        else:
            btn: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text=f"Not Found", callback_data="not_found"
            )
            markup.row(btn)

            connection.close()
            return markup

    @staticmethod
    def get_users_tickets_for_admin() -> types.InlineKeyboardMarkup | str:
        """
        Get ticket data.

        :return: None.
        """
        connection: pymysql.Connection = Connection.get_connection(HandlerDB.get_data())
        cursor = connection.cursor()

        query: str = "SELECT id_ticket, username, create_at, subject FROM users"
        cursor.execute(query)
        result: tuple = cursor.fetchall()

        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        response: str = ""

        if len(result) > 0:
            for i in range(len(list(result))):
                response += (f"<b>{i + 1}</b>. Sender: "
                             f"@{result[i][1]}| ID_TCK: <code>{result[i][0]}</code>| CREATE_AT: "
                             f"{result[i][2]}| Subject: "
                             f"<blockquote>'{result[i][3]}'</blockquote>\n")

                connection.close()
                return response
        else:
            btn: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text=f"Not Found", callback_data="not_found"
            )
            markup.row(btn)
            connection.close()
            return markup

    @staticmethod
    def insert_new_record_for_subscribe(
            message: types.Message | types.CallbackQuery,
            days: int,
            token_successful_payment: str = "PROMO",
            promo: str = "none"
    ) -> bool:
        """
        Insert a new record to database | Manager Plus Subscription.

        :param message: Message from user.
        :param days: Count of days for use PLUS.
        :param token_successful_payment: Token of successful payment.
        :param promo: A promo code.

        :return: bool.
        """
        time_of_pay: int = int(time.time())
        ex_time_for_sub: int = time_of_pay + SubOperations.days_to_sec(days)

        connection: pymysql.Connection = Connection.get_connection(HandlerDB.get_data())
        cursor = connection.cursor()

        query: str = f"""SELECT subscribe_date FROM plus_users WHERE tg_id = %s;"""
        cursor.execute(query, (str(message.from_user.id),))
        result: tuple = cursor.fetchall()
        if len(result) == 0:
            insert_q = f"""INSERT INTO plus_users (tg_id, username, firstname, cost_in_stars, refund_token,
                       subscribe_date, promo_code) VALUES ('{message.from_user.id}', '{message.from_user.username}', 
                       '{message.from_user.first_name}', 1, '{token_successful_payment}', 
                       {ex_time_for_sub}, '{promo}');"""
            cursor.execute(insert_q)
            connection.commit()
            connection.close()

            return True
        else:
            checked: tuple = HandlerDB.check_subscription(message)
            if checked[0] is False:
                if checked[1] == "ex_sub":
                    update_q = f"""UPDATE plus_users SET username = '{message.from_user.username}',
                               firstname = '{message.from_user.first_name}', cost_in_stars = 1,
                               refund_token = '{token_successful_payment}',
                               subscribe_date = {ex_time_for_sub} WHERE tg_id = '{message.from_user.id}';"""
                    cursor.execute(update_q)
                    connection.commit()
                    connection.close()
                    return True
                else:
                    connection.close()
                    return False

    @staticmethod
    def delete_record_for_subscribe(ref_token: str) -> bool | tuple:
        """
        Delete a record from database | Manager Plus Subscription.

        :param ref_token: REF-token.

        :return: Result of delete.
        """
        connection: pymysql.Connection = Connection.get_connection(HandlerDB.get_data())
        cursor = connection.cursor()

        query: str = "SELECT tg_id, firstname FROM plus_users WHERE refund_token = %s;"
        cursor.execute(query, (ref_token,))
        result: tuple = cursor.fetchall()
        if len(result[0]) == 0:
            connection.close()
            return False,
        else:
            tg_id: str = result[0][0]
            firstname: str = result[0][1]

            del_q: str = "DELETE FROM plus_users WHERE tg_id = %s;"
            cursor.execute(del_q, (tg_id,))
            connection.commit()
            connection.close()
            return True, tg_id, firstname

    @staticmethod
    def check_subscription(message: types.Message | types.CallbackQuery) -> bool | tuple:
        """
        Check subscription by message from user.

        :param message: Message from user | Callback Query.

        :return: tuple.
        """
        connection: pymysql.Connection = Connection.get_connection(HandlerDB.get_data())
        cursor = connection.cursor()

        query: str = f"SELECT subscribe_date FROM plus_users WHERE tg_id = %s;"
        cursor.execute(query, (str(message.from_user.id),))
        result: tuple = cursor.fetchall()
        if len(result) == 0:
            connection.close()
            return False, "not_sub"
        else:
            date: int = int(time.time())

            remains: int = result[0][0] - date

            if remains > 0:
                connection.close()
                return True, remains
            else:
                connection.close()
                return False, "ex_sub"

    @staticmethod
    def check_subscription_by_refund_token(refund_token: str) -> bool | tuple:
        """
        Check subscription by refund token from user.

        :param refund_token: REF-token.

        :return: Data.
        """
        connection: pymysql.Connection = Connection.get_connection(HandlerDB.get_data())
        cursor = connection.cursor()

        query: str = f"SELECT subscribe_date, tg_id FROM plus_users WHERE refund_token = %s;"
        cursor.execute(query, (refund_token,))
        result: tuple = cursor.fetchall()
        if len(result) == 0:
            connection.close()
            return False, "not_sub", "none"
        else:
            date: int = int(time.time())

            remains: int = result[0][0] - date

            if remains > 0:
                connection.close()
                return True, remains, result[0][1]
            else:
                connection.close()
                return False, "ex_sub", result[0][1]

    @staticmethod
    def check_refund_token(message: types.Message | types.CallbackQuery) -> str | bool:
        """
        Check (look for) refund token from database.

        :param message: Message from user | Callback Query.
        :return: REF-Token or False (otherwise).
        """
        connection: pymysql.Connection = Connection.get_connection(HandlerDB.get_data())
        cursor = connection.cursor()
        query: str = f"SELECT refund_token FROM plus_users WHERE tg_id = %s;"
        cursor.execute(query, (str(message.from_user.id),))
        result: tuple = cursor.fetchall()

        if len(result) != 0:
            refund_token = result[0][0]
            connection.close()
            return refund_token
        else:
            connection.close()
            return False

    @staticmethod
    def check_promo_code(promo: str) -> bool | tuple:
        """
        Get and check promo code from database.

        :param promo: Promo code from user.
        :return: Result | Data of promo.
        """
        connection: pymysql.Connection = Connection.get_connection(HandlerDB.get_data())
        cursor = connection.cursor()

        query: str = "SELECT num_uses, type_promo FROM plus_promo_codes WHERE promo_code = %s;"
        cursor.execute(query, (promo,))
        result = cursor.fetchall()
        if len(result) == 0:
            connection.close()

            return False,
        else:
            connection.close()

            return True, promo, result[0][0], result[0][1]

    @staticmethod
    def sub_promo_code(promo: str) -> bool | tuple:
        """
        Subtract the number of subscription uses.

        :param promo: Promo code.
        :return: Result | Data of promo.
        """
        connection: pymysql.Connection = Connection.get_connection(HandlerDB.get_data())
        cursor = connection.cursor()

        query: str = "SELECT num_uses FROM plus_promo_codes WHERE promo_code = %s;"
        cursor.execute(query, (promo,))
        result = cursor.fetchall()
        if len(result) == 0:
            connection.close()

            return False,
        else:
            if result[0][0] > 1:
                query: str = f"UPDATE plus_promo_codes SET num_uses = {result[0][0] - 1};"
                cursor.execute(query)
                connection.commit()
                connection.close()

                return True, "many"
            elif result[0][0] == 1:
                query: str = f"UPDATE plus_promo_codes SET num_uses = {result[0][0] - 1};"
                cursor.execute(query)
                connection.commit()
                connection.close()

                return True, "none"

    @staticmethod
    def show_promo_datas() -> bool | tuple:
        """
        Show promo datas from database without authorization.

        :return: PROMO Data.
        """
        connection: pymysql.Connection = Connection().get_connection(HandlerDB.get_data())
        cursor = connection.cursor()

        query: str = "SELECT promo_code, num_uses, type_promo FROM plus_promo_codes;"
        cursor.execute(query)
        result = cursor.fetchall()

        if len(result) == 0:
            connection.close()

            return False, "none"

        else:
            datas: str = ""
            for i in range(len(result)):
                datas += f"<b><u>{i + 1}</u></b>)" \
                         f" 🎫 <b>Promo code</b>: <code>{result[i][0]}</code>\n" \
                         f"    🔢 <b>Number of uses</b>: <code>{result[i][1]}</code>\n" \
                         f"    🌀 <b>Type</b>: <code>{result[i][2]}</code>" \
                         f"\n------------------------------------\n"
            return True, datas

    @staticmethod
    def add_new_promo_code(promo: str, num_uses: int, type_promo: str) -> bool | tuple:
        """
        Function for add a new promo code from admin. | Admin control.

        :param promo: A new promo code.
        :param num_uses: Number of uses the promo code.
        :param type_promo: Type of the promo code.

        :return: Result | Data of promo.
        """
        connection: pymysql.Connection = Connection.get_connection(HandlerDB.get_data())
        cursor = connection.cursor()

        query: str = "SELECT num_uses FROM plus_promo_codes WHERE promo_code = %s;"
        cursor.execute(query, (promo,))
        result = cursor.fetchall()
        if len(result) == 0:
            if type_promo == "plus_one_week" or type_promo == "plus_five_days" or type_promo == "plus_month":
                query: str = f"""INSERT INTO plus_promo_codes (promo_code, num_uses, type_promo) VALUES ('{promo}', 
                             {num_uses}, '{type_promo}');"""
                cursor.execute(query)
                connection.commit()

                connection.close()

                return True, promo, num_uses, type_promo

            else:
                connection.close()

                return False, "invalid_type"
        else:
            connection.close()

            return False, "already_exist"

    @staticmethod
    def delete_promo_code(promo: str) -> bool:
        """
        Function for delete a promo code from admin. | Admin control.

        :param promo: A promo code.
        :return: Result of delete a promo code.
        """
        connection: pymysql.Connection = Connection.get_connection(HandlerDB.get_data())
        cursor = connection.cursor()

        query: str = "SELECT num_uses FROM plus_promo_codes WHERE promo_code = %s;"
        cursor.execute(query, (promo,))
        result = cursor.fetchall()
        if len(result) == 0:
            connection.close()

            return False
        else:
            del_query: str = "DELETE FROM plus_promo_codes WHERE promo_code = %s;"
            cursor.execute(del_query, (promo,))
            connection.commit()

            connection.close()

            return True


class SubOperations:
    """Operations for manage subscription."""

    @staticmethod
    def days_to_sec(days: int) -> int:
        """Converter 'DAYS TO SECONDS'."""
        return days * 86400

    @staticmethod
    def sec_to_days(sec: int | float) -> int | float:
        """Converter 'SECONDS TO DAYS'."""
        return sec / 86400
