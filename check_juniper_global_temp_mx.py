#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#   Autors: David Hannequin <david.hannequin@fullsave.com>,
#   Date: 2015-03-31
#   URL: http://www.fullsave.com
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
	parser.add_argument('-H', '--hostname', default='')
    	parser.add_argument('-U', '--username', default='nagios')
    	parser.add_argument('-K', '--key', default='~/.ssh/id_dsa')
	parser.add_argument('-w', '--warning', default='80', type=int)
	parser.add_argument('-c', '--critical', default='90', type=int)
    	args = parser.parse_args()
	
	hostname = args.hostname
	username = args.username
	key = args.key
	critical = args.critical
	warning = args.warning

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname, username=username, key_filename=key)

	stdin, stdout, stderr = ssh.exec_command('show chassis routing-engine')

	data = stdout.readlines()
	
	ssh.close()		

	temp = data[4]

	temp = re.search("(\d+)",temp)

	temp = int(temp.group(0))

	if temp >= critical:
		print ('CRITICAL - Temperature : %s degrees C  |temp=%s' % (temp, temp))
		raise SystemExit(2)
	elif temp >= warning:
		print ('WARNING - Temperature : %s degrees C |temp=%s' % (temp, temp))
		raise SystemExit(1)
	else:
		print ('OK - Temperature : %s degrees C |temp=%s' % (temp, temp))
		raise SystemExit(0)

if __name__ == "__main__":
    main()
