"""Module for generate PDF-system documents."""
import datetime
from fpdf import FPDF, FontFace


class GenerateTicketDataUniversal:
    """Class for generate ticket-data for any users."""

    @staticmethod
    async def generate(name: str, text_data: str) -> str:
        """
        Generate ticket-data.

        :param name: Name.
        :param text_data: Ticket Data (big-format).

        :return: Title of file.
        """
        pdf = FPDF()

        pdf.add_font("DinCWFont_TTF", "", "./manager_cw_bot_api/styles/DIN2014-Regular.ttf", uni=True)
        pdf.add_font("DinCWFont_TTF", "I", "./manager_cw_bot_api/styles/DIN2014-Italic.ttf", uni=True)
        pdf.add_font("DinCWFont_TTF", "B", "./manager_cw_bot_api/styles/DIN2014-Bold.ttf", uni=True)
        pdf.set_font("DinCWFont_TTF", "", 13)

        pdf.add_page()

        time = (datetime.datetime.
                now(datetime.timezone(datetime.timedelta(hours=3))).
                strftime('%d.%m.%Y | %H:%M:%S'))

        pdf.write_html("""
        <section>
        <table width="100%">
          <thead>
            <tr>
              <th width="40%" align='left'><a href='https://cwr.su/'><img 
              src='./manager_cw_bot_api/styles/logo_email.png'></a></th>
              <th width="60%" align='right'>
                <h5>CODEWRITER COMPANY\nSELF-EMPLOYED LAPTEV ALEXANDER A.\nTEL.: +7 995 024-61-04, CWR.SU</h5>
              </th>
            </tr>
          </thead>
        </table>
        </section>
          <font size="22"><p align='left'>Ticket Data from Manager CW Bot's Ticket System<br>
          Данные из Тикет Системы Manager CW бота</p></font>
          <p><b>""" + name + """</b>, below you can see your TicketData, which you have 
          requested in the <a href='https://t.me/helper_cwBot'>Manager CW Bot</a>.<br><br>
          The date and time when the document was generated (Moscow time | MSK UTC+3): 
          """ + time + """.</p>
          <p>- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
          - - - - - - - - - - - - - - - - - - -</p>
          <p>\uf000</p>
          <table width="100%">
            <thead>
              <tr>
                <th width="20%">ID | Идентификатор</th>
                <th width="30%">Sender | Отправитель</th>
                <th width="25%">Subject* | Тема</th>
                <th width="25%">Created | Дата/Время создания</th>
              </tr>
            </thead>
            <tbody>
              """ + text_data + """
            </tbody>
          </table>
          <p>*"Subject" (the word) in this case refers to the first 25 characters of the letter. 
          To view the entire email / ticket, go to <a href='https://t.me/helper_cwBot'>Manager CW Bot</a>.<br>
          This document does not provide for the display of emojis or other other symbols.</p>

          <p>Your data is <b>always safe</b>!<br>
          If you have not requested this type of document, please contact technical support by writing to the 
          email listed below.</p>
          <p><b>Important!</b> Using CW services (CWR.SU ) - you accept all the rules and the agreement written on 
          the website <a href='https://acdn.cwr.su/'><b>acdn.cwr.su</b></a> in the corresponding section 
          on the main page.<br>
          <i>If</i> you <i>don't agree with them (agreement / rules)</i>, 
          <i>destroy this document</i> and stop using CW services.</p>
        """, tag_styles={
            "a": FontFace(color="#390085"),
            "h5": FontFace(color="#424242", size_pt=17)
        })

        pdf.add_page()

        pdf.write_html("""
        <p><i>Sincerely, the CW team.
          <br><br>
          If you have any questions about purchasing a product, please contact: 
          <a href='mailto:b2b@cwr.su'>b2b@cwr.su</a>.
          <br>
          On cooperation issues: <a href='mailto:cwr@cwr.su'>cwr@cwr.su</a>.
          <br>
          For technical issues and problems: <a href='mailto:help@cwr.su'>help@cwr.su</a>.</i>
          <br>
          <br></p>
          <p>Director and developer, creator, designer of the CW product: Laptev Alexander A.</p>
          <br>
          <center><img src="./manager_cw_bot_api/styles/stamp.png" width=100 height=100></center>
          <p><i>*This document is valid due to the stamp at the end of the contents of this document.</i></p>
          <p align='center'>© CW | All rights reserved | 2023 - 2024.</p>
        """, tag_styles={
            "a": FontFace(color="#390085")
        })

        file_path: str = "ticket_data_from_manager_cw_bot.pdf"
        pdf.output(file_path)

        return file_path


class GenerateReceiptForUser:
    """Class for generate a receipt to the user."""

    @staticmethod
    async def generate(name: str, receipt_data: str) -> str:
        """
        Generate Receipt-data.

        :param name: Name.
        :param receipt_data: Receipt Data.

        :return: Title of file.
        """
        pdf = FPDF()

        pdf.add_font("DinCWFont_TTF", "", "./manager_cw_bot_api/styles/DIN2014-Regular.ttf", uni=True)
        pdf.add_font("DinCWFont_TTF", "I", "./manager_cw_bot_api/styles/DIN2014-Italic.ttf", uni=True)
        pdf.add_font("DinCWFont_TTF", "B", "./manager_cw_bot_api/styles/DIN2014-Bold.ttf", uni=True)
        pdf.set_font("DinCWFont_TTF", "", 13)

        pdf.add_page()

        time = (datetime.datetime.
                now(datetime.timezone(datetime.timedelta(hours=3))).
                strftime('%d.%m.%Y | %H:%M:%S'))

        pdf.write_html("""
                <section>
                <table width="100%">
                  <thead>
                    <tr>
                      <th width="40%" align='left'><a href='https://cwr.su/'><img 
                      src='./manager_cw_bot_api/styles/logo_email.png'></a></th>
                      <th width="60%" align='right'>
                        <h5>CODEWRITER COMPANY\nSELF-EMPLOYED LAPTEV ALEXANDER A.\nTEL.: +7 995 024-61-04, CWR.SU</h5>
                      </th>
                    </tr>
                  </thead>
                </table>
                </section>
                  <font size="22"><p align='left'>Payment Receipt from the Manager CW Bot<br>
                  Квитанция об оплате из Manager CW бота</p></font>
                  <p><b>""" + name + """</b>, below you can see your Subscription "CW PREMIUM" 
                  Payment Receipt from the <a href='https://t.me/helper_cwBot'>Manager CW Bot</a>.<br><br>
                  The date and time when the document was generated (Moscow time | MSK UTC+3): 
                  """ + time + """.</p>
                  <p>- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                  - - - - - - - - - - - - - - - - - - - - - - -</p>
                  <p>\uf000</p>
                  <table width="100%">
                    <thead>
                      <tr>
                        <th width="20%">Payment ID* | Идентификатор оплаты</th>
                        <th width="20%">Payer | Плательщик</th>
                        <th width="20%">Product** | Продукт (Цифровой товар)</th>
                        <th width="20%">Payment Date/Time | Дата/Время оплаты</th>
                        <th width="20%">Payment method | Способ оплаты</th>
                      </tr>
                    </thead>
                    <tbody>
                      """ + receipt_data + """
                    </tbody>
                  </table>
                  <p>*Currently, you can only purchase digital goods in the 
                  <a href='https://t.me/helper_cwBot'>Manager CW Bot</a>.</p>

                  <p>Your data is <b>always safe</b>!<br>
                  *Payment ID is a unique token that is used to refund TGStars (XTR) or funds (RUB / USD / and more).
                  <br>
                  **This receipt document was generated automatically. Please keep it, as it may be needed in case of 
                  rejection of this digital product.</p>
                  <p><b>Important!</b> Using CW services (CWR.SU ) - you accept all the rules and the agreement written 
                  on the website <a href='https://acdn.cwr.su/'><b>acdn.cwr.su</b></a> in the corresponding section 
                  on the main page.<br>
                  <i>If</i> you <i>don't agree with them (agreement / rules)</i>, 
                  <i>destroy this document</i> and stop using CW services.</p>
                """, tag_styles={
            "a": FontFace(color="#390085"),
            "h5": FontFace(color="#424242", size_pt=17)
        })

        pdf.add_page()

        pdf.write_html("""
                <p><i>Sincerely, the CW team.
                  <br><br>
                  If you have any questions about purchasing a product, please contact: 
                  <a href='mailto:b2b@cwr.su'>b2b@cwr.su</a>.
                  <br>
                  On cooperation issues: <a href='mailto:cwr@cwr.su'>cwr@cwr.su</a>.
                  <br>
                  For technical issues and problems: <a href='mailto:help@cwr.su'>help@cwr.su</a>.</i>
                  <br>
                  <br></p>
                  <p>Director and developer, creator, designer of the CW product: Laptev Alexander A.</p>
                  <br>
                  <center><img src="./manager_cw_bot_api/styles/stamp.png" width=100 height=100></center>
                  <p><i>*This document is valid due to the stamp at the end of the contents of this document.</i></p>
                  <p align='center'>© CW | All rights reserved | 2023 - 2024.</p>
                """, tag_styles={
            "a": FontFace(color="#390085")
        })

        file_path: str = "receipt_data_from_manager_cw_bot.pdf"
        pdf.output(file_path)

        return file_path


class GenerateReceiptRefundForUser:
    """Class for generate a receipt to the user for refund."""

    @staticmethod
    async def generate(name: str, receipt_data: str) -> str:
        """
        Generate Receipt-data.

        :param name: Name.
        :param receipt_data: Receipt Data.

        :return: Title of file.
        """
        pdf = FPDF()

        pdf.add_font("DinCWFont_TTF", "", "./manager_cw_bot_api/styles/DIN2014-Regular.ttf", uni=True)
        pdf.add_font("DinCWFont_TTF", "I", "./manager_cw_bot_api/styles/DIN2014-Italic.ttf", uni=True)
        pdf.add_font("DinCWFont_TTF", "B", "./manager_cw_bot_api/styles/DIN2014-Bold.ttf", uni=True)
        pdf.set_font("DinCWFont_TTF", "", 13)

        pdf.add_page()

        time = (datetime.datetime.
                now(datetime.timezone(datetime.timedelta(hours=3))).
                strftime('%d.%m.%Y | %H:%M:%S'))

        pdf.write_html("""
                <section>
                <table width="100%">
                  <thead>
                    <tr>
                      <th width="40%" align='left'><a href='https://cwr.su/'><img 
                      src='./manager_cw_bot_api/styles/logo_email.png'></a></th>
                      <th width="60%" align='right'>
                        <h5>CODEWRITER COMPANY\nSELF-EMPLOYED LAPTEV ALEXANDER A.\nTEL.: +7 995 024-61-04, CWR.SU</h5>
                      </th>
                    </tr>
                  </thead>
                </table>
                </section>
                  <font size="22"><p align='left'>Receipt for the refund of funds from the Manager CW Bot<br>
                  Квитанция о возврате денежных средств от Manager CW бота</p></font>
                  <p><b>""" + name + """</b>, below you can see your receipt for the refund of funds for the 
                  subscription "CW PREMIUM" from the 
                  <a href='https://t.me/helper_cwBot'>Manager CW Bot</a>.<br><br>
                  The date and time when the document was generated (Moscow time | MSK UTC+3): 
                  """ + time + """.</p>
                  <p>- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                  - - - - - - - - - - - - - - - - - - - - - - -</p>
                  <p>\uf000</p>
                  <table width="100%">
                    <thead>
                      <tr>
                        <th width="20%">Refund ID | Идентификатор возврата</th>
                        <th width="20%">Recipient | Получатель</th>
                        <th width="20%">Ref. Amount | Сумма возврата</th>
                        <th width="20%">Ref. Date/Time | Дата/Время возврата</th>
                        <th width="20%">Ref. method | Способ возврата</th>
                      </tr>
                    </thead>
                    <tbody>
                      """ + receipt_data + """
                    </tbody>
                  </table>
                  
                  <p>Your data is <b>always safe</b>!</p>
                  
                  <p><b>Important!</b> Using CW services (CWR.SU ) - you accept all the rules and the agreement written 
                  on the website <a href='https://acdn.cwr.su/'><b>acdn.cwr.su</b></a> in the corresponding section 
                  on the main page.<br>
                  <i>If</i> you <i>don't agree with them (agreement / rules)</i>, 
                  <i>destroy this document</i> and stop using CW services.</p>
                """, tag_styles={
            "a": FontFace(color="#390085"),
            "h5": FontFace(color="#424242", size_pt=17)
        })

        pdf.add_page()

        pdf.write_html("""
                <p><i>Sincerely, the CW team.
                  <br><br>
                  If you have any questions about purchasing a product, please contact: 
                  <a href='mailto:b2b@cwr.su'>b2b@cwr.su</a>.
                  <br>
                  On cooperation issues: <a href='mailto:cwr@cwr.su'>cwr@cwr.su</a>.
                  <br>
                  For technical issues and problems: <a href='mailto:help@cwr.su'>help@cwr.su</a>.</i>
                  <br>
                  <br></p>
                  <p>Director and developer, creator, designer of the CW product: Laptev Alexander A.</p>
                  <br>
                  <center><img src="./manager_cw_bot_api/styles/stamp.png" width=100 height=100></center>
                  <p><i>*This document is valid due to the stamp at the end of the contents of this document.</i></p>
                  <p align='center'>© CW | All rights reserved | 2023 - 2024.</p>
                """, tag_styles={
            "a": FontFace(color="#390085")
        })

        file_path: str = "receipt_refund_data_from_manager_cw_bot.pdf"
        pdf.output(file_path)

        return file_path
