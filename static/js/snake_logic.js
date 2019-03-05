var unit = 30;
var speed = '100';
var xGridSize = 10;
var yGridSize = 10;
//产生场地
var table = $('<table>');
table.className = 'snake';
table.setAttribute('cellspacing', 0);
table.setAttribute('border-collapse', 'collapse');
table.style.border = "2px solid #404293";
for (var i = 0; i < yGridSize; i++) {
    var tr = $('<tr>');
    for (var j = 0; j < xGridSize; j++) {
        var td = $('<td>');
        td.style.width = unit + 'px';
        td.style.height = unit + 'px';
        td.style.backgroundColor = '#eee';
        td.style.border = "1px solid #fff";
        tr.appendChild(td);
    }
    table.appendChild(tr);
}
$('body')[0].appendChild(table);

//蛇身上的一个节点类
function Node(left, top) {
    this.left = left;
    this.top = top;

    this.equals = function (node) {
        return left == node.left && top == node.top;
    }

    this.exist = function (left, top) {
        return this.left == left && this.top == top;
    }

    this.isValid = function () {
        if (this.left < 0 || this.left > xGridSize - 1 || this.top < 0 || this.top > yGridSize - 1) {
            return false;
        }
        return true;
    }

    this.toString = function () {
        return '{left:' + left + ', top:' + top + '}';
    }
}

//贪吃蛇
function Snake() {
    this.body = [];
    this.validFoodArea = [];        // 可生成食物的地方

    this.food;

    //测试坐标在不在蛇身上
    this.exist = function (left, top, exceptHead) {
        var i = exceptHead ? 1 : 0;
        for (; i < this.body.length; i++) {
            if (this.body[i].exist(left, top)) {
                return true;
            }
        }
        return false;
    };

    function indexOf(node) {
        return node.top * xGridSize + node.left;
    };

    function getTd(index) {
        return $('.snake td')[index];
    };

    this.keyCode; //方向

    this.isValidDir = function (keyCode) {
        return Math.abs(keyCode - this.keyCode) % 2 == 1;// 等于1为合法
    };

    //!important
    this.move = function () {
        //根据方向移动
        switch (this.keyCode) {
            case 37://<--
                var left = this.body[0].left - 1;
                var top = this.body[0].top;
                break;
            case 38:
                var left = this.body[0].left;
                var top = this.body[0].top - 1;
                break;
            case 39://-->
                var left = this.body[0].left + 1;
                var top = this.body[0].top;
                break;
            case 40:
                var left = this.body[0].left;
                var top = this.body[0].top + 1;
                break;
        }
        if (this.isFood(left, top)) {//如果前方是食物
            this.eat(left, top);//吃掉
            this.updateValidFoodArea();         // 更新可生成食物的区域
            this.getNewFood();
            this.showFood();
        } else {
            var node = this.body.pop();         // 删除并取出数组尾部
            node.left = left;
            node.top = top;
            this.body.unshift(node);            // 从数组的头部插入
            this.updateValidFoodArea();         // 更新可生成食物的区域
        }
        //显示
        this.show();
    };

    this.isFood = function (left, top) {
        if (left == this.food.left && top == this.food.top) {//发现前方是食物
            return true;
        }
        return false;
    };

    this.eat = function (left, top) {
        var td = getTd(indexOf(this.food));
        td.style.backgroundImage = '';
        this.body.unshift(this.food);//向数组的开头添加一个元素
    };

    //显示蛇的形状
    this.show = function () {
        var cells = $('.snake td');
        //清空所有
        for (var i = 0; i < cells.length; i++) {
            cells[i].style.backgroundColor = '#eee';
            cells[i].style.borderRadius = '0';
        }
        var head = this.body[0];
        if (this.exist(head.left, head.top, true)) {
            clearInterval(window.timer);
            alert('失败...咬到自己，游戏结束！');
            return;
        }
        if (!head.isValid()) {
            clearInterval(window.timer);
            alert('失败...撞墙，游戏结束！');
            return;
        }
        for (var i = 0; i < this.body.length; i++) {
            var node = this.body[i];
            var index = indexOf(node);
            var td = cells[index];
            if (i == this.body.length - 1)
                td.style.backgroundColor = '#8D2130';
            else
                td.style.backgroundColor = i == 0 ? '#000' : '#666';
            td.style.borderRadius = '8px';
        }
    };

    this.showFood = function () {
        var node = this.food;
        var index = indexOf(node);
        var td = $('.snake td')[index];
        td.style.background = "#eee url('/static/images/food.png') 2px 0 no-repeat";
    }

    //获取一个食物节点
    this.getNewFood = function () {
        var index = Math.floor(Math.random() * this.validFoodArea.length);// 0-->length-1
        this.food = this.validFoodArea[index];
        return this.validFoodArea[index];

    };

    this.toString = function () {
        var str = '[' + this.body[0];
        for (var i = 1; i < this.body.length; i++) {
            str += this.body[i];
            str += ',';
        }
        return str + ']';
    }
    // 0 --- 399
    this.updateValidFoodArea = function () {
        this.validFoodArea = [];
        for (var i = 0; i < xGridSize; i++) {
            for (var j = 0; j < yGridSize; j++) {
                if (!this.exist(i, j, 0)) {
                    this.validFoodArea.push(new Node(i, j));
                }
            }
        }
    }

    var first = new Node(Math.floor(Math.random() * xGridSize),
        Math.floor(Math.random() * yGridSize));
    this.body.push(first);      //生成初始蛇
    this.updateValidFoodArea();
    this.getNewFood();             //生成初始食物
    this.showFood();
    this.show();
}

var timer;
var snake = new Snake();

document.onkeyup = function (e) {
    var keyCode = e.keyCode;
    if (keyCode < 37 || keyCode > 40) {
        return;
    }
    if (snake.keyCode) {// 方向已经初始化
        if (snake.isValidDir(keyCode)) {
            snake.keyCode = keyCode;
        }
    } else {// 方向未初始化
        snake.keyCode = keyCode;
        timer = setInterval(function () {
            snake.move();
        }, speed);
    }
}