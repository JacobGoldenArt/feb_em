from dotenv import load_dotenv
import logging
import json
import time

# Styling
from rich import print as rprint
from rich.panel import Panel
from rich.markdown import Markdown
from rich.style import Style
from rich.prompt import Prompt
from rich.console import Console

# griptape items
from griptape.structures import Agent
from griptape.rules import Rule, Ruleset

# get current date/time
# format like Wed Dec 23, 1:33am
current_date_time = time.strftime("%a %b %d, %I:%M%p")


# load the .env file
load_dotenv()

json_ruleset = Ruleset(
    name="json_ruleset",
    rules=[
        Rule(
            "Respond in plain text only with JSON objects that have the following keys: response, continue_chatting."
        ),
        Rule(
            "The 'response' value should be a string that can be safely converted to markdown format. Include line returns when necessary."
        ),
        Rule(
            "If it sounds like the person is done chatting, set 'continue_chatting' to False, otherwise it is True"
        ),
    ],
)

system_ruleset = Ruleset(
    name="sys_ruleset",
    rules=[
        Rule(
            "You are a helpful AI assistant named Em. You are here to help Jacob with any questions he may have. !Important- Please don't use disclaimers like: 'As an AI...' Just anwser the questions in a direct and friendly manner. If you don't know that anwser, just say something like: 'I would need to do more research on that subject to give you an accurate anwser.'"
        ),
    ],
)


# Create a sub-class of the Agent class
class Em(Agent):
    def respond(self, user_input):
        # initialize the console
        console = Console()
        with console.status(spinner="simpleDotsScrolling", status=""):
            agent_response = self.run(user_input)
        try:
            data = json.loads(agent_response.output_task.output.value)
        except json.decoder.JSONDecodeError:
            print("Invalid JSON")
            return False
        response = data["response"]
        continue_chatting = data["continue_chatting"]

        formatted_response = Markdown(code_theme="lightbulb", markup=response)

        print("")
        rprint(
            Panel.fit(
                formatted_response,
                style=Style(color="#ffffff"),
                border_style="#C5B841",
                title="Em",
                subtitle=current_date_time,
                subtitle_align="right",
                title_align="left",
            )
        )
        print("")

        return continue_chatting


agent = Em(
    rulesets=[system_ruleset, json_ruleset],
    logger_level=logging.ERROR,
)


# Keep track of when we're chatting
def chat(agent):
    is_chatting = True
    while is_chatting:  # While chatting is still true
        user_input = Prompt.ask("[#C5B841]Jacob")
        is_chatting = agent.respond(user_input)


# Intrduce yourself to the user
agent.respond("Greet Jacob.")


chat(agent)
