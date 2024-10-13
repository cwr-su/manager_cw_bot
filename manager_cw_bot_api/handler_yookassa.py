import uuid
import json
import logging

from yookassa import Payment, Configuration

from manager_cw_bot_api.handler_db_sub_operations import HandlerDB


class Yookassa:
    """Class of manage operations for Yookassa."""

    @staticmethod
    async def auth(file_path="bot.json") -> None:
        """
        Authorization in Yookassa API.

        :param file_path: File path.
        :return: None.
        """
        with open(file_path, "r", encoding='utf-8') as file:
            data: dict = json.load(file)
            id_y: str = data["YOOKASSA_API"]["API_ID"]
            key_y: str = data["YOOKASSA_API"]["API_KEY"]
            Configuration.account_id = id_y
            Configuration.secret_key = key_y

            logging.info(
                "Successful authorisation in YooKassa API"
            )

    @staticmethod
    async def create_payment(email: str) -> tuple:
        """
        Create yookassa-payment and send the receipt to the customer.

        :param email: Email of the user.
        :return: Tuple with data.
        """
        await Yookassa.auth()
        idempotence_key = str(uuid.uuid4())

        payment = Payment.create({
            "amount": {
                "value": "5.00",
                "currency": "RUB"
            },
            "capture": True,
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/helper_cwBot"
            },
            "description": "CW Premium",
            "receipt": {
                "customer": {
                    "email": email
                },
                "items": [
                    {
                        "description": "CW Premium",
                        "quantity": 1,
                        "amount": {
                            "value": "5.00",
                            "currency": "RUB"
                        },
                        "vat_code": 1
                    }
                ]
            }
        }, idempotence_key)

        logging.info(
            f"Successful YooKassa invoicing for EMail: {email} | YooKassa API"
        )

        return payment.confirmation.confirmation_url, payment.id

    @staticmethod
    async def check_payment(payment_id: str, tg_id: int) -> tuple:
        """
        Check payment by confirmation id.

        :param payment_id: Payment confirmation id.
        :param tg_id: TG ID.

        :return: Tuple with result.
        """
        try:
            payment = Payment.find_one(payment_id)
            if payment.status == "succeeded":
                logging.info(
                    f"The payment was successful. Payment ID: {payment_id}; User ID: {tg_id}"
                )
                return True,
            elif payment.status == "canceled":
                await HandlerDB.yookassa_delete_record_conf_id(tg_id)
                logging.info(
                    f"The payment was canceled. Payment ID: {payment_id}; User ID: {tg_id}. "
                    f"The record from database was deleted (payment_id)."
                )
                return False, "canceled"
            else:
                logging.info(
                    f"The payment hasn't gone through yet. "
                    f"Payment ID: {payment_id}; User ID: {tg_id}"
                )
                return False, payment.paid
        except Exception as ex:
            if "account_id and secret_key are required" in str(ex):
                await Yookassa.auth()
                payment = Payment.find_one(payment_id)

                if payment.status == "succeeded":
                    logging.info(
                        f"The payment was successful. Payment ID: {payment_id}; User ID: {tg_id}"
                    )
                    return True,
                elif payment.status == "canceled":
                    await HandlerDB.yookassa_delete_record_conf_id(tg_id)
                    logging.info(
                        f"The payment was canceled. Payment ID: {payment_id}; User ID: {tg_id}. "
                        f"The record from database was deleted (payment_id)."
                    )
                    return False, "canceled"
                else:
                    logging.info(
                        f"The payment hasn't gone through yet. "
                        f"Payment ID: {payment_id}; User ID: {tg_id}"
                    )
                    return False, payment.paid
            else:
                logging.warning(f"The exception has arisen: {ex}.")
                return False, f"Error: {ex}."
