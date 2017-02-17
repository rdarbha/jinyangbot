from flask import Flask
from flask import request
from flask import jsonify

import traceback

app = Flask(__name__)

debug = True

def parse_slack_message(slack_message):
    '''
    Consumes a slack POST message that was sent in JSON format.
    Validates the fields and passes back a simplified dict containing:
    {
    "username":<slack_username>,
    "command":<slash_command>,
    "text":<slash_command_arguments>,
    "channel_name":<slack_channel_command_issued_in>
    }
    Slack POST messages send JSON that looks like the following:
    {"token": "uto4ItLoT82ceQoBpIvgtzzz",
              "team_id": "T0C3TFAGL",
              "team_domain": "my_team_name",
              "channel_id": "D0C3VQDAS",
              "channel_name": "directmessage",
              "user_id": "U0C3TFAQ4",
              "user_name": "my_username",
              "command": "/weather",
              "text": "2d6",
              "response_url": "https://hooks.slack.com/commands/T0C3TFAGL/112373954929/8k4mT8sMpIRdslA0IOMKvWSS"}
    '''

    if "user_name" not in slack_message:
        raise DicebotException("Invalid Slack message, no user_name in slack message: " + slack_message)

    if "command" not in slack_message:
        raise DicebotException("No command in slack message: " + slack_message)

    if "text" not in slack_message:
        raise DicebotException("No text in slack message: " + slack_message)

    if "channel_name" not in slack_message:
        raise DicebotException("No channel in slack message: " + slack_message)

    return {"username": slack_message["user_name"],
            "command": slack_message["command"],
            "text": slack_message["text"],
            "channel_name": slack_message["channel_name"]}

def generate_slack_response(text, in_channel=True):
    '''
    Consumes a string message to send to slack in a public format.
    If the message should be sent only to the user set in_channel=False
    '''

    # If you wish to add slack token validation without putting the values in source
    # Heroku env variables can be set on the heroku console
    # and checked with this code
    #
    # if SLACK_WEBHOOK in os.environ:
    #      webhook = os.environ["SLACK_WEBHOOK"]
    #      token = os.environ["SLACK_TOKEN"]

    if in_channel:
        where = "in_channel"
    else:
        where = "ephemeral"
    response = dict()
    response["response_type"] = where
    response["text"] = text
    response["attachments"] = []

    if debug:
        print("Slack Response: " + str(response))

    return jsonify(response)

def return_quote(quote_option):
    return {
        1 : "Erlich Bachman, this is you as an old man. I'm ugly and I'm dead. Alone."
        2 : "Eric Bachman, is your refrigerator running? This is Mike Hunt."
        3 : "Eric Bachman, this is your mom, and you, you are not my baby. "
    }[quote_option]

@app.route('/', methods=["GET", "POST"])
def index():
    return 'Hello world'

@app.route('/test', methods=["GET", "POST"])
def test():
    return 'Hello world test'

@app.route('/jinyang', methods=["GET", "POST"])
def jinyang():

    if debug:
        print(request.form)

#     try:
#         # First parse the inbound slack message and get a simple dict
#         slack_dict = parse_slack_message(request.form)

#         output = slack_dict["text"]

#     return generate_slack_response(output)

    # quote_option = random.randint(1, 3)

    # output = return_quote(quote_option)
    quote_option = {
        1 : "Erlich Bachman, this is you as an old man. I'm ugly and I'm dead. Alone.",
        2 : "Eric Bachman, is your refrigerator running? This is Mike Hunt.",
        3 : "Eric Bachman, this is your mom, and you, you are not my baby. "
    }

    output = quote_options[random.randint(1,3)]

    return jsonify({"response_type" : "in_channel", "text" : output})

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.run()

