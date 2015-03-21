## douban-python 安装 ##
使用源码包安装

a). 安装gdata.py。下载gdata.py压缩包，然后按照如下方法安装
```
sudo python setup.py install
```

or

```
python setup.py install --home=~
```
and set your PYTHONPATH to include your home directory.

b). 下载 douban-python源码包并解压

c). 按照如下命令安装douban-python
```
sudo python setup.py install
```

**注**：如果你使用的是subversion >=1.5的版本取得的代码,采用setuptools-0.6-rc8,那么你会遇到一个setuptools的bug导致安装无法完成。此时，如果你使用的是gentoo linux,可以emerge setuptools-0.6\_rc8-[r1](https://code.google.com/p/douban-python/source/detail?r=1);或者，你可以给setuptools打上这个patch:
```
　　Index: setuptools/command/egg_info.py
　　===================================================================
　　--- setuptools/command/egg_info.py (revision 61076)
　　+++ setuptools/command/egg_info.py (working copy)
　　@@ -217,9 +217,9 @@
　　 data = f.read()
　　 f.close()
　　
　　- if data.startswith('8'):
　　+ if data.startswith('8') or data.startswith('9'):
　　 data = map(str.splitlines,data.split('\n\x0c\n'))
　　- del data[0][0] # get rid of the '8'
　　+ del data[0][0] # get rid of the '8' or '9'
　　 dirurl = data[0][3]
　　 localrev = max([int(d[9]) for d in data if len(d)>9 and d[9]]+[0])
　　 elif data.startswith('<?xml'):
　　Index: setuptools/command/sdist.py
　　===================================================================
　　--- setuptools/command/sdist.py (revision 61076)
　　+++ setuptools/command/sdist.py (working copy)
　　@@ -86,7 +86,7 @@
　　 f = open(filename,'rU')
　　 data = f.read()
　　 f.close()
　　- if data.startswith('8'): # subversion 1.4
　　+ if data.startswith('8') or data.startswith('9'): # subversion 1.4 or 1.5
　　 for record in map(str.splitlines, data.split('\n\x0c\n')[1:]):
　　 if not record or len(record)>=6 and record[5]=="delete":
　　 continue # skip deleted
```