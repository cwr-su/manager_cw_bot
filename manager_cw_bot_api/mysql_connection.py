"""
Module of the connection to MySQL Server for get CONNECTION-object for
manage DataBase (DB).
"""
import datetime
import pymysql
import logging


class Connection:
    """
    Class for the connection to database (MySQL).
    """
    @staticmethod
    async def get_connection(mysql_data: dict) -> pymysql.Connection | str:
        """
        Get connection for manage the DB.

        :param mysql_data: MySQL Data.
        :type mysql_data: Dict.

        :return: Connection to DB (otherwise: str about error).
        """
        try:
            connection: pymysql.Connection = pymysql.Connection(
                host=mysql_data["HOST"],
                user=mysql_data["USERNAME"],
                password=mysql_data["PASSWORD"],
                database=mysql_data["DB_NAME"],
                port=mysql_data["PORT"]
            )

        except Exception as ex:
            logging.warning(f"No connection to the Database (MySQL) occurred! "
                            f"The exception has arisen: {ex}")
            connection: str = "Error of connection"

        logging.info(
            "Successful connection to the database (MySQL)"
        )

        return connection
