# coding: utf8
""" 
@File: main.py
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

import time
import random
from datetime import datetime

from core.Autocommit import GitAutomator
from fairyland.framework.modules.journal import Journal
from fairyland.framework.utils.datetimes import DateTimeUtils


class Main:

    @staticmethod
    def run():
        Journal.info("开始执行")
        git_automator = GitAutomator(
            repo_path="data/repository/AustinPractice",
            remote_url="git@github.com:AustinFairyland/AustinPractice.git",
        )

        git_automator.checkout_branch()
        git_automator.modify_and_commit(
            file_path="_main.py",
            content=f"print('{time.time()}')",
            commit_message="Modify file and commit",
        )
        git_automator.push_changes()
        Journal.info("执行结束")

    @staticmethod
    def keep_run():
        while True:
            Journal.info("开始执行")
            git_automator = GitAutomator(
                repo_path="data/repository/AustinPractice",
                remote_url="git@github.com:AustinFairyland/AustinPractice.git",
            )

            git_automator.checkout_branch()
            git_automator.modify_and_commit(
                file_path="_main.py",
                content=f"print('{DateTimeUtils.normdatetime()}')",
                commit_message="Modify file and commit",
            )
            git_automator.push_changes()
            Journal.info("执行结束")
            sleep_time = random.randint(100, 500)
            Journal.warning(f"{sleep_time}秒后继续执行...")
            time.sleep(sleep_time)


if __name__ == "__main__":
    # Main.run()
    Main.keep_run()
