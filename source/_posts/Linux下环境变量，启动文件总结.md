title: Linux下环境变量，启动文件总结
date: 2015-06-22 11:53:59
tags: 
- linux
- 环境变量
categories: 
- 技术
---

#Linux环境变量与启动文件

最近在搭建hadoop yarn的环境，在配置环境变量的时候遇到一些问题，借这个机会系统的学习了一下Linux的环境变量配置以及作用，，总结如下以供备忘，主要参考了[《Linux命令行与Shell脚本大全》](http://book.douban.com/subject/11589828/)及部分网上文章。

##1.  首先明确环境变量的作用  
其实在不同系统中，环境变量总是扮演着相同的角色，每当安装完新环境，新软件，第一件事总是配置环境变量。
###环境变量 ： 
- 存储有关shell会话和`工作环境`的信息（如Java，hadoop，python等路径，主要是各个bin文件夹的绝对地址）
- 变量储存在`内存`中，方便程序以及脚本访问


##2.  进而我们谈谈环境变量的分类：

###局部变量：
- 特性：`作用于当前shell，`在子shell或者其它shell不可见（反映了局部变量的在当前进程可用的意义）  **见例1**
- 定义：
```bash 
        $  varname=abc       #局部变量名尽量使用小写; = 左右不要有空格，否则变量名会被解析为命令
```
- 显示： 
```bash
        $  echo $varname     #用$+变量名引用
```
- 删除：       
```bash
        $ unset varname   
```

###全局变量：
- 特性：作用于当前shell`及所有shell创建的子进程`; 系统登录时已经默认设置了许多全局环境变量。  **见例2**
- 定义：
```bash
        $  varname=abc 
        $  export varname    #先建立局部变量，用export导成全局变量
```
- 显示：
```bash
        $ printenv           #显示系统环境变量，系统环境变量一律大写  
        $ echo $varname      #显示单个变量
```

- 删除： 
```bash
        $ unset varname      #只对子进程中变量有效，父进程中的全局变量仍然存在。
```

##3.  提到系统默认定义的全局环境变量，我们举个例子
PATH变量是我们经常使用和修改的环境变量，它定义了`提供命令解析的搜索路径`。所以每当我们安装了新的环境，总要在更新PATH变量，这样就可以直接在任何位置使用命令，而不会出现commond not found的问题。 <br />　　其它系统变量的修改与添加也大致一样。
###PATH变量：  
- 特性： 命令行输入命令的搜索路径, 如：
```bash
    $ start-dfs.sh   #启动HDFS，而不用进入../hadoop2.5.2/sbin/目录下
```
- 查看： 
```bash
    $ echo $PATH
    /usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games    #不同值之间由:分割
```
- 添加值，修改：
```bash
    $ PATH=$PATH:/home/user/test  #添加目录/home/user/test, 只在当前shell有效
    $ export PATH=.:/HOME/eobin:$PATH     #单点符在PATH变量中代表当前路径，变量名可以放在末尾
```
通常我们把对于PATH变量的改动`写在系统或用户的启动文件中`，比如说~/.bashrc中，在登陆系统或者打开新shell时自动加载。

##4.  讲到启动文件，最后我们看看这几个启动文件是如何加载系统环境变量的：

###/etc/profile:    
- 作用：系统默认的`主启动文件`，每个用户登录时都会加载这个文件。
- 变量持续时间：声明的变量会在每个新shell中存在，除非在子进程中被修改

###$HOME/.bash_profile:  
- 作用：用户专属的启动文件， 定义用户专属的环境变量，该文件会`先检查并加载HOME目录中的.bashrc文件`（如果存在）



###$HOME/.bashrc:   
- 作用： `交互式shell的启动文件`，用于定制自己的明明别名和私有脚本函
- 这里有一点疑问，书中提到
>如果bash是作为交互式shell启动的，它不去访问/etc/profile, 而会去用户的HOME目录检查.bashrc是否存在  - p116 《Linux命令行与Shell脚本大全》

但/etc/profile是随系统登录时就启动的，任何`交互式shell`都是其子进程，所以我认为不用访问自然会加载其中变量，而此处特地指出，不明其所以然，也许没有理解交互式shell的意义。当然结果并没有什么不同，都会以.bashrc中的设置为准。


##5. 附例：

-例1   局部变量只在当前进程中有效
```bash
robin@esp:~$ varname=abc       定义变量varname
robin@esp:~$ echo $varname     显示，有值
abc
robin@esp:~$ bash              新建子进程
robin@esp:~$ echo $varname     显示，无值

robin@esp:~$ exit              退出子进程
exit
robin@esp:~$ echo $varname     显示，有值
abc
```

-例2   全局变量的作用范围
```bash
robin@esp:~$ echo $varname           显示变量，无值

robin@esp:~$ bash                    新建子进程2
robin@esp:~$ export varname=bash2    定义全局变量
robin@esp:~$ echo $varname           显示，有值
bash2
robin@esp:~$ bash                    新建子进程3
robin@esp:~$ echo $varname           显示，有值
bash2
robin@esp:~$ exit                    退出到bash2
exit
robin@esp:~$ exit                    退出到原始进程
exit
robin@esp:~$ echo $varname           显示，无值
```

###欢迎批评交流
##全剧终

Robin 
2015.6.22 夜
