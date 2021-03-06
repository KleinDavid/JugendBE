from services.loggingService import LoggingService
from services.session import Session
from services.dataService import DataService
from threading import Timer, Thread, Event


class SessionService:
    _sessions = []
    _dataService = {}
    _checkSessionsTime = 60/6
    _removeSessionTime = 600

    def __init__(self, _data_service):
        self._dataService = _data_service
        stop_flag = Event()
        timer = Timer(stop_flag, self._checkSessionsTime, self.sessiontimer)
        timer.start()

    def login(self, password):
        if self._dataService.check_passwords(password):
            return {'Token': self.generate_session_and_token(), 'Role': self._dataService.getRoleByPassword(password)}
        return None

    def generate_session_and_token(self):
        highest_id = 0
        for session in self._sessions:
            if session.id > highest_id:
                highest_id = session.id

        session = Session(highest_id + 1, self._dataService)
        self._sessions.append(session)
        LoggingService.log('new Session: ' + session.token)
        return session.token

    def check_login(self, token):
        for session in self._sessions:
            if session.token == token:
                session.lastRequestInSeconds = 0
                return True
        return False

    def sessiontimer(self):
        for session in self._sessions:

            if session.screeContext.lastResultInSections >= self._removeSessionTime:
                LoggingService.log('remove Session: ' + session.token + ' after ' + str(session.totalTime/60) + ' Minutes')
                self._sessions.remove(session)

            session.screeContext.lastResultInSections = session.screeContext.lastResultInSections + self._checkSessionsTime
            session.totalTime = session.totalTime + self._checkSessionsTime

    def getSessionByToken(self, token):
        for session in self._sessions:
            if session.token == token:
                return session
        return None


class Timer(Thread):
    time = 10000
    action = ''
    counter = 0

    def __init__(self, event, time, action):
        self.time = time
        self.action = action

        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(self.time):
            self.counter = self.counter + 1
            self.action()
