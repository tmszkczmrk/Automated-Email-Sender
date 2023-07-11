from os import remove, rename
from sys import exit
from flask import Flask
from flask_mail import Mail, Message
from time import sleep
from smtplib import SMTPServerDisconnected
from socket import gaierror
import multiprocessing
import schedule
import time
import datetime

class Sendmail:

    def __init__(self, mailing_path, email_address, email_password, email_server, emails_file_path,
                 sender_name, subject, body_html, body_plain, time_to_sleep, attachment_names, log_file='logs.txt'):

        self.main_path = '.\\Projects\\' + mailing_path + "\\"
        self.email_address = email_address
        self.email_password = email_password
        self.email_server = email_server
        self.emails_file_path = self.main_path + emails_file_path
        self.sender_name = sender_name
        self.subject = subject
        self.body_html = self.main_path + body_html
        self.body_plain = self.main_path + body_plain
        self.time_to_sleep = time_to_sleep
        self.attachment_names = attachment_names
        self.log_file = self.main_path + log_file

    def start_flask_app(self):

        flask_app = Flask(__name__)

        mail_settings = {
            "DEBUG": False,
            "MAIL_PORT": 465,
            "MAIL_USE_TLS": False,
            "MAIL_USE_SSL": True,

            "MAIL_SERVER": self.email_server,
            "MAIL_USERNAME": self.email_address,
            "MAIL_PASSWORD": self.email_password,
        }

        flask_app.config.update(mail_settings)

        return flask_app

    def count_emails(self):

        with open(self.emails_file_path, 'r', encoding='utf-8') as f:
            for counter in enumerate(f):
                pass
        return counter[0] + 1

    def send_mail(self):

        flask_app = self.start_flask_app()

        email_handler = Mail(flask_app)

        with flask_app.app_context():

            with open(self.emails_file_path, 'r', encoding='utf-8') as emails:

                for counter, email in enumerate(emails, start=1):

                    email = email.strip()

                    with open(self.log_file, 'a', encoding='utf-8', buffering=1) as backup:
                        backup.write(f'[{datetime.datetime.now().day}.{datetime.datetime.now().month} {datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}] - {email}\n')

                    try:

                        msg = Message(sender=(self.sender_name, self.email_address),
                                      subject=self.subject,
                                      recipients=[email],
                                      html=open(self.body_html, encoding='utf-8').read(),
                                      body=open(self.body_plain, encoding='utf-8').read(),
                                      reply_to=self.email_address,
                                      extra_headers={'Disposition-Notification-To': self.email_address}
                                      )

                        if self.attachment_names:

                            for attachment_name in self.attachment_names:
                                with flask_app.open_resource(self.main_path + attachment_name) as attachment:
                                    msg.attach(attachment_name, 'application/pdf', attachment.read())
                        else:
                            pass

                        email_handler.send(msg)
                        time_to_execute = round((((self.count_emails() - counter) * self.time_to_sleep) / 86400), 2)
                        # system('cls')
                        print(f'{self.email_address}: {email}  ---  {counter}/'
                              f'{self.count_emails()} --- {time_to_execute} days left')

                        sleep(self.time_to_sleep)

                    except (SMTPServerDisconnected, gaierror):

                        print('Network disconnected...')
                        sleep(60)
                        print('Continue...')
                        continue

                    except KeyboardInterrupt:

                        print('Preparing to close...')
                        sleep(2)
                        print('Fixing file...')

                        temp_name = f'{self.emails_file_path}.tmp'
                        flag = True

                        with open(self.emails_file_path, 'r', encoding='utf-8') as f:
                            with open(temp_name, 'a', encoding='utf-8') as output:
                                for line in f.readlines():
                                    if flag:
                                        if line.strip() == email:
                                            flag = False
                                            continue
                                    if not flag:
                                        output.write(line)

                        print(f'Closing {self.emails_file_path}')
                        emails.close()
                        sleep(1)
                        remove(self.emails_file_path)
                        rename(temp_name, self.emails_file_path)

                        print('Bye bye')
                        exit()

                    except Exception as err:

                        print(err)
                        pass
        return True


def main():

    test = Sendmail(mailing_path='Test',
                      email_address='test@test.com',
                      email_password='p455wo0rd',
                      email_server='mail-server.com',
                      emails_file_path='recipients.txt',
                      sender_name='Test',
                      subject='Lorem ipsum',
                      body_html='content.html',
                      body_plain='content.txt',
                      time_to_sleep=30,
                      attachment_names=[],
                      log_file='log.txt',
                      )

    try:

        test_pool = multiprocessing.Process(target=test.send_mail)
        test_pool.start()
        test_pool.join()

    except KeyboardInterrupt:
        pass

    return True


if __name__ == '__main__':

    main()


    #time_to_start = "08:30"
    #schedule.every().day.at(time_to_start).do(main)
    #print(f'\nScheduled sending at {time_to_start}...')

    #while True:
    #    schedule.run_pending()
    #    time.sleep(60)