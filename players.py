# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE


class CliPlayerMixin(object):
    _bin = ''
    _fixed_args = ()
    filename = ''
    append_newline = True

    def __init__(self, *options):
        self._player = None
        self.options = options

    def load(self, filename):
        self.filename = filename

    def play(self):
        self.stop()
        args = (self._bin, ) + self._fixed_args + self.options + (self.filename, )
        self._player = Popen(args, stdin=PIPE, stdout=PIPE)

    def send(self, cmd):
        if self._player:
            try:
                cmd = cmd + '\n' if self.append_newline else cmd
                self._player.stdin.write(cmd)
            except:
                pass


class Mplayer(CliPlayerMixin):
    _bin = '/usr/bin/mplayer'
    _fixed_args = ('-slave', )

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
