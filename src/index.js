const Jimp = require('jimp');
const cv = require('@/opencv');
const math = require('mathjs')
var oriImg = await Jimp.read('./1.jpg');   
//读取本地文件1.jpg，将来考虑改为base64读取以节省本地空间
var oriMat = cv.matFromImageData(oriImg.bitmap);    
//将jimp读取数据转换为Mat
var concIn = new Array
//用于存放每个点对应的浓度（x）
var circles = new Array(cirNum);    
/*用于存放取样区域的数组，cirNum为传入取样区域数目，格式为
[x0,y0,r0],
[x1,y1,r1],
[x2,y2,r2],
...*/
var maxRand
//控制随机取样次数
function createFunction(expression) {
    // 使用Function构造函数创建一个函数
    return new Function('R', 'G', 'B', 'return ' + expression);
}
var calcRate = createFunction(expIn)
//根据输入计算式计算各个点的数值


function randomNum(minNum,maxNum){ 
    //生成从minNum到maxNum的随机数
    switch(arguments.length){ 
        case 1: 
            return parseInt(Math.random()*minNum+1,10); 
        break; 
        case 2: 
            return parseInt(Math.random()*(maxNum-minNum+1)+minNum,10); 
        break; 
            default: 
                return 0; 
            break; 
    } 
} 

var linage = new Array
for(i=0;i<math.min(concIn.length,circles.length);i++)
//根据浓度点数和指定点数较少的循环防止溢出
{
    var point = new Array
    for(j=0;j<maxRand;j++)
    {
        //随机取点并获取该点的RGB值
        var x = randomNum((circles[i][0]-circles[i][2]),(circles[i][0]+circles[i][2]))
        var y = randomNum((circles[i][0]-circles[i][1]),(circles[i][0]+circles[i][1]))
        let pixelValue = oriMat.ucharPtr(y,x)
        //pixelValue:[R,G,B,A]
        let R = pixelValue[0]
        let G = pixelValue[1]
        let B = pixelValue[2]
        try
        {
            point.push(calcRate(R,G,B))
        }
        catch(error)
        {
            console.log(error)
            //检测除0错误
        }
    }
    linage.push([concIn[i],math.mean(point),math.std(point)])
    //读取点位的x,y,err
}

