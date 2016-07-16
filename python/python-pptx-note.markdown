#python-pptx learning note

##Working with Presentations

- `prs = Presentation()` - 打开一个新的`Presentation`, `save`即可得到`.pptx`文件
- `prs =Presentation('xxx')` - 打开一个现有的pptx文件. `.ppt`文件是无效的. 同名储存的话, 将会覆盖源文件
- 还可以用`file-like`对象创建`Presentation`, 并储存为一个`file-like`对象. 这意味着可以从网上读取`StringIO`或`BytesIO`流对象, 作为`Presentation`的输入

##Working with Slides

- `slide layout`(幻灯片布局)相当于一张幻灯片的模板. 每个`slide layout`都是基于`slide master`的, 可以定义全局的`slide master`, 也可以定义多`slide master`
- ppt有9类`slide layout`:
 - Title (presentation title slide)
 - Title and Content
 - Section Header (sometimes called Segue)
 - Two Content (side by side bullet textboxes)
 - Comparison (same but additional title for each side by side content box)
 - Title Only
 - Blank
 - Content with Caption
 - Picture with Caption
- `python-pptx`使用`prs.slide_layouts[0]`~`prs.slide_layouts[0]`来表示与上对应的`slide layout`

```python
SLD_LAYOUT_TITLE_AND_CONTENT = 1

prs = Presentation()
slide_layout = prs.slide_layouts[SLD_LAYOUT_TITLE_AND_CONTENT]
slide = prs.slides.add_slide(slide_layout)
```
- 使用时, 可以创建一个`slide layout`的枚举类, 或定义一个有意义的常数, 如上所示, 不失为一个好习惯
- `prs.slide_layouts`是`Presentation`对象内含的`collection of slide of slide layouts`, 但将它赋给另一个变量,  就得到了一个`slide layout`对象, 使用可能会更简单. 变量赋值是**旧瓶装旧酒**
- `prs.slides`是`Presentation`内的`collection of slides`, 类似与`list`. `add slide`方法是基于`slides`, 而非`Presentation`.
- `add_slide()`方法在`slides`的末尾增加一张新的幻灯片. 即相当于`list.append`

##Understanding Shapes

- 除了幻灯片背景, 几乎所有幻灯片上的元素都是一个`shape`, 约有6~10种不同类型的`shape`.
- 典型的6大类`shape`:
 - `auto shapre` - 常规shape, 可以有填充与轮廓, 可以包含文本. 一些是可调整的. 文本框是一个autoshape
 - `picture` - 一张光栅(?)照片. autoshape可用图片做填充
 - `graphic frame` - 表格, 图表, 多媒体的容器.
 - `group shape` - 即多个shape的组合. 目前`python-pptx`尚不支持
 - `line/connector` - 即连接线. 尚不支持
 - `content part` - 莫名其妙
- 实际使用的9类`shape`:
 - shape shapes – auto shapes with fill and an outline
 - text boxes – auto shapes with no fill and no outline
 - placeholders – auto shapes that can appear on a slide layout or master and be inherited on slides that use that layout, allowing content to be added that takes on the formatting of the placeholder
 - line/connector – as described above
 - picture – as described above
 - table – that row and column thing
 - chart – pie chart, line chart, etc. python-pptx doesn’t support creating these yet.
 - smart art – not supported yet, although preserved if present
 - media clip – not supported yet, although preserved if present
- 每张幻灯片都维护着一棵`shape`树, 可通过以下方式获得:

```python
shapes = slide.shapes
```

##Working with AutoShapes

- 总计有182种不同形状的auto shapes
- ppt用英制单位储存长度值, 大多数办公文档都以英制单位储存长度值
- 在英制单位里,1英寸可用整数914400表示
