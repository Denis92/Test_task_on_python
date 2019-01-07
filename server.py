from modul_for_term import Main_Class
import zmq


class Class_Server(Main_Class):
    def start(self):
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind('tcp://127.0.0.1:5000')
        self.print_term(0, 0, 'Server ON, but client not connected')


serv = Class_Server()
serv.start()
if serv.recv_str() == 'server_status':
    serv.send_str('ON')
    serv.print_term(0, 0, 'Server ON, client connected')
    serv.print_term(0, 1, 'If you want to exit, type "exit"')
    while True:
        serv.hidden_input(2, 3)
        msg_input = serv.recv_str()
        serv.answer_loc -= 1
        serv.print_term(0, serv.answer_loc, f'Client message : {msg_input}')
        if serv.answer_loc == 5:
            serv.answer_loc = serv.term.height - 1
        serv.print_term(0, 2, f'Type your answer')
        msg_out = serv.input_term(0, 3)
        serv.send_str(msg_out)
        serv.exit_serv(msg_out)
        serv.print_term(0, 2, '')
