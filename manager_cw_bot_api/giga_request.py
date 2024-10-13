"""
Module of the GigaChatAI model.
"""
import json
import requests
import logging
import abc


class BaseGetData(abc.ABC):
    """The base class for retrieving configuration data."""

    @staticmethod
    @abc.abstractmethod
    async def get_data(file_path) -> dict:
        """
        Base function for getting data (from conf-file, which created by admin).

        :param file_path: File Path of JSON-API-keys for Bot and settings for the GIGACHAT.
        :return: Dict with data.
        """


class BaseVersionAI(abc.ABC):
    """Base class for selecting the AI version."""

    @staticmethod
    @abc.abstractmethod
    async def request(request: str) -> str:
        """
        AI Version. Return answer to the user (str).

        :param request: Request from the user.
        :return: Answer (tuple) pro-version ("deep" answer).
        """


class BaseGetToken(abc.ABC):
    """The base class for obtaining a token AI-API"""

    @staticmethod
    @abc.abstractmethod
    async def get_token(auth_token_giga: str) -> str:
        """
        Get token for admin-AI-Account.

        :param auth_token_giga: Authorization token.
        :return: Access (Auth) Token (answer).
        """


class GetAuthTokenSber(BaseGetToken):
    """The base class for obtaining a token AI SBER API (GigaChat API)."""
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

        response: dict = requests.request(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
            verify=False
        ).json()

        return response['access_token']


class BaseAIText(abc.ABC):
    """AI text-chat-model base class."""

    @staticmethod
    @abc.abstractmethod
    async def request(request_of_user: str, token_giga: str, temperature_giga: float,
                      top_p_giga: float, n_giga: int, auth_token_giga: str) -> str:
        """
        Answer for the user from the request (from the user) by some AI Model.

        :param request_of_user: Request from the user.
        :param token_giga: Token of some AI Model.
        :param temperature_giga: Temperature of an answer.
        :param top_p_giga: Alternative to temperature.
        :param n_giga: Quality and count answer for the generated.
        :param auth_token_giga: Authorization token of some AI Model.

        :return: Result.
        """


class BaseAIImage(abc.ABC):
    """AI image-generate-model base class."""

    @staticmethod
    @abc.abstractmethod
    async def request(query: str, auth_token_giga: str, token_giga: str) -> str:
        """
        Create image for some users.

        :param query: Query from the user.
        :param auth_token_giga: Authorization token for some AI Model.
        :param token_giga: Token for requests.

        :return: Image data.
        """


class GigaChatPro(BaseAIText):
    """
    The class of AI-text model GigaChat.
    Version of the AI-assistance: GigaPro.
    """

    @staticmethod
    async def request(request_of_user: str, token_giga: str, temperature_giga: float,
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

        :return: Result.
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
            logging.info("Sending a request to retrieve text in PRO mode at the user's request")
            response: dict = requests.request(
                method="POST",
                url=url,
                data=body,
                headers=headers,
                verify=False
            ).json()

            logging.info("Successful! I return the answer as text / lines")

            return response['choices'][0]['message']['content']

        except Exception as ex:
            new_token: str = await GetAuthTokenSber.get_token(auth_token_giga)

            with open("bot.json", encoding='utf-8') as f:
                dt: dict = json.load(f)

            dt["GIGACHAT"]["TOKEN"] = new_token

            with open("bot.json", 'w', encoding='utf-8') as fl:
                json.dump(dt, fl, ensure_ascii=False, indent=4)

            logging.warning(
                f"The AI token has expired. But it's already been updated. Write the "
                f"AI model enquiry again. The exception has arisen: {ex}"
            )

            return "Sorry! I updated the data. Please, repeat your request :)"


class GigaChatLight(BaseAIText):
    """
    The class of AI-text model GigaChat.
    Version of the AI-assistance: GigaLight.
    """

    @staticmethod
    async def request(request_of_user: str, token_giga: str, temperature_giga: float,
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
            logging.info("Sending a request to retrieve text in PRO mode at the user's request")
            response: dict = requests.request(
                method="POST",
                url=url,
                data=body,
                headers=headers,
                verify=False
            ).json()

            logging.info("Successful! I return the answer as text / lines")

            return response['choices'][0]['message']['content']

        except Exception as ex:
            new_token: str = await GetAuthTokenSber.get_token(auth_token_giga)

            with open("bot.json", encoding='utf-8') as f:
                dt: dict = json.load(f)

            dt["GIGACHAT"]["TOKEN"] = new_token

            with open("bot.json", 'w', encoding='utf-8') as fl:
                json.dump(dt, fl, ensure_ascii=False, indent=4)

            logging.warning(
                f"The AI token has expired. But it's already been updated. Write the "
                f"AI model enquiry again. The exception has arisen: {ex}"
            )

            return "Sorry! I updated the data. Please, repeat your request :)"


class GigaImagePro(BaseAIImage):
    """Class of generate images for premium-users."""

    @staticmethod
    async def request(request: str, auth_token_giga: str, token_giga: str) -> bytes | str:
        """
        Create image for Premium users.

        :param request: Request / Query from the user.
        :param auth_token_giga: Authorization token for GigaChatAI (requests only now).
        :param token_giga: Token for requests.

        :return: Image data | Result (str).
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
                    "content": request
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
            logging.info(
                "Sending a request to get the AI image at the user's request"
            )
            response: dict = requests.request(
                method="POST",
                url=url,
                headers=headers,
                data=payload,
                verify=False
            ).json()
            if "<img" in str(response["choices"][0]["message"]["content"]):
                src: str = str(response["choices"][0]["message"]["content"]).split('"')[1]

                url_get_data: str = "https://gigachat.devices.sberbank.ru/api/v1/files/" + \
                                    src + "/content"
                headers_get_data: dict = {
                    'Accept': 'application/jpg',
                    'Authorization': 'Bearer ' + token_giga
                }

                response: bytes = requests.request(
                    method="GET",
                    url=url_get_data,
                    headers=headers_get_data,
                    stream=True,
                    verify=False
                ).content

                logging.info(
                    "Successful! The picture was generated, I am returning the response as bytes "
                    "(later converted to a file)"
                )

                return response
            else:
                src: str = str(response["choices"][0]["message"]["content"])

                logging.info(
                    "Something wrong. Perhaps the user did not request an image, but entered a "
                    "text generation request"
                )

                return src

        except Exception as ex:
            new_token: str = await GetAuthTokenSber.get_token(auth_token_giga)

            with open("bot.json", encoding='utf-8') as f:
                dt: dict = json.load(f)

            dt["GIGACHAT"]["TOKEN"] = new_token

            with open("bot.json", 'w', encoding='utf-8') as fl:
                json.dump(dt, fl, ensure_ascii=False, indent=4)

            logging.warning(
                f"The AI token has expired. But it's already been updated. Write the "
                f"AI model enquiry again. The exception has arisen: {ex}"
            )

            return "Sorry! I updated the data. Please, repeat your request :)"


class GetData(BaseGetData):
    """The class-sector for getting conf-data from conf-file."""

    @staticmethod
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

            logging.info(
                "The request to retrieve AI-model data from the configuration file was successful"
            )

            return response


class VersionAIImagePro(BaseVersionAI):
    @staticmethod
    async def request(request: str) -> bytes | str:
        """
        Create a new image for premium-user.

        :param request: Request/Query from premium-user.
        :return: Image data.
        """
        data: dict = await GetData.get_data()

        img_data: bytes | str = await GigaImagePro.request(
            request,
            data["auth_token"],
            data["token"]
        )
        return img_data


class VersionAIPro(BaseVersionAI):
    @staticmethod
    async def request(request: str) -> str:
        """
        GigaChatPro Version. Return answer to the user (str).

        :param request: Request from the user.
        :return: Answer (tuple) pro-version ("deep" answer).
        """
        data: dict = await GetData.get_data()
        answer: str = await GigaChatPro.request(
            request,
            data["token"],
            data["temperature"],
            data["top_p"],
            data["n"],
            data["auth_token"]
        )
        return answer


class VersionAILight(BaseVersionAI):
    @staticmethod
    async def request(request: str) -> str:
        """
        GigaChatLight Version. Return answer to the user (str).

        :param request: Request from the user.
        :return: Answer (tuple) light-version ("low" answer).
        """
        data: dict = await GetData.get_data()
        answer: str = await GigaChatLight.request(
            request,
            data["token"],
            data["temperature"],
            data["top_p"],
            data["n"],
            data["auth_token"]
        )
        return answer
