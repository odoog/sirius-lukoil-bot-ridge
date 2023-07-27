import logging
from global_transferable_entities.user import User
from state_constructor_parts.action import ActionChangeUserVariableToInput, ActionChangeStage, Action, ActionBack, ActionChangeUserVariable
from bot import Bot
from message_parts.message import Message, MessageKeyboard, MessageKeyboardButton, MessagePicture
from global_transferable_entities.scope import Scope
from state_constructor_parts.stage import Stage
from statistics_entities.stage_stats import StageStatsVisitCount
from statistics_entities.user_stats import UserStatsVisitCount, UserStatsCurrentStage

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        filename='log.txt')
    logging.info("Program started")

    Stage.set_common_statistics([StageStatsVisitCount()])
    User.set_common_statistics([UserStatsVisitCount(),
                                UserStatsCurrentStage()])

    # --- Helper methods ---

    # --- State constructor ---

    _scope = Scope([

        Stage(name="NewUser",
              user_input_actions=[ActionChangeStage("Main"),
                                  ActionChangeUserVariable("bus_count", 0)]),

        Stage(name="Main",
              message=Message(
                  text="Привет, выбери роль",
                  keyboard=MessageKeyboard(
                      buttons=[
                          MessageKeyboardButton(text="Бизнесмен",
                                                actions=[
                                                    ActionChangeStage("Business"),
                                                    lambda scope, user : ActionChangeUserVariable("bus_count", user.get_variable("bus_count") + 1)]),
                          MessageKeyboardButton(text="Заправщик",
                                                actions=[ActionChangeStage("Gasman")]),
                          MessageKeyboardButton(text="Менеджер",
                                                actions=[ActionChangeStage("Manager")])
                      ]
                  )
              )),

        Stage(name="Business",
              message=Message(
                  text=lambda scope, user: "Привет, бизнесмен. Ты был тут {} раз".format(user.get_variable("bus_count")),
                  keyboard=MessageKeyboard(
                      buttons=[
                          MessageKeyboardButton(text="Купить баксы",
                                                actions=[ActionChangeStage("Buy-dollar")]),
                          MessageKeyboardButton(text="Продать баксы"),
                          MessageKeyboardButton(text="Выйти",
                                                actions=[ActionChangeStage("Main")])
                      ]
                  )
              )),

        Stage(name="Gasman",
              message=Message(
                  text="Привет, заправщик",
                  keyboard=MessageKeyboard(
                      buttons=[
                          MessageKeyboardButton(text="Покурить"),
                          MessageKeyboardButton(text="Заправиться"),
                          MessageKeyboardButton(text="Выйти",
                                                actions=[ActionChangeStage("Main")])
                      ]
                  )
              )),

        Stage(name="Manager",
              message=Message(
                  text="Привет, менеджер",
                  keyboard=MessageKeyboard(
                      buttons=[
                          MessageKeyboardButton(text="Нанять"),
                          MessageKeyboardButton(text="Уволить"),
                          MessageKeyboardButton(text="Выйти",
                                                actions=[ActionChangeStage("Main")])
                      ]
                  )
              )),

        Stage(name="Buy-dollar",
              message=Message(
                  text="Сколько хочешь купить",
                  keyboard=MessageKeyboard(
                      buttons=[
                          MessageKeyboardButton(text="Выйти",
                                                actions=[ActionBack()])
                      ]
                  )
              )),


    ], main_stage_name="Main")

    logging.info("Program started")

    bot = Bot('6698770018:AAHR67hFEF1qqlCHdLJWQP6rZmPXjQa9xWY', _scope)

    bot.start_polling(poll_interval=2,
                      poll_timeout=1)
