#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#   Autors: David Hannequin <david.hannequin@fullsave.com>,
#   Date: 2015-03-31
#   URL: http://www.fullsave.com
#   
#   Plugins to check BGP IPv4 and IPv6 state.
#
# Shinken plugin is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shinken plugin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Shinken.  If not, see <http://www.gnu.org/licenses/>.
#
# Requires: Python >= 2.7 
# Requires: Python Paramiko

import os
import re
import argparse
import paramiko

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--hostname', default='', help='ip or hostname for BGP router')
    parser.add_argument('-U', '--username', default='nagios', help='ssh user for BGP router')
    parser.add_argument('-K', '--key', default='~/.ssh/id_dsa', help='ssh private key for BGP routeur')
    parser.add_argument('-P', '--peer', default='', help='bgp peer ipv4 or ipv6')
    args = parser.parse_args()
	
    hostname = args.hostname
    username = args.username
    key = args.key
    peer = args.peer
    
    cmd = 'show bgp neighbor ' + peer
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, key_filename=key)
    
    stdin, stdout, stderr = ssh.exec_command(cmd)

    data = stdout.readlines()

    if not data:
        print ('UNKNOWN - State is UNKNOWN')
        raise SystemExit(3)
    
    ssh.close()		

    as_juniper = data[1]
    
    as_number = as_juniper.split();
    
    as_number = str(as_number[1])
    
    as_jstate = data[2]
    
    as_jstate = as_jstate.split();
    
    as_jstate = str(as_jstate[3])

    if as_jstate in 'Established':
        print ('OK - %s state is %s' % (as_number, as_jstate.lower()))
        raise SystemExit(0)
    elif as_jstate in 'Connect' or as_jstate in 'Active' or as_jstate in 'OpenConfirm' or as_jstate in 'OpenSent':
        print ('WARNING - %s state is %s' % (as_number, as_jstate.lower()))
        raise SystemExit(1)
    else:
        print ('CRITICAL - %s state is %s' % (as_number, as_jstate.lower()))
        raise SystemExit(2)

if __name__ == "__main__":
    main()
