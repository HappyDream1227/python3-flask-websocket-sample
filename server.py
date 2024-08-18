# from gevent.pywsgi import WSGIServer
# from geventwebsocket.handler import WebSocketHandler
from flask import Flask, render_template, request
from flask_sock import Sock
# from waitress import serve
import eventlet
from eventlet import wsgi
app = Flask(__name__)
sock = Sock(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return 'test'


@sock.route('/echo')
def echo(sock):
    while True:
        data = sock.receive()
        sender_addr = request.remote_addr
        print(data, 'data received from', sender_addr)
        sock.send(data)

if __name__ == '__main__':
    # # local development, this works well
    # app.run()

    # # using WSGIServer in production but not works.
    # http_server = WSGIServer(('0.0.0.0', 8000), app, handler_class=WebSocketHandler)
    # http_server.serve_forever()

    # # using waitress in production but not works too.
    # serve(app, host='0.0.0.0', port=8000)

    # using eventlet in production, this works.
    wsgi.server(eventlet.listen(('0.0.0.0', 8000)), app)

