import sys
import time
import logging
import os
import smtplib

from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


port = 587
server = "smtp-mail.outlook.com"


# file path
currentDir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = currentDir / ".env" # .env file variables
load_dotenv(envars)

# read the variables from the .env file
sender = os.getenv("Email")
senderPassword = os.getenv("Password")
# senderTuple = ("Stock price folder", f"{sender}")

def emailToSend(subject, reciever, Event, folder):

    port = 587
    server = "smtp-mail.outlook.com"

    emailMsg = EmailMessage()
    emailMsg["Subject"] = subject
    emailMsg["From"] = formataddr(("Stock price folder", f"{sender}"))
    emailMsg["To"] = reciever
    emailMsg["BCC"] = sender

    emailMsg.set_content(
        f"""\
        Hi,
        Please note that {Event} has taken place with this folder {folder}
        """
    )

        # html version of the message

    emailMsg.add_alternative(
        f"""\
        <html>
            <body>
                <p>Hi, </p>
                <p> Please note that <strong> {Event} </strong> has taken place with this folder <strong> {folder}  </strong> </p>
            </body>
        </html>
        """,
            subtype="html"
    )

    # preparing the email to be sent and logging to the email server.

    with smtplib.SMTP(server, port) as server:
        server.starttls()
        server.login(sender, senderPassword)
        server.sendmail(sender, reciever, emailMsg.as_string())


def file_creation(event):
    print("file created")
    emailToSend(
        subject="test",
        reciever="unamedpersonemail@gmail.com",
        Event="file created",
        folder="main folder"
    )

def file_deleted(event):
    print("file deleted")
    emailToSend(
    subject="file deleted",
    reciever="unamedpersonemail@gmail.com",
    Event="file deleted",
    folder="main folder"
    )

def file_modified(event):
    print("file modified")
    emailToSend(
        subject="test",
        reciever="unamedpersonemail@gmail.com",
        Event="file modified",
        folder="main folder"
    )

def file_moved(event):
    print("file moved")
    emailToSend(
        subject="test",
        reciever="unamedpersonemail@gmail.com",
        Event="file moved",
        folder="main folder"
    )

if __name__ == "__main__":

# testing the emailToSend funtion
# It works!!

    # emailToSend(
    #     "test",
    #     "unamedpersonemail@gmail.com",
    #     "demo",
    #     "Demo folder"
    # )


# file and event handlers 

    event_handler = FileSystemEventHandler()

    event_handler.on_created = file_creation
    event_handler.on_deleted = file_deleted
    event_handler.on_modified = file_modified
    event_handler.on_moved  = file_moved

    path = "C:/Users/abdal/OneDrive/Desktop/desktop of Desktop"

# an opserver that will call on the event handler when an event takes place.
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

#
    try:
        print("Monitoring")
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        print("Done")
        observer.join()

