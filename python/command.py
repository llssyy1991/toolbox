import pika
import uuid
from wait_dialog import Wait_dialog
from fail_dialog import Fail_dialog
from PyQt4.QtCore import *
from static_parameter import *
import static_parameter
import time
from util_functions import debug_log_timestamped, WARN_TAG
import datetime

# command_with_waiting_dial is used to send a command to robot, while keep a modal dialogue which
# disconnect user's input in order not let user break crash the program

response_value = None

class command_with_waiting_dial(QObject):

    statue_update = pyqtSignal(str)
    def __init__(self,address=robot_address):
        super(command_with_waiting_dial,self).__init__()
        self.address = address
        self.dial = None
        self.fail_dial = None
        self.com = None
        # self.lin_com = command_without_waiting_dial()

    # commands : must be a list
    # example : [check_er]
    def send_command(self,commands,Channel,Response):
        self.commands=commands
        self.dial=Wait_dialog()
        if self.commands[0] in command_captions:
            print "cmd is :" + self.commands[0]
            self.dial.ui.label.setText("executing command : " + command_captions[self.commands[0]])
        else:
            self.dial.ui.label.setText("executing command : " + self.commands[0])
        self.dial.show()
        self.commands=commands

        while self.com is not None and not self.com.isFinished():
            time.sleep(1) # Wait for last command to finish before sending new one

        self.com=command_without_waiting_dial(self.address,commands,Channel,Response)
        self.com.statue_update.connect(self.command_result)

        self.com.start()

    # according to the response given by
    # handle success/fail event of sending command
    def command_result(self,result):
        self.statue_update.emit(result)

        if self.commands:
            self.commands.pop(0)

        if not self.commands:
            self.dial.close()
            return

        if result != "True":
            self.dial.close()
            self.fail_dial = Fail_dialog()
            self.fail_dial.ui.fail_label.setText(result)
            self.fail_dial.show()
            return

        if self.dial is None:
            return

        if self.commands[0] in command_captions:
            self.dial.ui.label.setText("executing command : " + command_captions[self.commands[0]])
        else:
            self.dial.ui.label.setText("executing command : " + self.commands[0])



# Command_without_waiting_dial is used to send command to robot , but not
# blocking the soc application

class command_no_waiting_dial(QObject):

    def __init__(self,address=robot_address):
        super(command_no_waiting_dial,self).__init__()
        self.address = address
        self.fail_dial = None
        self.com = None

    def send_command(self,commands,Channel,Response):
        self.commands=commands

        while self.com is not None and not self.com.isFinished():
            time.sleep(1) # Wait for last command to finish before sending new one

        self.com=command_without_waiting_dial(self.address,commands,Channel,Response)
        self.com.statue_update.connect(self.command_result)

        self.com.start()

    def command_result(self,result):
        if self.commands:
            self.commands.pop(0)

        if result != "True":
            self.fail_dial = Fail_dialog()
            self.fail_dial.ui.fail_label.setText(result)
            self.fail_dial.show()
            return

        if self.dial is None:
            return

        if self.commands[0] in command_captions:
            self.dial.ui.label.setText("executing command : " + command_captions[self.commands[0]])
        else:
            self.dial.ui.label.setText("executing command : " + self.commands[0])

class command_without_waiting_dial(QThread):

    statue_update = pyqtSignal(str)
    def __init__(self,address = robot_address,Commands = None,Channel = None,Response = None):
        super(command_without_waiting_dial,self).__init__()
        self.address = address
        if Commands != None:
            self.commands = Commands[:]
        else:
            self.commands = []
            debug_log_timestamped("Initializing command handler for: "+Channel+", "+Response)
        self.Channel = Channel
        self.Response = Response
        self.connection_counter = 0
        self.interrupt = False
        self.channel = None

    def run(self):        
        try:
            for command in self.commands:
                self.send_command(command)
        except:
            # the queue will attempt to connect for at most 25 time, if exceeded 25 times, a signal will
            # be sent to commander to close wait dialog and create another dialog to declare the reason that
            # makes the command sending fail
            debug_log_timestamped(WARN_TAG+"Failed to send command. (Attempt " + str(self.connection_counter+1)+")")
            self.connection_counter = self.connection_counter + 1
            if self.connection_counter >= 25:
                debug_log_timestamped(WARN_TAG+" Timed out. Giving up on command sending.")
                return
            self.run()

    def attemp_connect(self):
        # making connection between
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=self.address, heartbeat_interval = 0))
        if self.connection == False:
            debug_log_timestamped("Connection failed.")

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue = self.Channel)

    #send command to windows
    #return response if successful
    def send_command(self, Command):        
        debug_log_timestamped("Sending command: "+str(Command))
        if self.channel is None:
            if self.address != "localhost":
                self.attemp_connect()
        
        self.interrupt = False
        
        if self.address == "localhost": #Skip command sending if running locally
            debug_log_timestamped("Response: skipped -- running on localhost")
            self.statue_update.emit("True")
            return "True" 
        static_parameter.robot_copy.handler.result = self
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange = '',
            routing_key = self.Channel,
            properties = pika.BasicProperties(
            reply_to = self.Response,#name of the call back queue
            correlation_id = self.corr_id
        ),
        body = str(Command)
    )
        print "interrupt is :" + str(self.interrupt)
        while self.response is None and not self.interrupt:
            self.connection.process_data_events()

        if self.interrupt:
            self.response = "False"
        self.interrupt = False
        debug_log_timestamped("Response: "+str(self.response))

        if self.response == "False":
            # based on different command, different dialogue will be shown to notify the user that
            # what happened that makes the operation unsuccessful
            self.statue_update.emit(Command+"  failed")
            self.terminate()
            return "False"
        self.statue_update.emit("True")
        return self.response


    def send_command_timeout(self, Command, timeout):

        debug_log_timestamped("Sending command: " + str(Command))
        self.interrupt = False

        if self.address == "localhost":  # Skip command sending if running locally
            debug_log_timestamped("Response: skipped -- running on localhost")
            self.statue_update.emit("True")
            return "True"
        static_parameter.robot_copy.handler.result = self
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.Channel,
            properties=pika.BasicProperties(
                reply_to=self.Response,  # name of the call back queue
                correlation_id=self.corr_id
            ),
            body=str(Command)
        )
        time_start = datetime.datetime.now()

        while self.response is None and not self.interrupt:
            time_current = datetime.datetime.now()
            if (time_current - time_start).total_seconds() > timeout:
                break
            self.connection.process_data_events()

        if self.interrupt:
            self.response = "False"
        self.interrupt = False
        debug_log_timestamped("Response: " + str(self.response))

        if self.response == "False":
            # based on different command, different dialogue will be shown to notify the user that
            # what happened that makes the operation unsuccessful
            self.statue_update.emit(Command + "  failed")
            self.terminate()
            return "False"
        self.statue_update.emit("True")
        return self.response

    #accept response from 'windows-response' queue
    #store the response body in self.win_response
    def terminate_and_send(self,commands):
        self.termin = True
        time.sleep(1)
        self.commands = commands[:]
        self.start()

    def no_response_communicate(self,command):
        debug_log_timestamped("Sending command: "+str(command))
        if self.address == "localhost":
            return
        elif self.channel is None:
            self.attemp_connect()
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange = '',
            routing_key = self.Channel,
            properties = pika.BasicProperties(
            reply_to = self.Response,#name of the call back queue
            correlation_id = self.corr_id
        ),
        body = str(command)
    )

command=command_with_waiting_dial(robot_address)


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import *
    from login import Log_in
    app = QApplication(sys.argv)
    command = command_with_waiting_dial(robot_address)
    command.send_command(["check_gpr","check_gpr","shutdown_gpr"],linux_channel,linux_response)
    mainwindow = Log_in()
    mainwindow.show()
    sys.exit(app.exec_())
