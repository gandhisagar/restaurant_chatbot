from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
import zomatopy
import json
import settings

class ActionSearchRestaurants(Action):
    def name(self):
        return 'action_restaurant'

    def run(self, dispatcher, tracker, domain):
        config={ "user_key":"6ce88a5ec1419e335afa1c7f92f4b739"}
        zomato = zomatopy.initialize_app(config)
        loc = tracker.get_slot('location')
        cuisine = tracker.get_slot('cuisine')
        budget = tracker.get_slot('budget')

        if loc not in (settings.TIER_1 or settings.TIER_2):
            response = "We do not operate in that area yet"

        else:
            location_detail=zomato.get_location(loc, 1)
            d1 = json.loads(location_detail)
            lat=d1["location_suggestions"][0]["latitude"]
            lon=d1["location_suggestions"][0]["longitude"]
            cuisines_dict={'bakery':5,'chinese':25,'cafe':30,'italian':55,'biryani':7,'north indian':50,'south indian':85,
                           'American': 1, 'Mexican': 73}
            results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 25)
            d = json.loads(results)
            response=""
            if d['results_found'] == 0:
                response= "no results"
            else:
                for restaurant in d['restaurants']:
                    if restaurant['restaurant']['average_cost_for_two'] <= budget:
                        response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ \
                                 restaurant['restaurant']['location']['address'] + " with a average_cost_for_two of "+ \
                                 restaurant['restaurant']['average_cost_for_two'] + "\n"

        dispatcher.utter_message("-----"+response)
        return [SlotSet('location',loc)]

