from blessings import Terminal
import zmq
import os


class Main_Class:
    """The class is used to output text in the terminal and to send/receive messages(zmq)"""
    term = Terminal()
    answer_loc = term.height - 1

    def __init__(self):
        self.context = zmq.Context()
        os.system('clear')

    def print_term(self, x, y, text):
        """Printing text in the terminal"""
        with self.term.location(x, y):
            print(f'{text}{self.clear_str(len(text))}')

    def input_term(self, x, y):
        """Input text in terminal"""
        with self.term.location(x, y):
            msg_input = input("Input your text : ")
        return msg_input

    def send_str(self, text):
        """Send message in zmq"""
        self.socket.send_string(text)

    def recv_str(self):
        """Receive message from zmq"""
        msg_input = self.socket.recv_string()
        return msg_input

    def exit_serv(self, message):
        """Close server and client"""
        if message == 'exit':
            os.system('clear')
            exit()

    def clear_str(self, val=0):
        """Clear string"""
        return ' ' * (self.term.width - val)

    def hidden_input(self, y, y_input_line):
        """Hiding the input line"""
        self.print_term(0, y, 'You must wait answer')
        with self.term.hidden_cursor():
            self.print_term(0, y_input_line, '')


def main():
    pass


if __name__ == '__main__':
    main()
