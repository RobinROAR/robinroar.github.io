title: 理解Linux的环境变量、启动文件和命令目录
date: 2015-06-22 11:53:59
tags: 
- linux
- 环境变量
categories: 
- 技术
---


在搭建hadoop 的环境 时配置环境变量的时候遇到些问题，于是系统总结了Linux中的环境变量、启动文件等相关知识发,以供备忘。

##1.  环境变量的作用  
在不同系统中，环境变量总是扮演着相同的角色，安装完新环境，新软件，第一件事总是配置环境变量。
###环境变量 ： 
- 存储有关shell会话和`工作环境`的信息（如Java，hadoop，python等路径，主要是各个bin文件夹的绝对地址）
- 变量储存在`内存`中，方便程序以及脚本访问


##2.  环境变量的分类：

###局部变量：
- 特性：`作用于当前shell，`在子shell或者其它shell不可见（反映了局部变量的在当前进程可用的意义）  **见例1**
- 定义：
```bash 
        $  varname=abc       #局部变量名尽量使用小写; = 左右不要有空格，否则变量名会被解析为命令
```
- 显示： 
```bash
        $  echo $varname     #echo命令要使用$变量名
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
        $ printenv                 #显示系统环境变量，系统环境变量一律大写  
        $ echo $varname      #显示单个变量
```

- 删除： 
```bash
        $ unset varname      #只对子进程中变量有效，父进程中的全局变量仍然存在。
```

##3.  系统默认定义的全局环境变量
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
- **添加值，修改**：
```bash
    $  PATH=$PATH:/home/user/test  #添加目录/home/user/test, 只在当前shell有效
    $  export PATH=.:/HOME/eobin:$PATH     #单点符在PATH变量中代表当前路径，变量名可以放在末尾
```
通常我们把对于PATH变量的改动`写在系统或用户的启动文件中`，比如说~/.bashrc中，在登陆系统或者打开新shell时自动加载。

##4. 启动文件与系统环境变量的加载：

###/etc/profile:    
- 作用：系统默认的`主启动文件`，每个用户登录时都会加载这个文件。
- 变量持续时间：声明的变量会在每个新shell中存在，除非在子进程中被修改

###$HOME/.bash_profile:  
- 作用：用户专属的启动文件， 定义用户专属的环境变量，该文件会`先检查并加载HOME目录中的.bashrc文件`（如果存在）



###$HOME/.bashrc:   
- 作用： `交互式shell的启动文件`，用于定制自己的命名别名和私有脚本
- 这里有一点疑问，书中提到
>如果bash是作为交互式shell启动的，它不去访问/etc/profile, 而会去用户的HOME目录检查.bashrc是否存在  - p116 《Linux命令行与Shell脚本大全》

但/etc/profile是随系统登录时就启动的，任何`交互式shell`都是其子进程，所以我认为不用访问自然会加载其中变量，而此处特地指出，不明其所以然，也许没有理解交互式shell的意义。当然结果并没有什么不同，都会以.bashrc中的设置为准。

### 一般来说Linux启动加载配置文件顺序如下：/etc/profile → /etc/profile.d/*.sh → ~/.bash_profile → ~/.bashrc → [/etc/bashrc]

##5. 附例：

- **例1**   局部变量只在当前进程中有效
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

- **例2**   全局变量的作用范围
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

##几个命令目录详解：/bin,/sbin,/usr/sbin,/usr/bin 
经过对环境变量的了解，我们发现上述四个目录经常被写在环境变量中。这些目录的作用，是存放各种'存放命令'。
###/sbin：
从名字来解释，bin是binary的所写，而s可以理解为super的所写。所以/sbin目录主要用于存放一些超级用户指令，同时，也必须要求用用有root权限才能使用。
这些命令主要有：:cfdisk、dhcpcd、dump、e2fsck、fdisk、halt、ifconfig、ifup、 ifdown、init、insmod、lilo、lsmod、mke2fs、modprobe、quotacheck、reboot、rmmod、 runlevel、shutdown等。
###/bin：
与上面相同，/bin目录中也是系统命令，是一些较为普通的基本指令，一般来说管理员和普通用户都可以使用/bin目录下的命令。
主要包括cat、cp、chmod df、dmesg、gzip、kill、ls、mkdir、more、mount、rm、su、tar等。
###/usr/sbin:
该目录主要存放一些用户自主安装的系统管理程序。
包括dhcpd、httpd、imap、in.*d、inetd、lpd、named、netconfig、nmbd、samba、sendmail、squid、swap、tcpd、tcpdump等。
###/usr/bin：
这个目录的内容就比较广泛，基本包括了用户安装的各种软件运行脚本以及执行命令。
如c++、g++、gcc、chdrv、diff、dig、du、eject、elm、free、gnome*、gzip、htpasswd、kfm、ktop、last、less、locale、m4、make、man、mcopy、ncftp、 newaliases、nslookup passwd、quota、smb*、wget等。
###Tips：
- 如果命令调用不到，就要考虑以上四个目录是否在你的PATH变量中.比如说，查看得知：PATH=$PATH:$HOME/bin。那么，我们则需如下改动：    PATH=$PATH:$HOME/bin:/sbin:/usr/bin:/usr/sbin
- 善于创建链接：ln命令：
比如我们安装包Node.js,由于各种原因，安装后/usr/bin中默认的调用命令是nodejs,而其他第三方包写在脚本中的调用方法是node，这时有两个解决方法：
	1. 使用alias命令：建立 alias node=nodejs   这种方法可以解决bash中输入命令的问题，但却在一些第三方包安装过程无效。
	2. 使用ln命令建立软链接： ln -s /usr/bin/nodejs /usr/bin/node  软链接可以完美解决第三方包安装的问题，具体使用可查询ln命令。 


##END

Robin 
2015.6.22 夜
