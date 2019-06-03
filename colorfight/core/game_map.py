# -*- coding:utf-8 -*-
# Author:DaoYang

from .position import Position
from .constants import GOLD_MINE_RATE, ATTACK_EMPTY_TIME, MAX_COST, BUILD_BASE_TIME
import random
import time
import math


class MapCell:
    def __init__(self, position):
        self.position = position

        #  0: 无人占 其他: 为用户id
        self.owner = 0
        self.occupy_time = 0
        self.is_taking = False
        self.attacker = 0
        # 进攻的时间
        self.attack_time = 0
        self.attack_type = ""
        # 进攻结束时间
        self.finish_time = 0
        self.last_update_time = 0
        # land gold base
        self.cell_type = "land"
        # empty occupied fighting building
        self.build_state = "empty"
        # build base 是否结束
        self.build_finish = True
        # 建筑base开始时间
        self.build_time = 0

    def loads(self, **kwargs):
        for kw in kwargs:
            if hasattr(self, kw):
                setattr(self, kw, kwargs[kw])

    def clear_cell(self):
        msg = {
            "owner": 0,
            "occupy_time": 0,
            "is_taking": False,
            "attacker": 0,
            "attack_time": 0,
            "attack_type": '',
            'finish_time': 0,
            'last_update_time': 0,
            "cell_type": self.cell_type,
            "build_state": 'empty',
            'build_finish': True,
            'build_time': 0,
        }
        self.loads(**msg)

    def refresh_attack(self, current_time):
        # 有cell攻击结束
        if self.build_state == 'fighting' and self.finish_time < current_time:
            flag = {'a': self.attacker, 's': self.owner}
            msg = {
                "owner": self.attacker,
                "occupy_time": current_time,
                "is_taking": True,
                "attacker": 0,
                "attack_time": 0,
                "attack_type": "",
                'finish_time': 0,
                'last_update_time': current_time,
                "build_state": 'occupied',
                'build_finish': True,
                'build_time': 0,
            }
            self.loads(**msg)
            return True, flag
        return False, {}

    def refresh_build(self, current_time):
        # base建成
        if self.cell_type == "base" and self.build_finish == False and self.build_time + BUILD_BASE_TIME*1000 <= current_time:
            self.build_finish = True
            self.build_state = "occupied",
            return True
        return False

    def info(self):
        return {
            "position": self.position.info(),
            "owner": self.owner,
            "occupy_time": self.occupy_time,
            "is_taking": self.is_taking,
            "attacker": self.attacker,
            "attack_time": self.attack_time,
            "attack_type": self.attack_type,
            'finish_time': self.finish_time,
            'last_update_time': self.last_update_time,
            "cell_type": self.cell_type,
            "build_state": self.build_state,
            'build_finish': self.build_finish,
            'build_time': self.build_time,
        }


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = self.generate_cells(width, height)

    # isinstance(object, classinfo)
    # 判断实例是否是这个类或者object是变量
    # 接受Position
    def __getitem__(self, location):
        if isinstance(location, Position):
            return self.cells[location.y][location.x]
        elif isinstance(location, tuple):
            return self.cells[location[1]][location[0]]

    # 判断合法
    def __contains__(self, item):
        if isinstance(item, Position):
            return 0 <= item.x < self.width and 0 <= item.y < self.height
        elif isinstance(item, tuple):
            return 0 <= item[0] < self.width and 0 <= item[1] < self.height
        else:
            return False

    def get_cells(self):
        # 返回一维cells
        return [self.cells[y][x] for y in range(self.height) for x in range(self.width)]

    def get_cells_2d(self):
        # 返回二维cells
        return self.cells

    # 获取一个随机的空cell
    def get_random_empty_cell(self):
        empty_cells = [cell for cell in self.get_cells() if cell.owner == 0 and cell.cell_type == 'land']
        if not empty_cells:
            return None
        return random.choice(empty_cells)

    def info(self):
        info = [[None for _ in range(self.width)] for _ in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                info[y][x] = self.cells[y][x].info()
        return info

    def generate_cells(self, width, height):
        # 初始化二维cells
        cells = [[None for _ in range(width)] for _ in range(height)]
        for x in range(width):
            for y in range(height):
                cells[y][x] = MapCell(Position(x, y))
        # 随机金矿
        for i in range(int(width * height * GOLD_MINE_RATE)):
            cell_y = random.choice(cells)
            cell_choice = random.choice(cell_y)
            cell_choice.cell_type = 'gold'
        return cells

    def born(self, user):
        cell = self.get_random_empty_cell()
        if cell == None:
            return False
        msg = {
            'build_state': "occupied",
            'cell_type': 'base',
            'owner': user.uid,
            'occupy_time': int(round(time.time() * 1000)),
            'finish_time': int(round(time.time() * 1000)),
            'last_update_time': int(round(time.time() * 1000)),
        }
        cell.loads(**msg)

        user.get_cell(cell)
        return True

    def get_k1(self, pos, uid):
        count = 0
        for item in pos.get_surrounding_cardinals_8():
            if self.__getitem__(item).owner == uid:
                count = count + 1
        return count - 1

    def get_attack_time(self, uid, x, y, cost, current_time):
        cell = self.__getitem__(Position(x, y))
        if cell.is_taking and str(cell.owner) != str(uid):
            x = current_time - cell.occupy_time
            k1 = self.get_k1(cell.position, uid) / 8
            k2 = cost / 2 / MAX_COST
            print(x, k1, k2)
            return (3 + 30 * math.pow(2, -x / 1000 / 30)) * (1 - k1) * (1 - k2)
        else:
            return 2

    def attack_valid(self, uid, x, y):
        # 判断邻近, 是否可被攻击
        adjacent_flag = False
        for pos in Position(x, y).get_surrounding_cardinals_4():
            if self.__getitem__(pos).owner == uid:
                adjacent_flag = True
        if adjacent_flag and self.__getitem__(pos).build_state != 'fighting':
            return True
        else:
            return False

    def build_valid(self, uid, x, y):
        # 判断是否是自己的领地, 金币大于60
        if self.__getitem__(Position(x, y)).owner == uid:
            return True
        else:
            return False

