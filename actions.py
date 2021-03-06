from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
from rasa_core.events import AllSlotsReset
from rasa_core.events import Restarted
import zomatopy
import json
import settings
import pandas as pd
import re
from email_service import send_msg_to_clinet

# Form entity fields 
from rasa_core.actions.forms import (
    BooleanFormField,
    EntityFormField,
    FormAction,
    FreeTextFormField
)

#This action procreates the data to be used later
# these are all mandatory fields which are to be filled before making a zomato API query
class ActionFetchFormAndData(FormAction):
	RANDOMIZE = False
	@staticmethod
	def required_fields():
		return [
		EntityFormField("location", "location"),
		EntityFormField("cuisine", "cuisine"),
		EntityFormField("budget", "budget")
		]
		
	def name(self):
		return 'action_fetch_form_and_data'

# Once we have all information entered by the user, this subroutine will be invoked		
	def submit(self, dispatcher, tracker, domain):
		config={ "user_key":"2fab14e6a218fa1238aa56e9da9581b7"}
		zomato = zomatopy.initialize_app(config)
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		budget_range = tracker.get_slot('budget')
			
		location_detail=zomato.get_location(loc, 1)
		d1 = json.loads(location_detail)
		lat=d1["location_suggestions"][0]["latitude"]
		lon=d1["location_suggestions"][0]["longitude"]
		cuisines_dict={'mexican':73,'chinese':25,'italian':55,'american':1,'north indian':50,'south indian':85}
		
		dispatcher.utter_message ('Location: '+ loc)
		dispatcher.utter_message ('Cuisine: '+ cuisine)
		dispatcher.utter_message ('Budget: '+ budget_range)
		# create a corpus in the form of dataframe
		cached_res = pd.DataFrame(columns=['Name','Address','Avg budget for two','Rating'])
		count = 0
		# Total of 50 entries at max. to be fetched from Zomato, 10 at a time
		while count != 5:
			results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 10)
			res_json = json.loads(results)
			response=""
			if res_json['results_found'] == 0:
				break
			else:
				for restaurant in res_json['restaurants']:
					cached_res = cached_res.append({'Name':restaurant['restaurant']['name'],
															'Address': restaurant['restaurant']['location']['address'],
															'Avg budget for two':restaurant['restaurant']['average_cost_for_two'],
															'Rating':restaurant['restaurant']['user_rating']['aggregate_rating']},ignore_index=True)
			count+=1
			
		if len(cached_res) == 0:
			dispatcher.utter_template("utter_no_restaurants_found", tracker)
			disptatch.utter_message("Sorry! No restaurants found!")
			SlotSet("budget", None)
			return[SlotSet("cuisine", None)]
		else:
			return[SlotSet("result_restaurants_details",cached_res.to_json())] #this filled slot will be exported back to be used in search function

#Actual function that validates and populates the view to be consumed by user
class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_restaurant'

	def run(self, dispatcher, tracker, domain):
		response = ""
		try:
			loc = tracker.get_slot('location')
			cuisine = tracker.get_slot('cuisine')
			budget_code = tracker.get_slot('budget')
			cached_res = pd.read_json(tracker.get_slot('result_restaurants_details'))
			cuisines=['mexican','chinese','italian','american','north indian','south indian']
			
			dispatcher.utter_message('Budget_range: '+ budget_code)
			dispatcher.utter_message('Cuisine: '+ cuisine)
			# Location validation
			if loc not in (settings.TIER_1 or settings.TIER_2):
				dispatcher.utter_template("utter_invalid_location",tracker)
				dispatcher.utter_message("Sorry! we don't serve in "+loc)
				return [SlotSet('location',None)]
			# Cuisine validation
			if 	cuisine not in cuisines:
				dispatcher.utter_template("utter_invalid_cuisine",tracker)
				dispatcher.utter_message("Sorry! "+cuisine+" is not in the list.")
				return [SlotSet('cuisine',None)]
			# Budget validation
			if str(budget_code) not in ["<300","300-700 range",">700"]:
				return[SlotSet('budget', None)]
			#Populate the result based on the budget specified by the user
			if budget_code == "<300":
				res = cached_res.loc[cached_res['Avg budget for two'] <=300]
				if len(res) == 0:
					SlotSet("budget", None)
					dispatcher.utter_template("utter_no_restaurants_found", tracker)
					dispatcher.utter_message("Sorry! No restaurants found!")
					return[SlotSet("res_restaurant", None)]
				else:
					for index, row in res.head(5).iterrows():
						response = response+row['Name']+" in "+ row['Address']+" has been rated "+str(row['Rating'])+"\n"
					return[SlotSet("res_restaurant", response)]
			
			elif budget_code == "300-700 range":
				res = cached_res.loc[(cached_res['Avg budget for two'] > 300) &  (cached_res['Avg budget for two'] <= 700)]
				if len(res) == 0:
					SlotSet("budget", None)
					dispatcher.utter_template("utter_no_restaurants_found", tracker)
					dispatcher.utter_message("Sorry! No restaurants found!")
					return[SlotSet("res_restaurant", None)]
				else:
					for index, row in res.head(5).iterrows():
						response = response+row['Name']+" in "+ row['Address']+" has been rated "+str(row['Rating'])+"\n"
					return[SlotSet("res_restaurant", response)]
			
			elif budget_code == ">700":				
				res = cached_res.loc[cached_res['Avg budget for two'] >700]
				if len(res) == 0:
					SlotSet("budget", None)
					dispatcher.utter_template("utter_no_restaurants_found", tracker)
					dispatcher.utter_message("Sorry! No restaurants found!")
					return[SlotSet("res_restaurant", None)]
				else:
					for index, row in res.head(5).iterrows():
						response = response+row['Name']+" in "+ row['Address']+" has been rated "+str(row['Rating'])+"\n"	
					return[SlotSet("res_restaurant", response)]
		except Exception as e:
			print ("Exception is : ", e)

# Send the top 10 searches on email 
class ActionSendRestaurantData(Action):
	def name(self):
		return 'action_send_data'

	def run(self, dispatcher, tracker, domain):
		response = ""
		email_id = tracker.get_slot('email')
		if email_id == None:
			dispatcher.utter_template("utter_email_not_recognized", tracker)
			dispatcher.utter_message("Email not recognized")
			return[SlotSet('email',None)]
		# email-id validation	
		list_email = re.findall('([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)',email_id) 
		try:
			loc = tracker.get_slot('location')
			cuisine = tracker.get_slot('cuisine')
			budget_code = tracker.get_slot('budget')

			dispatcher.utter_message ('Location: '+ loc)
			dispatcher.utter_message ('Cuisine: '+ cuisine)
			dispatcher.utter_message ('Budget: '+ budget_range)
			dispatcher.utter_message ('Email: '+ email_id)
			
			cached_res = pd.read_json(tracker.get_slot('result_restaurants_details'))
			# content preparation based on the budget specified
			if budget_code == "<300":
				res = cached_res.loc[cached_res['Avg budget for two'] <=300]
				if len(res) == 0:
					SlotSet("budget", None)
					dispatcher.utter_template("utter_no_restaurants_found", tracker)
					dispatcher.utter_message("Sorry! No restaurants found!")
					return[SlotSet("res_restaurant", None)]
				else:
					for index, row in res.head(10).iterrows():
						response = response+row['Name']+" in "+ row['Address']+" has been rated "+str(row['Rating'])+"\n"
					return[SlotSet("res_restaurant", response)]
			
			elif budget_code == "300-700 range":
				res = cached_res.loc[(cached_res['Avg budget for two'] > 300) &  (cached_res['Avg budget for two'] <= 700)]
				if len(res) == 0 :
					SlotSet("budget", None)
					dispatcher.utter_template("utter_no_restaurants_found", tracker)
					dispatcher.utter_message("Sorry! No restaurants found!")
					return[SlotSet("res_restaurant", None)]
				else:
					for index, row in res.head(10).iterrows():
						response = response+row['Name']+" in "+ row['Address']+" has been rated "+str(row['Rating'])+"\n"
					return[SlotSet("res_restaurant", response)]
			
			elif budget_code == ">700":				
				res = cached_res.loc[cached_res['Avg budget for two'] >700]
				if len(res) == 0:
					SlotSet("budget", None)
					dispatcher.utter_template("utter_no_restaurants_found", tracker)
					dispatcher.utter_message("Sorry! No restaurants found!")
					return[SlotSet("res_restaurant", None)]
				else:
					for index, row in res.head(10).iterrows():
						response = response+row['Name']+" in "+ row['Address']+" has been rated "+str(row['Rating'])+"\n"	
					return[SlotSet("res_restaurant", response)]

			send_msg_to_clinet(data_to_send=response, email_id_requested=email_id)
			return [SlotSet('location',loc)]
		except Exception as e:
			print ("Exception is : ", e)

# Operational functions
class ActionGoodBye(Action):
	def name(self):
		return 'action_bye'
		
	def run(self, dispatcher, tracker, domain):
		dispatcher.utter_template("utter_goodbye",tracker)
		return[AllSlotsReset()]
			
class ActionRestarted(Action): 	
	def name(self): 		
		return 'action_restarted' 	
	def run(self, dispatcher, tracker, domain): 
		return[Restarted()]
		
class ActionReset(Action): 	
	def name(self): 		
		return 'action_reset' 	
	def run(self, dispatcher, tracker, domain): 		
		return[AllSlotsReset()]
