# -*- coding:utf-8 -*-
# Author:DaoYang

from channels.generic.websocket import AsyncWebsocketConsumer
from .core.constants import game_list
from .core.colorfight import ColorFight
import json, time


class ActionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.game_id = self.scope['url_route']['kwargs']['game_id']

        print(self.user_name, self.game_id)

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

        if message['action'] == 'register':
            content = message['content']
            game_id = content['game_id']
            user_name = content['user_name']

            game = game_list[game_id]

            success, uid = game.register(user_name)
            res = {
                'response_type': 'register',
                'content': {
                    'state': success,
                    'uid': uid,
                }
            }
            await self.send(
                text_data=json.dumps({
                    'message': res
                })
            )
        elif message['action'] == 'attack':
            content = message['content']
            uid = content['uid']
            game_id = content['game_id']
            x = content['x']
            y = content['y']
            cost = content['cost']

            if game_id in game_list:
                game = game_list[game_id]
                game.attack(uid, x, y, cost, int(round(time.time() * 1000)))

            print(content)
            await self.send(
                text_data=json.dumps({
                    'message': {
                        'response_type': 'attack',
                        'content': {
                            'state': 'success',
                        }
                    }
                })
            )
        elif message['action'] == 'build':
            content = message['content']
            uid = content['uid']
            game_id = content['game_id']
            x = content['x']
            y = content['y']

            if game_id in game_list:
                game = game_list[game_id]
                game.build(uid, x, y, int(round(time.time() * 1000)))
            print(content)
            await self.send(
                text_data=json.dumps({
                    'message': {
                        'response_type': 'build',
                        'content': {
                            'state': 'success',
                        }
                    }
                })
            )


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.game_id = self.scope['url_route']['kwargs']['game_id']

        print(self.user_name, self.game_id)

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        if message['action'] == 'get_info':
            content = message['content']
            game_id = content['game_id']
            uid = content['uid']

            if game_id in game_list:
                game = game_list[game_id]
                if uid in game.users:
                    res = {
                        'response_type': 'get_info',
                        'content': {
                            'state': 'success',
                            'game': game.info(),
                            'user': game.users[uid].info(),
                            'map': game.game_map.info(),
                        }
                    }
                    await self.send(
                        text_data=json.dumps({
                            'message': res
                        })
                    )
            else:
                res = {
                    'response_type': 'get_info',
                    'content': {
                        'state': 'failed',
                        'game': {},
                        'user': {},
                    }
                }
                await self.send(
                    text_data=json.dumps({
                        'message': res
                    })
                )
