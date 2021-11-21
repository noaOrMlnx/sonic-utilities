import click
from tabulate import tabulate
from swsscommon.swsscommon import ConfigDBConnector

import utilities_common.cli as clicommon

DHCP_RELAY = 'DHCP_RELAY'
config_db = ConfigDBConnector()

@click.group(cls=clicommon.AliasedGroup, name="dhcprelay_helper")
def dhcp_relay_helper():
    """Show DHCP_Relay helper information"""
    pass

@dhcp_relay_helper.command('ipv6')
def get_dhcpv6_helper_address():
    """Parse through DHCP_RELAY table for each interface in config_db.json and print dhcpv6 helpers in table format"""
    if config_db is not None:
        config_db.connect()
        table_data = config_db.get_table(DHCP_RELAY)
        if table_data is not None:
            vlans = config_db.get_keys(DHCP_RELAY)
            for vlan in vlans: 
                output = get_data(table_data, vlan)
                print(output)
            

def get_data(table_data, vlan):
    vlan_data = table_data.get(vlan)
    helpers_data = vlan_data.get('dhcpv6_servers')
    if helpers_data is not None:
        addr = {vlan:[]}
        for ip in helpers_data:
            addr[vlan].append(ip)
    output = tabulate({'Interface':[vlan], vlan:addr.get(vlan)}, tablefmt='simple', stralign='right') + '\n'
    return output

