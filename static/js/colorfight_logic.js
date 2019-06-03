hostUrl = "http://127.0.0.1:8000/";

var attackImg = new Image();
attackImg.src = '/static/images/attack.png';
var baseImg = new Image();
baseImg.src = '/static/images/base.png';
var shieldImg = new Image();
shieldImg.src = '/static/images/shield.png';

var gameStatus = {'cells': [], 'info': [], 'state': 'alive', 'current_time': 0, 'users': {}, 'selected': -1};
gameSize = 25;


GetGameInfo = function () {
    $.ajax({
        url: hostUrl + "colorfight/getgameinfo/",
        method: "POST",
        dataType: "json",
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({"game_id": game_id}),
        success: function (data) {
            var gameInfo = data;
            console.log(data);
            gameStatus.state = gameInfo['info']['game_state']
            if (gameStatus.state == 'alive') {
                gameStatus.cells = gameInfo['game_map'];
                gameStatus.current_time = gameInfo['info']['time'];
                gameStatus.users = gameInfo['users'];
                ListUsers(gameInfo['users'], gameStatus.current_time);
                ListGame(gameInfo['info']);
                WriteTimeLeft(gameInfo['info']);
            } else if (gameStatus.state == 'dead') {
                WriteTimeLeft(gameInfo['info']);
            } else if (gameStatus.state == 'none') {
                WriteTimeLeft(gameInfo['info']);
            }
        },
    }).always(function () {
        if (gameStatus.state == 'alive')
            setTimeout(GetGameInfo, 400);
    });
}

ListGame = function(gameInfo){
    $('#game_msg').empty();
    var game_msg = document.getElementById("game_msg");
    var strHTML = "";
    strHTML += "<p>游戏ID: "+ gameInfo['game_id'] +"</p>";
    strHTML += "<p>游戏时长: "+ gameInfo['game_time'] +"</p>";
    strHTML += "<p>等待加入时长: "+ (gameInfo['plan_start_time'] - gameInfo['create_time'])/1000 +"</p>";
    strHTML += "<p>已过时长: "+ parseInt((gameInfo['time']-gameInfo['plan_start_time'])/1000)  + "</p>";
    strHTML += "<p>玩家个数: "+ Object.keys(gameStatus.users).length +"</p>";
    game_msg.innerHTML=strHTML;

}

ListUsers = function(usersInfo, current_time){
    $('#user_list').empty();

    var users_key = Object.keys(usersInfo).sort(function(a,b){ return usersInfo[b]["score"]-usersInfo[a]["score"]; });
    var user_list = document.getElementById("user_list");
    var strHTML = "";
    for (var key in users_key){
        var user = usersInfo[users_key[key]];
        var color = HashIdToColor(user['uid']);
        var style = "style='background-color: " +color+";'";
        strHTML += "<p class='rounded user_p' "+ style+" uid='"+user['uid']+"'>"+ "<span style=\"color:#ffffff;\">"+user['username']+"|"+user['score']+"|"+parseInt(user['gold'])+"</span>"+"</p>";
    }
    user_list.innerHTML=strHTML;
}

InitCells = function () {
    for (var y = 0; y < gameSize; y++)
        for (var x = 0; x < gameSize; x++) {

        }
}

InitGame = function () {
    InitCells();
    WriteTimeLeft();
}

WriteTimeLeft = function (info) {
    var s = '';
    if (info['game_state'] == 'alive') {
        if (info['plan_start_time'] && info['plan_start_time'] > info['time']) {
            s += "The game will start in " + parseInt((info['plan_start_time'] - info['time']) / 1000).toString();
        }
        else if (info['time'] < info['finish_time']) {
            s += 'Time left: ' + parseInt((info['finish_time'] - info['time']) / 1000).toString() + ' s';
        }
    } else if (info['game_state'] == 'dead') {
        s += 'Game ended!';
    } else if (info['game_state'] == 'none') {
        s += 'Game is none! Please check game_id!';
    }

    $('#time_left').text(s);
}

DrawGame = function () {
    var canvas = $('#my_canvas');
    canvas.clearCanvas();

    var w = canvas[0].width;

    var cellWidth = w / gameSize;

    var strokeWidth = 3;
    if (gameStatus['cells'].length != 0) {
        for (var y = 0; y < gameSize; y++)
            for (var x = 0; x < gameSize; x++) {
                var cell = gameStatus['cells'][y][x];

                if (cell['build_state'] == 'empty') {
                    var fillColor = '#DDDDDD';
                }
                else if (cell['build_state'] == 'occupied' || cell['build_state'] == 'base'
                    || cell['build_state'] == 'build_base') {
                    // 颜色淡化
                    var take_time = gameStatus.current_time - cell['occupy_time']
                    var fillColor = CombineColor(HashIdToColor(cell['owner']), HashIdToColor(0), Math.min(0.9, take_time/1000/90));
                } else if (cell['build_state'] == 'fighting') {
                    // 正在攻击的
                    var p = (gameStatus.current_time - cell['attack_time']) / (cell['finish_time'] - cell['attack_time']);
                    var fillColor = CombineColor(HashIdToColor(cell['owner']), HashIdToColor(cell['attacker']), Math.min(1, p));
                }
                if (cell['cell_type'] == 'land' || cell['cell_type'] == 'base') {
                    canvas.drawRect({
                        fillStyle: fillColor,
                        strokeStyle: 'white',
                        strokeWidth: strokeWidth,
                        x: cell['position'].x * cellWidth,
                        y: cell['position'].y * cellWidth,
                        fromCenter: false,
                        width: cellWidth - strokeWidth,
                        height: cellWidth - strokeWidth,
                        cornerRadius: 8
                    });
                } else if (cell['cell_type'] == 'gold') {
                    canvas.drawPolygon({
                        fillStyle: fillColor,           // 填充颜色
                        strokeStyle: '#ddb129',         // 边框颜色
                        strokeWidth: 2,                 // 边框厚度
                        x: cell['position'].x * cellWidth,
                        y: cell['position'].y * cellWidth,
                        fromCenter: false,
                        radius: (cellWidth - strokeWidth * 2) / 2,   // 半径
                        sides: 6                        // x边形
                    });
                }
                if (cell['cell_type'] == 'base' && cell['build_finish'] == true) {
                    canvas.drawImage({
                        source: baseImg,
                        x: cell['position'].x * cellWidth,
                        y: cell['position'].y * cellWidth,
                        fromCenter: false,
                        width: cellWidth - strokeWidth,
                        height: cellWidth - strokeWidth,
                        // 透明度
                        opacity: Math.abs(1),
                    });
                }
                if (cell['build_state'] == 'fighting') {
                    if (cell['attack_type'] == 'attack') {
                        canvas.drawImage({
                            source: attackImg,
                            x: cell['position'].x * cellWidth,
                            y: cell['position'].y * cellWidth,
                            fromCenter: false,
                            width: cellWidth - strokeWidth,
                            height: cellWidth - strokeWidth,
                            // 透明度
                            opacity: Math.abs(1),
                        });
                    } else if (cell['attack_type'] == 'shield') {
                        canvas.drawImage({
                            source: shieldImg,
                            x: cell['position'].x * cellWidth,
                            y: cell['position'].y * cellWidth,
                            fromCenter: false,
                            width: cellWidth - strokeWidth,
                            height: cellWidth - strokeWidth,
                            // 透明度
                            opacity: Math.abs(1),
                        });
                    }
                }else if (cell['build_state'] == 'building' && cell["build_finish"] == false) {
                    canvas.drawImage({
                        source: baseImg,
                        x: cell['position'].x * cellWidth,
                        y: cell['position'].y * cellWidth,
                        fromCenter: false,
                        width: cellWidth - strokeWidth,
                        height: cellWidth - strokeWidth,
                        // 透明度
                        opacity: Math.abs(0.2),
                    });
                }
            }
    }
}

HexCombine = function (src, dest, per) {
    var isrc = parseInt(src, 16);
    var idest = parseInt(dest, 16);
    var curr = Math.floor(isrc + (idest - isrc) * per);
    return ("0" + curr.toString(16)).slice(-2).toUpperCase()
}

CombineColor = function (src, dest, per) {
    if (per < 0) {
        per = 0;
    }
    return "#" + HexCombine(src.slice(1, 3), dest.slice(1, 3), per) +
        HexCombine(src.slice(3, 5), dest.slice(3, 5), per) +
        HexCombine(src.slice(5), dest.slice(5), per)
}
GetRandomColor = function () {
    var r = ("0" + Math.floor(Math.random() * 255).toString(16)).slice(-2).toUpperCase();
    var g = ("0" + Math.floor(Math.random() * 255).toString(16)).slice(-2).toUpperCase();
    var b = ("0" + Math.floor(Math.random() * 255).toString(16)).slice(-2).toUpperCase();

    return '#' + r + g + b;
}
var colors = ['#DDDDDD', '#E6194B', '#3Cb44B', '#FFE119', '#0082C8', '#F58231',
    '#911EB4', '#46F0F0', '#F032E6', '#D2F53C', '#008080',
    '#AA6E28', '#800000', '#AAFFC3', '#808000', '#000080', '#FABEBE', '#E6BEFF']
HashIdToColor = function (id) {
    if (id < colors.length) {
        return colors[id];
    } else {
        while (colors.length <= id) {
            colors.push(GetRandomColor());
        }
        return colors[id];
    }
}


$(function () {
    var canvas = $('#my_canvas');
    canvas[0].width = canvas.parent().width() * 0.9;
    canvas[0].height = canvas[0].width;


    GetGameInfo();
    // InitGame();
    setInterval(DrawGame, 50);
})
