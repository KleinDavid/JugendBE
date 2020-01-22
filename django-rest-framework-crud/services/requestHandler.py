from Models.ServerAction import ServerAction
from Models.ServerResult import ServerResult
from services.actionService import ActionService
from services.dataService import DataService
from services.sessionService import SessionService
import json
from rest_framework.response import Response
from json import JSONEncoder


class RequestHandler:
    dataService = DataService()
    sessionService = SessionService(dataService)
    actionService = ActionService(dataService, sessionService)

    @staticmethod
    def get_data_from_request(request):
        return json.loads(request.body.decode('utf-8'))['data']

    @staticmethod
    def get_token_from_request(request):
        return json.loads(request.body.decode('utf-8'))['token']

    def check_token(self, request):
        token = self.get_token_from_request(request)
        return self.sessionService.check_login(token)

    def handleExecuteAction(self, request):
        data = self.get_data_from_request(request)
        server_action = ServerAction
        server_action.Type = data["Type"]
        server_action.Input = data["Input"]
        server_action.Name = data["Name"]
        server_action.Token = data["Token"]
        server_action.Id = data["Id"]
        return Response(json.loads(MyEncoder().encode(self.actionService.executeAction(server_action))))


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
