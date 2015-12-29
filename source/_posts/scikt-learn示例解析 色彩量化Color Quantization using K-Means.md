title: scikt-learn示例解析 色彩量化Color Quantization using K-Means
date: 2015-10-21 20:04:03
tags: 
- scikt-learn
- 机器学习
- kmeans
categories: 
- 技术

---
翻译并解释了scikt-learn官网示例，留作备忘。
#Scikt-learn Example：Color Quantization using K-Means 
通过k-Means进行图像的色彩量化
url： http://scikit-learn.org/stable/auto_examples/cluster/plot_color_quantization.html
##简介
**色彩量化**是数据压缩的一个有效手段。这个示例提供了一个基于像素的色彩量化例子，将一副图片从96615个独立颜色降低到64色，大幅减小了图像大小，同时保留图片的基本外观。
示例通过聚类方法K-Means，从每一点的像素值中选取64个聚类中心，然后将所有点按照距离度量最接近的像素值分配，从而达到色彩量化的目的。在实际操作中，图像是以三维数组存储的（w，h，d），每一个RGB像素也需要一个长度为3的数组来表示（红绿蓝）。除此之外，示例使用了另一个方法random codebook，即随机挑选像素值作为聚类中心，然后再将所有像素分类，对比实验。
- 以下是示例的结果：我们可以发现，96615色降到64色后图片外观基本可以保持不变，而图3由于是随机生成的聚类中心，所以色彩有变化。
<table border="1" align="center"><span style="font-size:24px;color:#006600;"></span>  
<caption align="top">示例结果</caption>  
 <tr><td><img src="http://7xjz3b.com1.z0.glb.clouddn.com/plot_color_quantization_0011.png" width = "400" height = "300" alt="" align=center /></td>  <td></td>  </tr>  
<tr><td><img src="http://7xjz3b.com1.z0.glb.clouddn.com/plot_color_quantization_002.png" width = "400" height = "300" alt="" align=center /></td> <td><img src="http://7xjz3b.com1.z0.glb.clouddn.com/plot_color_quantization_003.png" width = "400" height = "300" alt="" align=center /></td>  </tr>  
</table>  

##代码分析
对源代码分段解释一下，其实英文文档的注释已经比较全面，只是有些细节需要补充。
```python
# Authors: Robert Layton <robertlayton@gmail.com>
#          Olivier Grisel <olivier.grisel@ensta.org>
#          Mathieu Blondel <mathieu@mblondel.org>
#
# License: BSD 3 clause

print(__doc__)
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
from sklearn.datasets import load_sample_image
from sklearn.utils import shuffle
from time import time
```
- 几个包的引用，对矩阵处理肯定需要numpy，然后最后绘图的步骤需要matplotlib，time包是用来统计每一步的执行时间的。
- 然后是引用scikt-learn相关组组件，KMeans是实现聚类的方法，pairwise_distances_argmin是一个计算相似度的方法，后面细说。load_sample_image是读取sklearn内置图片的方法，shuffle是一个随机排列数组的方法。

```python
n_colors = 64
# Load the Summer Palace photo
china = load_sample_image("china.jpg")
# Convert to floats instead of the default 8 bits integer coding. Dividing by
# 255 is important so that plt.imshow behaves works well on float data (need to
# be in the range [0-1]
china = np.array(china, dtype=np.float64) / 255
# Load Image and transform to a 2D numpy array.
w, h, d = original_shape = tuple(china.shape)
assert d == 3
image_array = np.reshape(china, (w * h, d))
print("Fitting model on a small sub-sample of the data")
t0 = time()
image_array_sample = shuffle(image_array, random_state=0)[:1000]
kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)
print("done in %0.3fs." % (time() - t0))
# Get labels for all points
print("Predicting color indices on the full image (k-means)")
t0 = time()
labels = kmeans.predict(image_array)
print("done in %0.3fs." % (time() - t0))
```
英文注释已经比较详细了，这里只补充一下要点。
- 原始图像读出的三维数组是int8类型的，红绿蓝各为0-255，这里用numpy转成了float64类型并/255是为了后面plt画图包的显示。
- 中间reshape了一下原始数组，从3维转成2维，是为了方便后面的聚类和分类，实际像素的排列是没有变化的。
- 这里让K-means模型学习的数据并不是原始图像，而是从原始图像**随机选取**了1000个像素的颜色值，这里就用到刚才提到的shuffle方法，具体功能可以点[源码](http://scikit-learn.org/stable/modules/generated/sklearn.utils.shuffle.html#sklearn.utils.shuffle)，这样可以大大减少计算时间，并得到几乎一样的结果。
- 然后就是根据聚类中心对原始图像每一个像素分类，用所属聚类中心的颜色代替。**有一点注意**，K-means方法在预测时，由于要计算欧式距离，sklearn的实现十分消耗内存，对于大一点的图像就会出现MemoryError的问题，解决方法可以用类似的MiniBatchKmeans方法代替K-Means。

```python
codebook_random = shuffle(image_array, random_state=0)[:n_colors + 1]
print("Predicting color indices on the full image (random)")
t0 = time()
labels_random = pairwise_distances_argmin(codebook_random,image_array,axis=0)
print("done in %0.3fs." % (time() - t0))
```
这里实现的是random-codebook对比方法。
- 这里codebook-random的作用相当于K-means模型中生成的聚类中心，只不过这里时完全随机罢了。
- 然后后面用到了pairwise_distances_argmin方法，作用相当于上面means.predict(image_array)，就是将原始图像每一个像素的颜色归属到距离大最近的codebook中的颜色。具体功能可以看[源码](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances_argmin.html#sklearn.metrics.pairwise_distances_argmin).

```python
def recreate_image(codebook, labels, w, h):
    """Recreate the (compressed) image from the code book & labels"""
    d = codebook.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = codebook[labels[label_idx]]
            label_idx += 1
    return image
```
这里实现了一个画图方法。返回的是一个三维数组，然后通过后面的matplotlib包实现画图。
- 具体很简单，就是用numpy生成一个原始图像大小的0矩阵，然后按照每个聚类中心的颜色codebook，和原始图像每一个像素点归属的聚类中心labels，重新生成描述图像的三维数组。
- 这里完成了2D到3D的转变，也就是从分类标签到图像数组的转换，又回到了原始的三维数组。

```python
# Display all results, alongside original image
plt.figure(1)
plt.clf()
ax = plt.axes([0, 0, 1, 1])
plt.axis('off')
plt.title('Original image (96,615 colors)')
plt.imshow(china)

plt.figure(2)
plt.clf()
ax = plt.axes([0, 0, 1, 1])
plt.axis('off')
plt.title('Quantized image (64 colors, K-Means)')
plt.imshow(recreate_image(kmeans.cluster_centers_, labels, w, h))

plt.figure(3)
plt.clf()
ax = plt.axes([0, 0, 1, 1])
plt.axis('off')
plt.title('Quantized image (64 colors, Random)')
plt.imshow(recreate_image(codebook_random, labels_random, w, h))
plt.show()
```
最后就是通过matpolt画出原始图和两张处理后的图，都是基本方法，可以自己了解matplotlib包，不再详细记录。

###End

-Robin 
2015.10.21 夜
<!--end-->