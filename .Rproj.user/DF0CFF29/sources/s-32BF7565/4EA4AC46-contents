library(ggplot2);library(reshape2);library(dplyr);library(scales)
mytheme = theme_bw()+theme(
  #panel.grid.major = element_blank(),
  #panel.grid.minor = element_blank(),
  axis.title = element_text(face = 'bold'),
  axis.text = element_text(face = 'bold'),
  legend.title = element_text(face = 'plain'),
  legend.text = element_text(face = 'plain'),
  legend.position = 'right',
  text = element_text( face = 'plain'),
  
)

organ_df = read.csv('organ_znconc_df.csv')

# 锌浓度
# 整理数据
organ_df = read.csv('main_result/field1_zndata.csv')
concdf =subset(organ_df,select = c('day','ZRTC','ZSTC','ZLFC','ZERC'))
names(concdf) = c('das','Root','Stem','Leaf','Ear')
concdf = melt(concdf,id.vars = 'das',variable.name = 'position',value.name = 'conc')
ggplot(concdf,aes(das,conc,color=position))+
  geom_line()+
  mytheme
ggsave('figconc.png',width = 5,height = 4)

#锌含量
concdf =subset(organ_df,select = c('day','ZART','ZAST','ZALF','ZAER'))
names(concdf) = c('das','Root','Stem','Leaf','Ear')
concdf = melt(concdf,id.vars = 'das',variable.name = 'position',value.name = 'content')
ggplot(concdf,aes(das,content,color=position))+
  geom_line()+
  mytheme
ggsave('figcontent.png',width = 5,height = 4)

# 需锌和吸锌


tran = function(df){
  df = melt(df,id.vars = 'day',variable.name = 'zncontent_type',value.name = 'value')
  return(df)
}

field1_df =tran(read.csv('main_result/field1_zn_contentdata.csv')) 
field1_df$value = field1_df$value /15000
fig1_znneed = ggplot(field1_df)+
  geom_line(aes(day,value,color = zncontent_type))+
  mytheme
fig1_znneed

# 各器官锌浓度
field1conc_df =read.csv('main_result/field1_zndata.csv')
concdf =subset(field1conc_df,select = c('day','ZRTC','ZSTC','ZLFC','ZERC'))
names(concdf) = c('das','Root','Stem','Leaf','Ear')
concdf = melt(concdf,id.vars = 'das',variable.name = 'position',value.name = 'conc')
fig1_organ = ggplot(concdf,aes(das,conc,color=position))+
  geom_line()+
  mytheme
fig1_organ





