#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import pylirc
import select
import functions
from threading import Thread

pygame.mixer.init()
beep = pygame.mixer.Sound('pa.wav')


def deal_code(code):
    if not code:
        return
    beep.play()
    btn = code['config']
    print btn
    for func in functions.__dict__.values():
        if callable(func) and btn == getattr(func, 'func_doc', None):
            task = Thread(target=func)
            task.daemon = True
            task.start()
            break


if __name__ == '__main__':
    fileno = pylirc.init('remote', 'ir.conf', False)
    if not fileno:
        print 'failed to initialize lirc'
        pylirc.exit()
        exit(1)

    epoll = select.epoll()
    epoll.register(fileno, select.EPOLLIN)
    print 'Start waiting for signals'
    while True:
        for e_fileno, event in epoll.poll(0.4):
            if e_fileno == fileno and event & select.EPOLLIN:
                for code in pylirc.nextcode(1) or []:
                    deal_code(code)
