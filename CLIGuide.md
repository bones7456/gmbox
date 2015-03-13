本指南只适用于 gmbox 0.2.4，0.3/0.4尚未有cli版本。

# 简介 #

GUI的使用，相信大家不会有什么问题，在这里说明一下CLI的使用方法。

CLI有两种模式：交互模式和批处理模式。交互模式下，可以接受用户输入的指令，并执行相应的动作；批处理模式则由命令行传入需要执行的指令，程序执行完毕后即自动退出。下面分别结束这两种模式。


# 交互模式 #

## 交互模式的启动 ##

交互模式可以在执行了安装脚本后，在终端里执行 gmbox 打开，如果不安装，也可以直接执行 src/cli.py 启动，注意启动交互模式不能跟任何参数。

看到gmbox的提示符 "gmbox> " 则表示成功进入交互模式。

windows版本也可以在命令提示符里执行 `cli.exe` 打开交互模式的CLI。

## 交互模式命令介绍 ##

`help` 可以查看目前支持的命令，键入 `help 命令名` 可以查看某个命令的帮助。

**榜单下载的命令：**

`lists` 可以列出目前支持的榜单。无参数。

`list  <榜单名>` 或 `l <榜单名>` 参数`lists`列出的榜单名的所有歌曲，默认列出上次list的榜单或华语新歌。

`search <关键字>` 或 `s <关键字>` 搜索包含关键字的歌曲。

`down num1,[num2,[num3,...]]` 或 `d num1,[num2,[num3,...]]` 下载上次搜索或list的结果里面的某几首歌曲，须跟逗号分割的数字为参数。参数支持2-5这样的形式，表示范围。

`downall` 或 `da` 下载上次搜索或list的结果的全部歌曲。

**专辑下载的命令：（类似榜单下载）**

`albums` 可以列出目前支持的专辑列表。无参数。

`albumlist <专辑列表名>` 或 `al <专辑列表名>` 列出专辑列表的所有专辑，默认列出上次albumslist的专辑或影视新碟。

`albumsearch <关键字>` 或 `as <关键字>` 搜索包含关键字的专辑。


`albumdown num1,[num2,[num3,...]]` 或 `ad num1,[num2,[num3,...]]` 下载上次搜索或albumlist的结果里面的某几首歌曲，须跟逗号分割的数字为参数。参数支持2-5这样的形式，表示范围。

`albumdownall` 或 `ada` 下载上次albumlist或albumsearch的所有专辑。

`albumsongs num` 或 `ass num` 列出上次搜索或albumlist的结果中的第num个专辑的所包含的歌曲。

**config 命令**

`config` 不加参数的config命令可以列出当前的设置。

`config key vaule` 可以修改配置项key的值为vaule，目前有以下几个配置：

  * `config savedir       <LOCAL_PATH>        `设置歌曲保存路径为LOCAL\_PATH

  * `config id3utf8       True|False  `设置是否转换ID3信息到UTF-8编码

  * `config makeartistdir True|False  `设置下载时是否建立歌手目录

  * `config makealbumdir  True|False  `设置下载专辑时是否下载到专辑目录

  * `config addalbumnum   True|False  `设置下载专辑时是否在专辑下载时前置专辑序号

**其他命令**

`version` 查看当前运行的gmbox的版本。

`exit` 退出

# 批处理模式 #

## 批处理模式的启动 ##

和交互模式类似，在执行命令行时，加上任何参数，就会进入批处理模式。

## 批处理模式参数介绍 ##

**可以执行 `gmbox -h`(linux安装时) 或 `./cli.py -h`(linux未安装时) 或 `cli.exe -h` (windows时) 来获得在线的帮助**

**其实批处理模式的参数和交互模式的命令基本可以一一对应，除了专辑相关的单字母参数改成大写以外**

`  --version             `显示程序版本并推出

`  -h, --help            `显示帮助信息并退出

`  -b, --lists           `列出所有支持的榜单名,并退出

`  -l 榜单名, --list=榜单名    `列出榜单歌曲

`  -s 关键词, --search=关键词  `搜索包含关键词的歌曲

`  -a, --downall         `search(-s)或list(-l)后下载全部歌曲.

`  -d "1,3-6", --down="1,3-6"` search(-s)或list(-l)后下载部分歌曲.后面跟歌曲序号(注意需要引号)

`  -B, --albumlists      `列出所有支持的专辑榜单名,并退出

`  -L 专辑列表名, --albumlist=专辑列表名` 列出专辑列表的歌曲

`  -S 关键词, --albumsearch=关键词` 搜索包含关键词的专辑

`  -A, --albumdownall    `albumsearch或albumlist后下载全部歌曲.

`  -D "1,3-6", --albumdown="1,3-6"` albumsearch(-S)或albumlist(-L)后下载部分专辑.后面跟专辑序
号(注意需要引号)