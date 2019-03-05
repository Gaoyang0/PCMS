# -*- coding:utf-8 -*-
# Author:DaoYang


from flask import Flask, request, Response
import json
from snake_ai import snakeAI

app = Flask(__name__)


# 转换
def change_coordinate(node, width):
    return node['top']*width+node['left']


@app.route('/')
def hello_world():
    return 'snake AI 已开启!'


# 延时检测
@app.route('/test_delayed/')
def test_delayed():
    return Response(json.dumps({'status': 'OK'}), mimetype='application/json')


@app.route('/snake-ai/', methods=['POST'])
def snake_ai():
    data = request.json
    if data['type'] == 'ai_decision':
        width = data['message']['map_size']['width']
        height = data['message']['map_size']['height']
        snake = [0] * (width*height + 1)
        food = change_coordinate(data['message']['food'], width)
        for i in range(len(data['message']['body'])):
            snake[i] = change_coordinate(data['message']['body'][i], width)

        snake_ai = snakeAI.snake_fun(width, height)
        snake_ai.set_map(food, snake, len(data['message']['body']))
        direction = snake_ai.get_one_step()

        rt = {
            'type': 'ai_control',
            'message': {
                'direction': direction,
            },
        }
        return Response(json.dumps(rt), mimetype='application/json')
    else:
        return Response(json.dumps({
            'type': 'ai_control',
            'message': {
                'direction': -1,
            },
        }), mimetype='application/json')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
