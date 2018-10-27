
## Generated Story 255706069223404498
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "delhi"}
    - slot{"location": "delhi"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - utter_ask_budget
* restaurant_search{"budget": "expensive"}
    - slot{"budget": "expensive"}
    - action_restaurant
    - utter_goodbye
    - export

## Generated Story 1993277579540566202
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "mumbai"}
    - slot{"location": "mumbai"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "North Indian"}
    - slot{"cuisine": "North Indian"}
    - utter_ask_budget
* restaurant_search{"budget": "moderate"}
    - slot{"budget": "moderate"}
    - action_restaurant
* goodbye
    - utter_goodbye

## Generated Story 3320800183399695936
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "italy", "budget": "cheap"}
    - slot{"location": "italy"}
	- slot{"budget": "cheap"}
	- utter_ask_cuisine
* restaurant_search{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - action_restaurant
* goodbye
    - utter_goodbye

## Generated Story -4639179087166749998
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "hyderabad", "cuisine": "Mexican", "budget": "expensive"}
    - slot{"location": "hyderabad"}
    - slot{"cuisine": "Mexican"}
    - slot{"budget": "expensive"}
    - action_restaurant
    - slot{"location": "delhi"}
    - export


## Generated Story 4963448062290237512
* greet
    - utter_greet
* restaurant_search{"location": "delhi", "cuisine": "chinese"}
    - slot{"location": "delhi"}
    - slot{"cuisine": "chinese"}
    - utter_ask_budget
* restaurant_search{"budget": "moderate"}
    - slot{"budget": "moderate"}
    - action_restaurant
* goodbye
    - utter_goodbye
    - export

## Generated Story -9057212234804734937
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "hyderabad"}
    - slot{"location": "hyderabad"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "South Indian", "budget": "expensive"}
    - slot{"cuisine": "chinese"}
	- slot{"budget": "expensive"}
    - action_restaurant
    - utter_ask_email_question
* ask_email_address
    - utter_ask_for_email_id
* affirm
    - action_send_data{"email_id": "abc@gmail.com"}
    - utter_goodbye
    - export


## Generated Story -9057212234804734938
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "delhi", "budget": "cheap"}
    - slot{"location": "hyderabad"}
	- slot {"budget": "cheap"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "Italian"}
    - action_restaurant
    - utter_ask_email_question
* ask_email_address
    - utter_ask_for_email_id
* affirm
    - action_send_data{"email_id": "abc@gmail.com"}
    - utter_goodbye
    - export

## Generated Story -9057212234804734941
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "ahmedabad"}
    - slot{"location": "ahmedabad"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "North Indian"}
    - utter_ask_budget
* restaurant_search{"budget": "moderate"}
    - action_restaurant
    - utter_ask_email_question
* ask_email_address
    - utter_ask_for_email_id
* affirm
    - action_send_data{"email_id": "xyz@gmail.com"}
    - utter_goodbye
    - export




