"""Module for sending EMail"""
import datetime
import json
import smtplib
import os
import logging

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


class SenderEmail:
    """Class for send email."""

    @staticmethod
    async def get_email_data_admin(file_path="bot.json") -> dict:
        """
        Get EMail-data of admin email.

        :param file_path: File path.
        :return: Dict with data.
        """
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                data: dict = json.load(f)
                data = data["EMAIL_DATA"]
                dct: dict = {
                    "EMAIL": data["EMAIL"],
                    "NAME": data["NAME"],
                    "PORT": data["PORT"],
                    "HOST": data["HOST"],
                    "PASSWORD": data["PASSWORD"],
                    "ADMIN_EMAIL": data["ADMIN_EMAIL"],
                    "ANSWER": [True, "Ok"]
                }
                return dct

        except Exception as ex:
            print(ex)
            return {"ANSWER": [False, f"Error: {ex}"]}

    @staticmethod
    async def send_others_ticket_data_in_email_format(
            receiver_email: str,
            subject: str,
            name: str,
            file_path="ticket_data_from_manager_cw_bot.pdf"
    ) -> tuple:
        """
        Func for send email.

        :param receiver_email: Receiver email.
        :param subject: Subject of email.
        :param name: Name.
        :param file_path: File path.

        :return: Result of sending.
        """
        try:
            text: str = """
            <html>
              <head>
              <style>
              body,
              #main {
                margin: 0;
                padding: 10px;
                background-color: rgb(240, 240, 255);
                box-sizing: border-box;
                font-family: "Trebuchet MS", Helvetica, sans-serif;
                font-size: 17px;
                //color: rgb(0, 0, 0);
                -webkit-hyphens: auto;
                overflow-wrap: break-word;
                hyphens: auto;
              }
              p {
                color: rgb(0, 0, 0);
              }
              a {
                text-decoration: none;
                color: rgb(113, 5, 255);
              }
              #foot, #hd {
                font-size: 14.5px;
                text-align: center;
              }
              #hd {
                font-weight: 900;
                font-size: 20.5px;
                text-align: center;
              }
              #hd>a {
                color: rgb(57, 0, 133);
              }
              .hd_section {
                display: inline;
                text-align: center;
              }
              </style>
              </head>
              <body>
                <div id="main">
                  <p id='hd'><a href='cwr.su'>CW | CodeWriter | CWR.SU</a></p>
                  <p>🤝 Hello, <b>""" + name + """</b>!<br/>Below, in email-attachment you can 
                  see your TicketData, which you have requested in the 
                  <a href='https://t.me/helper_cwBot'>Manager CW Bot</a>.</p><br/>
                  <br/>
                  <i>Sincerely, the CW team.
                  <br/><br/>
                  If you have any questions about purchasing a product, please contact: 
                  <a href='mailto:b2b@cwr.su'>b2b@cwr.su</a>.
                  <br/>
                  On cooperation issues: <a href='mailto:cwr@cwr.su'>cwr@cwr.su</a>.
                  <br/>
                  For technical issues and problems: 
                  <a href='mailto:help@cwr.su'>help@cwr.su</a>.</i>
                  <br/>
                  <br/></p>
                  <p>👤 Director and developer, creator, designer of the CW product: Laptev 
                  Alexander A.</p>
                  <p>👌🏻 This system notification is generated automatically by CW System. 
                  You don't need to answer it!</p>
                  <p id='foot'>© CW | All rights reserved | 2023 - 2024.<br/></p>
                </div>
              </body>
            </html>
            """

            result: dict = await SenderEmail.get_email_data_admin()
            sender_name: str = result["NAME"]
            sender_email: str = result["EMAIL"]
            password: str = result["PASSWORD"]
            host: str = result["HOST"]
            port: int = result["PORT"]

            message: MIMEMultipart = MIMEMultipart()

            message['From'] = formataddr((sender_name, sender_email))
            message['Subject'] = subject

            message.attach(MIMEText(
                _text=text,
                _subtype='html',
                _charset='utf-8')
            )

            with open(file_path, "rb") as file:
                doc = MIMEBase(
                    _maintype='application',
                    _subtype='octet-stream'
                )
                doc.set_payload(file.read())
                encoders.encode_base64(doc)
                doc.add_header(
                    _name='Content-Disposition',
                    _value=f"attachment; filename={file_path}"
                )

            message.attach(doc)

            with smtplib.SMTP(host, port) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())

                os.remove(file_path)
                logging.info(
                    "The email has been successfully sent!"
                )
                return True, "Sent!"

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")
            return False, ex

    @staticmethod
    async def send_check_email_temp_code(
            receiver_email: str,
            subject: str,
            name: str,
            code: str
    ) -> tuple:
        """
        Func for send email.

        :param receiver_email: Receiver email.
        :param subject: Subject of email.
        :param name: Name.
        :param code: Temp ver. code.

        :return: Result of sending.
        """
        try:
            text: str = """
            <html>
              <head>
              <style>
              body,
              #main {
                margin: 0;
                padding: 10px;
                background-color: rgb(240, 240, 255);
                box-sizing: border-box;
                font-family: "Trebuchet MS", Helvetica, sans-serif;
                font-size: 17px;
                //color: rgb(0, 0, 0);
                -webkit-hyphens: auto;
                overflow-wrap: break-word;
                hyphens: auto;
              }
              p {
                color: rgb(0, 0, 0);
              }
              a {
                text-decoration: none;
                color: rgb(113, 5, 255);
              }
              #foot, #hd {
                font-size: 14.5px;
                text-align: center;
              }
              #hd {
                font-weight: 900;
                font-size: 20.5px;
                text-align: center;
              }
              #hd>a {
                color: rgb(57, 0, 133);
              }
              .hd_section {
                display: inline;
                text-align: center;
              }
              </style>
              </head>
              <body>
                <div id="main">
                  <p id='hd'><a href='cwr.su'>CW | CodeWriter | CWR.SU</a></p>
                  <p>🤝 Hello, <b>""" + name + """</b>! Below you can copy the verification code 
                  to confirm the action (change/add this EMail) in the 
                  <a href='https://t.me/helper_cwBot'>Manager CW Bot</a>. The code was requested 
                  at """ + \
                  datetime.datetime.now(
                      datetime.timezone(datetime.timedelta(hours=3))
                  ).strftime('%d.%m.%Y | %H:%M:%S MSK+3') + \
                  """<br/>
                  <br/>
                  ❕ If you are NOT doing this, contact technical support 
                  immediately by 📧 EMail, which is listed below.</p><br/>
                  <p>🔑 Verification code: """ + code + """ ✅</p>
                  <br/>
                  <p><i>Sincerely, the CW team.
                  <br/><br/>
                  If you have any questions about purchasing a product, please contact: 
                  <a href='mailto:b2b@cwr.su'>b2b@cwr.su</a>.
                  <br/>
                  On cooperation issues: <a href='mailto:cwr@cwr.su'>cwr@cwr.su</a>.
                  <br/>
                  For technical issues and problems: 
                  <a href='mailto:help@cwr.su'>help@cwr.su</a>.</i>
                  <br/>
                  <br/></p>
                  <p>👤 Director and developer, creator, designer of the CW product: Laptev 
                  Alexander A.</p>
                  <p>👌🏻 This system notification is generated automatically by CW System. 
                  You don't need to answer it!</p>
                  <p id='foot'>© CW | All rights reserved | 2023 - 2024.<br/></p>
                </div>
              </body>
            </html>
            """
            result: dict = await SenderEmail.get_email_data_admin()
            sender_name: str = result["NAME"]
            sender_email: str = result["EMAIL"]
            password: str = result["PASSWORD"]
            host: str = result["HOST"]
            port: int = result["PORT"]

            message: MIMEText = MIMEText(
                _text=text,
                _subtype='html',
                _charset='utf-8'
            )

            message['From'] = formataddr((sender_name, sender_email))
            message['Subject'] = subject

            with smtplib.SMTP(host, port) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())

                logging.info(
                    "The email has been successfully sent!"
                )
                return True, "Sent!"

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")
            return False, ex

    @staticmethod
    async def send_receipt_to_user_in_email_format(
            receiver_email: str,
            subject: str,
            name: str,
            file_path="receipt_data_from_manager_cw_bot.pdf"
    ) -> tuple:
        """
        Func for send email.

        :param receiver_email: Receiver email.
        :param subject: Subject of email.
        :param name: Name.
        :param file_path: File path.

        :return: Result of sending.
        """
        try:
            text: str = """
                <html>
                  <head>
                  <style>
                  body,
                  #main {
                    margin: 0;
                    padding: 10px;
                    background-color: rgb(240, 240, 255);
                    box-sizing: border-box;
                    font-family: "Trebuchet MS", Helvetica, sans-serif;
                    font-size: 17px;
                    //color: rgb(0, 0, 0);
                    -webkit-hyphens: auto;
                    overflow-wrap: break-word;
                    hyphens: auto;
                  }
                  p {
                    color: rgb(0, 0, 0);
                  }
                  a {
                    text-decoration: none;
                    color: rgb(113, 5, 255);
                  }
                  #foot, #hd {
                    font-size: 14.5px;
                    text-align: center;
                  }
                  #hd {
                    font-weight: 900;
                    font-size: 20.5px;
                    text-align: center;
                  }
                  #hd>a {
                    color: rgb(57, 0, 133);
                  }
                  .hd_section {
                    display: inline;
                    text-align: center;
                  }
                  </style>
                  </head>
                  <body>
                    <div id="main">
                      <p id='hd'><a href='cwr.su'>CW | CodeWriter | CWR.SU</a></p>
                      <p>🤝 Hello, <b>""" + name + """</b>!<br/>Below, in email-attachment you 
                      can see your Subscription "CW PREMIUM" Payment 
                      Receipt from the <a href='https://t.me/helper_cwBot'>Manager CW Bot</a>.</p>
                      <br/>
                      <br/>
                      <i>Sincerely, the CW team.
                      <br/><br/>
                      If you have any questions about purchasing a product, please contact: 
                      <a href='mailto:b2b@cwr.su'>b2b@cwr.su</a>.
                      <br/>
                      On cooperation issues: <a href='mailto:cwr@cwr.su'>cwr@cwr.su</a>.
                      <br/>
                      For technical issues and problems: 
                      <a href='mailto:help@cwr.su'>help@cwr.su</a>.</i>
                      <br/>
                      <br/></p>
                      <p>👤 Director and developer, creator, designer of the CW product: Laptev 
                      Alexander A.</p>
                      <p>👌🏻 This system notification is generated automatically by CW System. 
                      You don't need to answer it!</p>
                      <p id='foot'>© CW | All rights reserved | 2023 - 2024.<br/></p>
                    </div>
                  </body>
                </html>
                """

            result: dict = await SenderEmail.get_email_data_admin()
            sender_name: str = result["NAME"]
            sender_email: str = result["EMAIL"]
            password: str = result["PASSWORD"]
            host: str = result["HOST"]
            port: int = result["PORT"]

            message: MIMEMultipart = MIMEMultipart()

            message['From'] = formataddr((sender_name, sender_email))
            message['Subject'] = subject

            message.attach(MIMEText(
                _text=text,
                _subtype='html',
                _charset='utf-8')
            )

            with open(file_path, "rb") as file:
                doc = MIMEBase(
                    _maintype='application',
                    _subtype='octet-stream'
                )
                doc.set_payload(file.read())
                encoders.encode_base64(doc)
                doc.add_header(
                    _name='Content-Disposition',
                    _value=f"attachment; filename={file_path}"
                )

            message.attach(doc)

            with smtplib.SMTP(host, port) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())

                os.remove(file_path)
                logging.info(
                    "The email has been successfully sent!"
                )
                return True, "Sent!"

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")
            return False, ex

    @staticmethod
    async def send_receipt_refund_to_user_in_email_format(
            receiver_email: str,
            subject: str,
            name: str,
            file_path="receipt_refund_data_from_manager_cw_bot.pdf"
    ) -> tuple:
        """
        Func for send email.

        :param receiver_email: Receiver email.
        :param subject: Subject of email.
        :param name: Name.
        :param file_path: File path.

        :return: Result of sending.
        """
        try:
            text: str = """
                    <html>
                      <head>
                      <style>
                      body,
                      #main {
                        margin: 0;
                        padding: 10px;
                        background-color: rgb(240, 240, 255);
                        box-sizing: border-box;
                        font-family: "Trebuchet MS", Helvetica, sans-serif;
                        font-size: 17px;
                        //color: rgb(0, 0, 0);
                        -webkit-hyphens: auto;
                        overflow-wrap: break-word;
                        hyphens: auto;
                      }
                      p {
                        color: rgb(0, 0, 0);
                      }
                      a {
                        text-decoration: none;
                        color: rgb(113, 5, 255);
                      }
                      #foot, #hd {
                        font-size: 14.5px;
                        text-align: center;
                      }
                      #hd {
                        font-weight: 900;
                        font-size: 20.5px;
                        text-align: center;
                      }
                      #hd>a {
                        color: rgb(57, 0, 133);
                      }
                      .hd_section {
                        display: inline;
                        text-align: center;
                      }
                      </style>
                      </head>
                      <body>
                        <div id="main">
                          <p id='hd'><a href='cwr.su'>CW | CodeWriter | CWR.SU</a></p>
                          <p>🤝 Hello, <b>""" + name + """</b>!<br/>Below, in email-attachment you can see receipt for 
                          the refund of funds for the subscription "CW PREMIUM" from the 
                          <a href='https://t.me/helper_cwBot'>Manager CW Bot</a>.</p><br/>
                          <br/>
                          <i>Sincerely, the CW team.
                          <br/><br/>
                          If you have any questions about purchasing a product, please contact: 
                          <a href='mailto:b2b@cwr.su'>b2b@cwr.su</a>.
                          <br/>
                          On cooperation issues: <a href='mailto:cwr@cwr.su'>cwr@cwr.su</a>.
                          <br/>
                          For technical issues and problems: <a href='mailto:help@cwr.su'>help@cwr.su</a>.</i>
                          <br/>
                          <br/></p>
                          <p>👤 Director and developer, creator, designer of the CW product: Laptev Alexander A.</p>
                          <p>👌🏻 This system notification is generated automatically by CW System. 
                          You don't need to answer it!</p>
                          <p id='foot'>© CW | All rights reserved | 2023 - 2024.<br/></p>
                        </div>
                      </body>
                    </html>
                    """

            result: dict = await SenderEmail.get_email_data_admin()
            sender_name: str = result["NAME"]
            sender_email: str = result["EMAIL"]
            password: str = result["PASSWORD"]
            host: str = result["HOST"]
            port: int = result["PORT"]

            message: MIMEMultipart = MIMEMultipart()

            message['From'] = formataddr((sender_name, sender_email))
            message['Subject'] = subject

            message.attach(MIMEText(
                _text=text,
                _subtype='html',
                _charset='utf-8')
            )

            with open(file_path, "rb") as file:
                doc = MIMEBase(
                    _maintype='application',
                    _subtype='octet-stream'
                )
                doc.set_payload(file.read())
                encoders.encode_base64(doc)
                doc.add_header(
                    _name='Content-Disposition',
                    _value=f"attachment; filename={file_path}"
                )

            message.attach(doc)

            with smtplib.SMTP(host, port) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())

                os.remove(file_path)
                logging.info(
                    "The email has been successfully sent!"
                )
                return True, "Sent!"

        except Exception as ex:
            logging.warning(f"The exception has arisen: {ex}.")
            return False, ex
