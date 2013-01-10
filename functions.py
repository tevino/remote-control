# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, call
from players import Mplayer, Pianobar

_current_player = None


def reboot():
    'R2C2'
    call(['sudo', '/sbin/reboot'])


def shutdown():
    'POWER'
    call(['sudo', '/sbin/shutdown', '-h', 'now'])


def turn_volume():
    'VOLUME+'
    _turn_volume('+')


def turn_volume_down():
    'VOLUME-'
    _turn_volume('-')


def stop_mplayer():
    'STOP'
    _current_player.stop()


def resume_mplayer():
    'PLAY'
    _current_player.pause()

### Colored button ###


def funkyhouse():
    'RED'
    _play_fm('funkyhouse')


def smoothjazz():
    'YELLOW'
    _play_fm('smoothjazz')


def hit90s():
    'GREEN'
    _play_fm('hit90s')


def pandora():
    'BLUE'
    pianobar = Pianobar()
    pianobar.play()
    switch_current_player(pianobar)


def love():
    'FAVS'
    try:
        _current_player.love()
    except AttributeError:
        print 'unsupported operate'


def next():
    'NEXT'
    try:
        _current_player.next()
    except AttributeError:
        print 'unsupported operate'

#### util functions ####


def switch_current_player(new_player):
    global _current_player
    if _current_player is not None:
        _current_player.stop()
    _current_player = new_player


def _play_fm(channel):
    mplayer = Mplayer('-playlist')
    mplayer.load(_get_pls(channel))
    mplayer.play()
    switch_current_player(mplayer)


def _get_pls(channel):
    p = Popen(['/usr/bin/difmplay', '-p', 'echo -n', channel], stdout=PIPE)
    url = p.stdout.readline()
    p.terminate()
    return url


def _turn_volume(direction):
    assert direction in ('+', '-')
    call(['/usr/bin/amixer', '-q', 'sset', 'Master', '5%' + direction], stdout=PIPE, stderr=PIPE)
