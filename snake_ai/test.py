from snake_ai import snakeAI

s = snakeAI.snake_fun(5, 5)
snake = [0] * (5*5 + 1)

snake[0] = 2
snake[1] = 3
print(snake)
s.set_map(12, snake, 2, 5, 5)
re = s.get_one_step()
print(re)