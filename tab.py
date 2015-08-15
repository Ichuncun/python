#/usr/bin/env python
import sys
import readline
import rlcompleter
import atexit
import os
# tab completion
readline.parse_and_bind('tab: complete')
# history file
histfile = os.path.join(os.environ['HOME'], '.python_history')
try:
	readline.read_history_file(histfile)
except IOError:
	pass
atexit.register(readline.write_history_file, histfile)
