from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os.path import abspath
from argparse import ArgumentParser
from time import sleep
from smtplib import SMTP
from email.message import EmailMessage


def init():
    parser = ArgumentParser(
        description="Monitors status of your parcel every 30 minutes and alerts the user if there is an update.")
    parser.add_argument("tid", help="Tracking ID of parcel.")
    parser.add_argument("pid", help="Delivery postal code.")
    args = parser.parse_args()

    return args.tid, args.pid, 0


class CheckStatus:
    def __init__(self, tid, pid, flag, *args):
        self.status = None
        self.email_flag = flag
        self.id = tid
        self.pid = pid
        self.url = f'https://track.bpost.cloud/btr/web/#/search?lang=en&itemCode={self.id}&postalCode={self.pid}'
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        self.driver = webdriver.Chrome(executable_path=abspath("chromedriver"),
                                       options=self.chrome_options)

        if self.email_flag:
            self.email = Email(args[0], args[1])

    def check(self):
        self.driver.get(self.url)
        self.status = self.driver.find_element_by_class_name('heading').text

    def get_sender(self):
        response =  self.driver.find_element_by_class_name('parceln').text
        return response.split()[3]

    def set_email_flag(self, flag):
        self.email_flag = flag

    def detect_change(self):
        current_status = self.status
        self.check()
        if not current_status == self.status:
            print(f"Package status has changed to: {self.status}.")
            if self.email_flag:
                self.email.send(status)


class Email:

    def __init__(self, *args):
        self.server = SMTP('smtp.gmail.com', 587)
        self.email = args[0]
        self.password = args[1]
        self.server.login(self.email, self.password)
        self.msg = EmailMessage()

    def send(self, status):
        self.msg['Subject'] = 'Your bpost parcel status has changed!'
        self.msg['From'] = self.email
        self.msg['To'] = self.email
        self.msg.set_content(status)
        self.server.send_message(self.msg)


if __name__ == '__main__':
    tid, pid, flag = init()
    status = CheckStatus(tid, pid, flag)
    status.check()
    print(f"Monitoring status of bpost package from {status.get_sender()}...")
    while 1:
        sleep(1800)
        status.detect_change()
