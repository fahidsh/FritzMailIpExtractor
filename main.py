"""
FritzMailIpExtractor
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

import IpInfo
from ImapClient import ImapClient, ImapInfo


def save_list_to_file(list_to_save, file_name):
    # save list to file, create file if it does not exist
    with open(file_name, 'w') as f:
        for item in list_to_save:
            f.write("%s\n" % item)


def main(name):
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
        ip_info = IpInfo.get_ip_info_from_subject_and_date(message[0], message[1])
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
    main("PyCharm")
