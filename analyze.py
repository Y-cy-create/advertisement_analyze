import pandas as pd
import scipy.stats as st
from pingouin import pairwise_tukey
import numpy as np
import plotly.offline as py
import plotly.graph_objects as go
import statsmodels.api as sm
from statsmodels.formula.api import ols
data = pd.read_csv('consumption_data.csv', encoding = 'big5')
data_complete = data.isnull().any()
alist = data[data['廣告'] == '廣告1']['消費金額'].tolist()
blist = data[data['廣告'] == '廣告2']['消費金額'].tolist()
clist = data[data['廣告'] == '廣告3']['消費金額'].tolist()
dlist = data[data['地區'] == '北部']['消費金額'].tolist()
elist = data[data['地區'] == '中部']['消費金額'].tolist()
flist = data[data['地區'] == '南部']['消費金額'].tolist()
ash = st.shapiro(alist)
bsh = st.shapiro(blist)
csh = st.shapiro(clist)
dsh = st.shapiro(dlist)
esh = st.shapiro(elist)
fsh = st.shapiro(flist)
all_lev = st.levene(alist, blist, clist, center='mean')
f_value, p_value = st.f_oneway(alist, blist, clist)
m_comp = pairwise_tukey(data=data, dv='消費金額', between='廣告')
table = m_comp.drop(columns = ['mean(A)', 'mean(B)', 'T', 'p-tukey', 'hedges'])
# 「A」欄反轉資料
add_A = table['B'].tolist()
# 「B」欄反轉資料
add_B = table['A'].tolist()
# 「diff」欄反轉資料
diff =  (table['diff'] - 2 * table['diff']).tolist()
# 「se」欄反轉資料
se = table['se'].tolist()
# 將反轉資料合併
table2 = pd.DataFrame(zip(add_A, add_B, diff, se), columns = ['A', 'B', 'diff', 'se'])
new_table = pd.concat([table, table2], ignore_index=True)
new_table['上界'] = new_table['diff'] + new_table['se']*1.96
new_table['下界'] = new_table['diff'] - new_table['se']*1.96
n1 = np.sign(12)
n2 = np.sign(-5.6)
justice = []
for i in range(0, new_table.shape[0]):
      a = np.sign(new_table.iloc[i, 4]) # 上界正負數判斷
      b = np.sign(new_table.iloc[i, 5]) # 下界正負數判斷
      if a == b:
        justice.append('Yes')
      else:
        justice.append('No')


new_table['是否顯著'] = justice
fig = go.Figure()
for i in range(0, new_table.shape[0]):
    if new_table.iloc[i, 6] == 'Yes':
        color = 'firebrick'
        name = '顯著'
    else:
        color = 'green'
        name = '不顯著'
    fig.add_trace(go.Scatter(
        x = [new_table.iloc[i, 5], new_table.iloc[i,2], new_table.iloc[i,4]],
        y = [new_table.iloc[i,0] + '-' + new_table.iloc[i,1], new_table.iloc[i,0] + '-' + new_table.iloc[i,1], new_table.iloc[i,0] + '-' + new_table.iloc[i,1]],
        mode = "lines+markers",
        textfont=dict(
        family="sans serif",
        size=16,
        color=color),
        line=dict(color=color, width=2),
        name = name,
        legendgroup = name,
        ))

fig.update_layout(
      title={
          'text': "<b>One-Way ANOVA 廣告效益分析</b>",
          'y': 0.95,
          'x': 0.5,
          'xanchor': 'center'},
      width=1800,
      height=960,
      boxmode='group',
      font=dict(
          family="Courier New, monospace",
          size=20,
          color="lightslategrey"
      )
      )

# # 另存互動式網頁
# py.plot(fig, filename='One-Way ANOVA 廣告效益分析', auto_open=True)
# # 另存.png圖檔
# fig.write_image("C:/Users/RexTung/PycharmProjects/pythonProject1/One-Way ANOVA 廣告效益分析.png")

abc_lev = st.levene(alist, blist, clist, center='mean')
def_lev = st.levene(dlist, elist, flist, center='mean')
model = ols('消費金額 ~ C(廣告) + C(地區) + C(廣告):C(地區)', data=data).fit()
Results = sm.stats.anova_lm(model)
var1 = data['廣告'].unique().tolist()
var2 = data['地區'].unique().tolist()
ad1_list = []
ad2_list = []
ad3_list = []
for i in var1:
    for ii in var2:
        if i == '廣告1':
            ad1_list.append(data[data ['廣告'] == i][data ['地區'] == ii]['消費金額'].mean())
        elif i == '廣告2':
            ad2_list.append(data[data ['廣告'] == i][data ['地區'] == ii]['消費金額'].mean())
        elif i == '廣告3':
            ad3_list.append(data[data ['廣告'] == i][data ['地區'] == ii]['消費金額'].mean())

cross_table = pd.DataFrame((ad1_list, ad2_list, ad3_list), columns = var2, index = var1)
fig = go.Figure()
# 廣告1分布圖
fig.add_trace(go.Scatter(
              x= var2,
              y= cross_table.iloc[0,:].tolist(),
              mode="lines+markers",
              textfont=dict(
              family="sans serif",
              size=16,
              color="royalblue"),
           line=dict(color='royalblue', width=2),
              name = '廣告1'
              ))
# 廣告2分布圖
fig.add_trace(go.Scatter(
              x= var2,
              y= cross_table.iloc[1,:].tolist(),
              mode="lines+markers",
              textfont=dict(
              family="sans serif",
              size=16,
              color="firebrick"),
           line=dict(color='firebrick', width=2),
              name = '廣告2'
              ))
# 廣告3分布圖
fig.add_trace(go.Scatter(
              x= var2,
              y= cross_table.iloc[2,:].tolist(),
              mode="lines+markers",
              textfont=dict(
              family="sans serif",
              size=16,
              color="green"),
           line=dict(color='green', width=2),
              name = '廣告3'
              ))

fig.update_layout(
      title={
          'text': "<b>廣告效益分析</b>",
          'y':0.95,
          'x':0.5,
          'xanchor': 'center'},
      yaxis_title='平均消費金額',
      xaxis={
          'title': '地區',
          'tickmode': 'linear'
          },
      width=1800,
      height=960,
      boxmode='group',
      font=dict(
          family="Courier New, monospace",
          size=20,
          color="lightslategrey"
      )
      )

# 另存html檔
py.plot(fig, filename='多因子變異數分析', auto_open=True)
# 另存png檔
fig.write_image("C:/Users/RexTung/PycharmProjects/pythonProject1/多因子變異數分析.png")


