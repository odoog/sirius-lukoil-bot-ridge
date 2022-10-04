import logging
import os
from global_transferable_entities.user import User
from state_constructor_parts.action import ActionChangeUserVariableToInput, ActionChangeStage, Action
from bot import Bot
from message_parts.message import Message, MessageKeyboard, MessageKeyboardButton, MessagePicture
from global_transferable_entities.scope import Scope
from state_constructor_parts.stage import Stage
from data_access_layer.google_tables import SheetsClient
from statistics_entities.stage_stats import StageStatsVisitCount
from statistics_entities.user_stats import UserStatsVisitCount, UserStatsCurrentStage

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        filename='log.txt')
    logging.info("Program started")

    # --- Helper methods ---

    # --- State constructor ---

    Stage.set_common_statistics([StageStatsVisitCount()])
    User.set_common_statistics([UserStatsVisitCount(),
                                UserStatsCurrentStage()])

    _scope = Scope([

        Stage(name="NewUser",
              user_input_actions=[ActionChangeStage("AskingForWord")]),

        Stage(name="AskingForWord",
              message=Message(text="Введите слово:"),
              user_input_actions=[ActionChangeUserVariableToInput("word"),
                                  ActionChangeStage("AskingForMeaning")]),

        Stage(name="AskingForMeaning",
              message=Message(text="Введите значение:"),
              user_input_actions=[ActionChangeUserVariableToInput("meaning"),
                                  ActionChangeStage("WordMeaningPairSaved")]),

        Stage(name="WordMeaningPairSaved",
              message=Message(text="Пара сохранена!"),
              user_input_actions=[ActionChangeUserVariableToInput("meaning"),
                                  ActionChangeStage("AskingForWord"),
                                  Action(action_function=lambda _, user, __, ___: google_sheets.insert_word_pair(
                                      user.get_variable("word"),
                                      user.get_variable("meaning")))],
              is_gatehouse=True),

    ], main_stage_name="AskingForWord")

    logging.info("Program started")

    bot = Bot(os.environ['telegram_token'], _scope)
    google_sheets = SheetsClient(os.environ['sheets_token'])

    if os.environ['startup_mode'] == "webhook":
        logging.info("Starting using webhook")
        bot.start_webhook(port=8443,
                          server_ip=os.environ['server_ip'],
                          sertificate_path=os.environ['certificate_path'],
                          key_path=os.environ['key_path'])
    else:
        logging.info("Starting using polling")

        bot.start_polling(poll_interval=2,
                          poll_timeout=1)
