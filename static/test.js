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


DrawGame = function () {
    var canvas = $('#my_canvas');

    // if (gameStatus['selectId'] == 2) {
    //     var fillColor = HashIdToColor(owner);
    // } else {
    //     if (cell['c'] == 0) {
    //         var fillColor = CombineColor(HashIdToColor(0), HashIdToColor(owner), Math.min(1, cell['t'] / 8));
    //     } else {
    //         var fillColor = CombineColor(HashIdToColor(owner), HashIdToColor(attacker), Math.min(1, (currTime - cell['at']) / (cell['f'] - cell['at'])));
    //     }
    // }
    var fillColor = HashIdToColor(3);
    console.log(fillColor);
    canvas.drawRect({
        fillStyle: fillColor,
        strokeStyle: 'white',
        strokeWidth: 2,
        x: 20,
        y: 20,
        fromCenter: false,
        width: 50,
        height: 50,
        cornerRadius: 8
    });

    // 颜色淡化
    var fillColor = CombineColor(HashIdToColor(0), HashIdToColor(3), Math.min(1,0.4));
    console.log(fillColor);
    canvas.drawRect({
        fillStyle: fillColor,
        strokeStyle: 'white',
        strokeWidth: 2,
        x: 120,
        y: 20,
        fromCenter: false,
        width: 50,
        height: 50,
        cornerRadius: 8
    });

    // 正在攻击的
    var fillColor = CombineColor(HashIdToColor(3), HashIdToColor(2), Math.min(1, 0.5));
    console.log(fillColor);
    canvas.drawRect({
        fillStyle: fillColor,
        strokeStyle: 'white',
        strokeWidth: 2,
        x: 220,
        y: 20,
        fromCenter: false,
        width: 50,
        height: 50,
        cornerRadius: 8
    });
}


$(function () {
    // if (cell['c'] == 0) {
    //     var fillColor = CombineColor(HashIdToColor(0), HashIdToColor(owner), Math.min(1, cell['t'] / 8));
    // } else {
    //     var fillColor = CombineColor(HashIdToColor(owner), HashIdToColor(attacker), Math.min(1, (currTime - cell['at']) / (cell['f'] - cell['at'])));
    // }
    var canvas = $('#my_canvas');
    canvas[0].width = canvas.parent().width() * 0.9;
    canvas[0].height = canvas[0].width;

    setInterval(DrawGame, 50);
})
