from ipaddress import IPv4Address, AddressValueError


class IPAddress:
    """IP address class"""

    def __init__(self, ip):
        self._ip = ip

    @property
    def ip(self):
        """Returns IP address"""
        return self._ip

    @staticmethod
    def validate(ip):
        """Returns True if IP address is valid otherwise False"""
        try:
            IPv4Address(ip)
        except AddressValueError:
            return False
        else:
            return True

    @staticmethod
    def geo_info(ip):
        """TBI"""
        pass

    @staticmethod
    def external_ip(ip):
        """TBI"""
        pass
