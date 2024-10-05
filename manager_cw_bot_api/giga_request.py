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
    async def get_token(auth_token_giga: str) -> str:
        """
        Get token for admin-AI-Account GigaChat.

        :param auth_token_giga: Authorization token for GigaChatAI (requests only now).
        :return: Access (Auth) Token for GigaChatAI (answers).
        """
        url: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        payload: str = 'scope=GIGACHAT_API_PERS'
        headers: dict = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': '7d0518ce-47eb-47be-8d2d-4d817e351aae',
            'Authorization': 'Basic ' + auth_token_giga
        }

        response: dict = requests.request("POST", url, headers=headers, data=payload, verify=False).json()

        return response['access_token']

    @staticmethod
    async def request_pro(request_of_user: str, token_giga: str, temperature_giga: float,
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
            response: dict = requests.request("POST", url, data=body, headers=headers, verify=False).json()
            return response['choices'][0]['message']['content']
        except Exception as e:
            ans: dict = requests.request('POST', url, data=body, headers=headers, verify=False).json()
            print(
                f"Error - pro (e): {e} | Response: "
                f"{ans}")
            new_token: str = await GigaChat.get_token(auth_token_giga)

            with open("bot.json", encoding='utf-8') as f:
                dt: dict = json.load(f)

            dt["GIGACHAT"]["TOKEN"] = new_token

            with open("bot.json", 'w', encoding='utf-8') as fl:
                json.dump(dt, fl, ensure_ascii=False, indent=4)

            return "Sorry! I updated the data. Please, repeat your request :)"

    @staticmethod
    async def request_light(request_of_user: str, token_giga: str, temperature_giga: float,
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
            response: dict = requests.request("POST", url, data=body, headers=headers, verify=False).json()
            return response['choices'][0]['message']['content']
        except Exception as e:
            ans: dict = requests.request('POST', url, data=body, headers=headers, verify=False).json()
            print(f"Error - light (e): {e} | Response: "
                  f"{ans}")

            print(auth_token_giga)

            new_token: str = await GigaChat.get_token(auth_token_giga)

            with open("bot.json", encoding='utf-8') as f:
                dt: dict = json.load(f)

            dt["GIGACHAT"]["TOKEN"] = new_token

            with open("bot.json", 'w', encoding='utf-8') as fl:
                json.dump(dt, fl, ensure_ascii=False, indent=4)

            return "Sorry! I updated the data. Please, repeat your request :)"


class GigaImage:
    """Class of generate images for premium-users."""

    def __init__(self, query: str) -> None:
        self.__query: str = query

    @staticmethod
    async def get_token(auth_token_giga: str) -> str:
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
            'RqUID': '7d0518ce-47eb-47be-8d2d-4d817e351aae',
            'Authorization': 'Basic ' + auth_token_giga
        }

        response: dict = requests.request("POST", url, headers=headers, data=payload, verify=False).json()
        return response['access_token']

    async def giga_create(self, auth_token_giga: str, token_giga: str) -> bytes | str:
        """
        Create image for premium-user.

        :param auth_token_giga: Authorization token for GigaChatAI (requests only now).
        :param token_giga: Token for requests.
        :return: Image data.
        """
        url: str = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        payload: str = json.dumps({
            "model": "GigaChat-Pro",
            "messages": [
                {
                    "role": "system",
                    "content": "Ты — Василий Кандинский"
                },
                {
                    "role": "user",
                    "content": self.__query
                },
            ],
            "function_call": "auto",
            "size": "best"
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
            ans: dict = requests.request('POST', url, data=payload, headers=headers, verify=False).json()
            print(f"Error - GenerateImage (e): {e} | Response:"
                  f"{ans}")
            new_token: str = await GigaImage.get_token(auth_token_giga)

            with open("bot.json", encoding='utf-8') as f:
                dt: dict = json.load(f)

            dt["GIGACHAT"]["TOKEN"] = new_token

            with open("bot.json", 'w', encoding='utf-8') as fl:
                json.dump(dt, fl, ensure_ascii=False, indent=4)

            return "Sorry! I updated the data. Please, repeat your request :)"


async def get_data(file_path="bot.json") -> dict:
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


async def create(query: str) -> bytes | str:
    """
    Create a new image for premium-user.

    :param query: Query from premium-user.
    :return: Image data.
    """
    data: dict = await get_data()

    creator: GigaImage = GigaImage(query)
    img_data: bytes | str = await creator.giga_create(data["auth_token"], data["token"])
    return img_data


async def pro(request: str) -> str:
    """
    GigaChatPro Version. Return answer to the user (str).

    :param request: Request from the user.
    :return: Answer (tuple) pro-version ("deep" answer).
    """
    data: dict = await get_data()
    answer: str = await GigaChat.request_pro(
        request, data["token"], data["temperature"], data["top_p"], data["n"], data["auth_token"]
    )
    return answer


async def light(request: str) -> str:
    """
    GigaChatLight Version. Return answer to the user (str).

    :param request: Request from the user.
    :return: Answer (tuple) light-version ("low" answer).
    """
    data: dict = await get_data()
    answer: str = await GigaChat.request_light(
        request, data["token"], data["temperature"], data["top_p"], data["n"], data["auth_token"]
    )
    return answer
