from funct_for_zmq import Main_Class
import zmq


class Class_Client(Main_Class):
    def start(self):
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:5000")
        self.print_term(0, 1, 'Server OFF')


clnt = Class_Client()
clnt.start()
clnt.send_str('server_status')
if clnt.recv_str() == 'ON':
    while True:
        clnt.print_term(0, 1, 'Server ON ')
        clnt.print_term(0, 0, f'Type your answer')
        msg_out = clnt.input_term(0, 2)
        clnt.send_str(msg_out)
        clnt.hidden_input(0, 2)
        msg_input = clnt.recv_str()
        clnt.answer_loc -= 1
        clnt.print_term(0, clnt.answer_loc, f'Server message : {msg_input}')
        if clnt.answer_loc == 4:
            clnt.answer_loc = clnt.term.height - 1
        clnt.exit_serv(msg_input)
