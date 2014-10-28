df = read.table("/Volumes/AhaStorage/A_Project/08_VoteCash/github/VoteCash/data/votemart.csv",header=T,sep=",",stringsAsFactors = F);
library(ggplot2)
library(dplyr)
library(DSC2014Tutorial)
slides("Visualization2")

df2 = df[df[,"main_type"]!="總統",]

df2 = filter(df,main_type=="總統")

g = ggplot(df,aes(x=vote_cnt,y=cost))
g+geom_point(aes(color=elect_ind))
g+geom_point(aes(color=main_type))
g+geom_point(aes(color=main_type))

g2 = ggplot(df2,aes(x=vote_cnt,y=cost))
g2+geom_point(aes(color=elect_ind))

summary(df_avg)
par(family='Heiti TC Light')
ggplot(df_avg,aes(x=main_type,fill=main_type))+geom_histogram()+
  labs(x='層級',y='記錄筆數',title='資料分佈')+
  theme(# for OS X (XQuartz device) to show Chinese characters
  text=element_text(family='Heiti TC Light'), 
  # rotate angle of x ticks
  axis.text.x=element_text(angle=90, hjust=1, vjust=.5),
  # change size of title
  plot.title=element_text(size=26)) 




df_avg = select(mutate(df,avg = cost/vote_cnt),cost,vote_cnt,avg,main_type,position_level,party)
df_avg = mutate(df_avg,main_type = as.factor(main_type))



give.n <- function(x){
  return(c(y = median(x)*0.7, label = length(x))) 
  # experiment with the multiplier to find the perfect position
}

# function for mean labels
median.n <- function(x){
  return(c(y = median(x)+10, label = round(median(x),0))) 
  # experiment with the multiplier to find the perfect position
}

#Figure1
ggplot(df_avg,aes(x=reorder(main_type,-position_level),y=avg,fill=main_type))+geom_boxplot(aes(alpha=.5))+ coord_flip()+
  labs(x='層級',y='平均每票花費(元新台幣)',title='一票值多少?')+
  scale_y_continuous(limits=c(0,300))+
  #stat_summary(fun.data = give.n, geom = "text", fun.y = median, colour = "red") +
  stat_summary(fun.data = median.n, geom = "text", fun.y = median)+
  theme(# for OS X (XQuartz device) to show Chinese characters
    text=element_text(family='Heiti TC Light'), 
    # rotate angle of x ticks
    axis.text.x=element_text(size=14, hjust=1, vjust=.5,color="black"),
    axis.text.y=element_text(size=14,color="#2c9893"),
    # change size of title
    plot.title=element_text(size=26)) 

#Figure2



df_avg2 = filter(df_avg,party=="中國國民黨" | party=="民主進步黨" | party=="無黨籍及未經政黨推薦")
ggplot(df_avg2,aes(x=reorder(main_type,-position_level),y=avg,fill=main_type))+
  geom_boxplot(aes(alpha=.5))+
  facet_grid( party~.,scales="free_x")+
  coord_flip()+
  labs(x='層級',y='平均每票花費(元新台幣)',title='各黨一票值多少?')+
  scale_y_continuous(limits=c(0,300))+
  #stat_summary(fun.data = give.n, geom = "text", fun.y = median, colour = "red") +
  stat_summary(fun.data = median.n, geom = "text", fun.y = median)+
  theme(# for OS X (XQuartz device) to show Chinese characters
    text=element_text(family='Heiti TC Light'), 
    # rotate angle of x ticks
    axis.text.x=element_text(size=14, hjust=1, vjust=.5,color="black"),
    axis.text.y=element_text(size=14,color="#2c9893"),
    # change size of title
    plot.title=element_text(size=26)) 
  


