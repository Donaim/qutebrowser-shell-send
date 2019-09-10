
from qutebrowser.commands import userscripts, runners
from qutebrowser.api import cmdutils
from qutebrowser.utils import (message, usertypes, log, qtutils, urlutils,
                               objreg, utils, standarddir, debug)
from qutebrowser.misc import objects

from os import path
import tempfile
import subprocess
import threading
import json

@cmdutils.register(instance='command-dispatcher', scope='window', overwrite=True)
@cmdutils.argument('close', choices=['True', 'False'])
@cmdutils.argument('prefix')
def shell_send(self, close=False, prefix='', quiet=False):
	''' Executes program with current selection as stdin (may be none)'''
	maybeshell = '' if close else ' && $SHELL'

	def _question_callback(program):
		def _selection_callback(text):
			if not text and not quiet:
				message.info("Nothing selected")

			def inthread():
				with tempfile.NamedTemporaryFile(mode='wt', encoding='utf-8') as infile:
					infile.write(text)
					infile.flush()

					tempname = '"' + infile.name + '"'
					cmd = f"x-terminal-emulator-exe {prefix} 'cat {tempname} | {program} {maybeshell}'"
					p = subprocess.Popen(['sh', '-c', cmd])
					p.wait()

					if p.returncode != 0 and not quiet:
						message.error(f'shell-send process "{cmd}" failed with: {p.returncode}')

			threading.Thread(target=inthread).start()

		caret = self._current_widget().caret
		caret.selection(callback=_selection_callback)

	message.ask_async(
		"Shell send:",
		usertypes.PromptMode.text,
		_question_callback,
		text="program: ")
