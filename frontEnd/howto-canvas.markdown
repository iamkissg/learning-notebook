# Canvas Tutorials on MDN

- <canvas> 是一个可以使用脚本(通常为JavaScript)在其中绘制图形的 HTML 元素.它可以用于制作照片集或者制作简单(也不是那么简单)的动画.
- 实际上，<canvas> 标签只有两个属性 `width` 和 `height` ; id 属性每个 HTML 元素都默认具有的属性. 给每个标签都加上一个id属性是个好主意，这样就能在脚本中很容易的找到它。
- 在<canvas>和</canvas>之间可以提供替换内容, 可以是文字描述或静态图片
- </canvas>标签不可省略. 若结束标签不存在, 文档的其余部分都会被认为是替代的内容.
- <canvas> 元素创造了一个固定大小的画布，它公开了一个或多个**渲染上下文**，其可以用来绘制和处理要展示的内容。
- <canvas> 元素有一个做 getContext() 的方法，这个方法是用来获得渲染上下文和它的绘画功能 。getContext()只有一个参数，上下文的格式, 如`'2d'`
- 可以用`if (canvas.getContext)`语句测试`getContext()`方法的存在
- 画布平面, x轴水平向右, y轴竖直向下
- `fillRect(x, y, width, height)` - 填充矩形
- `strokeRect(x, y, width, height)` - 矩形边框
- `clearRect(x, y, width, height)` - 清楚矩形区域
- 图形的基本元素是**路径**。路径是通过不同颜色和宽度的线段或曲线相连形成的不同形状的点的集合。一个路径，甚至一个子路径，都是**闭合**的:
 1. 首先，创建路径起始点。
 2. 然后使用画图命令去画出路径。
 3. 之后把路径封闭。
 4. 一旦路径生成，通过描边或填充路径区域来渲染图形。
- `beginPath()` - 新建一条路径，生成之后，图形绘制命令被指向到路径上生成路径。会清空前一次的痕迹
- `closePath()` - 闭合路径之后图形绘制命令又重新指向到上下文中。
- `stroke()` - 通过线条来绘制图形轮廓。路径不会自动闭合, 使用closePath()来闭合路径
- `fill()` - 通过填充路径的内容区域生成实心的图形。路径会自动闭合
- `moveTo(x, y)` - 移动笔触, 不会留下痕迹. (与python小乌龟一样)
- `lineTo(x, y)` - 绘制一条从当前位置到指定x以及y位置的直线。
- `arc(x, y, radius, startAngle, endAngle, anticlockwise)` - 画一个以（x,y）为圆心的以radius为半径的圆弧（圆），从startAngle开始到endAngle结束，按照anticlockwise给定的方向（默认为顺时针）来生成。
- ?`arcTo(x1, y1, x2, y2, radius)` - 根据给定的控制点和半径画一段圆弧，再以直线连接两个控制点(弓形?)
- `quadraticCurveTo(cp1x, cp1y, x, y)` - 绘制二次Bezier曲线(3个点)，x,y为结束点，cp1x,cp1y为控制点。起点为当前点.
- `bezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y)` - 绘制三次Bezier曲线(4个点)，x,y为结束点，cp1x,cp1y为控制点一，cp2x,cp2y为控制点二。
- `rect(x, y, width, height)` - 绘制一个左上角坐标为（x,y），宽高为width以及height的矩形
- `Path2D`对象, 用来缓存或记录绘画命令. Path2D()会返回一个新初始化的Path2D对象.
- 使用 SVG paths - `var p = new Path2D("M10 10 h 80 v 80 h -80 Z");` - 移动到点(M10, 10), 水平右移80个像素, 竖直下移80个像素, 水平左移80个像素, Z回到原点.
- `fillStyle = color` - 设置图形的填充颜色。
- `strokeStyle = color` - 设置图形轮廓颜色
- `globalAlpha = transparencyValue` - 全局透明度, 将影响到canvas里所有图形的透明度. 有效值从0.0到1.0, 默认1.0
- 在fillStyle或strokeStyle设置样式时, 用`rgba`设置颜色和透明度
- `lineWidth = value` - 设置线条宽度。线宽是指给定路径的中心到两边的粗细, 就是在路径的两边各绘制线宽的一半. 宽度为奇数, 偶数, 对路径中心的选取有影响.
- `lineCap = type` - 设置线条末端(线帽)样式。`butt`/`round`/`square`: 默认/圆帽/方帽
- `lineJoin = type` - 设定线条与线条间接合处的样式。`round`/`bevel`/`miter`: 圆角/平角/默认
- `miterLimit = value` - 限制当两条线相交时交接处最大长度；所谓交接处长度（斜接长度）是指线条交接处内角顶点到外角顶点的长度。若大于此值, 连接效果变成`bevel`
- `getLineDash()` - 返回一个包含当前虚线样式，长度为非负偶数的**数组**。
- `setLineDash(segments)` - 设置当前虚线样式。接受一个数组, 来指定线段与间隙的交替
- `lineDashOffset = value` - 设置虚线样式的起始偏移量
- 自定义填充或描边样式: 创建canvasGradient渐变对象, 用addColorStop方法为其上色
- `createLinearGradient(x1, y1, x2, y2)` - 接受 4 个参数，表示渐变的起点 (x1,y1) 与终点 (x2,y2)
- `createRadialGradient(x1, y1, r1, x2, y2, r2)` - 接受 6 个参数，前三个定义一个以 (x1,y1) 为原点，半径为 r1 的圆，后三个参数则定义另一个以 (x2,y2) 为原点，半径为 r2 的圆。
- ?`gradient.addColorStop(position, color)` - 接受 2 个参数，position 参数必须是一个 0.0 与 1.0 之间的数值，表示渐变中颜色所在的相对位置(相对于哪里的位置?)。color 参数必须是一个有效的 CSS 颜色值（如 #FFF， rgba(0,0,0,1)，等等）。
- `createPattern(image, type)` - 该方法接受两个参数。Image 可以是一个 Image 对象的引用，或者另一个 canvas 对象。Type 必须是下面的字符串值之一：repeat，repeat-x，repeat-y 和 no-repeat。图案的应用跟渐变很类似的，创建出一个 pattern 之后，赋给 fillStyle 或 strokeStyle 属性即可。
- `shadowOffsetX = float`|`shadowOffsetY = float` - 设定阴影在 X 和 Y 轴的延伸距离，不受变换矩阵所影响的。负值表示阴影会往上或左延伸，正值则表示会往下或右延伸，它们默认都为 0。
- `shadowBlur = float` - 设定阴影的模糊程度，其数值并不跟像素数量挂钩，也不受变换矩阵的影响，默认为 0。
- `shadowColor = color` - shadowColor 是标准的 CSS 颜色值，用于设定阴影颜色效果，默认是全透明的黑色。
- 填充规则:  根据某处在路径的外面或里面来决定该处是否被填充
 - "nonzero": non-zero winding rule, 默认值;(`ctx.fill("nonzero")`)
 - "evenodd":  even-odd winding rule.
- 绘制文本:
 - `fillText(text, x, y [, maxWidth])` - (x, y) 指定文本位置
 - `strokeText(text, x, y [, maxWidth])`
- 文本样式:
 - `font = value` - 当前用来绘制文本的样式. 这个字符串使用和 CSS font 属性相同的语法. 默认的字体是 10px sans-serif。
 - `textAlign = value` - 文本对齐选项. 可选的值包括：start, end, left, right or center. 默认值是 start。
 - `textBaseline = value` - 基线对齐选项. 可选的值包括：top, hanging, middle, alphabetic, ideographic, bottom。默认值是 alphabetic。
 - `direction = value` - 文本方向。可能的值包括：ltr, rtl, inherit。默认值是 inherit。
- `measureText()` - 将返回一个 TextMetrics对象的宽度、所在像素，这些体现文本特性的属性。
- 引入图像到canvas里:
 1. 获得一个指向HTMLImageElement的对象或者另一个canvas元素的引用作为源，也可以通过提供一个URL的方式来使用图片
 2. 使用drawImage()函数将图片绘制到画布上
- `HTMLImageElement` - 图片由Image()函数构造出来的，或者任何的<img>元素
- `HTMLVideoElement` - 用一个HTML的 <video>元素作为图片源，可以从视频中抓取当前帧作为一个图像
- `HTMLCanvasElement` - 可以使用另一个 <canvas> 元素作为你的图片源。
- `ImageBitmap` - 这是一个高性能的位图，可以低延迟地绘制，它可以从上述的所有源以及其它几种源中生成。
- 获得图片的途径:
 - 使用同一页面内的图片, 可用`document.images`集合或`document.getElementByTagName()`方法或`document.getElementById()`方法
 - ?使用其他域名下的图片, 在 HTMLImageElement上使用`crossOrigin`属性，可以请求加载其它域名上的图片。如果图片的服务器允许跨域访问图片，那么可以使用这个图片而不污染canvas，否则，使用这个图片将会污染canvas。(污染?)
 - 使用启发canvas元素, 与引用页面内图片类似, 但引入的应该是已经准备好的canvas. 一个常用的应用就是将第二个canvas作为另一个大的canvas的缩略图
 - 利用`Image()`方法构创建新的HTMLImageElement对象.
 - 通过data:url方式嵌入图像 - `img.src = 'data:image/gif;base64,R0lGODlhCwALAIAAAAAA3pn/ZiH5BAEAAAEALAAAAAALAAsAAAIUhA+hkcuO4lmNVindo7qyrIXiGBYAOw==';`
 - 使用<video>中的视频帧
- `drawImage(image, x, y)` - image 是 Image 或者 canvas 对象，x 和 y 是其在目标 canvas 里的起始坐标。
- `drawImage(image, x, y, width, height)` - width 和 height两个参数用来控制 当像canvas画入时应该缩放的大小
- `drawImage(image, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight)` - 除了image, 前4个是定义图像源的切片位置和大小，后4个则是定义切片的目标显示位置和大小。
- mozImageSmoothingEnabled 属性，值为 false 时，图像不会平滑地缩放。默认是 true 
- `save()` & `restore()` - 用来保存和恢复 canvas 状态的，都没有参数。Canvas 的状态就是当前画面应用的所有样式和变形的一个快照。
- 一个绘画的状态包括:
 - 当前应用的变形（即移动，旋转和缩放）
 - strokeStyle, fillStyle, globalAlpha, lineWidth, lineCap, lineJoin, miterLimit, shadowOffsetX, shadowOffsetY, shadowBlur, shadowColor, globalCompositeOperation 的值
 - 当前的裁切路径（clipping path）
- `translate(x, y)` - 移动坐标轴(或者说原点), x 是左右偏移量，y 是上下偏移量，如右图所示。
- `rotate(angle)` -接受一个参数：旋转的角度(angle)，顺时针方向，以弧度为单位的值。
- `scale(x, y)` - x,y 分别是横轴和纵轴的缩放因子，它们都必须是正值。值比 1.0 小表示缩小，比 1.0 大则表示放大
- ?`transform(m11, m12, m21, m22, dx, dy)` - 直接对变形矩阵做修改, 将当前的变形矩阵乘上下面的矩阵. 必须重置当前的变形矩阵为单位矩阵, 然后以相同的参数调用transform方法. 如果任意一个参数是无限大, 那么变形矩阵也必须被标记为无限大, 否则会抛出异常.
- `globalCompositeOperation = type`:
 1. source-over (default) - 新图形会覆盖原有内容
 2. destination-over - 在原有内容之下绘制新图形
 3. source-in - 新图形仅仅出现与原有内容重叠的部分, 其他区域都变成透明
 4. destination-in - 原有内容中与新图形重叠的部分被保留, 其他区域都变成透明
 5. source-out - 只保留新图形中与原有内容不重叠的部分
 6. destination-out - 只保留原有图形中与新图形不重叠的部分
 7. source-atop - 新图形与原有内容重叠的部分被绘制, 并覆盖在原有内容之上
 8. destination-atop - 重叠部分被保留, 覆盖在新图形之上
 9. lighter - 两图形重叠部分做加色处理
 10. darker - 两图形重叠部分做减色处理
 11. xor - 重叠部分变透明
 12. copy - 只有新图形被保留, 其他都被清除
- `clip()` - 创建裁剪路径, 默认情况下, canvas有一个与它自身一样大的裁切路径. 裁剪的作用是**遮罩**, 用来隐藏没有遮罩的部分. 裁剪路径也属于canvas状态的一部分, 可以被保存起来, 如果在创建裁剪路径时想保留原来的裁剪路径, 需要做的就是保存一些canvas的状态
- 动画的基本步骤:
 1. 清空 canvas\\
 除非接下来要画的内容会完全充满 canvas （例如背景图），否则你需要清空所有。最简单的做法就是用 clearRect 方法。
 2. 保存 canvas 状态\\
 如果要改变一些会改变 canvas 状态的设置（样式，变形之类的），又要在每画一帧之时都是原始状态的话，你需要先保存一下。
 3. 绘制动画图形（animated shapes）\\
 这一步才是重绘动画帧。
 4. 恢复 canvas 状态\\
 如果已经保存了 canvas 的状态，可以先恢复它，然后重绘下一帧
- 通常, 仅仅在脚本执行结束后才能看见结果, 因此在for循环内完成动画是不太可能的. 因此需要一些定时的执行的重绘的方法.
- `setInterval(function, delay)` - 每一个delay指定的时间间隔(毫秒)执行function
- `setTimeout(function, delay)` - 在delay(毫秒)后, 执行function
- `requestAnimationFrame(callback)` - 告诉浏览器执行一个动画, 要求浏览器在下一个重绘之前调用指定函数更新动画
- [MDN高级动](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Advanced_animations)
- `ImageData`对象中存储了canvas对象真实的像素数据, 包含以下只读属性:
 - width: 图片宽度, 单位像素
 - height: 图片高度, 单位像素
 - data: Uint8ClampedArray类型的一维数组，包含着RGBA格式的整型数据，范围在0至255之间（包括255）。每个部份被分配到一个在数组内连续的索引，左上角像素的红色部份在数组的索引0位置。像素从左到右被处理，然后往下，遍历整个数组。
- Uint8ClampedArray  包含高度 × 宽度 × 4 bytes数据，索引值从0到(高度×宽度×4)-1
- `createImageData(width, height)` - 创建新的具体特定尺寸的Image对象, 所有元素被预设为透明黑
- `createImageData(anotherImageData)` - 由存在的ImageData对象创建, 但新的对象像素全部被预设为透明黑, 而并非完全复制了图片数据
- `var myImageData = ctx.getImageData(left, top, width, height);` - 获得包含canvas上下文像素数据的ImageData对象. 任何canvas以外的元素都会被返回成一个透明黑的ImageData对象
- `layerx`和`layery`记录鼠标的当前位置. - **颜色选择器**
- `ctx.putImageData(myImageData, dx, dy);` - 写入像素数据 - **在场景中写入像素数据**
- 对像素粒度的值进行处理 - **灰度与颜色反转**
- 在imageSmoothingEnabled 属性的帮助下, 可放大显示图片. - **缩放与反锯齿**
- HTMLCanvasElement 提供一个`toDataURL()`方法，此方法在保存图片的时候非常有用。它返回一个包含被类型参数规定的图像表现格式的数据链接。返回的图片分辨率是96dpi。
- `canvas.toDataURL('image/png')` - 默认设定。创建一个PNG图片。
- `canvas.toDataURL('image/jpeg', quality)` - 创建一个JPG图片。你可以有选择地提供从0到1的品质量，1表示最好品质，0基本不被辨析但有比较小的文件大小。
- 当从画布中生成了一个数据链接，可以将它用于任何<image>元素，或者将它放在一个有download属性的超链接里用于保存到本地。

---

- 在离屏canvas上预渲染相似的图形或重复的对象 - 若在每一帧里有好多复杂的画图运算, 应考虑创建一个离屏canvas, 将图像在画布上画一次, 然后在每帧上画出视线以外的这个画布

```js
myEntity.offscreenCanvas = document.createElement("canvas");
myEntity.offscreenCanvas.width = myEntity.width;
myEntity.offscreenCanvas.height = myEntity.height;
myEntity.offscreenContext = myEntity.offscreenCanvas.getContext("2d");

myEntity.render(myEntity.offscreenContext);
```

- 避免浮点数的坐标点, 用整数取而代之. 当画一个没有整数坐标点的对象时, 会发生子像素渲染. 浏览器为了达到抗锯齿的效果会做额外的运算. 为了避免这种情况，在调用drawImage()函数时，用Math.floor(函数对所有的坐标点取整。
- 不要在用drawImage时缩放图像
- 使用多层画布画一个复杂的场景 - 有些元素不断地改变或移动, 而其他元素永远不变, 这种情况的优化是用多个画布元素去创建不同的层次
- 用css设置大的背景图 - 如果像大多数游戏那样，有一张静态的背景图，用一个静态的<div>元素，结合background 特性，以及将它置于画布元素之后。这么做可以避免在每一帧在画布上绘制大图。
- 如果游戏使用canvas, 而不需要透明, 应在画布上设置moz-opaque属性, 这能用于内部渲染优化(仅限Gecko)
- 用css transforms特性缩放画布 - `css transforms`特性由于调用GPU, 更快捷. 最好的情况是, 不将小画布放大, 而将大画布缩小.

## Tips

- canvas实际上有两套尺寸。一个是元素本身的大小，还有一个是元素绘图表面的大小\\
当设置元素的width与height属性时，实际上是同时修改了该元素本身的大小与元素绘图表面的大小。然而，如果是**通过css来设定canvas元素的大小，那么只会改变元素本身的大小**，而不会影响到绘图表面。在默认情况下，canvas元素与其绘图表面，都是300像素宽、150像素高。\\
当canvas元素的大小不符合其绘图表面的大小时，浏览器就会对绘图表面进行缩放，使其符合元素的大小
