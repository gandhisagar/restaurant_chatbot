from rasa_core.channels import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_slack_connector import SlackInput


nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/restaurantnlu')
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter)

input_channel = SlackInput('xoxp-463240680274-462635591185-466154502866-bd8121930618e59c5dfddbc68273ad4e', #app verification token
							'xoxb-463240680274-466353914309-7nWyAvZBKWvxJaR94WUyzhBp', # bot verification token
							'yflH1ofUqPEZTJFKxLpxhgac', # slack verification token
							True)

agent.handle_channel(HttpInputChannel(5004, '/', input_channel))