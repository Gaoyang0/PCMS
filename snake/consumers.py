# -*- coding:utf-8 -*-
# Author:DaoYang

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json, time, requests


class SnakeConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
        if message_type == 'delayed_test':
            target_address = text_data_json['message']['target_address']
            time_start = time.time()
            r = requests.post(target_address)
            time_end = time.time()
            print('延时检测: ', time_end - time_start)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'send_message',
                    'message': {
                        'type': 'delayed_test_result',
                        'message': {
                            'delayed': time_end - time_start
                        },
                    }
                }
            )


        elif message_type == 'map_data':
            body = text_data_json['message']['body']
            food = text_data_json['message']['food']
            direction = text_data_json['message']['direction']
            target_address = text_data_json['message']['target_address']
            map_size = text_data_json['message']['map_size']

            headers = {'content-type': 'application/json'}
            message = {
                'type': 'ai_decision',
                'message': {
                    'body': body,
                    'food': food,
                    'direction': direction,
                    'map_size': map_size,
                },
            }

            time_start = time.time()
            r = requests.post(target_address, data=json.dumps(message), headers=headers)
            time_end = time.time()
            # print('决策: ', time_end - time_start)
            res = r.json()
            if res['type'] == 'ai_control':
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'send_message',
                        'message': {
                            'type': 'control',
                            'message': {
                                'direction': res['message']['direction']
                            },
                        }
                    }
                )

    # Receive message from room group
    def send_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))



