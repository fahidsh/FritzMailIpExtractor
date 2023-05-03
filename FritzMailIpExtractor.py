"""
FritzMailIpExtractor.py
=======================
I have a FritzBox router at home and I have configured it to send me emails on router settings changes and on
change of the IP address. Previously I used a static IP address, but now for long time I am getting a dynamic
IP address from my ISP. The IP address changes at least once a day, but sometimes it changes more often. I wanted
to keep track of the IP addresses that were assigned to my router. But the IP addresses were saved in the emails.
So I wrote this script to extract the IP addresses from the emails and save them to a CSV file, eventually to database.
I could make the script save the IPs direct to database, but I wanted to keep my script it simple and generic, use
the least amount of dependencies and make it easy to understand and modify. So I decided to save the IPs to a CSV file.

The subject of the email contains the IP addresses and the date of the email contains the date and time when the
IP address was assigned to the router. The script reads the emails from the IMAP server and extracts the IP addresses
and the date and time from the email subject and date. Then it saves the IP addresses and the date and time to a
CSV file.

Example of the email subject that contains the IP addresses:
    Internet-Adresse: 37.24.81.123
    Internet-Adresse: 77.181.147.218, 2a01:c23:8200:8a81:7eff:4dff:fec2:9d85
Example of the email date:
    Sun, 5 Feb 2023 05:24:57
    Sat, 3 Jul 2021 15:30:20 +0200

The script uses the following modules:
    - imaplib
    - email
    - email.header
    - dataclasses
    - datetime
As far as I know all these modules are part of the standard library, so not have to install any additional modules.

The script uses the following classes:
    - ImapInfo
    - ImapClient
    - IpInfo
All the classes are included in this package.

Usage:
    - Either fill in the ImapInfo class with your IMAP server details or create an instance of the ImapInfo class
    with your IMAP server details in the first lines of the main() function. That's it. Then run the script.
    - The script will read the emails from the IMAP server and extract the IP addresses and the date and time from
    the email subject and date. Then it will save the IP addresses and the date and time to a CSV file.
    - The script will create a CSV file with the name "ip_info.csv" in the same directory where the script is located.

Author: Fahid Shehzad <https://github.com/fahidsh>
Date created: 2023-05-03
Date last modified: 2023-05-03
Python Version: 3.9
License: MIT License
"""

from dataclasses import dataclass
from datetime import datetime
import email
import imaplib
from email.header import decode_header


# ************************************
""" ImapInfo class """
# ************************************


@dataclass
class ImapInfo:
    user: str = "user@domain.com"
    password: str = "password"
    folder: str = "Inbox"
    server: str = "imap.domain.com"
    port: int = 993
    ssl: bool = True


# ************************************
""" InInfo class """
# ************************************

def get_ip_info_from_subject_and_date(subject: str = None, date: str = None):
    subject_identifier = "Internet-Adresse: "
    if subject.startswith(subject_identifier):
        # get ipv4 and ipv6 from subject
        if subject.count(",") == 1:
            ipv4, ipv6 = subject.replace(subject_identifier, "").split(", ")
            # remove [] and white spaces from ipv6 address
            ipv6 = ipv6.replace("[", "").replace("]", "").strip()
        else:
            ipv4 = subject.replace(subject_identifier, "").strip()
            ipv6 = ""

        ip_info = IpInfo(ipv4, ipv6, date)
        return ip_info
    else:
        return None


def get_ipv4_as_integer(ipv4: str = None):
    octets = ipv4.split(".")
    ip_number = (int(octets[0]) << 24) + (int(octets[1]) << 16) + (int(octets[2]) << 8) + int(octets[3])
    return ip_number


def get_ipv4_from_integer(ip_number: int = None):
    smallest_number = 16777216  # 1.0.0.0
    largest_number = 4294967295  # 255.255.255.255

    if ip_number is None or ip_number < smallest_number or ip_number > largest_number:
        return None

    octet1 = (ip_number >> 24) & 255
    octet2 = (ip_number >> 16) & 255
    octet3 = (ip_number >> 8) & 255
    octet4 = ip_number & 255
    ipv4_address = f"{octet1}.{octet2}.{octet3}.{octet4}"
    return ipv4_address


def get_ipv6_as_integer(ipv6: str = None):
    # split into 8 groups of 16-bit values
    groups = ipv6.split(':')
    # convert each group to 16-bit binary representation
    binary_groups = [bin(int(g, 16))[2:].zfill(16) for g in groups]
    # concatenate binary groups into 128-bit binary string
    binary_string = ''.join(binary_groups)
    # convert binary string to integer
    ip_number = int(binary_string, 2)
    return ip_number


def get_ipv6_from_integer(ip_number: int = None):
    # convert integer to binary string
    binary_string = bin(ip_number)[2:].zfill(128)
    # split binary string into 8 groups of 16-bit values
    binary_groups = [binary_string[i:i + 16] for i in range(0, 128, 16)]
    # convert each group to hexadecimal representation
    hex_groups = [hex(int(g, 2))[2:].zfill(4) for g in binary_groups]
    # concatenate hexadecimal groups into IPv6 address string
    ipv6_address = ':'.join(hex_groups)
    return ipv6_address


@dataclass
class IpInfo:
    ipv4: str
    ipv6: str
    datetime_string: str  # Sun, 5 Feb 2023 05:24:57 +0100

    def __init__(self, ipv4, ipv6, datetime_string):
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.datetime_string = datetime_string
        # Sun, 5 Feb 2023 05:24:57 +0100 or Sun, 5 Feb 2023 05:24:57
        date_format = datetime_string.count("+") == 1 and "%a, %d %b %Y %H:%M:%S %z" or "%a, %d %b %Y %H:%M:%S"
        self.dt = datetime.strptime(datetime_string, date_format)

    def __str__(self):
        return "IPv4: " + self.ipv4 + " IPv6: " + self.ipv6 + " Date: " + self.datetime_string

    def get_date(self):
        date = self.dt.strftime("%Y-%m-%d")
        return date

    def get_time(self):
        time = self.dt.strftime("%H:%M:%S")
        return time

    def get_sql_date(self):
        date = self.dt.strftime("%Y-%m-%d %H:%M:%S")
        return date

    def get_timestamp(self):
        timestamp = self.dt.timestamp()  # seconds since 1970-01-01 00:00:00
        return int(timestamp)

    def get_as_csv_string(self):
        return str(self.get_timestamp()) + ";" + self.ipv4 + ";" + self.ipv6 + ";" + self.get_sql_date()


# ************************************
""" ImapClient class """
# ************************************


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


# ************************************
""" Main Method """
# ************************************


def save_list_to_file(list_to_save, file_name):
    # save list to file, create file if it does not exist
    with open(file_name, 'w') as f:
        for item in list_to_save:
            f.write("%s\n" % item)


def main():
    i_info: ImapInfo = ImapInfo()
    client = ImapClient(i_info)
    print(f'Total E-Mails: {client.num_of_messages}')
    print(f'E-Mails to be processed(0 means all): {client.max_messages}')
    print(f'E-Mails to be skipped from start: {client.skip_messages}')
    print("----------------------------------------------")
    client.read_subjects()

    ip_info_list: list = []
    non_ip_mails: int = 0
    mails_with_ip: int = 0

    for message in client.messages_info_list:
        ip_info = get_ip_info_from_subject_and_date(message[0], message[1])
        if ip_info is not None:
            print(ip_info.get_as_csv_string())
            ip_info_list.append(ip_info.get_as_csv_string())
            mails_with_ip += 1
        else:
            non_ip_mails += 1
    print("----------------------------------------------")
    print(f"Total {non_ip_mails+ mails_with_ip} processed, {non_ip_mails} skipped, {mails_with_ip} with IP")
    save_list_to_file(ip_info_list, "ip_info.csv")


if __name__ == '__main__':
    main()
