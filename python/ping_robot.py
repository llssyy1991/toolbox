from PyQt4.QtCore import *
import os
import time
import script_cmd
import re

class network_check(QThread):

    def __init__(self, IP, robo, hostname):

        super(network_check, self).__init__()
        self.IP = IP
        self.robo = robo
        self.hostname = hostname

    def run(self):

        while(True):
            response = script_cmd.command_output_NoPopout(["ping", "-n", "1 ", self.IP])
            # print response
            result = re.search("TTL=", str(response))

            if result == None:
                if self.hostname == "windows":
                    self.robo.messenger.windows_off.emit()
                    print self.hostname + " is down ."

                if self.hostname == "linux":
                    self.robo.messenger.linux_off.emit()
                    print self.hostname + " is down ."
            time.sleep(15)

class wifi_check(QThread):

    static_SSID = "Rabit_1"

    def __init__(self, robo):
        super(wifi_check, self).__init__()
        self.transmit_rate = 0
        self.receive_rate = 0
        self.signal = 0
        self.robo = robo

    def run(self):

        while True:
            response = script_cmd.command_output_NoPopout("netsh wlan show interfaces")
            result = re.search(self.static_SSID, str(response))
            receive_rate = re.search("Receive rate .*:\s(\w*)", response, re.I)
            transmit_rate = re.search("Transmit rate .*:\s(\w*)", response, re.I)
            signal =  re.search("Signal .*:\s(\w*)", response, re.I)
            # print receive_rate.group(1)
            # print transmit_rate.group(1)
            # print signal.group(1)

            if receive_rate is not None:
                self.receive_rate = int(receive_rate.group(1))
                self.transmit_rate = int(transmit_rate.group(1))
                self.signal = int(signal.group(1))
            if result is None or receive_rate is None:
                self.robo.messenger.wifi_connectError.emit()
                self.robo.messenger.signal_strength.emit(self.signal)
                self.robo.messenger.receive_rate.emit(self.receive_rate)
                self.robo.messenger.transmit_rate.emit(self.transmit_rate)

            time.sleep(10)


if __name__ == '__main__':
    test = wifi_check(1)
    test.run()

