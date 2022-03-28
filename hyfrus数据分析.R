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
sentotal_df = read.csv('simlab/sen_result_total.csv')
senfirst_df = read.csv('simlab/sen_result_first.csv')
sentotal_df = melt(sentotal_df,id.vars = 'para',variable.name = 'goal',value.name = 'value')
senfirst_df = melt(senfirst_df,id.vars = 'para',variable.name = 'goal',value.name = 'value')
sentotal_df$type = 'total_order'
senfirst_df$type = 'first_order'
df = rbind(sentotal_df,senfirst_df)
Total_order_sensitivity = ggplot(sentotal_df,aes(goal,value,fill=para))+
  geom_bar(position = 'dodge',stat='identity',width = 0.7)+
  mytheme+
  scale_fill_brewer(palette = 'Set2')+
  labs(x='',y='Total order sensitivity',fill="Parameters")
# ggsave('Total order sensitivity.png',width=10,height=2.5)

pdf("Total_order_sensitivity .pdf",width=10,height=2.5)
Total_order_sensitivity 
dev.off()

First_order_sensitivity = ggplot(senfirst_df,aes(goal,value,fill=para))+
  geom_bar(position = 'dodge',stat='identity',width = 0.7)+
  mytheme+
  scale_fill_brewer(palette = 'Set2')+
  labs(x='',y='First order sensitivity',fill="Parameters")
# ggsave('First order sensitivity.png',width=10,height=2.5)

pdf("First_order_sensitivity.pdf",width=10,height=2.5)
First_order_sensitivity
dev.off()







