"""
Activate the licence key in CW.
"""
import requests
import abc


#        Dear User! DO NOT attempt to modify the contents of this file, as it may
# result in unfortunate consequences, including a fine. Thank you for your understanding.


class AbstractActivate(abc.ABC):
    """Abstract class for activate the licence key (API-KEY)."""

    @staticmethod
    @abc.abstractmethod
    async def activate(bot_id: int, licence_key: str) -> tuple:
        """
        Method for activate API Key.

        :param bot_id: Bot ID (activation Bot).
        :param licence_key: Licence key.

        :return: Tuple with data.
        """


class Activate(abc.ABC):
    """A class for activate the licence key (API-KEY)."""

    @staticmethod
    async def activate(bot_id: str, licence_key: str) -> tuple:
        """
        Method for activate API Key.

        :param bot_id: Bot ID (activation Bot).
        :param licence_key: Licence key.

        :return: Tuple with data.
        """
        data = {
            "licence_key": str(licence_key),
            "bot_id": str(bot_id)
        } 
        response = requests.post("https://api.cwr.ru/v1/", json=data, verify=False)

        #        Dear User! DO NOT attempt to modify the contents of this file, as it may
        # result in unfortunate consequences, including a fine. Thank you for your understanding.

        try:
            if response.json()['result'] == "True":
                return True, response.json()['message']
            else:
                return False, response.json()['message']
        except KeyError as ex:
            return False, str(ex)
