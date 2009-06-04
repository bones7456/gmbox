#!/usr/bin/env python
# -*- coding: utf-8 -*-

# gmbox, Google music box.
# Copyright (C) 2009, gmbox team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, sys, copy, time, re, logging, urllib, urllib2

from parser import *
from const import *
from utils import unistr,sizeread
#import config

log = logging.getLogger('lib.core')

# this variable should read from preference
userhome = os.path.expanduser('~')
musicdir=os.path.join(userhome,'Music','google_music','top100')

class Gmbox:
    '''核心模块,初始化完成以后,成为一个全局变量.
    功能包括:获取榜单,搜索歌曲,并维护一个当前列表,
    并且可以下载当前列表中的部分或全部歌曲,并集成缓存.'''
    
    def __init__(self):
        '''初始化一个空的gmbox对象'''
        self.songlist = {}
        self.cached_list={}

    def __str__(self):
        '''print对象的时候调用,由于win下可能会中文乱码,建议使用 listall 方法代替'''
        return '\n'.join(['Title="%s" Artist="%s" ID="%s"'%
            (song['title'],song['artist'],song['id']) for song in self.songlist])

    def listall(self):
        '''打印当前列表信息'''
        print '\n'.join(['Num=%d Title="%s" Artist="%s" ID="%s"'%
            (self.songlist.index(song)+1,song['title'],song['artist'],song['id']) 
            for song in self.songlist])

    def get_filename(self,i=0):
        '''生成当前列表的第i首歌曲的文件名'''
        song=self.songlist[i]
        filename=song['title']+'-'+song['artist']+'.mp3'
        return filename

    """以下函数未支持
    def get_title(self,i=0):
        song=self.songlist[i]
        return song['title']

    def get_artist(self,i=0):
        song=self.songlist[i]
        return song['artist']

    def get_id(self,i=0):
        song=self.songlist[i]
        return song['id']

    def down_lyrics(self,i=0):
        lyrics_uri_template='http://g.top100.cn/7872775/html/lyrics.html?id=%s'
        p=LyricsParser()
        print u'正在获取"'+key+u'"的歌词',
        print search_uri_template%key
        html=urllib2.urlopen(search_uri_template%key).read()
        #print html
        p.feed(re.sub(r'&#([0-9]{2,5});',unistr,html))
        self.songlist=p.songlist
        print 'done!'"""
        
    def get_url_html(self,url):
        '''获取指定url的html'''
        try:
            html = urllib2.urlopen(url).read()
        except urllib2.URLError:
            print '网络错误,请检查网络...'
            return
        except:
            print '未知错误!请到这里报告bug: http://code.google.com/p/gmbox/issues/entry'
            return
        return html
        
    def find_final_uri(self,i=0):
        '''找到最终真实下载地址，以供下一步DownLoad类下载'''
        song=self.songlist[i]
        songurl=song_url_template % (song['id'],)
        html=self.get_url_html(songurl)

        s=SongParser()
        s.feed(html)
        return s.url

    def downone(self,i=0,callback=None):
        '''下载榜单中的一首歌曲 '''
        filename = self.get_filename(i)
        localuri = os.path.join(musicdir,filename)
        
        if os.path.exists(localuri):
            print filename,u'已存在!'
            return
        
        url = self.find_final_uri(i)
        if url:
            self.download(url,filename,1,callback=callback)
        else:   #下载页有验证码时url为空
            print '出错了,也许是google加了验证码,请换IP后再试或等24小时后再试...'

    def downall(self):
        '''下载榜单中的所有歌曲'''
        [self.downone(i) for i in range(len(self.songlist))]

    def down_listed(self,songids=[],callback=None):
        '''下载榜单的特定几首歌曲,传入序号的列表指定要下载的歌'''
        [self.downone(i,callback) for i in songids if i in range(len(self.songlist))]
            
    
    def download(self, remote_uri, filename, mode=1, callback=None):
        '''下载模式 1 和 试听(缓存)模式 0'''
        #这里不用检测是否文件已存在了,上边的downone或play已检测了
        if mode:
            print u'正在下载:',filename
        else:
            print u'正在缓冲:',filename
        local_uri=os.path.join(musicdir,filename)
        cache_uri=local_uri+'.downloading'
        self.T=self.startT=time.time()
        (self.D,self.speed)=(0,0)
        c=callback if callback else self.update_progress
        c(-1,filename,0) #-1做为开始信号
        urllib.urlretrieve(remote_uri, cache_uri, c)
        c(-2,filename,0) #-2做为结束信号
        speed=os.stat(cache_uri).st_size/(time.time()-self.startT)
        #下载和试听模式都一样
        if callback==None:
            print '\r['+''.join(['=' for i in range(50)])+ \
                '] 100.00%%  %s/s       '%sizeread(speed)
        os.rename(cache_uri, local_uri)
        if os.name=='posix':
            '''在Linux下转换到UTF 编码，现在只有comment里还是乱码'''
            os.system('mid3iconv -e gbk "'+local_uri + '"')

    def update_progress(self, blocks, block_size, total_size):
        '''默认的进度显示的回调函数'''
        if total_size > 0 and blocks >= 0:
            percentage = float(blocks) / (total_size/block_size+1) * 100
            if int(time.time()) != int(self.T):
                self.speed=(blocks*block_size-self.D)/(time.time()-self.T)
                (self.D,self.T)=(blocks*block_size,time.time())
            print '\r['+''.join(['=' for i in range((int)(percentage/2))])+'>'+ \
                ''.join([' ' for i in range((int)(50-percentage/2))])+ \
                (']  %0.2f%%  %s/s    ' % (percentage,sizeread(self.speed))),

    def get_list(self,stype):
        '''获取特定榜单'''
        if stype in self.cached_list:
            self.songlist=copy.copy(self.cached_list[stype])
            return
        
        if stype in songlists:
            p=ListParser()
            print u'正在获取"'+stype+u'"的歌曲列表',
            sys.stdout.flush()
            for i in range(0, songlists[stype][1], 25):
                html=self.get_url_html(list_url_template%(songlists[stype][0],i))
                p.feed(re.sub(r'&#([0-9]{2,5});',unistr,html))
                print '.',
                sys.stdout.flush()
            print 'done!'
            self.songlist = p.songlist
            self.cached_list[stype]=copy.copy(p.songlist)
        else:
            #raise Exception
            print u'未知列表:"'+str(stype)+u'",仅支持以下列表: '+u'、'.join(
            ['"%s"'%key for key in songlists])
            log.debug('Unknow list:"'+str(stype))

    def search(self,key):
        '''搜索关键字'''
        if 's_'+key in self.cached_list:
            self.songlist=copy.copy(self.cached_list['s_'+key])
            return

        key = re.sub((r'\ '),'+',key)
        p=ListParser()
        print u'正在获取"'+key+u'"的搜索结果列表...',
        sys.stdout.flush()
        html=self.get_url_html(search_uri_template%key)
        p.feed(re.sub(r'&#([0-9]{2,5});',unistr,html))
        print 'done!'
        self.songlist=p.songlist
        self.cached_list['s_'+key]=copy.copy(p.songlist)
        
#全局实例化
gmbox=Gmbox()
