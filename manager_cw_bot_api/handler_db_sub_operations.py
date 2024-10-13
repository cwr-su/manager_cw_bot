"""Module for control the database."""
import json
import time
import logging
import pymysql

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from manager_cw_bot_api.mysql_connection import Connection


class HandlerDB:
    """Handler-class for manage database."""

    @staticmethod
    async def get_data(file_path="bot.json") -> dict:
        """
        Get data of the ADMIN Manager Bot.

        :param file_path: File Path of JSON-API-keys for Bot.
        :return: Dict with data.
        """
        with open(file_path, "r", encoding='utf-8') as file:
            data: dict = json.load(file)

            dct = dict()

            dct["MYSQL"] = data["MYSQL"]

            logging.info(
                "Obtained MySQL DB data from the conf. file for communication with the database"
            )

            return dct["MYSQL"]

    @staticmethod
    async def get_admin_email_from_file(file_path="bot.json") -> str:
        """
        Get data of the ADMIN Manager Bot.

        :param file_path: File Path of JSON-API-keys for Bot.
        :return: Dict with data.
        """
        with open(file_path, "r", encoding='utf-8') as file:
            data: dict = json.load(file)
            admin_email: str = data["EMAIL_DATA"]["ADMIN_EMAIL"]

            return admin_email

    @staticmethod
    async def yookassa_up_query(confirmation_id: str, tg_id: int) -> None:
        """
        Yookassa fast-query for update data.

        :param confirmation_id: Confirmation ID.
        :param tg_id: TG ID.

        :return: None.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = f"""UPDATE email_addresses SET yookassa_conf_id = '{confirmation_id}' 
        WHERE tg_id_sender = '{tg_id}';"""

        cursor.execute(query)
        connection.commit()
        connection.close()

    @staticmethod
    async def update_yookassa_data(
            call: types.CallbackQuery,
            confirmation_id: str,
            admin_id="None",
            admin_email="None"
    ) -> tuple:
        """
        Update payment data of yookassa in DB.

        :param call: Callback Query
        :param confirmation_id: Confirmation ID.
        :param admin_id: ID Admin.
        :param admin_email: Admin EMail.

        :return: Result.
        """
        try:
            tg_id: int = call.from_user.id

            if tg_id != admin_id:
                await HandlerDB.yookassa_up_query(confirmation_id, tg_id)
            else:
                email_data: tuple = await HandlerDB.get_email_data(tg_id)
                if email_data[0] is True and email_data[1][0] == admin_email:
                    await HandlerDB.yookassa_up_query(confirmation_id, tg_id)
                elif email_data[0] is False:
                    await HandlerDB.add_new_email(
                        admin_email,
                        tg_id,
                        call.from_user.username,
                        call.from_user.first_name,
                        False
                    )
                    await HandlerDB.yookassa_up_query(confirmation_id, tg_id)

            return True,

        except Exception as ex:
            logging.warning(
                f"The exception has arisen: {ex}"
            )
            return False, ex

    @staticmethod
    async def yookassa_get_conf_id(tg_id: int) -> tuple:
        """
        Get yookassa payment confirmation id from DB by TG ID.

        :param tg_id: TG ID.
        :return: Tuple with data-result.
        """
        try:
            connection: pymysql.Connection = await Connection.get_connection(
                await HandlerDB.get_data()
            )
            cursor = connection.cursor()

            query: str = "SELECT yookassa_conf_id FROM email_addresses WHERE tg_id_sender = %s;"
            cursor.execute(query, (str(tg_id),))
            result: tuple = cursor.fetchall()
            if len(result) > 0:
                if result[0][0] == "none":
                    return False, "None"
                else:
                    return True, result[0][0]
            else:
                return False, "None"

        except Exception as ex:
            logging.warning(
                f"The exception has arisen: {ex}"
            )
            return False, ex

    @staticmethod
    async def yookassa_delete_record_conf_id(tg_id) -> None:
        """Fast delete record (confirmation-id of payment from yookassa)."""
        try:
            connection: pymysql.Connection = await Connection.get_connection(
                await HandlerDB.get_data()
            )
            cursor = connection.cursor()
            query: str = f"""UPDATE email_addresses SET yookassa_conf_id = 'none' WHERE 
                         tg_id_sender = '{tg_id}';"""
            cursor.execute(query)
            connection.commit()
            connection.close()

        except Exception as ex:
            logging.warning(
                f"The exception has arisen: {ex}"
            )

    @staticmethod
    async def get_analytic_datas() -> tuple:
        """
        Get Analytics.

        :return: Tuple with data.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = "SELECT * FROM analytics;"
        cursor.execute(query)
        response: tuple = cursor.fetchall()
        connection.close()

        return response

    @staticmethod
    async def update_analytic_datas_count_ai_queries(count: int = 1) -> None:
        """
        Update analytic datas. Update CAQ.

        :param count: Count of AI queries.
        :return: None.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = "SELECT count_of_ai_queries FROM analytics;"
        cursor.execute(query)
        count_of_ai_queries = cursor.fetchall()

        if len(count_of_ai_queries) == 0:
            query: str = f"""INSERT INTO analytics (count_of_ai_queries)
                         VALUES ({count});"""
            cursor.execute(query)
        else:
            query: str = f"""UPDATE analytics SET 
                         count_of_ai_queries = {count_of_ai_queries[0][0] + count};"""
            cursor.execute(query)

        connection.commit()
        connection.close()

    @staticmethod
    async def update_analytic_datas_count_tickets_system(count: int = 1) -> None:
        """
        Update count of tickets. Update CTS.

        :param count: Count of Tickets in the TSystem.
        :return: None.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = "SELECT count_of_tickets_system FROM analytics;"
        cursor.execute(query)
        count_of_tickets_system = cursor.fetchall()

        if len(count_of_tickets_system) == 0:
            query: str = f"""INSERT INTO analytics (count_of_tickets_system)
                         VALUES ({count});"""
            cursor.execute(query)
        else:
            query: str = f"""UPDATE analytics SET 
                         count_of_tickets_system = {count_of_tickets_system[0][0] + count};"""
            cursor.execute(query)

        connection.commit()
        connection.close()

    @staticmethod
    async def get_email_data(tg_id: int) -> tuple:
        """
        Get email data by tg id.

        :param tg_id: Tg ID.
        :return: Tuple with EMail-data.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = "SELECT email, firstname FROM email_addresses WHERE tg_id_sender = %s;"
        cursor.execute(query, (str(tg_id),))
        result: tuple = cursor.fetchall()
        connection.close()

        if len(result) > 0 and (result[0][0] != "waiting" or result[0][0] == "ADMIN"):
            return True, result[0]
        else:
            return False, "None"

    @staticmethod
    async def get_temp_code_for_check_email(tg_id: int) -> tuple:
        """
        Get temp-code by tg id.

        :param tg_id: Tg ID.
        :return: Tuple with EMail-code-verification.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = "SELECT temp_check_code FROM email_addresses WHERE tg_id_sender = %s;"
        cursor.execute(query, (str(tg_id),))
        result: tuple = cursor.fetchall()
        connection.close()

        if len(result) > 0:
            return True, result[0]
        else:
            return False, "None"

    @staticmethod
    async def update_temp_code_for_check_email(
            tg_id: int,
            code: str,
            firstname: str,
            username: str,
            command: str,
            admin_id="None"
    ) -> tuple:
        """
        Update temp-code by tg id.

        :param tg_id: Tg ID.
        :param code: Code for ver.
        :param firstname: First name of user / admin.
        :param username: Username.
        :param command: Command
        :param admin_id: ID Admin.

        :return: Result.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        if command == "add":
            try:
                check: tuple = await HandlerDB.get_temp_code_for_check_email(tg_id)
                if check[0] is False:
                    if tg_id != admin_id:
                        query: str = f"""INSERT INTO email_addresses (email, tg_id_sender, 
                        username, firstname, temp_check_code) VALUES ('waiting', '{str(tg_id)}', 
                        '{username}', '{firstname}', '{code}');"""
                    else:
                        query: str = f"""INSERT INTO email_addresses (email, tg_id_sender, 
                        username, firstname, temp_check_code) VALUES ('ADMIN', '{str(tg_id)}', 
                        '{username}', '{firstname}', '{code}');"""
                    cursor.execute(query)
                else:
                    query: str = f"""UPDATE email_addresses SET temp_check_code = '{code}' 
                                 WHERE tg_id_sender = '{tg_id}';"""
                    cursor.execute(query)

                connection.commit()
                connection.close()
                return True, "Updated", "add"

            except Exception as ex:
                logging.warning(
                    f"The exception has arisen: {ex}"
                )
                return False, ex, "add"

        elif command == "del":
            try:
                check: tuple = await HandlerDB.get_temp_code_for_check_email(tg_id)
                if check[0] is True:
                    if tg_id != admin_id:
                        query: str = f"""UPDATE email_addresses SET temp_check_code = 'none' 
                                     WHERE tg_id_sender = '{tg_id}';"""
                        cursor.execute(query)
                    else:
                        admin_email: str = await HandlerDB.get_admin_email_from_file()

                        query: str = f"""UPDATE email_addresses SET temp_check_code = 'none', 
                        email = '{admin_email}' WHERE tg_id_sender = '{tg_id}';"""
                        cursor.execute(query)

                    connection.commit()
                    connection.close()
                    return True, "Updated", "del"
                else:
                    connection.close()
                    return False, "None", "del"

            except Exception as ex:
                logging.warning(
                    f"The exception has arisen: {ex}"
                )
                return False, ex, "del"

    @staticmethod
    async def add_new_email(
            email: str,
            tg_id: int,
            username: str,
            firstname: str,
            exists_in_db=True
    ) -> bool:
        """
        Add a new email to DB.

        :param email: EMail.
        :param tg_id: TG ID.
        :param username: Username.
        :param firstname: Firstname of user / admin.
        :param exists_in_db: Bool-result from past-check.

        :return: Result.
        """
        try:
            connection: pymysql.Connection = await Connection.get_connection(
                await HandlerDB.get_data()
            )
            cursor = connection.cursor()
            if exists_in_db is True:
                query: str = f"""UPDATE email_addresses SET email = '{email}', 
                username = '{username}', firstname = '{firstname}' WHERE tg_id_sender = 
                '{tg_id}';"""
                cursor.execute(query)
            else:
                query: str = f"""INSERT INTO email_addresses (email, username, tg_id_sender, 
                firstname) VALUES('{email}', '{username}', '{tg_id}', '{firstname}');"""
                cursor.execute(query)

            connection.commit()
            connection.close()
            return True

        except Exception as ex:
            logging.warning(
                f"The exception has arisen: {ex}"
            )
            return False
        
    @staticmethod
    async def add_new_ticket_data(
        id_ticket: str, 
        username: str, 
        tg_id_sender: int, 
        ticket_data: str, 
        create_at: str, 
        subject: str
    ) -> None:
        """
        Function for add new ticket data.

        :param id_ticket: ID Ticket.
        :param username: Sender's Telegram Username.
        :param tg_id_sender: Sender's Telegram ID.
        :param ticket_data: Data of the Ticket.
        :param create_at: CREATE_AT - data of the ticket.
        :param subject: Subject of the ticket.

        :return: None.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query = f"""INSERT INTO users (id_ticket, username, tg_id_sender, 
        ticket_data, create_at, subject) VALUES('{id_ticket}', '{username}', 
        '{tg_id_sender}', '{ticket_data}', '{create_at}', 
        '{subject}');"""

        cursor.execute(query)

        connection.commit()
        connection.close()

    @staticmethod
    async def get_ticket_data(
            tg_id: int,
            builder: InlineKeyboardBuilder
    ) -> InlineKeyboardBuilder | tuple:
        """
        Get ticket data.

        :param tg_id: User's id -- tg_id.
        :param builder: Builder.

        :return: Tuple with data.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = f"""SELECT id_ticket, create_at, subject FROM users WHERE 
                     tg_id_sender = %s ORDER BY create_at DESC;"""
        cursor.execute(query, (str(tg_id),))

        result: tuple = cursor.fetchall()
        response: str = ""
        response_big: str = ""
        count_msg: int = 0

        if len(result) > 0:
            for i in range(len(list(result))):
                if count_msg <= 5:
                    response += (f"<b>{i + 1}</b>. ID_TCK: <code>{result[i][0]}</code>| "
                                 f"CREATE_AT: {result[i][1]}| "
                                 f"Subject: <blockquote>'{result[i][2]}'</blockquote>\n")
                    count_msg += 1
                else:
                    response_big += (f"<tr>"
                                     f"  <td align='center'><code>{result[i][0]}</code></td>"
                                     f"  <td align='center'>You</td>"
                                     f"  <td align='center'>{result[i][2]}</td>"
                                     f"  <td align='center'>{result[i][1]}</td>"
                                     f"</tr>"
                                     f"")

            if count_msg <= 5:
                connection.close()
                return False, response
            else:
                return True, response, response_big

        else:
            btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text=f"Not Found", callback_data="back_on_main"
            )
            btn2: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text=f"🔙 Main", callback_data="back_on_main"
            )
            builder.row(btn1).row(btn2)
            connection.close()
            return builder

    @staticmethod
    async def get_users_tickets_for_admin() -> InlineKeyboardBuilder | tuple:
        """
        Get ticket data.

        :return: Tuple with data.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = """SELECT id_ticket, username, create_at, subject FROM 
                     users ORDER BY create_at DESC;"""
        cursor.execute(query)
        result: tuple = cursor.fetchall()

        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        response: str = ""
        response_big: str = ""
        count_msg: int = 0

        if len(result) > 0:
            for i in range(len(list(result))):
                if count_msg <= 5:
                    response += (f"<b>{i + 1}</b>. Sender: "
                                 f"@{result[i][1]}| ID_TCK: <code>{result[i][0]}</code>| "
                                 f"CREATE_AT: "
                                 f"{result[i][2]}| Subject: "
                                 f"<blockquote>'{result[i][3]}'</blockquote>\n")
                    count_msg += 1
                else:
                    response_big += (f"<tr>"
                                     f"  <td align='center'><code>{result[i][0]}</code></td>"
                                     f"  <td align='center'>@{result[i][1]}</td>"
                                     f"  <td align='center'>{result[i][3]}</td>"
                                     f"  <td align='center'>{result[i][2]}</td>"
                                     f"</tr>"
                                     f"")

            if count_msg <= 5:
                connection.close()
                return False, response
            else:
                return True, response, response_big

        else:
            btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text=f"Not Found", callback_data="back_on_main"
            )
            btn2: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text=f"🔙 Main", callback_data="back_on_main"
            )
            builder.row(btn1).row(btn2)
            connection.close()
            return builder

    @staticmethod
    async def insert_new_record_for_subscribe(
            message: types.Message | types.CallbackQuery,
            days: int,
            token_successful_payment: str = "PROMO",
            promo: str = "none"
    ) -> tuple:
        """
        Insert a new record to database | CW PREMIUM Subscription.

        :param message: Message from user.
        :param days: Count of days for use CW PREMIUM.
        :param token_successful_payment: Token of successful payment.
        :param promo: A promo code.

        :return: Result.
        """
        time_of_pay: int = int(time.time())
        ex_time_for_sub: int = time_of_pay + await SubOperations.days_to_sec(days)

        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = f"""SELECT subscribe_date FROM premium_users WHERE tg_id = %s;"""
        cursor.execute(query, (str(message.from_user.id),))
        result: tuple = cursor.fetchall()
        if len(result) == 0:
            insert_q = f"""INSERT INTO premium_users (tg_id, username, firstname, cost_in_stars, 
                       refund_token, subscribe_date, promo_code) VALUES ('{message.from_user.id}', 
                       '{message.from_user.username}', '{message.from_user.first_name}', 15, 
                       '{token_successful_payment}', {ex_time_for_sub}, '{promo}');"""
            cursor.execute(insert_q)
            connection.commit()
            connection.close()

            return True, "was_not_sub"
        else:
            checked: tuple = await HandlerDB.check_subscription(message)
            if checked[0] is False:
                if checked[1] == "ex_sub":
                    update_q = f"""UPDATE premium_users SET 
                               username = '{message.from_user.username}',
                               firstname = '{message.from_user.first_name}', cost_in_stars = 15,
                               refund_token = '{token_successful_payment}',
                               subscribe_date = {ex_time_for_sub} WHERE 
                               tg_id = '{message.from_user.id}';"""
                    cursor.execute(update_q)
                    connection.commit()
                    connection.close()
                    return True, "was_ex_sub"
                else:
                    connection.close()
                    return False, "error"
            else:
                connection.close()
                return False, "error"

    @staticmethod
    async def delete_record_for_subscribe(ref_token: str) -> tuple:
        """
        Delete a record from database | CW PREMIUM Subscription.

        :param ref_token: REF-token.

        :return: Result of delete.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = "SELECT tg_id, firstname FROM premium_users WHERE refund_token = %s;"
        cursor.execute(query, (ref_token,))
        result: tuple = cursor.fetchall()
        if len(result[0]) == 0:
            connection.close()
            return False,
        else:
            tg_id: str = result[0][0]
            firstname: str = result[0][1]

            del_q: str = "DELETE FROM premium_users WHERE tg_id = %s;"
            cursor.execute(del_q, (tg_id,))
            connection.commit()
            connection.close()
            return True, tg_id, firstname

    @staticmethod
    async def check_subscription(message: types.Message | types.CallbackQuery) -> tuple:
        """
        Check subscription by message from user.

        :param message: Message from user | Callback Query.

        :return: tuple.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = f"SELECT subscribe_date FROM premium_users WHERE tg_id = %s;"
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
    async def check_subscription_by_refund_token(refund_token: str) -> tuple:
        """
        Check subscription by refund token from user.

        :param refund_token: REF-token.

        :return: Data.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = f"SELECT subscribe_date, tg_id FROM premium_users WHERE refund_token = %s;"
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
    async def check_refund_token(message: types.Message | types.CallbackQuery) -> str | bool:
        """
        Check (look for) refund token from database.

        :param message: Message from user | Callback Query.
        :return: REF-Token or False (otherwise).
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()
        query: str = f"SELECT refund_token FROM premium_users WHERE tg_id = %s;"
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
    async def check_promo_code(promo: str) ->  tuple:
        """
        Get and check promo code from database.

        :param promo: Promo code from user.
        :return: Result | Data of promo.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = "SELECT num_uses, type_promo FROM premium_promo_codes WHERE promo_code = %s;"
        cursor.execute(query, (promo,))
        result = cursor.fetchall()
        if len(result) == 0:
            connection.close()

            return False,
        else:
            connection.close()

            return True, promo, result[0][0], result[0][1]

    @staticmethod
    async def sub_promo_code(promo: str) -> bool | tuple:
        """
        Subtract the number of subscription uses.

        :param promo: Promo code.
        :return: Result | Data of promo.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = "SELECT num_uses FROM premium_promo_codes WHERE promo_code = %s;"
        cursor.execute(query, (promo,))
        result = cursor.fetchall()
        if len(result) == 0 or result[0][0] == 0:
            connection.close()

            return False,
        else:
            if result[0][0] > 1:
                query: str = f"UPDATE premium_promo_codes SET num_uses = {result[0][0] - 1};"
                cursor.execute(query)
                connection.commit()
                connection.close()

                return True, "many"
            elif result[0][0] == 1:
                query: str = f"UPDATE premium_promo_codes SET num_uses = {result[0][0] - 1};"
                cursor.execute(query)
                connection.commit()
                connection.close()

                return True, "none"

    @staticmethod
    async def show_promo_datas() -> bool | tuple:
        """
        Show promo datas from database without authorization.

        :return: PROMO Data.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = "SELECT promo_code, num_uses, type_promo FROM premium_promo_codes;"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            connection.close()

            return False, "none"

        else:
            datas: str = ""
            for i in range(len(result)):
                if result[i][1] != 0:
                    datas += f"<b><u>{i + 1}</u></b>)" \
                             f" 🎫 <b>Promo code</b>: <code>{result[i][0]}</code>\n" \
                             f"    🔢 <b>Number of uses</b>: <code>{result[i][1]}</code>\n" \
                             f"    🌀 <b>Type</b>: <code>{result[i][2]}</code>" \
                             f"\n------------------------------------\n"

            if datas == "":
                return False, "none"
            else:
                return True, datas

    @staticmethod
    async def add_new_promo_code(promo: str, num_uses: int, type_promo: str) -> tuple:
        """
        Function for add a new promo code from admin. | Admin control.

        :param promo: A new promo code.
        :param num_uses: Number of uses the promo code.
        :param type_promo: Type of the promo code.

        :return: Result | Data of promo.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = "SELECT num_uses FROM premium_promo_codes WHERE promo_code = %s;"
        cursor.execute(query, (promo,))
        result = cursor.fetchall()
        if len(result) == 0:
            if (type_promo == "premium_one_week" or type_promo == "premium_five_days" or
                    type_promo == "premium_month"):
                query: str = f"""INSERT INTO premium_promo_codes (promo_code, num_uses, 
                             type_promo) VALUES ('{promo}', {num_uses}, '{type_promo}');"""
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
    async def delete_promo_code(promo: str) -> bool:
        """
        Function for delete a promo code from admin. | Admin control.

        :param promo: A promo code.
        :return: Result of delete a promo code.
        """
        connection: pymysql.Connection = await Connection.get_connection(
            await HandlerDB.get_data()
        )
        cursor = connection.cursor()

        query: str = "SELECT num_uses FROM premium_promo_codes WHERE promo_code = %s;"
        cursor.execute(query, (promo,))
        result = cursor.fetchall()

        if len(result) == 0 or result[0][0] == 0:
            connection.close()

            return False
        else:
            del_query: str = "DELETE FROM premium_promo_codes WHERE promo_code = %s;"
            cursor.execute(del_query, (promo,))
            connection.commit()

            connection.close()

            return True


class SubOperations:
    """Operations for manage subscription."""

    @staticmethod
    async def days_to_sec(days: int) -> int:
        """Converter 'DAYS TO SECONDS'."""
        return days * 86400

    @staticmethod
    async def sec_to_days(sec: int | float) -> int | float:
        """Converter 'SECONDS TO DAYS'."""
        return sec / 86400
