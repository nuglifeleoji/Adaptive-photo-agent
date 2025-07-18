from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionAskForFilter(Action):
    def name(self):
        return "action_ask_for_filter"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="What filter would you like? You can choose from natural, vintage, HDR, etc.")
        return []

class ActionTakePhoto(Action):
    def name(self):
        return "action_take_photo"

    def run(self, dispatcher, tracker, domain):
        # Add code to trigger the photo-taking functionality
        dispatcher.utter_message(text="The photo is being taken, smile!")
        # Simulate the photo capture
        print("Photo captured and saved.")
        return []
