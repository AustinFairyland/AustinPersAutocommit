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
from fairyland.framework.modules.journal import Journal


class GitAutomator:
    def __init__(self, repo_path, remote_url, branch_name="AutoCommit"):
        self.repo_path = repo_path
        self.remote_url = remote_url
        self.branch_name = branch_name
        self.repo = self.initialize_repo()
        Journal.success("远程仓库拉取成功...")

    def initialize_repo(self):
        if not os.path.exists(self.repo_path):
            Journal.info(f"开始克隆仓库: {self.remote_url} 到 {self.repo_path} ...")
            return Repo.clone_from(self.remote_url, self.repo_path)
        else:
            Journal.info(f"本地: {self.repo_path} 已有远程仓库: {self.remote_url}")
            return Repo(self.repo_path)

    def checkout_branch(self):
        try:
            self.repo.git.checkout(self.branch_name)
            Journal.success(f"切换分支 {self.branch_name} 成功")
        except GitCommandError:
            master_branch = (
                "ReleaseMaster" if "ReleaseMaster" in self.repo.heads else "master"
            )
            self.repo.git.checkout(master_branch)
            Journal.success(f"切换默认分支 {master_branch} 成功")
            self.repo.git.checkout("-b", self.branch_name)
            Journal.success(f"切换分支 {self.branch_name} 成功")

    def modify_and_commit(self, file_path, content, commit_message):
        Journal.info("开始需改文件...")
        full_path = os.path.join(self.repo_path, file_path)
        with open(full_path, "a") as file:
            file.write(content)
        Journal.success("文件写入完成...")
        self.repo.git.add(file_path)
        Journal.success("文件添加完成...")
        self.repo.index.commit(commit_message)
        Journal.success("文件提交暂存区完成...")

    def push_changes(self):
        origin = self.repo.remote(name="origin")
        origin.push(self.branch_name)
        Journal.success(f"文件提交远程分支 {self.branch_name} 完成...")
