from rest_framework.generics import ListCreateAPIView
from services.requestHandler import RequestHandler

requestHandler = RequestHandler()


class ExecuteAction(ListCreateAPIView):
    def post(self, request):
        return requestHandler.handleExecuteAction(request)
