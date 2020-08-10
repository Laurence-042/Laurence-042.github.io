---
title: PCA主成分分析降维的理解
tags:
- 机器学习
- 个人笔记
---

### 西瓜书的说明

数据$x_i$原始维度为d（d\*1的矩阵），需要使其降维到d'维的$z_i$。如果当一系列样本点$X=(x_1,x_2,...,x_m)$（显然$X$为一个d*m的矩阵）距离要降维到的超平面足够近（符合降维需求），并使X中每个样本降维后足够分散（否则降维就没有什么意义了）。为了方便讨论，不妨使$X$已中心化，即$\sum_ix_i=0$。

所以我们需要找到一个合适的d*d的变换矩阵$W=(w_1,w_2,...,w_d)$对样本点进行坐标系变换，使其映射到d维空间（同等维度），$w_i$为标准正交基向量，即$w_i^Tw_i=1$（显然$W^TW=I_d$）且当$i\neq j$时$w_i^Tw_j=0$。将$x_i$被变换到这个新坐标系后得到一个在新的坐标系下的的d维数据$y_i=(y_{i1};y_{i2};...;y_{id})$，$y_{ij}=w_j^Tx_i$，$y_i=W^Tx_i$。

若丢弃$y_i$其中的一些维度。可以得到$z_i=(z_{i1};z_{i2};...;z_{id‘})$，$z_i=W^Tx_i$**（此处的$W=(w_1,w_2,...,w_d')$是上面的d\*d矩阵$W$去除相应维度得到的d\*d'矩阵，之后的$W$以d\*d'维度的为准）**，$d'<d$，则基于投影重构的n维新样本点为$\hat{x_i}=\sum_{j=1}^{d'}z_{ij}w_j=Wz_i$。

### 或者可以更简练地说

找到一个合适的d*d'的变换矩阵$W=(w_1,w_2,...,w_{d'})$对样本点进行降维映射（或者说投影），使原始维度为d的数据$x_i$映射为d'维的$z_i$。和上面一样，也可以得到

$$
w_i^Tw_i=1\\
W^TW=I_{d'}\\
w_i^Tw_j=0,i\neq j\\
z_i=W^Tx_i\\
\hat{x_i}=\sum_{j=1}^{d'}z_{ij}w_j=Wz_i
$$

### 举个降维投影的例子

举个从二维空间投影到一维空间的例子。比如有个代表$(0,1)$的2*1的二维列向量
$$
x=\left[ \begin{array}{cc}
0\\
1
\end{array} 
\right ]
$$
要将它投影到一个在二维的超平面（也就是一条直线）上成为一个一维数据。假设超平面的向量为$(\frac{\sqrt 3}{2},\frac{1}{2})$，也就是一个与x轴正方向成$30^\circ$的直线，那么投影矩阵即为超平面的列向量表示
$$
W=\left[ \begin{array}{cc}
\frac{\sqrt 3}{2}\\
\frac{1}{2}
\end{array} 
\right ]
$$
投影后得到的一维向量为
$$
z=W^Tx=\left[ \begin{array}{cc}
\frac{\sqrt 3}{2}, \frac{1}{2}
\end{array} 
\right ]
\left[ \begin{array}{cc}
0\\
1
\end{array} 
\right ]
=[\frac{1}{2}]
$$
映射回二维空间
$$
\hat{x}=Wz=
\left[ \begin{array}{cc}
\frac{\sqrt 3}{2}\\
\frac{1}{2}
\end{array} 
\right ]
[\frac{1}{2}]
=
\left[ \begin{array}{cc}
\frac{\sqrt 3}{4}\\
\frac{1}{4}
\end{array} 
\right ]
$$
直观上可以理解为，通过$(0,1)$（也就是$x$)向一个途径$(0,0)$与$(\frac{\sqrt 3}{2},\frac{1}{2})$（也就是$W$）的直线做垂线，从$(0,0)$到垂足的距离为$\frac{1}{2}$（也就是$z$），垂足坐标为$(\frac{\sqrt 3}{4},\frac{1}{4})$（也就是$\hat{x}$）

### 开始推导

由于样本点距离要降维到的超平面足够近，也就是说原样本点$x_i$和重构后的样本点$\hat{x_i}$之间的距离应尽可能小。换句话说，也就是要最小化所有样本的总距离差$\sum_{i=1}^{m}||\hat{x_i}-x_i||_2$，即最小化$\sum_{i=1}^{m}\left\|WW^Tx_i-x_i\right\|_2$，即最小化
$$
\sum_{i=1}^{m}\left\|\sum_{j=1}^{d'}z_{ij}w_j-x_i\right\|_2
$$

推导部分由于忘记了大量包括但不限于如何处理转置的矩阵乘法展开之类的线代知识，只能看着[南瓜书上对10.14式的推导](https://datawhalechina.github.io/pumpkin-book/#/chapter10/chapter10?id=_1014)一边惊叹一边无地自容……总之可推出上式等于
$$
-\sum_{i=1}^{m}z_i^Tz_i+\sum_{i=1}^{m}x_i^Tx_i
$$
其中$\sum_{i=1}^{m}x_i^Tx_i$为一个常数（取决于样本集而非模型），所以上式可写为
$$
const-\sum_{i=1}^{m}z_i^Tz_i
$$
将$z_i=W^Tx_i$代入可化为
$$
const-\left(W^T\left(\sum_{i=1}^{m}x_ix_i^T\right)W\right)^T
$$
所以目标为最小化

$$
-\left(W^T\left(\sum_{i=1}^{m}x_ix_i^T\right)W\right)^T\\
s.t. W^TW=I
$$

设
$$
f(W)=-\left(W^T\left(\sum_{i=1}^{m}x_ix_i^T\right)W\right)^T\\
g(W)=(W^TW-I)^T
$$


使用拉格朗日乘子法，若要使$f(x)$最小同时满足$g(x)=0$，取$d'*d'$对角矩阵$\Lambda$定义拉格朗日函数
$$
L(W,\Lambda)=f(W)+g(W)\Lambda
$$
即
$$
L(W,\Lambda)=-\left(W^T\left(\sum_{i=1}^{m}x_ix_i^T\right)W\right)^T+\left(\Lambda^T(W^TW-I)\right)^T
$$

令对$W$求微分结果为0，利用矩阵微分公式$\frac{\partial}{\partial X}(X^TBX)^T=BX+B^TX$与$\frac{\partial}{\partial X}(BX^TX)^T=XB^T+XB$可得到
$$
\frac{\partial L}{\partial W}=-2(XX^TW)+W\Lambda^T+W\Lambda=-2(XX^TW)+2W\Lambda=0
$$

即
$$
XX^TW=W\Lambda
$$
展开即得
$$
XX^Tw_i=\lambda_i w_i
$$
 此式为矩阵特征值和特征向量的定义式，其中$\lambda_i,w_i$分别表示矩阵$XX^T$的特征值和单位特征向量 。取前d'大的特征值对应的单位特征向量即可得到$W$