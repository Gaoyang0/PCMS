# -*- coding:utf-8 -*-
# Author:DaoYang


import json
import time

from .game_map import GameMap
from .user import User
from .position import Position

from .constants import GAME_WIDTH, GAME_HEIGHT, GAME_TIME, START_DELAY_TIME, BUILD_BASE_TIME, BUILD_BASE_COST
import random


class ColorFight:
    def __init__(self):
        self.game_state = 'alive'
        self.width = GAME_WIDTH
        self.height = GAME_HEIGHT
        self.game_map = GameMap(self.width, self.height)
        self.game_id = str(random.randint(10000, 99999))

        self.game_time = GAME_TIME
        self.create_time = int(round(time.time() * 1000))
        self.plan_start_time = START_DELAY_TIME * 1000 + self.create_time
        self.finish_time = self.game_time * 1000 + self.plan_start_time
        self.last_update_time = self.plan_start_time

        self.users = {}
        self.errors = {}

    def config(self, game_time, start_delay_time):
        if 50 <= game_time <= 2000 and 0 <= start_delay_time <= 50:
            self.game_time = game_time
            self.create_time = int(round(time.time() * 1000))
            self.plan_start_time = start_delay_time * 1000 + int(round(time.time() * 1000))
            self.finish_time = self.game_time * 1000 + self.plan_start_time
            return True
        else:
            return False

    def update(self, current_time):
        for cell in self.game_map.get_cells():
            attacker = cell.attacker
            success, flag = cell.refresh_attack(current_time)
            if success:
                self.users[attacker].state = 'free'
                self.users[attacker].get_cell(cell)
                if cell.cell_type == 'land':
                    self.users[attacker].score += 1
                elif cell.cell_type == 'gold':
                    self.users[attacker].gold_source += 1
                    self.users[attacker].score += 10
                elif cell.cell_type == 'base':
                    cell.cell_type == 'land'
                    self.users[attacker].score += 20
                else:
                    pass
                # 占领的不是空地
                if flag['s'] != 0 and flag['a'] != flag['s']:
                    self.users[flag['s']].remove_cell(cell)
                    if cell.cell_type == 'gold':
                        self.users[flag['s']].gold_source -= 1
                    elif cell.cell_type == 'base':
                        cell.cell_type == 'land'
                        self.users[flag['s']].base_source -= 1

        for cell in self.game_map.get_cells():
            if cell.refresh_build(current_time):
                self.users[cell.owner].base_source += 1
                self.users[cell.owner].score += 15
        # 更新金币
        time_diff = (current_time - self.last_update_time)
        self.last_update_time = current_time
        for user in self.users.values():
            base_gold = time_diff*0.00025
            mine_gold = time_diff*0.0005
            user.gold += user.base_source*base_gold + user.gold_source*mine_gold

        # 更新AI死亡
        for user in self.users.values():
            if user.base_source <= 0:
                user.state = "dead"
                for cell in user.cells.values():
                    cell.clear_cell()
                    user.remove_cell(cell)

    def attack(self, uid, x, y, cost, current_time):
        # 判断合理?
        #     玩家是否具有攻击的CD
        #     判断是否相邻
        #     被攻击的领地是否能被攻击
        #
        # 判断是否是自己的领地?
        #     uid
        #
        # 获取攻击时间
        # 修改game_map的cell的状态
        # 把cell添加到user
        # 修改玩家状态
        if self.users[uid].state == 'free' and self.game_map.attack_valid(uid, x, y):
            attack_time = self.game_map.get_attack_time(uid, x, y, cost, current_time)
            cell = self.game_map.__getitem__(Position(x, y))
            attack_type = "attack"
            if cell.owner == uid:
                attack_type = 'shield'
            msg = {
                'build_state': "fighting",
                'is_taking': False,
                'finish_time': current_time + attack_time * 1000,
                'attacker': int(uid),
                'attack_time': current_time,
                'attack_type': attack_type,
            }
            cell.loads(**msg)
            self.users[uid].state = 'CD'
            self.users[uid].gold -= cost
            return True

    def build(self, uid, x, y, current_time):
        if self.game_map.build_valid(uid, x, y):
            if self.users[uid].gold>BUILD_BASE_COST:
                cell = self.game_map.__getitem__(Position(x, y))
                msg = {
                    "cell_type": "base",
                    "build_state": "building",
                    "build_finish": False,
                    "build_time": current_time,
                }
                cell.loads(**msg)
                self.users[uid].gold -= BUILD_BASE_COST
                return True

    def register(self, user_name):
        # Check whether user exists first
        for user in self.users.values():
            if user.username == user_name:
                return True, user.uid
        uid = len(self.users) + 1

        user = User(uid, user_name)
        # 加入user
        if self.game_map.born(user):
            user.state = 'free'
            user.base_source = 1
            self.users[uid] = user
            return True, uid
        else:
            return False, "-1"

    def info(self):
        return {
            "game_state": self.game_state,
            "game_time": self.game_time,
            "width": GAME_WIDTH,
            "height": GAME_HEIGHT,
            "game_id": self.game_id,
            "create_time": self.create_time,
            "plan_start_time": self.plan_start_time,
            "finish_time": self.finish_time,
            "last_update_time": self.last_update_time,
            "time": int(round(time.time() * 1000)),
        }

    def get_game_info(self):
        return {
            "info": self.info(),
            "error": self.errors,
            "game_map": self.game_map.info(),
            "users": {user.uid: user.info() for user in self.users.values()},
        }
