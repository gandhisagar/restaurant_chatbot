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
        entries = 1
        budget_lower_limit = 0
        budget_higher_limit = 0
        try:
            loc = tracker.get_slot('location')
            cuisine = tracker.get_slot('cuisine')
            budget_code = tracker.get_slot('budget')

            print ("Location: ", loc)
            print ("budget: ", budget_code)
            print ("Budget is: ", budget_code)

            if budget_code == "cheap":
                budget_higher_limit = 300
            elif budget_code == "moderate":
                budget_lower_limit = 300
                budget_higher_limit = 700
            else:
                budget_lower_limit = 700
                budget_higher_limit = 5000

            print ("Lower limit is:", budget_lower_limit)
            print ("Higher limit is:", budget_higher_limit)

            if str(loc) not in (settings.TIER_1 or settings.TIER_2):
                response = "We do not operate in that area yet"

            else:
                location_detail=zomato.get_location(loc, 1)
                d1 = json.loads(location_detail)
                lat=d1["location_suggestions"][0]["latitude"]
                lon=d1["location_suggestions"][0]["longitude"]
                cuisines_dict={'bakery':5,'chinese':25,'cafe':30,'italian':55,'biryani':7,'north indian':50,'south indian':85,
                               'American': 1, 'Mexican': 73}
                results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 25)
                # print ("Response of zomaoto: ", results)
                try:
                    d = json.loads(results)
                except Exception:
                    print ("Exception in loads going with encode")
                    result = results.encode('utf8')
                    d = json.loads(result)
                response=""
                print ("Response of zomaoto: ", d)
                if d['results_found'] == 0:
                    response= "no results"
                else:
                    for restaurant in d['restaurants']:
                        print ("restaurant is: ", restaurant)
                        if int(budget_lower_limit) <= int(restaurant['restaurant']['average_cost_for_two']) <= int(budget_higher_limit):
                            print ("Restaurant in limit")
                            if entries <= 5:
                                print ("5 not found")
                                entries += 1
                                response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ \
                                         restaurant['restaurant']['location']['address'] + " has been rated "+ \
                                         str(restaurant['restaurant']['user_rating']['aggregate_rating']) + "\n"

            dispatcher.utter_message("-----"+response)
            return [SlotSet('location',loc)]
        except Exception as e:
            print ("Exception is : ", e)

