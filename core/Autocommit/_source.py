# coding: utf8
""" 
@File: _source.py
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

from git import Repo, GitCommandError
import time
from datetime import datetime
from fairyland.framework.modules.journal import Journal


class GitAutomator:
    def __init__(self, repo_path, remote_url, branch_name="AutoCommit"):
        self.repo_path = repo_path
        self.remote_url = remote_url
        self.branch_name = branch_name
        self.repo = self.initialize_repo()
        Journal.success("The remote repository was pulled successfully...")

    def initialize_repo(self):
        if not os.path.exists(self.repo_path):
            Journal.info(
                f"Start cloning the repository: {self.remote_url} to {self.repo_path} ..."
            )
            return Repo.clone_from(self.remote_url, self.repo_path)
        else:
            Journal.info(
                f"Local: {self.repo_path} Existing remote repository: {self.remote_url}"
            )
            return Repo(self.repo_path)

    def checkout_branch(self):
        try:
            self.repo.git.checkout(self.branch_name)
            Journal.success(f"Switch branch successfully {self.branch_name} ")
        except GitCommandError:
            master_branch = (
                "ReleaseMaster" if "ReleaseMaster" in self.repo.heads else "master"
            )
            self.repo.git.checkout(master_branch)
            Journal.success(
                f"Toggling the default branch is complete {master_branch} ..."
            )
            self.repo.git.checkout("-b", self.branch_name)
            Journal.success(f"Branch switch completed {self.branch_name} ...")

    def modify_and_commit(self, file_name, content, commit_message):
        Journal.info("Start modifying the file...")
        now_date = datetime.now().date()
        file_path = os.path.join(
            self.repo_path,
            f"{now_date.year}",
            f"{now_date.month:02d}",
        )
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        full_path = os.path.join(file_path, file_name)
        with open(full_path, "a") as file:
            file.write(content)
        Journal.success("The file is written...")
        self.repo.git.add(f"{now_date.year}/{now_date.month:02d}/{file_name}")
        Journal.success("File added...")
        self.repo.index.commit(commit_message)
        Journal.success("File submission to staging area completed...")

    def push_changes(self):
        origin = self.repo.remote(name="origin")
        origin.push(self.branch_name)
        Journal.success(f"File commit remote branch complete {self.branch_name} ...")
