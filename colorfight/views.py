# -*- coding:utf-8 -*-
# Author:DaoYang

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.utils.safestring import mark_safe
import json, time
from colorfight.core.colorfight import ColorFight
import redis
from colorfight.core.constants import DELETE_DELAY_TIME, game_list

# conn = redis.Redis(host='127.0.0.1', port=6379)
# pipe = conn.pipeline()


def colorfight_test(request, game_id):
    return render(request, 'color_fight/colorfight.html', {'game_id': game_id})


def index(request):
    return render(request, 'color_fight/colorfight_index.html', {})


def instructions(request):
    return render(request, 'color_fight/instructions.html', {})


def createtest(request):
    if request.method == 'GET':
        return render(request, 'color_fight/createtest.html', {})
    elif request.method == 'POST':
        if request.is_ajax():
            data = json.loads(request.body.decode("utf8"))
            game_time = int(data['game_time'])
            start_delay_time = int(data['start_delay_time'])
            try:
                game = ColorFight()
                game.config(game_time, start_delay_time)
                game_list[str(game.game_id)] = game


                # game.config(game_time, start_delay_time)
                # # 存入redis
                # game_dict = Colorfight2dict(game)
                # pipe.set('game_dict'+str(game.game_id), json.dumps(game_dict))
                # pipe.execute()

                res = {
                    'game_id': game.game_id,
                    'state': 'success',
                    'game_room_url': 'http://127.0.0.1:8000/colorfight/AI_test/' + str(game.game_id) + '/'
                }
            except:
                res = {
                    'game_id': 0,
                    'state': 'failed',
                    'game_room_url': ''
                }
            return HttpResponse(json.dumps(res), content_type='application/json')


def test(request, game_id):
    print(request.get_host(), request.get_full_path_info())
    return HttpResponse(json.dumps({}), content_type='application/json')


def download(request, ):
    if request.method == 'GET':
        return render(request, 'color_fight/download.html', {})
    elif request.method == "POST":
        from django.http import FileResponse
        import os
        file_path = os.path.abspath('') + '\\download\\ColorFightExampleAI.rar'
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="ColorFightExampleAI.rar"'
        return response


def contactme(request, ):
    return render(request, 'color_fight/contactme.html', {})


def matchmsg(request, ):
    return render(request, 'color_fight/matchmsg.html', {})


def document(request, ):
    return render(request, 'color_fight/document.html', {})


# ajax
def getgameinfo(request):
    if request.is_ajax():
        data = json.loads(request.body.decode("utf8"))
        game_id = str(data['game_id'])

        if game_id in game_list:
            game = game_list[game_id]
            if game.finish_time > int(round(time.time() * 1000)):
                game.update(int(round(time.time() * 1000)))
                game_info = game.get_game_info()
                return HttpResponse(json.dumps(game_info), content_type='application/json')
            else:
                game_info = {
                    'info': {
                        'game_state': 'dead'
                    }
                }
                return HttpResponse(json.dumps(game_info), content_type='application/json')
        else:
            game_info = {
                'info': {
                    'game_state': 'none'
                }
            }
            return HttpResponse(json.dumps(game_info), content_type='application/json')
        # key = 'game_dict' + str(data['game_id'])
        # if conn.get(key):
        #     pipe.get(key)
        #     res = pipe.execute()
        #     game_dict = json.loads(str(res[0], encoding="utf8"))
        #     if game_dict['finish_time'] > int(round(time.time() * 1000)):
        #         pipe.get(key)
        #         res = pipe.execute()
        #         game_dict = json.loads(str(res[0], encoding="utf8"))
        #
        #         game = dict2Colorfight(game_dict)
        #         game_info = game.get_game_info()
        #         return HttpResponse(json.dumps(game_info), content_type='application/json')
        #     else:
        #         game_info = {
        #             'info': {
        #                 'game_state': 'dead'
        #             }
        #         }
        #         # 延时删除
        #         conn.expire(key, DELETE_DELAY_TIME)
        #         return HttpResponse(json.dumps(game_info), content_type='application/json')
        #
        # else:
        #     return HttpResponse(json.dumps({}), content_type='application/json')


