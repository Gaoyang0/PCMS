# -*- coding:utf-8 -*-
# Author:DaoYang



class snake_fun(object):
    def __init__(self, width, height):
        self.HEIGHT = height
        self.WIDTH = width
        self.FIELD_SIZE = self.HEIGHT * self.WIDTH

        self.HEAD = 0
        self.FOOD = 0
        self.UNDEFINED = (self.HEIGHT + 1) * (self.WIDTH + 1)
        self.SNAKE = 2 * self.UNDEFINED

        self.LEFT = -1
        self.RIGHT = 1
        self.UP = 0 - self.WIDTH
        self.DOWN = self.WIDTH
        self.ERR = -1111

        self.board = [0] * self.FIELD_SIZE
        self.snake = [0] * (self.FIELD_SIZE + 1)
        self.snake[self.HEAD] = 1 * self.WIDTH + 1
        self.snake_size = 1
        # 与上面变量对应的临时变量，蛇试探性地移动时使用
        self.tmpboard = [0] * self.FIELD_SIZE
        self.tmpsnake = [0] * (self.FIELD_SIZE + 1)
        self.tmpsnake[self.HEAD] = 1 * self.WIDTH + 1
        self.tmpsnake_size = 1

        self.food = 3 * self.WIDTH + 3
        self.best_move = self.ERR

        self.mov = [self.LEFT, self.RIGHT, self.UP, self.DOWN]

    # 检查一个cell有没有被蛇身覆盖，没有覆盖则为free，返回true
    def is_cell_free(self, idx, psize, psnake):
        return not (idx in psnake[:psize])

    # 检查某个位置idx是否可向move方向运动
    def is_move_possible(self, idx, move):
        flag = False
        if move == self.LEFT:
            flag = True if idx % self.WIDTH > 0 else False
        elif move == self.RIGHT:
            flag = True if idx % self.WIDTH < (self.WIDTH - 1) else False
        elif move == self.UP:
            flag = True if idx > (1 * self.WIDTH - 1) else False  # 即idx/WIDTH > 1
        elif move == self.DOWN:
            flag = True if idx < (self.FIELD_SIZE - 1 * self.WIDTH) else False  # 即idx/WIDTH < HEIGHT-2
        return flag

    # 重置board
    # board_refresh后，UNDEFINED值都变为了到达食物的路径长度
    # 如需要还原，则要重置它
    def board_reset(self, psnake, psize, pboard):
        for i in range(self.FIELD_SIZE):
            if i == self.food:
                pboard[i] = self.FOOD
            elif self.is_cell_free(i, psize, psnake):  # 该位置为空
                pboard[i] = self.UNDEFINED
            else:  # 该位置为蛇身
                pboard[i] = self.SNAKE

    # 广度优先搜索遍历整个board，
    # 计算出board中每个非SNAKE元素到达食物的路径长度
    def board_refresh(self, pfood, psnake, pboard):
        queue = []
        queue.append(pfood)
        inqueue = [0] * self.FIELD_SIZE
        found = False
        # while循环结束后，除了蛇的身体，
        # 其它每个方格中的数字代码从它到食物的路径长度
        while len(queue) != 0:
            idx = queue.pop(0)
            if inqueue[idx] == 1: continue
            inqueue[idx] = 1
            for i in range(4):
                if self.is_move_possible(idx, self.mov[i]):
                    if idx + self.mov[i] == psnake[self.HEAD]:
                        found = True
                    if pboard[idx + self.mov[i]] < self.SNAKE:  # 如果该点不是蛇的身体

                        if pboard[idx + self.mov[i]] > pboard[idx] + 1:
                            pboard[idx + self.mov[i]] = pboard[idx] + 1
                        if inqueue[idx + self.mov[i]] == 0:
                            queue.append(idx + self.mov[i])

        return found

    # 从蛇头开始，根据board中元素值，
    # 从蛇头周围4个领域点中选择最短路径
    def choose_shortest_safe_move(self, psnake, pboard):
        best_move = self.ERR
        min = self.SNAKE
        for i in range(4):
            if self.is_move_possible(psnake[self.HEAD], self.mov[i]) and pboard[psnake[self.HEAD] + self.mov[i]] < min:
                min = pboard[psnake[self.HEAD] + self.mov[i]]
                best_move = self.mov[i]
        return best_move

    # 从蛇头开始，根据board中元素值，
    # 从蛇头周围4个领域点中选择最远路径
    def choose_longest_safe_move(self, psnake, pboard):
        best_move = self.ERR
        max = -1
        for i in range(4):
            if self.is_move_possible(psnake[self.HEAD], self.mov[i]) and pboard[
                psnake[self.HEAD] + self.mov[i]] < self.UNDEFINED and pboard[
                psnake[self.HEAD] + self.mov[i]] > max:
                max = pboard[psnake[self.HEAD] + self.mov[i]]
                best_move = self.mov[i]
        return best_move

    # 检查是否可以追着蛇尾运动，即蛇头和蛇尾间是有路径的
    # 为的是避免蛇头陷入死路
    # 虚拟操作，在tmpboard,tmpsnake中进行
    def is_tail_inside(self):
        self.tmpboard[self.tmpsnake[self.tmpsnake_size - 1]] = 0  # 虚拟地将蛇尾变为食物(因为是虚拟的，所以在tmpsnake,tmpboard中进行)
        self.tmpboard[self.food] = self.SNAKE  # 放置食物的地方，看成蛇身
        result = self.board_refresh(self.tmpsnake[self.tmpsnake_size - 1], self.tmpsnake,
                                    self.tmpboard)  # 求得每个位置到蛇尾的路径长度
        for i in range(4):  # 如果蛇头和蛇尾紧挨着，则返回False。即不能follow_tail，追着蛇尾运动了
            if self.is_move_possible(self.tmpsnake[self.HEAD], self.mov[i]) and self.tmpsnake[self.HEAD] + self.mov[
                i] == self.tmpsnake[self.tmpsnake_size - 1] and self.tmpsnake_size > 3:
                result = False
        return result

    # 让蛇头朝着蛇尾运行一步
    # 不管蛇身阻挡，朝蛇尾方向运行
    def follow_tail(self):
        self.tmpsnake_size = self.snake_size
        self.tmpsnake = self.snake[:]
        self.board_reset(self.tmpsnake, self.tmpsnake_size, self.tmpboard)  # 重置虚拟board
        self.tmpboard[self.tmpsnake[self.tmpsnake_size - 1]] = self.FOOD  # 让蛇尾成为食物
        self.tmpboard[self.food] = self.SNAKE  # 让食物的地方变成蛇身
        self.board_refresh(self.tmpsnake[self.tmpsnake_size - 1], self.tmpsnake, self.tmpboard)  # 求得各个位置到达蛇尾的路径长度
        self.tmpboard[self.tmpsnake[self.tmpsnake_size - 1]] = self.SNAKE  # 还原蛇尾

        return self.choose_longest_safe_move(self.tmpsnake, self.tmpboard)  # 返回运行方向(让蛇头运动1步)

    # 在各种方案都不行时，随便找一个可行的方向来走(1步),
    def any_possible_move(self):
        best_move = self.ERR
        self.board_reset(self.snake, self.snake_size, self.board)
        self.board_refresh(self.food, self.snake, self.board)
        min = self.SNAKE

        for i in range(4):
            if self.is_move_possible(self.snake[self.HEAD], self.mov[i]) and self.board[
                self.snake[self.HEAD] + self.mov[i]] < min:
                min = self.board[self.snake[self.HEAD] + self.mov[i]]
                best_move = self.mov[i]
        return best_move

    def shift_array(self, arr, size):
        for i in range(size, 0, -1):
            arr[i] = arr[i - 1]

    # 虚拟地运行一次，然后在调用处检查这次运行可否可行
    # 可行才真实运行。
    # 虚拟运行吃到食物后，得到虚拟下蛇在board的位置
    def virtual_shortest_move(self):
        self.tmpsnake_size = self.snake_size
        self.tmpsnake = self.snake[:]  # 如果直接tmpsnake=snake，则两者指向同一处内存
        self.tmpboard = self.board[:]  # board中已经是各位置到达食物的路径长度了，不用再计算
        self.board_reset(self.tmpsnake, self.tmpsnake_size, self.tmpboard)

        food_eated = False
        while not food_eated:
            self.board_refresh(self.food, self.tmpsnake, self.tmpboard)
            move = self.choose_shortest_safe_move(self.tmpsnake, self.tmpboard)
            self.shift_array(self.tmpsnake, self.tmpsnake_size)
            self.tmpsnake[self.HEAD] += move  # 在蛇头前加入一个新的位置
            # 如果新加入的蛇头的位置正好是食物的位置
            # 则长度加1，重置board，食物那个位置变为蛇的一部分(SNAKE)
            if self.tmpsnake[self.HEAD] == self.food:
                self.tmpsnake_size += 1
                self.board_reset(self.tmpsnake, self.tmpsnake_size, self.tmpboard)  # 虚拟运行后，蛇在board的位置(label101010)
                self.tmpboard[self.food] = self.SNAKE
                food_eated = True
            else:  # 如果蛇头不是食物的位置，则新加入的位置为蛇头，最后一个变为空格
                self.tmpboard[self.tmpsnake[self.HEAD]] = self.SNAKE
                self.tmpboard[self.tmpsnake[self.tmpsnake_size]] = self.UNDEFINED

    # 如果蛇与食物间有路径，则调用本函数
    def find_safe_way(self):
        safe_move = self.ERR
        # 虚拟地运行一次，因为已经确保蛇与食物间有路径，所以执行有效
        # 运行后得到虚拟下蛇在board中的位置，即tmpboard，见label101010
        self.virtual_shortest_move()  # 该函数唯一调用处
        if self.is_tail_inside():  # 如果虚拟运行后，蛇头蛇尾间有通路，则选最短路运行(1步)
            return self.choose_shortest_safe_move(self.snake, self.board)
        safe_move = self.follow_tail()  # 否则虚拟地follow_tail 1步，如果可以做到，返回true
        return safe_move

    def set_map(self, new_food, new_snake, new_snake_size):
        self.food = new_food
        self.snake = new_snake
        self.snake_size = new_snake_size

    def get_one_step(self):
        # 重置矩阵
        self.board_reset(self.snake, self.snake_size, self.board)

        # 如果蛇可以吃到食物，board_refresh返回true
        # 并且board中除了蛇身(=SNAKE)，其它的元素值表示从该点运动到食物的最短路径长
        if self.board_refresh(self.food, self.snake, self.board):
            best_move = self.find_safe_way()  # find_safe_way的唯一调用处
        else:
            best_move = self.follow_tail()

        if best_move == self.ERR:
            best_move = self.any_possible_move()
        # 上面一次思考，只得出一个方向，运行一步
        if best_move != self.ERR:
            if best_move == self.LEFT:
                return 37
            elif best_move == self.RIGHT:
                return 39
            elif best_move == self.UP:
                return 38
            elif best_move == self.DOWN:
                return 40
        else:
            return -1
