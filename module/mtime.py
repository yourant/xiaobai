#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from datetime import datetime
from module.colors import color


class Timed:
    @staticmethod
    def timed(de=0):
        get_time = datetime.now()
        time.sleep(de)
        timed = color.cyan("["+str(get_time)[11:19]+"] ")
        return timed
    @staticmethod
    def dated(de=0):
        get_time=datetime.now()
        time.sleep(de)
        date=color.cyan("["+str(get_time)[0:10]+"] ")
        return date
    @staticmethod
    def no_style_dated(de=0):
        get_time=datetime.now()
        time.sleep(de)
        date=str(get_time)[0:10]
        return date
    @staticmethod
    def no_style_timed(de=0):
        get_time = datetime.now()
        time.sleep(de)
        no_color_timed = str(get_time)[11:19]
        return no_color_timed


now = Timed()


if __name__ == '__main__':
    print(datetime.now())
    print(now.dated())
    print(now.timed())
    print(now.no_style_timed())
    print(now.no_style_dated())