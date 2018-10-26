## Generated Story -7141567471036607073
* greet
    - utter_ask_howcanhelp
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "ahmedabad"}
    - slot{"location": "ahmedabad"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - utter_ask_budget
* restaurant_search
    - action_restaurant
    - utter_ask_email_question
* 
    - utter_ask_for_email_id
* email_data
    - action_send_data
    - utter_goodbye
    - export

