"""Module of the FSM-classes."""
from aiogram.fsm.state import State, StatesGroup


class GetTicketDataByIDTCK(StatesGroup):
    id_ticket: State = State()


class GetDataForSendNewTicket(StatesGroup):
    ticket_data: State = State()


class GetTicketDataForAnswerToUser(StatesGroup):
    ticket_data: State = State()


class GetTicketDataForAnswerToAdmin(StatesGroup):
    ticket_data: State = State()


class BusinessHandlerThanksFunctions(StatesGroup):
    only_text: State = State()
    only_sticker: State = State()
    message_and_sticker_step1_message: State = State()
    message_and_sticker_step2_sticker: State = State()


class BusinessHandlerCongratulationFunctions(StatesGroup):
    only_text: State = State()
    only_sticker: State = State()
    message_and_sticker_step1_message: State = State()
    message_and_sticker_step2_sticker: State = State()


class BusinessHandlerProblemWithBotFunctions(StatesGroup):
    only_text: State = State()
    only_sticker: State = State()
    message_and_sticker_step1_message: State = State()
    message_and_sticker_step2_sticker: State = State()


class GigaImage(StatesGroup):
    request: State = State()


class GetProcessQueryCDLight(StatesGroup):
    query: State = State()


class GetProcessQueryCDPro(StatesGroup):
    query: State = State()


class ProcessEditingEmailAfterConfirmation(StatesGroup):
    new_email: State = State()


class ProcessAddNewEmail(StatesGroup):
    new_email: State = State()


class ProcessEnterTheCodeForAddNewEMailForVerifyEmail(StatesGroup):
    code: State = State()


class ProcessEnteringPromoST1(StatesGroup):
    promo: State = State()


class ProcessAddNewPromoPromoST2(StatesGroup):
    promo: State = State()


class ProcessDeletePromoPromoST2(StatesGroup):
    promo: State = State()


class ProcessRefundingGetREFTokenST1(StatesGroup):
    token: State = State()


class ProcessEmergencyRefundingGetREFTokenST1(StatesGroup):
    user_id: State = State()
