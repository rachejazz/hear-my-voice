#############
# Add these 3 handlers to handle 3 intent responses
# add the following lines in the end
#sb.add_request_handler(RunjobIntentHandler())
#sb.add_request_handler(DeleteBranchIntentHandler())
#sb.add_request_handler(NewReleaseIntentHandler())
#############

class RunjobIntentHandler(AbstractRequestHandler):
    """Handler for Runjob Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RunjobIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "I have triggered build workflow. Site will be up in 1 minute."
        
        url="https://api.github.com/repos/rachejazz/hear-my-voice/actions/workflows/cicd.yaml/dispatches"
        data='{"ref":"release"}'
        headers={
	        "Accept":"application/vnd.github.v3+json",
	        "Authorization": "token ghp_jargon"
        }
        req=requests.post(url=url,data=data,headers=headers)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class DeleteBranchIntentHandler(AbstractRequestHandler):
    """Handler for DeleteBranch Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DeleteBranchIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "I have deleted release branch."
        
        headers = {'Authorization': "Token " + 'ghp_jargon'}
        branch_url="https://api.github.com/repos/rachejazz/hear-my-voice/git/refs/heads/release"
        url = "https://api.github.com/repos/rachejazz/hear-my-voice/git/refs/heads"
        
        requests.delete(url=branch_url,headers=headers)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class NewReleaseIntentHandler(AbstractRequestHandler):
    """Handler for NewRelease Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NewReleaseIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "I have created a new release branch"
        
        headers = {'Authorization': "Token " + 'ghp_jargon'}
        url = "https://api.github.com/repos/rachejazz/hear-my-voice/git/refs/heads"
        branches = requests.get(url, headers=headers).json()
        branch, sha = branches[-1]['ref'], branches[-1]['object']['sha']
        
        res = requests.post('https://api.github.com/repos/rachejazz/hear-my-voice/git/refs', json={
            "ref": "refs/heads/release",
            "sha": sha
            }, headers=headers)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

