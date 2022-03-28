library(ggplot2);library(reshape2);library(dplyr);library(scales);library(ggpubr)
mytheme = theme_bw()+theme(
  #panel.grid.major = element_blank(),
  #panel.grid.minor = element_blank(),
  axis.title = element_text(face = 'bold'),
  axis.text = element_text(face = 'bold'),
  legend.title = element_text(face = 'bold'),
  legend.text = element_text(face = 'bold'),
  legend.position = 'right',
  text = element_text( face = 'bold'),  
)
drawpdf=function(fig,figname,widthl,heightl){
  fignamepdf = paste(figname,'.pdf',sep="")
  pdf(fignamepdf,width =widthl,height = heightl)
  print(fig)
  dev.off()
  ppi=300
  fignamepng = paste(figname,'.png',sep="")
  png(fignamepng,width =widthl*ppi,height = heightl*ppi,res = ppi)
  print(fig)
  dev.off()
}

# ----------------------数据读取-------------------------
fieldlist = c('1','2','3','4','5','6','7','8','9','10','11','12','13_1','13_2',
              '13_3','13_4','14')
tran = function(fieldlist){
  filepathlist=c()
  for (i in fieldlist){
  filepath = paste('main_result//','field',i,'_sumZnbotdata.csv',sep='')
  print(filepath)
  filepathlist = c(filepathlist,filepath)
}  
  return(filepathlist)
}
filepathlist = tran(fieldlist)

field1 = read.csv(filepathlist[1])
field2 = read.csv(filepathlist[2])
field3 = read.csv(filepathlist[3])
field4 = read.csv(filepathlist[4])
field5 = read.csv(filepathlist[5])
field6 = read.csv(filepathlist[6])
field7 = read.csv(filepathlist[7])
field8 = read.csv(filepathlist[8])
field9 = read.csv(filepathlist[9])
field10 = read.csv(filepathlist[10])
field11 = read.csv(filepathlist[11])
field12 = read.csv(filepathlist[12])
field13_1 = read.csv(filepathlist[13])
field13_2 = read.csv(filepathlist[14])
field13_3 = read.csv(filepathlist[15])
field13_4 = read.csv(filepathlist[16])
field14 = read.csv(filepathlist[17])


field1 = melt(field1 ,id.vars='day',variable.name='type',value.name = 'value')
field1$field = '1'
field2 = melt(field2 ,id.vars='day',variable.name='type',value.name = 'value')
field2$field = '2'
field3 = melt(field3 ,id.vars='day',variable.name='type',value.name = 'value')
field3$field = '3'
field4 = melt(field4 ,id.vars='day',variable.name='type',value.name = 'value')
field4$field = '4'
field5 = melt(field5 ,id.vars='day',variable.name='type',value.name = 'value')
field5$field = '5'
field6 = melt(field6 ,id.vars='day',variable.name='type',value.name = 'value')
field6$field = '6'
field7 = melt(field7 ,id.vars='day',variable.name='type',value.name = 'value')
field7$field = '7'
field8 = melt(field8 ,id.vars='day',variable.name='type',value.name = 'value')
field8$field = '8'
field9 = melt(field9 ,id.vars='day',variable.name='type',value.name = 'value')
field9$field = '9'
field10 = melt(field10 ,id.vars='day',variable.name='type',value.name = 'value')
field10$field = '10'
field11 = melt(field11 ,id.vars='day',variable.name='type',value.name = 'value')
field11$field = '11'
field12 = melt(field12 ,id.vars='day',variable.name='type',value.name = 'value')
field12$field = '12'
field13_1 = melt(field13_1 ,id.vars='day',variable.name='type',value.name = 'value')
field13_1$field = '13_1'
field13_2 = melt(field13_2 ,id.vars='day',variable.name='type',value.name = 'value')
field13_2$field = '13_2'
field13_3 = melt(field13_3 ,id.vars='day',variable.name='type',value.name = 'value')
field13_3$field = '13_3'
field13_4 = melt(field13_4 ,id.vars='day',variable.name='type',value.name = 'value')
field13_4$field = '13_4'
field14 = melt(field14 ,id.vars='day',variable.name='type',value.name = 'value')
field14$field = '14'
df = rbind(field1,field2,field3,field4,field5,
           field6,field7,field8,field9,field10,
           field11,field12,field13_1,field13_2,field13_3,
           field13_4,field14)
df$value = df$value*10000*666.67/1000
zn_handle = read.csv('zn_handle.csv')
df = left_join(df,zn_handle,by='field')
rice_type = read.csv('rice_type.csv')
df = left_join(df,rice_type,by='field')

# -----------------开始处理数据--------------------
xddf = subset(df, rice_type=='黄华占')
xddfday = subset(xddf,type=='sumZnbot')
figxdznday = ggplot(xddfday,aes(day,value,color=field))+
  geom_line()+
  facet_grid(.~field)+
  mytheme+
  scale_y_reverse()+
  xlim(0,150)+
  ylim(0,-25)+
  scale_color_brewer(palette = 'Set2')+
  labs(x='DAS(d)',y='Cum Bottom Zn(g/mu)')
figxdznday


nddf = subset(df, rice_type=='99-25')
nddfday = subset(nddf,type=='sumZnbot')
figndznday = ggplot(nddfday,aes(day,value,color=field))+
  geom_line()+
  facet_grid(.~field)+
  mytheme+
  scale_y_reverse()+
  xlim(0,150)+
  ylim(0,-25)+
  labs(x='DAS(d)',y='Cum Bottom Zn(g/mu)')+
  scale_color_brewer(palette = 'Set2')
figndznday


jddf = subset(df, rice_type=='南粳9108')
jddfday = subset(jddf,type=='sumZnbot')
figjdznday = ggplot(jddfday,aes(day,value,color=field))+
  geom_line()+
  facet_grid(.~field)+
  mytheme+
  scale_y_reverse()+
  xlim(0,150)+
  ylim(0,-25)+
  scale_color_brewer(palette = 'Set2')+
  labs(x='DAS(d)',y='Cum Bottom Zn(g/mu)')
figjdznday

fig = ggarrange(figxdznday,figndznday,figjdznday,nrow = 3,ncol = 1,
                labels =c("(a)","(b)","(c)"),
                common.legend = F,legend = "right")
fig


drawpdf(fig,'三种水稻下边界锌元素流出量',12,7)









