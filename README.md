
# Automated Email Sender

Automated Email Sender is a Python-based project designed to simplify the process of sending mass emails. This application sends emails to a list of recipients with a specified message and can also include attachments. It uses Flask to create an application context and Flask-Mail to handle email sending.

## Features

* Support for both plain text and HTML emails
* Email attachment support
* Automatic reconnection after network interruptions
* Email sending scheduling support
* Keyboard interrupt handling

## Installation

Before installing the Automated Email Sender, ensure you have the following dependencies installed:

* Python 3.x
* Flask
* Flask-Mail
* schedule

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Flask, Flask-Mail, and schedule.

```bash
pip install flask flask-Mail schedule
```



## Usage

To use the Automated Email Sender, use the following code snippet as a guide:

```python
from email_sender import Sendmail

process = Sendmail(
mailing_path='Test',
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

process.send_mail()
```


## Configuration

The `Sendmail` class accepts the following arguments for configuration:

* `mailing_path`: The path where the project files are located (must be within "Projects" directory).
* `email_address`: The email address that you want to send emails from.
* `email_password`: The password for the email address you are sending emails from.
* `email_server`: The mail server you are using to send emails.
* `emails_file_path`: The path to a text file containing recipient email addresses, one per line.
* `sender_name`: The name that will appear as the sender of the email.
* `subject`: The subject line of the email.
* `body_html`: The path to an HTML file containing the email body.
* `body_plain`: The path to a plain text file containing the email body.
* `time_to_sleep`: The delay between sending emails, in seconds.
* `attachment_names`: A list of attachments to include with the email. These should be files located in `mailing_path`.
* `log_file`: The name of the file where the program will log the sent emails (default log.txt).


