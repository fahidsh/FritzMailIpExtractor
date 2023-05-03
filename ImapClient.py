import email
import imaplib
from dataclasses import dataclass
from email.header import decode_header


@dataclass
class ImapInfo:
    user: str = "user@domain.com"
    password: str = "password"
    folder: str = "Inbox"
    server: str = "imap.domain.com"
    port: int = 993
    ssl: bool = True


class ImapClient:
    messages_info_list: list = []

    def __init__(self, imap_info: ImapInfo, max_messages: int = 0, skip_messages: int = 0):
        if imap_info is None:
            raise Exception("No server specified")

        self.max_messages = max_messages
        self.skip_messages = skip_messages

        if imap_info.ssl:
            self.imap = imaplib.IMAP4_SSL(imap_info.server, imap_info.port)
        else:
            self.imap = imaplib.IMAP4(imap_info.server, imap_info.port)

        self.imap.login(imap_info.user, imap_info.password)
        # print(self.imap.list())  # print various inboxes
        self.status, self.messages = self.imap.select(imap_info.folder)
        self.num_of_messages = int(self.messages[0])

    def read_subjects(self):
        # if self.max_messages is not 0, then read only the first self.max_messages
        if self.max_messages != 0 and self.max_messages < self.num_of_messages:
            messages_to_read = self.max_messages
        else:
            messages_to_read = self.num_of_messages - 1

        for i in range(self.skip_messages, messages_to_read):
            res, msg = self.imap.fetch(str(i + 1), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    date = decode_header(msg["Date"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    # print("Subject:", subject)
                    # print("Date:", date)
                    self.messages_info_list.append((subject, date))
                    # self.messages_info_list.append({"subject": subject, "date": date})
