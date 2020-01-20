import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
import math
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


sale_df = pd.read_excel('C:/Users/satya.yalla/Documents/Tiger_Analytics_Learning_Path/Python_workspace/assignment/SaleData.xlsx')

#Q1

def least_sales(df):
    ls = df.groupby(["Item"])["Sale_amt"].min().reset_index()
    return ls

ls = least_sales(sale_df)


#Q2

def sales_year_region(df):   
    df["Year"] = df["OrderDate"].apply(lambda x : x.year)
    ls = df.groupby(["Region","Year","Item"])["Sale_amt"].sum().reset_index()
    return ls
    
ls = sales_year_region(sale_df)


#Q3

def days_diff(df,reference_date):
    df['days_diff']=df['OrderDate'].apply(lambda x:reference_date-x)
    return df
    
reference_date = pd.to_datetime('Dec 29th 2019')
ls = days_diff(sale_df,reference_date)


#Q4

def to_list(l):
    l1=[]
    for x in l:
        if x not in l1:
            l1.append(x)
    return l1

def mgr_slsmn(df):
    ls = df.groupby(["Manager"])["SalesMan"].apply(list).reset_index()
    ls["SalesMan"] = ls["SalesMan"].apply(to_list)
    return ls
    
ls = mgr_slsmn(sale_df)


#Q5

def slsmn_units(df):
    ls = df.groupby('Region')['SalesMan'].nunique().reset_index()
    ls1 = df.groupby('Region')['Sale_amt'].sum().reset_index()
    ls = pd.merge(ls,ls1,on=['Region'])
    ls.columns = ['Region','SalesMan_count','Total_Sales']
    
ls = slsmn_units(sale_df)
ls.columns=['Region','SalesMan_count','Total_Sales']


#Q6

def sales_pct(df):
    ls = df.groupby('Manager').sum()[['Sale_amt']].reset_index()
    total = df['Sale_amt'].sum()
    ls['Sale_amt'] = ls['Sale_amt']*100/total
    ls.columns = ['Manager','Percentage_Sales']
    return ls
    
ls = sales_pct(sale_df)


imdb_df = pd.read_csv('C:/Users/satya.yalla/Documents/Tiger_Analytics_Learning_Path/Python_workspace/assignment/imdb.csv',escapechar="\\")
movie_df = pd.read_csv('C:/Users/satya.yalla/Documents/Tiger_Analytics_Learning_Path/Python_workspace/assignment/movie_metadata.csv')


#Q7

def fifth_movie(df):
    return df.iloc[4]['imdbRating']
    
ls = fifth_movie(imdb_df)


#Q8

def movies(df):
    x = df[df['duration']==df[df['type']=='video.movie']['duration'].max()]['title']
    y = df[df['duration']==df[df['type']=='video.movie']['duration'].min()]['title']
    return 'Movie with Longest Runtime : {one}, with Shortest Runtime: {two}'.format(one=x.iloc[0],two=y.iloc[0])
    
result=movies(imdb_df)


#Q9

def sort_df(df):
    ls = df.sort_values(by=['year','imdbRating'],ascending=[True,False],na_position='last')
    return ls
    
ls = sort_df(imdb_df)


#Q10

def subset_df(df):
    ls = df[(df['gross']>2000000) & (df['budget']<1000000) & (df['duration']>=30.0) & (df['duration']<=180.0)]
    return ls

ls = subset_df(movie_df)


diamond_df = pd.read_csv('C:/Users/satya.yalla/Documents/Tiger_Analytics_Learning_Path/Python_workspace/assignment/diamonds.csv')


#Q11

def dupl_rows(df):    
    ls = df.pivot_table(index=df.columns.to_list(), aggfunc='size')
    count=0
    for i in ls:
        if(i>1):
            count+=1
    return count

print('No of Duplicte Rows ' + str(dupl_rows(diamond_df)))


#Q12

def drop_row(df):
    return df.dropna(subset=['carat','cut'])
    
diamond_df=drop_row(diamond_df)


#Q13

def sub_numeric(df):
    return df._get_numeric_data()

ls=sub_numeric(diamond_df)


#Q14

def toFloat(x):
    try:
        y = float(x)
    except ValueError:
        y = 1.0
    return y

def volume(df):
    ls = df.dropna(subset=['z'])[df['depth']<60]
    ls1 =df.dropna(subset=['z'])[df['depth']>=60]
    ls['volume'] = 8
    ls1['volume'] = ls1['x']*ls1['y']*ls1['z'].apply(toFloat)
    return pd.concat([ls1,ls])
    
diamond_df=volume(diamond_df)


#Q15

def impute(df):
    df['price'].fillna(value=df['price'].mean)
    return df

diamond_df = impute(diamond_df)


# BONUS QUESTIONS

#Q1

ls = imdb_df.groupby(['year','type'])["imdbRating"].mean().reset_index()
ls1 = imdb_df.groupby(['year','type'])["imdbRating"].min().reset_index()
ls = pd.merge(ls,ls1,on=['year','type'])
ls1 = imdb_df.groupby(['year','type'])["imdbRating"].max().reset_index()
ls = pd.merge(ls,ls1,on=['year','type'])
ls1 = imdb_df.groupby(['year','type'])['duration'].sum().reset_index()
ls = pd.merge(ls,ls1,on=['year','type'])
ls.columns=['year','type','avg_rating','min_rating','max_rating','total_run_time']
ls["genere_combo"]=[[]]*ls.shape[0]

def find_combo(year,typ,df,genere):
    ls = df[(df['year']==year) & (df['type']==typ)]
    ls = ls.iloc[:,16:44]
    l=[]
    for i in range(ls.shape[0]):
        for j in range(ls.shape[1]):
            if(ls.iloc[i,j]==1):
                if(genere[j] not in l):
                    l.append(genere[j])
    return l
    
genere = imdb_df.columns[16:44]
g_list=[[]]*ls.shape[0]

for i in range(ls.shape[0]):
    g_list[i] = find_combo(ls.iloc[i]['year'],ls.iloc[i]['type'],imdb_df,genere)

ls['genere_combo']=g_list
#print(ls)


#Q2

#part 1
imdb_df['movie_len']=imdb_df['title'].apply(lambda x:len(x)-7)
cor_value = imdb_df[imdb_df['type']=='video.movie']['movie_len'].corr(imdb_df[imdb_df['type']=='video.movie']['imdbRating'])

print("correlation value is : {}".format(cor_value))
print("as the value is close to zero therefore is no correlation")

#part 2
def find_count(l,quan,req):
    cnt=0
    if(req==25):
        for x in l:
            if(x<=quan[0.25]):
                cnt+=1
    elif(req==50):
        for x in l:
            if((x<=quan[0.5]) & (x>quan[0.25])):
                cnt+=1
    elif(req==75):
        for x in l:
            if((x<=quan[0.75]) & (x>quan[0.5])):
                cnt+=1
    else:
        for x in l:
            if(x>quan[0.75]):
                cnt+=1
    return cnt

def find_percentile(imdb_df):
    imdb_df = imdb_df.dropna(subset=['title'])
    imdb_df['movie_len']=imdb_df['title'].apply(lambda x:len(x)-7)
    d = imdb_df[imdb_df['type']=='video.movie']['movie_len'].quantile([0.25,0.5,0.75])
    ls = imdb_df[imdb_df['type']=='video.movie'].groupby('year')['movie_len'].min().reset_index()
    ls1 = imdb_df[imdb_df['type']=='video.movie'].groupby('year')['movie_len'].max().reset_index()
    ls = pd.merge(ls,ls1,on=['year'])
    ls.columns=['year','movie_title_min_len','movie_title_max_len']
    
    ls1 = imdb_df[imdb_df['type']=='video.movie'].groupby('year')['movie_len'].apply(list).reset_index()
    ls1['num_videos_less_than25Percentile'] = ls1['movie_len'].apply(find_count,quan=d,req=25)
    ls1['num_videos_25_50Percentile'] = ls1['movie_len'].apply(find_count,quan=d,req=50)
    ls1['num_videos_50_75Percentile'] = ls1['movie_len'].apply(find_count,quan=d,req=75)
    ls1['num_videos_greaterthan75Precentile'] = ls1['movie_len'].apply(find_count,quan=d,req=100)
    ls1.drop(['movie_len'],axis=1,inplace=True)
    
    ls = pd.merge(ls,ls1,on=['year'])
    return ls

ls = find_percentile(imdb_df)
#print(ls)

#part 3
def find_quartile(mv_len,quan):
    if(mv_len <= quan[0.25]):
        return '1st'
    elif(mv_len <= quan[0.5]):
        return '2nd'
    elif(mv_len <= quan[0.75]):
        return '3rd'
    return '4th'
    
d = imdb_df[imdb_df['type']=='video.movie']['movie_len'].quantile([0.25,0.5,0.75])
imdb_df['Quartile'] = imdb_df['movie_len'].apply(find_quartile,quan=d)

pd.crosstab(imdb_df[imdb_df['type']=='video.movie']['year'],[imdb_df[imdb_df['type']=='video.movie']['Quartile']])


#Q3

#dividing diamond dataframe into 4 bins
li = pd.qcut(diamond_df['volume'],4)

def find_bin(x,quan):
    if(x.right<=quan[0].right):
        return '1st bin'
    elif(x.right<=quan[1].right):
        return '2nd bin'
    elif(x.right<=quan[2].right):
        return '3th bin'
    return '4th bin'
    
bins = li.unique()
diamond_df['bin'] = li.apply(find_bin,quan=bins)
pd.crosstab(diamond_df['cut'],[diamond_df['bin']],normalize='index')


#Q4

y = int(movie_df['title_year'].max())
l = range(y,y-10,-1)
ls = movie_df[movie_df['title_year'].isin(l)]
ls = ls.sort_values(['title_year','gross'],ascending=[False,False])
ls['quarter'] = pd.qcut(ls['title_year'],4,[1,2,3,4])
ls1=ls.groupby('quarter')['director_name'].count().reset_index()

nrow_list = []
for i in range(ls1.shape[0]):
    nrow_list.insert(0,math.ceil(ls1.iloc[i,1]*0.1))

req_df = pd.DataFrame()
for i in range(1,5):
    req_df = req_df.append(ls[ls['quarter']==i].head(nrow_list[i-1]))

final_df = req_df.groupby('quarter')['imdb_score'].mean().reset_index()

req_df['url'] = req_df['movie_imdb_link'].apply(lambda x : x.split('?')[0])
req_df = pd.merge(req_df,imdb_df,on=['url'],how='left')
req_df = req_df.groupby('quarter').sum().loc[:,'Action':'Western'].reset_index()
final_df = pd.merge(final_df,req_df,on=['quarter'],how='left')
#print(final_df)


#Q5

def find_top_3_geners(row,index,geners):
    row = row[index:]
    d = {}
    l=[]
    cnt=3
    for i in range(len(row)-1):
        d[row[i]]=geners[i]
    for i in sorted(d.keys(),reverse=True):
        l.append(d[i])
        cnt-=1
        if(cnt<=0):
            break
    return l

imdb_df['decile'] = pd.qcut(imdb_df['duration'],10)
ls = imdb_df.groupby(['decile']).sum().reset_index()

ls['top_3_geners']=ls.apply(find_top_3_geners,index=ls.columns.get_loc('Action'),geners=ls.columns[ls.columns.get_loc('Action'):],axis=1)
ls = ls[['decile','nrOfWins','nrOfNominations','top_3_geners']]
ls1 = imdb_df.groupby('decile')['title'].count().reset_index()
ls1.columns=['decile','count']
ls = pd.merge(ls1,ls,on=['decile'])
#print(ls)