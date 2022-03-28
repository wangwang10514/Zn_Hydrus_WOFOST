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
sentotal_df = read.csv('simlab/zn_sen_resultXGquanju.csv')
senfirst_df = read.csv('simlab/zn_sen_resultXGyijie.csv')
sentotal_df$type = 'total_order'
senfirst_df$type = 'first_order'
df = rbind(sentotal_df,senfirst_df)
df = melt(df,id.vars = c('PARA','type'),variable.name = 'goal',value.name = 'value')

seldf = subset(df,goal=='ZRTC'|goal=='ZSTC'|goal=='ZLFC'|goal=='ZERC')






Zn_sen = ggplot(seldf,aes(PARA,value,fill=type))+
  geom_bar(position = 'dodge',stat='identity',width = 0.7)+
  mytheme+
  scale_fill_brewer(palette = 'RdYlGn')+
  labs(x='Parameters',y='Sensitivity',fill="Sensitivity type")+
  scale_fill_brewer(palette = 'Set2')+ 
  theme(axis.text.x = element_text(angle = 45, hjust = 1))+
  facet_grid(goal~.)
Zn_sen
ggsave("Zn_sen.png",width = 12,height=8)



pdf("Zn_sen.pdf",width = 12,height=8)
Zn_sen
dev.off()








