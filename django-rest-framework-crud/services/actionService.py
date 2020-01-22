from Models.ServerAction import ServerAction
from Models.ServerResult import ServerResult
from services.actionHandler import ActionHandler
from services.loggingService import LoggingService


class ActionService:
    dataService = {}
    sessionService = {}
    serverResult = ServerResult()
    actionResultData = {}
    loggingService = LoggingService()

    def __init__(self, data_service, session_service):
        self.dataService = data_service
        self.sessionService = session_service

    def executeAction(self, action):
        session = self.sessionService.getSessionByToken(action.Token)
        if session is None:
            action = ServerAction()
            action.Type = 'InitializeSessionAction'
            action.Input = {}
            action.Input['Token'] = ''
            session = self.sessionService.getSessionByToken(self.sessionService.generate_session_and_token())
        if not session.checkIfActionIsAvailable(action):
            result = ServerResult()
            result.Error = 'Action Not Available'
            return result

        action_handler = ActionHandler(action, session, self.dataService)
        action_handler.executeAction(True)
        return action_handler.serverResult

