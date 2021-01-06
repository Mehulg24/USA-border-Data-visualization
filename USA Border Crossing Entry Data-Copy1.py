#!/usr/bin/env python
# coding: utf-8

# In[129]:


import numpy as np
import pandas as pd
# 1.2 For plotting
import matplotlib.pyplot as plt
import matplotlib
import matplotlib as mpl     # For creating colormaps
import seaborn as sns
# 1.3 For data processing
from sklearn.preprocessing import StandardScaler
# 1.4 OS related
import os


# In[130]:


os.chdir("D:\\data analyst data\\download data")


# In[131]:


os.listdir()


# In[132]:


data = pd.read_csv("Border_Crossing_Entry_Data.csv.zip",
                   parse_dates = ['Date']
                  )


# In[145]:


data


# In[146]:


data.head()


# In[147]:


data.dtypes


# In[148]:


data.info() # check for any null values


# In[149]:


data.columns


# In[150]:


data.rename({
             'Port Name' : 'port_name',
             'State'     : 'state',
             'Port Code' : 'port_code',
             'Border'    : 'border',
             'Date'      : 'date',
             'Measure'   : 'measure',
             'Value'     : 'value',
             'Location'  : 'location'
             },inplace='True',axis=1)
data


# In[151]:


data['port_name'].nunique()


# In[152]:


data['port_code'].nunique()  # port_code and port_name are not the same


# In[153]:


diff= data[['port_name' , 'port_code']].drop_duplicates()
diff[diff['port_name'].duplicated(keep = False)] 


# In[154]:


data.loc[(data.port_code == 103) | (data.port_code == 3302)]


# In[155]:


data.loc[(data['port_name'] == 'Eastport') & (data['state'] == 'Maine'), 'port_name'] = 'Eastport Maine' 
# Rename Eastport located in Maine to 'Eastport Maine' to avoid confusion


# In[156]:


data.loc[(data.port_code == 103) | (data.port_code == 3302)]


# In[157]:


data['port_code'].nunique()


# In[158]:


data['port_name'].nunique() # port code and port name are now same


# In[159]:


data['year'] = data.date.dt.year
data['month'] = data.date.dt.month
data['weekdays'] = data.date.dt.weekday
data['weekday'] =  data.date.dt.weekday
data['weekday'] = data ['weekday'].map ({ 
                      0: 'Monday',
                      1: 'Tuesday',
                      2: 'Wednesday',
                      3: 'Thursday',
                      4: 'Friday',
                      5: 'Saturday',
                      6: 'Sunday'
                    }
                  )
data


# In[188]:


#1) What are total passengers travelled accross bonders

sns.barplot(x = 'border', y = 'value', data = data, estimator =sum)


# In[160]:


data['measure'].unique()


# In[161]:


gen_public =['Personal Vehicle Passengers','Bus Passengers','Personal Vehicles','Pedestrians','Train Passengers']
data.loc[data['measure'].isin(gen_public),'vehicle_cat'] ='gen_public_vehicle'
data.loc[~data['measure'].isin(gen_public),'vehicle_cat'] ='commercial_vehicle'
data['vehicle_cat'].unique()


# In[162]:


data


# In[163]:


ax = sns.boxplot(x = 'vehicle_cat' , y = 'year', hue = 'border', data = data )


# In[169]:


plt.figure(figsize=(12,10))
facet = sns.FacetGrid(data, col = 'state')
facet.map(sns.distplot, 'month')


# In[172]:


#2) What are total general public travelled accross bonders year vise
plt.figure(figsize=(18,12))
sns.barplot(data=data[data.vehicle_cat == 'gen_public_vehicle'], x='border',y='value' , hue = 'year' ,estimator = sum)


# In[173]:


#3) What are total commercial_vehicle travelled accross bonders year vise 
plt.figure(figsize=(18,12))
sns.barplot(data=data[data.vehicle_cat =='commercial_vehicle'], x='border',y='value', hue = 'year',estimator = sum)


# In[189]:


# Use group by method to find sum of values for all general public for borders 
data1= data[data.vehicle_cat=='gen_public_vehicle'].groupby(['border','measure']).sum().value.reset_index()
data1 


# In[191]:


# Use group by method to find sum of values for all commercial vehicle for borders 
data2= data[data.vehicle_cat=='commercial_vehicle'].groupby(['border','measure']).sum().value.reset_index()
data2


# In[195]:


#4) What are diffrrent type of meaures and their sum for both borders- plot bar chart only for vehlcle
plt.figure(figsize=(15,3))
sns.barplot(data = data[data.vehicle_cat == 'commercial_vehicle']
            , x = 'measure', y= 'value' , hue = 'border', estimator = sum )


# In[196]:


#5)What are diffrrent type of meaures and their sum for both borders- plot bar chart only for general public vehicle
plt.figure(figsize=(15,3))
sns.barplot(data = data[data.vehicle_cat == 'gen_public_vehicle']
            , x = 'measure', y= 'value' , hue = 'border' , estimator = sum)


# In[198]:


#6) find sum of values for all measures
data.groupby('measure').sum().value


# In[203]:


#8) which state has highest and lowest numebr vehicles travelled
state_travel = data.groupby(['state','vehicle_cat'])['value'].sum().sort_values(ascending=False).reset_index()
state_travel.head()


# In[221]:


plt.figure(figsize=(17,7))
sns.barplot(x = 'state', y = 'value', data = state_travel, hue = 'vehicle_cat')


# In[224]:


port_data=data.groupby(['port_name','vehicle_cat'])['value'].sum().sort_values(ascending=False).reset_index()
plt.figure(figsize=(15,40))
sns.barplot(data=port_data[port_data.vehicle_cat=='gen_public_vehicle'],y='port_name',x='value')


# In[35]:


border_count = data.border.value_counts()
border_count


# In[32]:


plt.figure(figsize=(7,6))
plt.pie(x = border_count.values,explode=[0.03,0.03], labels = border_count.index, autopct='%0.2f%%',)
plt.title('Composition of the Borders')
plt.show()


# In[ ]:





# In[186]:


sns.barplot(x = 'border', y = 'value' , hue = 'vehicle_cat',data = data , estimator =sum)


# In[184]:


plt.figure(figsize=(15,3))
sns.barplot(data=data, x='vehicle_cat',y='value',hue='border',estimator =sum)


# In[169]:


sns.distplot(data.year)


# In[216]:


sns.distplot(data.month)


# In[188]:


sns.distplot(data.port_code)


# In[229]:


temp = pd.DataFrame(data.groupby('state')['value'].sum().sort_values()).reset_index()
plt.figure(figsize=(18,12))
sns.barplot(x = 'state' , y = 'value' , data = temp)


# In[37]:


plt.figure(figsize=(18,12))

sns.barplot(x = 'state', y = 'weekdays', data = data)


# In[ ]:




