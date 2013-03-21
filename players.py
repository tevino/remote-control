# -*- coding: utf-8 -*-
import os
from subprocess import Popen, PIPE


class CliPlayerMixin(object):
    _bin = ''
    _addtional_args = ()
    filename = ''
    append_newline = True

    def __init__(self, args=None):
        self._player = None
        self.args = args or ()

    def load(self, filename):
        self.filename = filename

    def play(self):
        self.stop()
        args = (self._bin, ) + self.args + self._addtional_args +\
            (self.filename, )
        self._player = Popen(
            args, stdin=PIPE, stdout=PIPE, preexec_fn=os.setpgrp)

    def send(self, cmd):
        if self._player:
            try:
                cmd = cmd + '\n' if self.append_newline else cmd
                self._player.stdin.write(cmd)
            except:
                pass


class Mplayer(CliPlayerMixin):
    _bin = '/usr/bin/mplayer'
    _addtional_args = ('-slave', '-really-quiet', '-noconsolecontrols')

    def pause(self):
        self.send('p')

    def stop(self):
        if self._player:
            self.send('q')
            self._player.terminate()

    def next(self):
        self.send('n')


class Pianobar(CliPlayerMixin):
    _bin = '/usr/bin/pianobar'

    def stop(self):
        if self._player:
            self.send('q')
            self._player.terminate()

    def pause(self):
        self.send('p')

    def next(self):
        self.send('n')

    def love(self):
        self.send('+')
