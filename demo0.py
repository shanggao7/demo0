"""
Created on Tue Aug 23 2022

@author: Shang
"""
import streamlit as st
import numpy as np
import pandas as pd
import io

buffer = io.BytesIO()

st.set_page_config(page_title='安信EDS内部') # 设置网页标题
st.header('$券池&大宗池$')# 设置网页子标题

st.markdown("""---""") #### 分割线

#### 上传整理后的券池文件
st.subheader('上传文件')
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is None:
    st.warning('Please upload a file')
    st.stop()
else:
    xl = pd.ExcelFile(uploaded_file)
    st.write('上传文件中所有sheet名称: ',xl.sheet_names)
    sheetname = st.text_input('请输入需要打开的sheet名称 (默认为首项)', xl.sheet_names[0])
    df = pd.read_excel(uploaded_file,sheet_name = sheetname,header = 0)
    st.success('Successfully!')
#    st.write(df)

#df = pd.read_excel('券池_v1.xlsx',sheet_name = 'Sheet1',header = 0)
#st.dataframe(df)

st.markdown("""---""") #### 分割线
st.subheader('精确搜索')
##### 输入相应的证券简称得到对应的result
title = st.text_input('请输入证券简称', '新能车ETF')
st.write('结果为: ', df[df['证券简称']==title])

##### 输入相应的证券代码得到对应的result
code = st.text_input('请输入证券代码', '515700.SH')
st.write('结果为: ', df[df['证券代码']==code])


st.markdown("""---""") #### 分割线
st.subheader('筛选')
####### 选择星级
star = df['星级'].unique().tolist()  #星级的多重选择
##### 增加一个全选的选项
l1=[]
l1=star[:]
l1.sort(reverse=True)
l1.append('Select all')
star_selection = st.multiselect('星级',l1)

if 'Select all' in star_selection :
	star_selection=star

####### 选择来源
source = df['来源'].unique().tolist() #星级的多重选择
#source_selection = st.multiselect('来源:',source,default=source)
l2=[]
l2=source[:]
l2.append('Select all')
source_selection = st.multiselect('来源',l2)
##### 增加一个全选的选项
if 'Select all' in source_selection :
	source_selection=source

# 根据选择过滤数据
mask = (df['星级'].isin(star_selection)) & (df['来源'].isin(source_selection))
number_of_result = df[mask].shape[0]

# 根据筛选条件, 得到有效数据个数
st.markdown(f'*有效数据: {number_of_result}*')

# 根据选择分组数据
df_grouped = df[mask]
df_grouped = df_grouped.reset_index()

st.dataframe(df_grouped)

#### 可以将筛选出来的数据保存为excel格式
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    df_grouped.to_excel(writer, sheet_name='Sheet1')
    writer.save()

    st.download_button(
        label="Download the results",
        data=buffer,
        file_name="filtered_data.xlsx",
        mime="application/vnd.ms-excel"
    )

st.markdown("""---""")