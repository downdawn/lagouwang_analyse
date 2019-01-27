# coding=utf-8

# import pandas as pd
# from matplotlib import pyplot as plt


# 将工作要求分离出来
# data = pd.read_csv('./lagouwang_position_sz.csv',encoding='gbk',usecols=[0,1,2,3,4,5,6])
# # print(data.info())
#
# for i,text in enumerate(data['desc']):
#     with open('job_require.txt','a') as f:
#         f.write(text)

# 1、制作词云
# from wordcloud import WordCloud
# import jieba
# import numpy as np
# from PIL import Image
#
# text= open('./job_require.txt').read()
# word_list = jieba.cut(text, cut_all=True)
# wl_split = ' '.join(word_list).replace('算机', '').replace('以上', '').replace('上学', '')\
#     .replace('学历', '').replace('岗位', '').replace('职责', '').replace('经验', '').replace('优先', '')\
#     .replace('相关', '').replace('专业', '').replace('熟练', '').replace('掌握', '').replace('据库', '')\
#     .replace('开发', '').replace('责任', '').replace('要求', '').replace('任职', '').replace('具备', '')\
#     .replace('大', '').replace('熟悉', '').replace('能力', '').replace('使用', '').replace('技术', '')\
#     .replace('工作', '').replace('考虑', '').replace('负责', '').replace('分析', '').replace('数据', '')\
#     .replace('仓库', '').replace('分布', '').replace('互联', '').replace('自动化', '').replace('解决', '')\
#     .replace('问题', '').replace('至少', '').replace('挖掘', '').replace('系统', '').replace('构设', '').replace('架计', '')
# print(wl_split)
# alice_mask = np.array(Image.open("aboutphoto.jpg"))
# # my_wordcloud = WordCloud(font_path=r"C:\\WINDOWS\\Fonts\\simsun.ttc").generate(wl_split)
# my_wordcloud = WordCloud(font_path=r"C:\\WINDOWS\\Fonts\\simsun.ttc",background_color='white', max_words=500, max_font_size=80, random_state=40, mask=alice_mask).generate(wl_split)
# plt.imshow(my_wordcloud)
# plt.axis('off')
# plt.show()


# 2、工资-饼图
# from pyecharts import Pie
# datas = pd.read_csv('./lagouwang_position_sz.csv',encoding='gbk',usecols=[7,8,9,10])
#
# scores = datas['range'].groupby(datas['range']).count()
# print(scores)
# pie1 = Pie("工资", title_pos='left', width=900)
# pie1.add(
#     "工资",background_color='black',
#     attr=['10.0k-15.0k', '15.0k-20.0k', '20.0k-30.0k', '30.0k-45.0k',],  # 要与scores一一对应
#     value=scores.values,
#     radius=[40, 75],
#     center=[50, 50],
#     is_random=True,
#     is_label_show=True,
# )
# pie1.render(path='salary.html')

# 3、经验-饼图
# from pyecharts import Pie,Line,Scatter
# datas = pd.read_csv('./lagouwang_position_sz.csv',encoding='gbk',usecols=[0,1,2,3,4,5,6])
# # print(datas['平均工资编码'])
# scores = datas['work_years'].groupby(datas['work_years']).count()
# print(scores)
# pie1 = Pie("经验", title_pos='left', width=900)
# pie1.add(
#     "经验",background_color='black',
#     attr=['1-3年', '3-5年 ', '5-10年', '经验不限'],
#     value=scores.values,
#     radius=[40, 75],
#     center=[50, 50],
#     is_random=True,
#     is_label_show=True,
# )
# pie1.render(path='experience.html')
