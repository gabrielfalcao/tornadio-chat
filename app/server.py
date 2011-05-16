import redis
import tornadio
import tornadio.server
from datetime import datetime, timedelta
from os.path import dirname, abspath, join
from tornado.web import RequestHandler
from tornado.web import Application

LOCAL_FILE = lambda *path: join(abspath(dirname(__file__)), *path)
db = redis.Redis(host='localhost', port=6379, db=0)


class MainHandler(RequestHandler):
    def get(self):
        self.render("index.html")


class ClockConnection(tornadio.SocketConnection):
    members = set()

    def on_open(self, *args, **kwargs):
        self.members.add(self)
        n = datetime.now().strftime('%H:%M:%S')
        self.send(n)

    def on_message(self, message):
        n = datetime.now().strftime('%H:%M:%S')
        for p in self.members:
            p.send(n)

    def on_close(self):
        self.members.remove(self)


class ChatParticipant(tornadio.SocketConnection):
    participants = set()

    def on_open(self, *args, **kwargs):
        self.participants.add(self)
        self.send_system_info('welcome')
        for msg in (db.get("message") or []):
            self.broadcast(msg, but_me=True)

    @property
    def now(self):
        time = datetime.now() + timedelta(milliseconds=500)
        return time.strftime('%H:%M:%S')

    def broadcast(self, msg, but_me=False):
        participants = filter(lambda p: not p.is_closed, self.participants)
        if but_me:
            participants.remove(self)

        map(lambda p: p.send(msg), participants)

    def send_system_info(self, msg, but_me=False):
        data = {
            "msg": msg,
            'at': self.now,
            'type': 'info',
        }
        self.broadcast(data, but_me=but_me)

    def send_chat_message(self, text, broadcast=False, but_me=False):
        data = {
            "msg": text,
            'at': self.now,
            'type': 'message',
        }
        if broadcast:
            self.broadcast(data, but_me=but_me)
        else:
            self.send(data)

    def on_message(self, message):
        db.append("message", message)
        self.send_chat_message(message, True)

    def on_close(self):
        self.send_system_info("A user has left", True)

ChatRouter = tornadio.get_router(ChatParticipant, resource='chat')
ClockRouter = tornadio.get_router(ClockConnection, resource='clock')

application = Application(
    [
        (r"/", MainHandler),
        ChatRouter.route(),
        ClockRouter.route(),
    ],
    template_path=LOCAL_FILE('views'),
    static_path=LOCAL_FILE('public'),
    socket_io_port=8000,
    debug=True,
)

if __name__ == "__main__":
    print "listening at localhost:8000"
    tornadio.server.SocketServer(application)
