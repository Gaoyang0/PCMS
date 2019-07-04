# -*- coding:utf-8 -*-
# Author:DaoYang

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json, time, requests


class SnakeConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'channels_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        if message_type == 'map_data':
            body = text_data_json['message']['body']
            food = text_data_json['message']['food']
            direction = text_data_json['message']['direction']
            target_address = text_data_json['message']['target_address']
            map_size = text_data_json['message']['map_size']

            message = {
                'type': 'request_res',
                'message': {
                    'body': body,
                    'food': food,
                    'direction': direction,
                    'map_size': map_size,
                },
            }

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'request_res',
                    'message': {
                        'type': 'request_res',
                        'message': {
                            'body': body,
                            'food': food,
                            'direction': direction,
                            'map_size': map_size,
                        },
                    }
                }
            )
        elif message_type == 'res':
            direction = text_data_json["message"]["direction"]
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'send_res',
                    'message': {
                        'type': 'control',
                        'message': {
                            'direction': direction
                        },
                    }
                }
            )


    def send_res(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))


    def request_res(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))



