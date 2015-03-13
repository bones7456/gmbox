# 简介 #

现在gmbox由两部分组成：核心库（libgmbox）和gtk前端（gmbox-gtk），两部分版本号独立的，libgmbox只使用纯python标准库。

欢迎有闲人士开发其它gui前端（qt/wxwidget等），或者播放器插件。

# 安装 #

libgmbox的目录已做成标准的python包，你可以从svn仓库中检出

```
svn co https://gmbox.googlecode.com/svn/trunk/libgmbox libgmbox
```

你可以使用 easy\_install 命令，安装到系统中

```
cd libgmbox
sudo easy_install .
```

如果你不想安装到系统中，只需要把 “libgmbox/libgmbox”目录放到你的项目下即可。

如果你是一个打包党，你可以为这个库打一个包，推荐包名“python-libgmbox”。

# 使用 #

## 读取歌曲 ##

假设你已经安装了libgmbox了，那么可以进入python shell，执行

```
>>> from libgmbox import Song
>>> song = Song("Sb1ee641ab6133e1a")
>>> print song.name, song.artist, song.album
海阔天空 Beyond 25周年精选 CD3
```

这样就能获得一首歌的信息了。

## 获得试听和歌词地址 ##

```
>>> song.load_streaming()
>>> print song.songUrl
http://audio2.top100.cn/201107161706/2CB66EF6515C572C35E9C4CD4AB87171/streaming1/Special_99073/M0099073007.mp3
>>> print song.lyricsUrl
http://lyric.top100.cn/Special_99073/M0099073007.lrc
```

“load\_streaming()”函数是必须的，调用后才会song实例有“songUrl”和“lyricsUrl“这两个属性。这个函数会再进行一次http请求，出于效率，应该在有需要的时候才调用，如果第二次调用，不会再发出http请求。

## 获得下载地址 ##

```
>>> song.load_download()
>>> song.downloadUrl
'http://www.google.cn/music/top100/url?q=http://file4.top100.cn/201107161712/F7B3497A90786CCDAB1F9D8F4E2286AE/Special_99073/%25E6%25B5%25B7%25E9%2598%2594%25E5%25A4%25A9%25E7%25A9%25BA.mp3&ct=rdl&cad=dl&ei=4lUhTuizG8-CkgX8wrnsAw&sig=CC71EE72E0A7D3BE33F239F225A42D49'
```

“load\_download()”的作用类似上面的“load\_streaming()”,注意，短时间内连续请求会遭服务器封禁，目前还不支持处理验证码。

## 调试输出所有信息 ##

如果你调试一首歌的所有可读取属性，可以使用“print\_song”这个工具函数

```
>>> from libgmbox import print_song
>>> print_song(song)
album: 25周年精选 CD3
albumId: Bbefeb834db932f82
albumThumbnailLink: http://lh4.googleusercontent.com/public/VX-Q8Sg2cIyv1A4c6kadPqZB8OsTOUeukLqLyL_EUZPhPuD8cKn5m9fuhuE9WEyQjMX1HfmDR65cFtM_ik6844802RakdfR7YYQRyXNBEQbXRN_fxtynCZlzcwMjVbYgdvg
artist: Beyond
artistId: A887b2d5bdd631594
canBeDownloaded: true
canBeStreamed: true
duration: 322.0
genre: pop
hasFullLyrics: true
hasRecommendation: false
hasSimilarSongs: true
id: Sb1ee641ab6133e1a
label: 新艺宝唱片公司(环球唱片)
labelHash: 71a06868016526c49bb0697ada4d7d3e
language: zh-yue
lyricsUrl: http://lyric.top100.cn/Special_99073/M0099073007.lrc
name: 海阔天空
providerId: M0099073007
songUrl: http://audio2.top100.cn/201107161701/D48855B9C2CAAC4E66958D50D5B078B7/streaming1/Special_99073/M0099073007.mp3
```

## 基本类 ##

Song类是表示歌曲，而Song的集合则是Songlist类，而Songlist类的集合则是Directory。

Songlist只是个基类，如果要使用，则通过子类处理，Directory同理。

## 专辑 ##

Songlist的一个子类是专辑Album。

```
>>> from libgmbox import Album
>>> album = Album("B5f03f5ad567ecbec")
>>> print_song(album.songs[0])
```

album.songs是一个list对象，保存了该专辑的Song实例。每一个Songlist类子类都有这个属性。 类似、搜索歌曲、热歌排行、新歌排行、相似歌曲等等，这些结果都是Song的集合，它们都是Songlist的子类。

类似“print\_song()”，输出一个Songlist子类信息可用“print\_songlist()”。

```
>>> from libgmbox import print_songlist
>>> print_songlist(album)
```

## 搜索专辑 ##

Directory的一个子类是搜索专辑DirSearch，

```
>>> from libgmbox import DirSearch
>>> dir_search = DirSearch("海阔天空")
>>> len(dir_search.songlists)
16
>>> first_songlist = dir_search.songlists[0]
>>> len(first_songlist.songs)
0
>>> first_songlist.load_songs()
>>> len(first_songlist.songs)
10
>>> print_song(first_songlist.songs[0])
```

dir\_search.songlists是一个list对象，保存了该专辑的Songlist实例。但是注意，刚取出的Songlist对象里的songs属性是没有Song实例的，这是避免一下子发出很多http请求来获取Songlist的歌曲信息，当你需要时才调用一次“load\_songs()”即可。

同理，输出一个Directory子类信息可用“print\_directory()”，这会一下子发出很多http请求。

```
>>> from libgmbox import print_directory
>>> print_directory(dir_search)
```

## 翻页 ##

有些Songlist子类可以实行翻页，比如歌曲搜索Search

```
>>> from libgmbox import Search
>>> search = Search('beyond')
>>> len(search.songs)
20
>>> search.load_songs(21, 20)
>>> len(search.songs)
40
```

search.songs原本只有20首，调用了“load\_songs(21, 20)”，表示从21首开始，20个结果，之后便变成了40首。

Directory子类同理。

# 下一步 #

Songlist和Directory的已实现子类及其参数请阅读[源代码](https://code.google.com/p/gmbox/source/browse/#svn%2Ftrunk%2Flibgmbox%2Flibgmbox)，已经添加了大量的注释，我已经懒得又写一遍了。

建议阅读顺序

  * test.py 一个测试示例文件
  * utility.py 工具函数文件
  * const.py 常量文件
  * core.py 解析核心文件