#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries, Dataset and Identifying Data

# In[64]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


# In[6]:


df = pd.read_csv("hotel_bookings.csv")


# In[8]:


df.head()


# In[10]:


df.tail(10)


# In[16]:


df.shape


# In[55]:


df.columns


# # Exploring & Cleaning the Data

# In[23]:


df.info()


# In[28]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], format='%d/%m/%Y')


# In[30]:


df.info()


# In[33]:


#Categorical Values have datatype 'Object' 
#Hence, although describe is used for numeric data, using "include" allows us perform the operation on object datatypes as well

df.describe(include = "object")


# In[41]:


for col in df.describe(include = "object").columns:

    print(col)
    print(df[col].unique())
    print("/"*50)


# In[44]:


df.isnull().sum()


# In[46]:


#We are doing this ONLY because the dataset has 1L+ values and we cannot simply delete particualr null entries
#Hence we have dropped the entire cols.
df.drop(['agent','company'], axis = 1, inplace = True)

#This removes the Null Entries
df.dropna(inplace = True)


# In[48]:


df.isnull().sum()


# In[50]:


df.describe()


# In[52]:


#Outlier: ADR value 5000 is wild, that should not be possible.

df = df[df['adr']<500]


# In[54]:


df.describe()


# # Data Analysis and Visualizations

# In[84]:


cancel_perc = df['is_canceled'].value_counts(normalize = True)
cancel_perc

#37 percentile is quite a significant proportion. 

## Bar Plot
plt.figure(figsize = (10,6))
plt.bar(['Canceled','Not Canceled'],df['is_canceled'].value_counts(), color = 'g', edgecolor = 'k',width = 0.9)
plt.xlabel('Is_Canceled')
plt.ylabel('Calculations')
plt.title('First Chart to explore cancelations')
plt.show()


# In[96]:


## CountPlot

plt.figure(figsize = (10,6))
sns.countplot(x = 'hotel',hue = 'is_canceled', palette = 'Blues', data = df)
plt.xlabel('Type of Hotel')
plt.ylabel('Count Of reservations')
plt.legend(['Not Canceled','Canceled'])
plt.title('Second Chart based on Hotel')
plt.show()


# In[103]:


resort_Hotel = df[df['hotel'] == 'Resort Hotel']
resort_Hotel['is_canceled'].value_counts(normalize = True)#


# In[105]:


City_Hotel = df[df['hotel'] == 'City Hotel']
City_Hotel['is_canceled'].value_counts(normalize = True)


# In[157]:


df['month'] = df['reservation_status_date'].dt.month #dt

plt.figure(figsize = (15,7))
sns.countplot(x = 'month' ,hue = 'is_canceled', data = df)
plt.legend(['Not_Canceled', 'Canceled'])
plt.xlabel('Months')
plt.ylabel('No. of Cancellation')
plt.title('Chart based on Months')
plt.show()


# In[158]:


#To prove that price is an important factor for cancelation
#Refer: #df = df.groupby(['size', 'sex']).agg(mean_total_bill=("total_bill", 'mean'))

adr_monthly = df[df['is_canceled'] == 1]
adr_monthly = adr_monthly.groupby('month').agg(adr_sum=("adr","sum"))#agg()
adr_monthly = adr_monthly.reset_index()

sns.barplot(x = "month",y = "adr_sum",data = adr_monthly)





# In[175]:


canceled_data = df[df['is_canceled'] == 1]
top_10_countries = canceled_data['country'].value_counts()[:10] #Top 10, Slicing, vc
#print(top_10_countries)

plt.figure(figsize = (10,10))
plt.pie(top_10_countries, autopct = "%.2f", labels = top_10_countries.index ,colors = sns.color_palette('pastel'), textprops={'fontsize': 10}, wedgeprops={"linewidth": 1, "edgecolor": "white"})
plt.title("My Pie Chart")
plt.show()

#Hence it is evident from the Pie Chart that PRT is a country to focus on be it Improving he aminities, Pricing, Advertising etc.


# In[178]:


Agent_Type = df['market_segment'].value_counts()
Agent_Type


# In[180]:


Agent_Type_Perc = df['market_segment'].value_counts(normalize = True)
Agent_Type_Perc

#Therefore it is evident that most reservations are done through Online TA


# In[183]:


canceled_data = df[df['is_canceled'] == 1]
TA_Cancel_Data = canceled_data['market_segment'].value_counts(normalize = True)
TA_Cancel_Data


# # Conclusion

# Most Cancelations:
# 1. Hotel Type - City
# 2. Month -January
# 3. Pricing - High
# 4. Country - Portugese
# 5. Market Segment - Online TA
