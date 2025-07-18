from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# 询问用户选择滤镜的动作
class ActionAskForFilter(Action):
    def name(self) -> str:
        return "action_ask_for_filter"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        dispatcher.utter_message(text="What filter would you like for the photo? Options are: natural, bright, vintage, bw, hdr, lomo.")
        return []

# 拍照动作
class ActionTakePhoto(Action):
    def name(self) -> str:
        return "action_take_photo"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        dispatcher.utter_message(text="Photo taken successfully!")
        # 在此你可以调用你的拍照系统，做相应的操作
        return []
