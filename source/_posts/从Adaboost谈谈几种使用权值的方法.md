title: 从AdaBoost谈谈基于权值的投票方法
date: 2015-12-29 15:51:34
tags:
- AdaBoost
- 分类
- 机器学习
categories: 
- 理论
mathjax: true 
---
这周计算机视觉课在讲运动分析时重温了AdaBoost方法，感觉比之前的理解又深入了些，在这里谈谈体会。
##AdaBoost
###Boosting思想
通过融合多个弱分类器，用加权投票的方式构建一个准确率更高的强分类器。
- 弱分类器：准确率大于0.5,即仅比随机猜测略好
- 强分类器：准确率高，并能在多项式时间（计算时间$m(n)=O(n^k)$,k为常数）内解决问题。

###理论依据
- [A general lower bound on the number of examples needed for learning[J]. Information and Computation, 1989](http://www.sciencedirect.com/science/article/pii/0890540189900023)
M Kearns and L Valiant数学上证明了Boosting弱方法强化思想
- [ Experiments with a new boosting algorithm[C]//ICML. 1996](http://www.public.asu.edu/~jye02/CLASSES/Fall-2005/PAPERS/boosting-icml.pdf)
Freund and Schapire 提出AdaBoost方法
- [Viola P, Jones M. Rapid object detection using a boosted cascade of simple features[C]//Computer Vision and Pattern Recognition, 2001. CVPR 2001](http://www.merl.com/papers/docs/tr2004-043.pdf)
Viola and Jones  在人脸检测中应用Adaboost，引起轰动

###核心
1. 对**样本加权**：每个样本赋予权重，某次迭代中没有被正确分类的样本权重提高
2. 对**每个弱分类器加权**：若某一分类准确率高，其权重也越高。
3. 根据规则迭代，直到收敛。

###算法
假设输入m个样本$(x_1,y_1),...,(x_m,y_m),其中x_i\in{X}, y_i=\{1,-1\}$
####算法
1. 初始化样本权重： $D_1(i)=\frac{1}{m}$
2. 开始循环：For $t$=1 to T:
	1. 训练一个弱分类器
	2. 循环判断。如果得出的弱分类器分类误差 /<1/2或 准确率 = 1,中止循环
	3. 计算分类器权重
	4. 更新样本权重
3. 构建基本分类器的线性组合，得到最终的强分类器。

####重点
#####1. 训练（挑选）弱分类器
#####2. 计算分类器权重
#####3. 更新样本权重
####总结：
1. 每次迭代是在当前样本下训练一个新的分类器，这些分类器**是由一种分类模型根据加权的样本数据学习出的结果**，是独立且固定的，并计算出一个固定的分类器权重，不会随着过程而更改。
2. 每次迭代后样本的权重也会有变化，并重归一化到0-1区间，同时所有样本权重加和值为1。

##谈谈其它基于权值的投票方法
在上课的过程中想到，这种Adaboost的提升方法朝向似曾相识，和前面背景提取时构建的混合高斯模型，以及神经网络等都有相似之处，这里简单比较一下。


##未写完
