import pandas as pd

# 读取文件数据
df=pd.read_csv('D:\work3\数据集\shortstay_20200201_20200215.csv', sep='\t',engine='python',header=[0])

# 列csv文件中所有列
df.columns = [ 'date','time', 'x', 'y','gs']

#  删除date列中的重复项，也就是说剩下的date都是已经分好的类别
date_cate = df.drop_duplicates(subset=['date'])
print(date_cate.date)
print(range(len(date_cate)))    # date中的所有类，也就是文件数
for name in date_cate.date:
    print(name)
    # 当date为某一个类时，存入一个小的csv文件中，文件名为类名
    df[df.date == name].to_csv(u"D:\work3\数据集\%s" %name+".csv")
