import click
import utilities_common.cli as clicommon
from tabulate import tabulate

from swsscommon.swsscommon import SonicV2Connector


# STATE_DB Table
DHCPv6_COUNTER_TABLE = 'DHCPv6_COUNTER_TABLE'

# DHCPv6 Counter Messages
messages = ["Unknown", "Solicit", "Advertise", "Request", "Confirm", "Renew", "Rebind", "Reply", "Release", "Decline", "Relay-Forward", "Relay-Reply"]

class DHCPv6_Counter(object):
    def __init__(self):
        self.db = SonicV2Connector(use_unix_socket_path=False)
        self.db.connect(self.db.STATE_DB)
        self.table_name = DHCPv6_COUNTER_TABLE + self.db.get_db_separator(self.db.STATE_DB)


    def get_interface(self):
        """ Get all names of all interfaces in DHCPv6_COUNTER_TABLE """
        vlans = []
        for key in self.db.keys(self.db.STATE_DB):
            if DHCPv6_COUNTER_TABLE in key:
                vlans.append(key[21:])
        return vlans
        

    def get_dhcp6relay_msg_count(self, interface, msg):
        """ Get count of a dhcp6relay message """
        count = self.db.get(self.db.STATE_DB, self.table_name + str(interface), str(msg))
        data = [str(msg), count]
        return data

    
    def clear_table(self, interface):
        """ Reset all message counts to 0 """
        for msg in messages:
            self.db.set(self.db.STATE_DB, self.table_name + str(interface), str(msg), '0') 

def print_count(counter, intf):
    """Print count of each message"""
    data = []
    for i in messages:
        data.append(counter.get_dhcp6relay_msg_count(intf, i))
    print(tabulate(data, headers = ["Message Type", intf], tablefmt='simple', stralign='right') + "\n")


#
# 'dhcp6relay_counters' group ###
#


@click.group(cls=clicommon.AliasedGroup, name="dhcp6relay_counters")
def dhcp6relay_counters():
    """Show DHCPv6 counter"""
    pass


# 'counts' subcommand ("show dhcp6relay_counters counts")
@dhcp6relay_counters.command('counts')
@click.option('-i', '--interface', required=False)
@click.option('--verbose', is_flag=True, help="Enable verbose output")
def counts(interface, verbose):
    """Show dhcp6relay message counts"""

    counter = DHCPv6_Counter()
    counter_intf = counter.get_interface()

    if interface:
        print_count(counter, interface)
    else:
        for intf in counter_intf:
            print_count(counter, intf)


# 'clear' subcommand ("clear dhcp6relay_counters counts")
@dhcp6relay_counters.command('clear')
@click.option('-i', '--interface', required=False)
@click.option('--verbose', is_flag=True, help="Enable verbose output")
def clear(interface, verbose):
    """Clear dhcp6relay message counts"""
    
    counter = DHCPv6_Counter()
    counter_intf = counter.get_interface()

    if interface:
        counter.clear_table(interface)
        print("Cleared DHCPv6 Relay Counter " + interface)
    else:
        for intf in counter_intf:
            counter.clear_table(intf)
        print("Cleared DHCPv6 Relay Counters")

