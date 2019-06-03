# -*- coding:utf-8 -*-
# Author:DaoYang

from .constants import INITIAL_GOLD


class User:
    def __init__(self, uid, username):
        self.uid = uid
        self.username = username

        self.gold = INITIAL_GOLD
        self.gold_source = 0
        self.base_source = 0
        # dead free fighting
        self.state = "dead"
        self.cells = {}
        self.score = 0

    # 添加一个cell
    def get_cell(self, cell):
        self.cells[cell.position.__str__()] = cell

    # 删除一个cell
    def remove_cell(self, cell):
        if cell.position.__str__() in self.cells:
            del self.cells[cell.position.__str__()]

    def info(self):
        return {
            "uid": self.uid,
            "username": self.username,
            "gold": self.gold,
            "state": self.state,
            "gold_source": self.gold_source,
            "cells": {cell.position.__str__(): cell.info() for cell in self.cells.values()},
            "score": self.score,
            "base_source": self.base_source,
        }
