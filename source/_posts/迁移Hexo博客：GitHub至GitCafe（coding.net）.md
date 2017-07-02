title: 迁移Hexo博客：GitHub至GitCafe(coding.net)
date: 2015-11-10 20:23:39
tags: 
- hexo
- GitPages
- GitCafe/coding.net
- 博客迁移
categories: 
- 技术
---
昨天着手将博客从GitHub迁移到GitCafe，心里长草多时终于付诸行动。整体过程还算顺利，迁移后功能基本正常，但中间遇到几点零碎问题，现记录如此，一供自己备忘，二可以帮助遇到同样困难的朋友。
**20160317新增部署到coding.net (GitCafe被吃啦，5月1号停止服务，好残酷zZZ)**
##引子
这里主要谈谈迁移博客的原因，主要来自如下几点：
- 搜索引擎检索：无法被百度检索是在Gitpages上部署博客最主要的问题，主要原因是Github服务器默认屏蔽了百度的爬虫。网上的几种解决方案并不触及本质，效果有限。
- 访问速度：国内地址访问Github的速度还是不够完美
- 屏蔽隐患：因为GFW有过暂时屏蔽Github的不良记录，所以博客被屏蔽的隐患始终存在。

而相比较来说GitCafe因为是在国内的实现，这些问题基本都没有，而且两者本是同根生，迁移起来技术成本很小。但因为GitHub的影响力和作用也不想放弃，所以确定了迁移博客到GitCafe，同时两边同步更新的策略。

##主要步骤
共有如下几个关键点：
### 项目迁移:
需要在Gitcafe上生成一个相同的项目。GitCafe与GitHub本地环境相同，完全可以使用一套git软件，只是在远程项目配置上稍有不同。我们需要做的：
- 注册GitCafe帐号，新建一个**与帐号同名的任务**，这样GitCafe会默认该项目为page项目。*(注意名称区分大小写，GitCafe的特点)*
- 将本地博客项目push到Gitcafe项目下的gitcafe-pages分支：
   - 进入hexo博客的默认部署目录 username.io/.deploy_git
   - 添加新的远程仓库：
   ```bash
      $ git remote add gitcafe git@gitcafe.com:Username/Username.git
   ```
   *(add后用最好gitcafe而不是origin，否则与原来Github的远程仓库地址冲突；Username注意大小写)*
   - push到GitCafe项目下的gitcafe-pages分支：
   ```bash
      $ git checkout gitcafe-pages
      $ git push -u gitcafe gitcafe-pages
   ```
   *(注意push完再切换回master分支，因为hexo默认的部署文件我们都已master分支为主)*

### 同步更新
已完成迁移工作，下面需要配置同步更新Github和GitCafe的功能。我选择的修改hexo的配置文件，通过hexo命令完成同步更新的方法，很简单，感觉比再写一个同步更新脚本更舒服些。
我们只需要修改一下根目录下hexo的配置文件_config.yml：
```xml
deploy:
  type: git
  repo: 
    github: git@github.com:robinroar/robinroar.github.io,master
    gitcafe: git@gitcafe.com:RobinROAR/RobinROAR.git,gitcafe-pages
```
*（可以看出一个是推送到GitHub项目的master分支，一个是推送到GitCafe项目的gitcafepages分支，省略了本地的默认分支master）*
这样就可以用老方法**hexo d**同步更新两个项目.

### 绑定域名
最后需要绑定域名，这里注意几点：
- 在服务商添加域名解析时不要使用A记录的方式了，因为网上原来的GitCafe服务器的Ip地址由于DOS攻击已经暂时在2015.5前后关闭，官网提供的解决方案是改用CNAME记录，指向Username.gitcafe.io即可。
- 原来在博客文件目录中的CNAME文件需要移除，因为现在是一个项目两处同时更新，两处的CNAME文件指向同一个域名，好像会有点问题。解决方法很简单，只需要把CNAME文件移出根目录下的source目录即可，下此部署时该文件就不会部署到服务器了。

*（但博客目录中的CNAME文件的作用我还有点疑惑，是将原本到username.github.io的访问导到CNAME中的地址？这样是否会引起循环？如有赐教不胜感激）*

##重要Tips
- GitCafe区分大小写，包括url的地址，项目的名称等
- Hexo通过配置文件进行push/pull操作的博客目录是的username.io/.deploy_git/
- GitCafe下使用的分支是gitcafe-pages


###End

### 20160317迁移到coding.net

GitCafe已经没法push了，5.1日前所有内容都将迁移到coding.net。国内竞争激烈，产业的存活期不稳定，也算是使用国内服务的弊端之一吧。

转移到Coding.net的步骤和上面基本一致，值得注意的几点：
- coding.net的pages服务需要创建的pages分支名叫coding-pages。
- 虽说系统自动把项目迁移从GitCafe迁移过来，但还是要自己绑定公钥。

希望这家公司靠谱点，能多撑一段时间:)

-Robin 
2015.11.10 
2016.March 17, 2016 7:33 PM  迁移到coding.net