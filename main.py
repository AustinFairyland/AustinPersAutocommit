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
        Journal.info("Start execution...")
        git_automator = GitAutomator(
            repo_path="data/repository/AutocommitRepository",
            remote_url=os.environ.get("GIT_REMOTE_URL")
            if os.environ.get("GIT_REMOTE_URL")
            else "git@github.com:AustinFairyland/AutocommitRepository.git",
            branch_name=os.environ.get("GIT_REMOTE_BRANCH") if os.environ.get("GIT_REMOTE_BRANCH") else "ReleaseMaster",
        )
        git_automator.checkout_branch()
        git_automator.modify_and_commit(
            file_name=f"_main_{datetime.now().date()}.py",
            content=f"print('{DateTimeUtils.normdatetime()}')\n",
            commit_message=":art: Modify file and commit",
        )
        git_automator.push_changes()
        Journal.info("End of execution...")

    @classmethod
    def keep_run(cls):
        while True:
            cls.run()
            sleep_time = random.randint(5000, 10000)
            Journal.warning(f"Execution continues after {sleep_time} seconds")
            time.sleep(sleep_time)


if __name__ == "__main__":
    print(end="")
    git_remote_url = os.environ.get("GIT_REMOTE_URL")
    git_remote_branch = os.environ.get("GIT_REMOTE_BRANCH")
    Journal.info(f"Env Path: GIT_REMOTE_URL: {git_remote_branch}") if git_remote_url else Journal.info("Not Found Env Path: GIT_REMOTE_URL")
    Journal.info(f"Env Path: GIT_REMOTE_BRANCH: {git_remote_branch}") if git_remote_branch else Journal.info("Not Found Env Path: GIT_REMOTE_BRANCH")
    Main.keep_run()
