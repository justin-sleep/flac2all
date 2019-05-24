#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4 ai
#
# File Created: Fri 12 Apr 17:15:29 BST 2019
# Copyright 2019
#
# All rights reserved
#
# ============================================================|

__VERSION__ = (0, 0, 1)

import multiprocessing as mp
import core
import sys

import signal


def worker_process(target_host):
	print("Spawned worker process")
	eworker = core.encode_worker()
	# because we are a process, we just exit at the end
	sys.exit(eworker.run(target_host))


try:
	hostname = sys.argv[1]
except IndexError:
	print("Usage: %s $master_hostname" % sys.argv[0])
	sys.exit(1)

procs = []
while len(procs) != mp.cpu_count():
	procs.append(mp.Process(target=worker_process, args=(hostname,)))

[x.start() for x in procs]
# And now wait

# We instruct the parent to ignore SIGINT now, otherwise it
# gets terminated before the children, preventing the children
# from exiting cleanly
signal.signal(signal.SIGINT, signal.SIG_IGN)

while True:
	[x.join(timeout=1) for x in procs]
	if len([x for x in procs if x.is_alive() is True]) == 0:
		# All worker processes are done, exit
		sys.exit(0)
