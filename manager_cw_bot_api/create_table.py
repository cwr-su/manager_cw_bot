"""
Module of the creation tables for the DB.
"""
import pymysql


class CreateTable:
    """
    Class of the creation tables for admin.
    """
    def __init__(self, connection: pymysql.connections.Connection, cursor):
        self._connection: pymysql.connections.Connection = connection
        self._cursor = cursor

    def create(self) -> None:
        """
        Create tables in MySQL.

        :return: None.
        """
        query: str = """CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY AUTO_INCREMENT,
                id_ticket VARCHAR(25) UNIQUE NOT NULL,
                username VARCHAR(255) NOT NULL,
                tg_id_sender VARCHAR(25) NOT NULL,
                ticket_data text NOT NULL,
                create_at VARCHAR(255) NOT NULL,
                status VARCHAR(255) NOT NULL DEFAULT "50",
                subject VARCHAR(25) NOT NULL DEFAULT "NotSubject"
                );
                """
        self._cursor.execute(query)

        query: str = """CREATE TABLE IF NOT EXISTS analytics (
                count_of_ai_queries INT NOT NULL DEFAULT 1,
                count_of_tickets_system INT NOT NULL DEFAULT 1
                );
                """
        self._cursor.execute(query)

        query: str = f"""CREATE TABLE IF NOT EXISTS premium_users(
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                tg_id VARCHAR(255) UNIQUE NOT NULL,
                username VARCHAR(255) NOT NULL,
                firstname VARCHAR(255) NOT NULL,
                cost_in_stars INTEGER NOT NULL,
                refund_token VARCHAR(255) NOT NULL,
                subscribe_date INTEGER NOT NULL,
                promo_code VARCHAR(255) DEFAULT "none"
                );
                """
        self._cursor.execute(query)

        query: str = f"""CREATE TABLE IF NOT EXISTS premium_promo_codes(
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                promo_code VARCHAR(255) UNIQUE NOT NULL,
                num_uses INTEGER NOT NULL,
                type_promo VARCHAR(255) NOT NULL
                );
                """
        self._cursor.execute(query)

        query: str = f"""CREATE TABLE IF NOT EXISTS email_addresses(
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                email VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL,
                tg_id_sender VARCHAR(255) UNIQUE NOT NULL,
                firstname VARCHAR(255) NOT NULL DEFAULT "none",
                yookassa_conf_id VARCHAR(255) DEFAULT "none",
                temp_check_code VARCHAR(255) DEFAULT "none"
                );
                """
        self._cursor.execute(query)
        self._connection.commit()
        self._connection.close()
