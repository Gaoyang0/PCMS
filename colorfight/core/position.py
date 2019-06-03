# -*- coding:utf-8 -*-
# Author:DaoYang

from .constants import GAME_WIDTH, GAME_HEIGHT


# 计算周围Position的辅助类
class Direction:
    North = (0, -1)
    South = (0, 1)
    West = (-1, 0)
    East = (1, 0)

    @staticmethod
    def get_all_cardinals():
        return [Direction.North, Direction.South, Direction.West, Direction.East]


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 判断两个Position类对应的坐标是否相等
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # 判断两个Position类对应的坐标是否不相等
    def __ne__(self, other):
        return not self.__eq__(other)

    # 计算hash
    def __hash__(self):
        return hash((self.x, self.y))

    # 相加返回新Position类
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    # 相减返回新Position类
    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    # 相加返回相加后自身Position类
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    # 相减返回相减后自身Position类
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __str__(self, ):
        return "("+str(self.x)+","+str(self.y)+")"

    # 判断Position是否合法
    def is_valid(self):
        return 0 <= self.x < GAME_WIDTH and 0 <= self.y < GAME_HEIGHT

    # 打印
    def __repr__(self):
        return "Position({}, {})".format(self.x, self.y)

    # 用于计算周围的Position
    def directional_offset(self, direction):
        return self + Position(*direction)

    # 以列表的形式返回上下左右的四个Position类
    def _get_all_surrounding_cardinals_4(self):
        return [self.directional_offset(d) for d in Direction.get_all_cardinals()]

    # 以列表的形式返回上下左右的合法的几个Position类
    def get_surrounding_cardinals_4(self):
        return [position for position in self._get_all_surrounding_cardinals_4() if position.is_valid()]

    def get_surrounding_cardinals_8(self):
        return [position for position in [self + Position(1, 1), self + Position(1, -1),
                                          self + Position(-1, 1), self + Position(-1, -1),
                                          self + Position(0, 1), self + Position(0, -1),
                                          self + Position(1, 0), self + Position(-1, 0), ] if position.is_valid()]

    def info(self):
        return {
            'x': self.x,
            'y': self.y
        }

