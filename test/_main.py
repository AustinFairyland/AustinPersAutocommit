# coding: utf8
""" 
@File: _main.py
@Editor: PyCharm
@Author: Austin (From Chengdu.China) https://fairy.host
@HomePage: https://github.com/AustinFairyland
@OperatingSystem: Windows 11 Professional Workstation 23H2 Canary Channel
@CreatedTime: 2024-01-28
"""
from __future__ import annotations

import os
import sys
import warnings
import platform
import asyncio

sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import typing
import types

from fairyland.framework.utils.datetimes import DateTimeUtils


class Test:

    def __init__(self):
        pass

    @staticmethod
    def test():
        day_second = 60 * 60 * 24
        print(day_second / 200)
        print(DateTimeUtils.normdatetime())


if __name__ == "__main__":
    __main = Test()
    __main.test()
