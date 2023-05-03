from dataclasses import dataclass
from datetime import datetime


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
