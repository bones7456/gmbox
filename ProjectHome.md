# [谷歌音乐](http://www.google.cn/music)已经停止服务，因此gmbox目前已经无法使用 :( #
> by bones7456

https://images2-focus-opensocial.googleusercontent.com/gadgets/proxy?url=http://dl.dropbox.com/u/2992664/wiki/gmbox.png&container=focus&gadget=a&no_expand=1&resize_h=0&rewriteMime=image%2F*

无法下载封面问题见[这里](https://code.google.com/p/gmbox/issues/detail?id=119)

目前功能：
  * 支持网页版大部分功能，包括搜索、排行榜、标签、专题、挑歌、相似歌曲、艺术家热歌、艺术家专辑。
  * 支持复制和导出试听/下载/歌词地址，自定义下载文件名格式。
  * 支持调用外部播放器，可自定义参数方便以单实例运行和播放列表。
  * 支持调用外部下载工具，也可以自定义参数。
  * 支持http代理。
  * 独立可供二次开发的[核心库](https://code.google.com/p/gmbox/wiki/LibgmboxReadme)。

计划开发：
  * cli版
  * 保存播放和下载列表
  * 断点续传
  * 下载速度显示和控制
  * 更详细的文件名模板选项
  * 详细信息显示。

下载：
目前为beta版，最新代码可从仓库下载。
```
svn checkout https://gmbox.googlecode.com/svn/trunk/gmbox-gtk gmbox-gtk
```
运行“./gmbox-gtk.py”即可。更新在程序目录下运行
```
svn update
```
即可。
