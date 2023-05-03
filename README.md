# FritzMailIpExtractor

---
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

---
## Examples of the email subject and date
Example of the email subject that contains the IP addresses:
- `Internet-Adresse: 37.24.81.123`
- `Internet-Adresse: 77.181.147.218, 2a01:c23:8200:8a81:7eff:4dff:fec2:9d85`

Example of the email date:
- `Sun, 5 Feb 2023 05:24:57`
- `Sat, 3 Jul 2021 15:30:20 +0200`

---
## Modules
The script uses the following modules:
- imaplib
- email
- email.header
- dataclasses
- datetime

As far as I know all these modules are part of the standard library, so not have to install any additional modules.

### Python Version: 3.9
The script was written and tested with Python 3.9. I have not tested it with other versions of Python. But I think it should work with Python 3.7 and above.

---
## Classes
The script uses the following classes:
- ImapInfo
- ImapClient
- IpInfo

All the classes are included in this package.

---
## Usage
Usage:
- Either fill in the `ImapInfo` class with your IMAP server details or create an instance of the `ImapInfo` class with your IMAP server details in the first lines of the `main()` function. That's it. Then run the script.
- The script will read the emails from the IMAP server and extract the IP addresses and the date and time from the email subject and date. Then it will save the IP addresses and the date and time to a CSV file.
- The script will create a CSV file with the name `ip_info.csv` in the same directory where the script is located.

### Example of the CSV file
```csv
timestamp;ipv4;ipv6;readable-date
1638073710;77.12.203.217;2a01:c22:ca01:211:7eff:4dff:fec2:9d85;2021-11-28 05:28:30
1638160050;77.190.187.93;2a01:c22:d601:d537:7eff:4dff:fec2:9d85;2021-11-29 05:27:30
1631289069;37.24.81.123;;2021-09-10 17:51:09
```

### As Table
| timestamp | ipv4          | ipv6                                      | readable-date         |
|-----------|---------------|-------------------------------------------|-----------------------|
| 1638073710| 77.12.203.217 | 2a01:c22:ca01:211:7eff:4dff:fec2:9d85      | 2021-11-28 05:28:30   |
| 1638160050| 77.190.187.93 | 2a01:c22:d601:d537:7eff:4dff:fec2:9d85     | 2021-11-29 05:27:30   |
| 1631289069| 37.24.81.123  |                                           | 2021-09-10 17:51:09   |

> Note: 
> - The `readable-date` is in the format `YYYY-MM-DD HH:MM:SS`.
> - Column headers are not part of the generated CSV file.

---
## Author
Author: Fahid Shehzad 
[GitHub](https://github.com/fahidsh)

---
## About
- Date created: 2023-05-03
- Date last modified: 2023-05-03

---
## License
License: MIT License