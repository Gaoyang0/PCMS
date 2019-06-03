# -*- coding:utf-8 -*-
# Author:DaoYang

from colorfight.core.position import Position
from colorfight.core.game_map import GameMap, MapCell
from colorfight.core.colorfight import ColorFight
from colorfight.core.constants import GAME_HEIGHT, GAME_WIDTH
from colorfight.core.position import Position
import json, redis, time

def test_create_instance():
    try:
        game = ColorFight()
    except Exception as e:
        print(e)
        assert(False)

def test_get_game_info():
    try:
        game = ColorFight()
        info = game.get_game_info()
        # print(info)
        assert(isinstance(info, dict))
        # Turn
        assert("turn" in info)
        assert(info["turn"] >= 0)
        # Game Map
        assert("game_map" in info)
        game_map = info["game_map"]
        assert(len(game_map) == GAME_HEIGHT)
        assert(len(game_map[0]) == GAME_WIDTH)
        # User
        assert("users" in info)
    except Exception as e:
        print(e)
        assert(False)

def d(key, conn):
    conn.delete(key)

from colorfight.core.constants import game_list
import os
if __name__ == '__main__':
    a = os.path.abspath('')
    print(a+'\\download\\111.png')
    # color = "#fff"
    # style = "style='background-color: " +color+";'"
    # strHTML = "<p " + style + ">" +"ads" + "</p>"
    # print(strHTML)
    # def take_key(dict):
    #     return dict["score"]
    # dict = {
    #     2: {"score": 20},
    #     1: {"score": 25},
    #     3: {"score": 15},
    #     4: {"score": 60},
    # }
    # user_list = []
    # for item in dict.values():
    #     user_list.append(item)
    # print(user_list)
    # user_list.sort(key=take_key)
    # print(user_list)
    # dirtyUserIds = {}
    # dirtyUserIds[5] = set()
    # dirtyUserIds[6] = set()
    # dirtyUserIds[5].add('base')
    # dirtyUserIds[5].add('energy')
    # print(dirtyUserIds)
    # import math
    #
    # print(3 + 30 * math.pow(2, -1))
    # game = ColorFight()
    # game.config(500, 20)
    # game.register('gao')
    # time.sleep(10)
    # for c in game.users['1'].cells.values():
    #     print(game.game_map.get_attack_time('1', c.position.x, c.position.y, 4, int(round(time.time() * 1000))))
    # uid = '0'
    # print(game.users[uid].info())
    # print(len({'s': 's'}))
    # p1 = Position(0, 0)
    # print(p1.get_surrounding_cardinals())
    # cells = [[None for _ in range(5)] for _ in range(5)]
    # print(cells)
    # print([cells[y][x] for y in range(5) for x in range(5)])

    # cells = GameMap(25, 25)
    # print(cells)


    # test_create_instance()

    # test_get_game_info()

    # game = Colorfight()
    # dict1 = Colorfight2dict(game)
    #
    # r = redis.Redis(host='127.0.0.1', port=6379)
    # r.set('dict', json.dumps(dict1))
    # s = json.loads(str(r.get('dict'), encoding="utf8"))
    #
    # g = dict2Colorfight(s)
    #
    # dict2 = Colorfight2dict(g)
    # print(dict1.__eq__(dict2))
    # # print()
    # game = Colorfight()
    # dict = Colorfight2dict(game)
    #
    # conn = redis.Redis(host='127.0.0.1', port=6379)
    # pipe = conn.pipeline()
    #
    # pipe.set('game_info', json.dumps(dict))
    # pipe.execute()
    # # pipe.delete('game_info')
    # # pipe.execute()
    #
    # res = conn.get('game_info')
    # print(res)
    # # pipe.get('game_info')
    # # res = pipe.execute()
    # # print(res[0])

    # conn = redis.Redis(host='127.0.0.1', port=6379)
    # # pipe = conn.pipeline()
    # # pipe.delete('game_dict')
    # # pipe.execute
    # conn.set('s', 1156)
    # conn.expire('s', 10)
    # conn.set('s', 5648)
    import random
    # print()
    # dict = {
    #     's': 45,
    #     'a': 'ass'
    # }
    # print('s' in dict)








    # temp = cells_info[0][0]
    # print(cells_info[0][0])
    # p = Position(cells_info[0][0]['position'][0], cells_info[0][0]['position'][1])
    # del cells_info[0][0]['position']
    # print(cells_info[0][0])
    # map_cell = MapCell(p, **cells_info[0][0])
    # print(map_cell.info())
    # gm = GameMap(25, 25)

    # for cell_row in cells_info:
    #     for map_cell in cell_row:
    #         p = Position(map_cell['position'][0], map_cell[0][0]['position'][1])
    #         del cells_info[0][0]['position']
    #         map_cell = MapCell(p, **cells_info[0][0])





    #
    # r = redis.Redis(host='127.0.0.1', port=6379)
    #
    # print(json.dumps(dict))
    # r.set('dict', '')
    # print(r.get('dict'))
    # g = dict2Colorfight(dict)
    # print(g)

    # game = Colorfight()
    # cells_info = game.game_map.info()
    # print(cells_info)
    # for x in cells_info:
    #     for y in x:


