# Connect to a switch through Telnet
import telnetlib
import re
from time import sleep
import datetime


#Global Variables
WAIT_TIME_15 = 15
WAIT_TIME_1 = 1
TELENT_TIMEOUT = 60


class SwitchObj:
    def __init__(self, hostname='', username='admin', password='admin', prompt='', port=23):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.prompt = prompt + ".*#"
        self.tn = None
        self.tn = self.connect(prompt)


    def __enter__(self):
        return self


    def __exit__(self):
        self.disconnect()


    def connect(self, prompt):
        tn = telnetlib.Telnet(self.hostname, self.port)
        print(tn)
        sleep(WAIT_TIME_1)
        tn.write("\x0D")

        if self.username:
            tn.read_until("login:", TELENT_TIMEOUT)
            tn.write(self.username + '\n')
            sleep(WAIT_TIME_1 * 5)
            tn.read_until("Password:", TELENT_TIMEOUT)
            tn.write(self.password + '\n')
            sleep(WAIT_TIME_1 * 5)

        tn.write("configure terminal")
        sleep(WAIT_TIME_1 * 5)
        tn.write("hostname " + prompt + "\n")
        sleep(WAIT_TIME_1 * 5)
        tn.write("no page\n")
        sleep(WAIT_TIME_1 * 5)
        tn.write("exit\n")
        sleep(WAIT_TIME_1 * 5)

        out = tn.read_until(self.prompt, TELENT_TIMEOUT)
        out = re.search(prompt, out)

        if out:
            print("Successfully Connected to terminal")
            return tn
        else:
            return None


    def disconnect(self):
        self.tn.close()
        sleep(1)


    def execute_command(self, command, longWait=False, verify_prompt=True):
        if not command[-1] == '\n':
            command = '\n' + command + '\n'
        self.tn.write(command)
        sleep(WAIT_TIME_1 * 2)
        if longWait:
            sleep(WAIT_TIME_15 * 2)
        if verify_prompt:
            out = self.tn.read_until(self.prompt, TELENT_TIMEOUT)
            return out
        else:
            return None


def connectToHost(ip_addr, port, username, password, prompt):
    switch = SwitchObj(hostname=ip_addr, username=username,
                       password=password, prompt=prompt, port=port)
    filename = "Log_File.txt"
    log_file = open(filename, "a+")
    log_file.write("\n" + str(datetime.datetime.now()) + "\n================================\n")
    log_file.write(switch.execute_command("\nshow system\n"))
    log_file.write("\n" + str(datetime.datetime.now()) + "\n================================\n")
    switch.disconnect()
    log_file.close()


#Connect to Host
connectToHost("10.93.56.106")
