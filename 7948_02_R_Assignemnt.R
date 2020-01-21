library(readxl)
library(dplyr)
library(plyr)
library(lubridate)
library(readr)


sale_df <- read_xlsx('C:/Users/satya.yalla/Documents/Tiger_Analytics_Learning_Path/Python_workspace/assignment/SaleData.xlsx')


# Question 1
df <- sale_df %>%
              group_by(Item) %>%
              summarise(min_sale = min(Sale_amt))
#print(df)


# Question 2
sale_df$year <- year(ymd(sale_df$OrderDate))
df <- sale_df %>%
              group_by(year,Region,Item) %>%
              summarise(total_sales = sum(Sale_amt))
#print(df)


# Question 3
ref_date <- ymd("2019-12-29")
sale_df$days_off <- as.Date(ref_date,format="%Y-%m-%d") - as.Date(sale_df$OrderDate,format="%Y-%m-%d")
#print(sale_df$days_off)


# Question 4
df <- sale_df %>% 
              group_by(manager = Manager) %>%
              summarise(list_of_salesman = list(unique(SalesMan)))
#print(df)


# Question 5
df <- sale_df %>%
              group_by(Region) %>%
              summarise(salesmen_count=lengths(list(unique(SalesMan))),total_sales=sum(Sale_amt))
#print(df)


# Question 6
total_amt <- sum(sale_df$Sale_amt)
df <- sale_df %>% 
              group_by(Manager) %>%
              summarise(percent_sales=(sum(Sale_amt)/total_amt)*100)
#print(df)


imdb_df <- read_delim('C:/Users/satya.yalla/Documents/Tiger_Analytics_Learning_Path/Python_workspace/assignment/imdb.csv',delim=',',escape_backslash=T,escape_double=F)


# Question 7
imdb_df$imdbRating[5]


# Question 8
movie_list <- imdb_df %>%
                      filter(type=="video.movie")
shortest_movie_title <- movie_list %>%
                                    filter(duration==min(as.numeric(as.character(duration)),na.rm=TRUE)) %>%
                                    select(title)

longest_movie_title <- movie_list %>%
                                  filter(duration==max(as.numeric(as.character(duration)),na.rm=TRUE)) %>%
                                  select(title)


# Question 9
imdb_df[with(imdb_df, order(imdb_df$year, imdb_df$imdbRating)), ]


# Question 10
df <- imdb_df %>% 
              filter(type=="video.movie",as.numeric(as.character(duration))>=30,as.numeric(as.character(duration))<=180)



diamond_df <- read.csv('C:/Users/satya.yalla/Documents/Tiger_Analytics_Learning_Path/Python_workspace/assignment/diamonds.csv')


# Question 11
df <- ddply(diamond_df,names(diamond_df),nrow)

duplicate_rows <- 0
for(row in 1:nrow(df[11])){
  if(df[row,11]>1){
    duplicate_rows <- duplicate_rows+1
  }
}
#print(duplicate_rows)


# Question 12
diamond_df <- diamond_df[!duplicated(diamond_df[c('carat','cut')]),]


# Question 13
select_if(diamond_df,is.numeric)


# Question 14
diamond_df$z <- as.numeric(as.character(diamond_df$z))

diamond_df$volume[diamond_df$depth < 60] = 8
depth_60 <- diamond_df$depth >= 60
diamond_df$volume[depth_60] = diamond_df$x[depth_60]*diamond_df$y[depth_60]*diamond_df$z[depth_60]


# Question 15
diamond_df$price[is.na(diamond_df$price)] = mean(diamond_df$price[!is.na(diamond_df$price)])
