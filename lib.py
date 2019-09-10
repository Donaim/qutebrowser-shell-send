
from qutebrowser.commands import userscripts, runners
from qutebrowser.api import cmdutils
from qutebrowser.utils import (message, usertypes, log, qtutils, urlutils,
                               objreg, utils, standarddir, debug)
from qutebrowser.misc import objects

from os import path
import tempfile
import subprocess
import json

@cmdutils.register(instance='command-dispatcher', scope='window', overwrite=True)
@cmdutils.argument('close', choices=['True', 'False'])
@cmdutils.argument('prefix')
def shell_send(self, close, prefix='', quiet=False):
	''' Executes program with current selection as stdin (may be none)'''
	maybeshell = '' if close else ' && $SHELL'

	def _question_callback(program):
		def _selection_callback(text):
			if not text and not quiet:
				message.info("Nothing selected")

			tempname = None
			with tempfile.TemporaryFile(mode='wt', encoding='utf-8') as infile:
				infile.write(text)
				tempname = infile.name

			retcode = subprocess.call(f"x-terminal-emulator-exe {prefix} 'cat {tempname} | {program} {maybeshell}'")
			if retcode != 0:
				message.error(f'Shell subprocess failed with: {retcode}')

		caret = self._current_widget().caret
		caret.selection(callback=_selection_callback)

	message.ask_async(
		"Shell send:",
		usertypes.PromptMode.text,
		_question_callback,
		text="program: ")
