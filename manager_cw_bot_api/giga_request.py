"""
Module of the GigaChatAI model.
"""
import json

import requests


class GigaChat:
    """
    The class of AI-text model GigaChat.
    Now: Available only two version of the AI-assistance: GigaPro / GigaLite.
    """

    @staticmethod
    def get_token(auth_token_giga: str) -> str:
        """
        Get token for admin-AI-Account GigaChat.

        :param auth_token_giga: Authorization token for GigaChatAI (requests only now).
        :return: Access (Auth) Token for GigaChatAI (answers).
        """
        url: str = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
        payload: str = 'scope=GIGACHAT_API_PERS'
        headers: dict = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': '6f0b1291-c7f3-43c6-bb2e-9f3efb2dc98e',
            'Authorization': 'Basic ' + auth_token_giga
        }

        response: dict = requests.post(url, headers=headers, data=payload, verify=False).json()
        return response['access_token']

    @staticmethod
    def request_pro(request_of_user: str, token_giga: str, temperature_giga: float,
                    top_p_giga: float, n_giga: int, auth_token_giga: str) -> str:
        """
        Answer for the user from the request (from the user) by GigaChatPRO.
        Limited Version of the Answers for the user. Premium answers (PRO).

        :param request_of_user: Request from the user.
        :param token_giga: Token of the GigaChatAI.
        :param temperature_giga: Temperature of an answer.
        :param top_p_giga: Alternative to temperature.
        :param n_giga: Quality and count answer for the generated.
        :param auth_token_giga: Authorization token of the GigaChatAI.
        """
        url: str = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

        headers: dict = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token_giga
        }

        body: str = json.dumps({
            "model": "GigaChat-Pro",
            "messages": [
                {
                    "role": "user",
                    "content": request_of_user
                }
            ],
            "temperature": temperature_giga,
            "top_p": top_p_giga,
            "n": n_giga
        })

        try:
            response: dict = requests.post(url, data=body, headers=headers, verify=False).json()
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(
                f"Error - pro (e): {e} | Response:"
                f" {requests.post(url, data=body, headers=headers, verify=False).json()}")
            new_token: str = GigaChat.get_token(auth_token_giga)

            with open("bot.json", encoding='utf-8') as f:
                dt: dict = json.load(f)

            dt["GIGACHAT"]["TOKEN"] = new_token

            with open("bot.json", 'w', encoding='utf-8') as fl:
                json.dump(dt, fl, ensure_ascii=False, indent=4)

            return "Sorry! I updated the data. Please, repeat your request :)"

    @staticmethod
    def request_light(request_of_user: str, token_giga: str, temperature_giga: float,
                      top_p_giga: float, n_giga: int, auth_token_giga: str) -> str:
        """
        Answer for the user from the request (from the user) by GigaChatLight.
        Light answers ('Really' Light).

        :param request_of_user: Request from the user.
        :param token_giga: Token of the GigaChatAI.
        :param temperature_giga: Temperature of an answer.
        :param top_p_giga: Alternative to temperature.
        :param n_giga: Quality and count answer for the generated.
        :param auth_token_giga: Authorization token of the GigaChatAI.
        """
        url: str = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

        headers: dict = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token_giga
        }

        body: str = json.dumps({
            "model": "GigaChat",
            "messages": [
                {
                    "role": "user",
                    "content": request_of_user
                }
            ],
            "temperature": temperature_giga,
            "top_p": top_p_giga,
            "n": n_giga
        })

        try:
            response: dict = requests.post(url, data=body, headers=headers, verify=False).json()
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error - light (e): {e} | Response:"
                  f" {requests.post(url, data=body, headers=headers, verify=False).json()}")
            new_token: str = GigaChat.get_token(auth_token_giga)

            with open("bot.json", encoding='utf-8') as f:
                dt: dict = json.load(f)

            dt["GIGACHAT"]["TOKEN"] = new_token

            with open("bot.json", 'w', encoding='utf-8') as fl:
                json.dump(dt, fl, ensure_ascii=False, indent=4)

            return "Sorry! I updated the data. Please, repeat your request :)"


class GigaImage:
    """Class of generate images for plus-users."""

    def __init__(self, query: str) -> None:
        self.__query: str = query

    @staticmethod
    def get_token(auth_token_giga: str) -> str:
        """
        Get token for admin-AI-Account GigaChat.

        :param auth_token_giga: Authorization token for GigaChatAI (requests only now).
        :return: Access (Auth) Token for GigaChatAI (answers).
        """
        url: str = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
        payload: str = 'scope=GIGACHAT_API_PERS'
        headers: dict = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': '6f0b1291-c7f3-43c6-bb2e-9f3efb2dc98e',
            'Authorization': 'Basic ' + auth_token_giga
        }

        response: dict = requests.post(url, headers=headers, data=payload, verify=False).json()
        return response['access_token']

    def giga_create(self, auth_token_giga: str, token_giga: str) -> bytes | str:
        """
        Create image for plus-user.

        :param auth_token_giga: Authorization token for GigaChatAI (requests only now).
        :param token_giga: Token for requests.
        :return: Image data.
        """
        url: str = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        payload: str = json.dumps({
            "model": "GigaChat",
            "messages": [
                {
                    "role": "system",
                    "content": "Ты — Александр Кандинский"
                },
                {
                    "role": "user",
                    "content": self.__query
                },
            ],
            "function_call": "auto"
        })
        headers: dict = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token_giga
        }

        try:
            response: dict = requests.request("POST", url, headers=headers, data=payload, verify=False).json()
            if "<img" in str(response["choices"][0]["message"]["content"]):
                src: str = str(response["choices"][0]["message"]["content"]).split('"')[1]

                url_get_data: str = "https://gigachat.devices.sberbank.ru/api/v1/files/" + src + "/content"
                headers_get_data: dict = {
                    'Accept': 'application/jpg',
                    'Authorization': 'Bearer ' + token_giga
                }

                response: bytes = requests.request("GET",
                                                   url_get_data,
                                                   headers=headers_get_data,
                                                   stream=True,
                                                   verify=False).content
                return response
            else:
                src: str = str(response["choices"][0]["message"]["content"])
                return src

        except Exception as e:
            print(f"Error - GenerateImage (e): {e} | Response:"
                  f" {requests.post(url, data=payload, headers=headers, verify=False).json()}")
            new_token: str = GigaImage.get_token(auth_token_giga)

            with open("bot.json", encoding='utf-8') as f:
                dt: dict = json.load(f)

            dt["GIGACHAT"]["TOKEN"] = new_token

            with open("bot.json", 'w', encoding='utf-8') as fl:
                json.dump(dt, fl, ensure_ascii=False, indent=4)

            return "Sorry! I updated the data. Please, repeat your request :)"


def get_data(file_path="bot.json") -> dict:
    """
    Get data of the GigaChatSettings.

    :param file_path: File Path of JSON-API-keys for Bot and settings for the GIGACHAT.
    :return: Dict with data.
    """
    with open(file_path, encoding="utf-8") as file:
        data: dict = json.load(file)

        token: str = data["GIGACHAT"]["TOKEN"]
        auth_token: str = data["GIGACHAT"]["AUTH_TOKEN"]

        temperature: float = data["GIGACHAT"]["ANSWER_SETTING"]["TEMPERATURE"]
        top_p: float = data["GIGACHAT"]["ANSWER_SETTING"]["TOP_P"]
        n: int = data["GIGACHAT"]["ANSWER_SETTING"]["N"]

        response: dict = {
            "token": token,
            "auth_token": auth_token,
            "temperature": temperature,
            "top_p": top_p,
            "n": n
        }
        return response


def create(query: str) -> bytes | str:
    """
    Create a new image for plus-user.

    :param query: Query from plus-user.
    :return: Image data.
    """
    data: dict = get_data()

    creator: GigaImage = GigaImage(query)
    img_data: bytes | str = creator.giga_create(data["auth_token"], data["token"])
    return img_data


def pro(request: str) -> str:
    """
    GigaChatPro Version. Return answer to the user (str).

    :param request: Request from the user.
    :return: Answer (str) pro-version ("deep" answer).
    """
    data: dict = get_data()
    answer: str = GigaChat.request_pro(
        request, data["token"], data["temperature"], data["top_p"], data["n"], data["auth_token"]
    )
    return answer


def light(request: str) -> str:
    """
    GigaChatLight Version. Return answer to the user (str).

    :param request: Request from the user.
    :return: Answer (str) light-version ("low" answer).
    """
    data: dict = get_data()
    answer: str = GigaChat.request_light(
        request, data["token"], data["temperature"], data["top_p"], data["n"], data["auth_token"]
    )
    return answer
