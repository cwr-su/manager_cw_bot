"""
Module of the connection to MySQL Server for get CONNECTION-object for
manage DataBase (DB).
"""
<<<<<<< HEAD
import pymysql
import datetime

=======
import datetime

import pymysql

>>>>>>> f20ff53 (Updated data manager)

class Connection:
    """
    Class for the connection to database (MySQL).
    """
    @staticmethod
<<<<<<< HEAD
    def get_connection(mysql_data: dict) -> pymysql.connections.Connection | str:
=======
    def get_connection(mysql_data: dict) -> pymysql.Connection | str:
>>>>>>> f20ff53 (Updated data manager)
        """
        Get connection for manage the DB.

        :param mysql_data: MySQL Data.
        :type mysql_data: Dict.

        :return: Connection to DB (otherwise: str about error).
        """
        try:
<<<<<<< HEAD
            connection = pymysql.connections.Connection(
=======
            connection: pymysql.Connection = pymysql.Connection(
>>>>>>> f20ff53 (Updated data manager)
                host=mysql_data["HOST"],
                user=mysql_data["USERNAME"],
                password=mysql_data["PASSWORD"],
                database=mysql_data["DB_NAME"],
                port=mysql_data["PORT"]
            )

        except Exception as e:
            with open("logs.txt", 'a') as logs:
                logs.write(f"{datetime.datetime.now()} | {e} | "
                           f"The error of database in __init__ of "
<<<<<<< HEAD
                           f"gigachatai.py of GigaChatAI-Class.\n")
            connection = "Error of connection"
=======
                           f"mysql_connection.py of Connection-Class.\n")
            connection: str = "Error of connection"
>>>>>>> f20ff53 (Updated data manager)

        return connection
