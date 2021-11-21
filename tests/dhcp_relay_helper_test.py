import sys
import os

import show.main as show
from click.testing import CliRunner

expected_table = """\
--------  ------------
Vlan1000  fc02:2000::1
          fc02:2000::2
--------  ------------

"""

class TestDhcpRelayHelper(object):

    def test_show_dhcpv6_helper(self):
        runner = CliRunner()
        result = runner.invoke(show.cli.commands["dhcprelay_helper"].commands["ipv6"])
        print(result.output)
        assert result.output == expected_table

