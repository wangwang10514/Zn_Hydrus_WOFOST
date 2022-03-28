library(ggplot2);library(reshape2);library(dplyr);library(scales);library(ggpubr);library(RColorBrewer)

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
conc_df1 = read.csv('main_result/field1_soildata.csv')
conc_df2 = read.csv('main_result/field2_soildata.csv')
conc_df3 = read.csv('main_result/field3_soildata.csv')
conc_df4 = read.csv('main_result/field4_soildata.csv')
conc_df5 = read.csv('main_result/field5_soildata.csv')
conc_df6 = read.csv('main_result/field6_soildata.csv')
conc_df7 = read.csv('main_result/field7_soildata.csv')
conc_df8 = read.csv('main_result/field8_soildata.csv')
conc_df9 = read.csv('main_result/field9_soildata.csv')
conc_df10 = read.csv('main_result/field10_soildata.csv')
conc_df11 = read.csv('main_result/field11_soildata.csv')
conc_df12 = read.csv('main_result/field12_soildata.csv')
conc_df13_1 = read.csv('main_result/field13_1_soildata.csv')
conc_df13_2 = read.csv('main_result/field13_2_soildata.csv')
conc_df13_3 = read.csv('main_result/field13_3_soildata.csv')
conc_df13_4 = read.csv('main_result/field13_4_soildata.csv')
conc_df14 = read.csv('main_result/field14_soildata.csv')
conc_df1$field = '1'
conc_df2$field = '2'
conc_df3$field = '3'
conc_df4$field = '4'
conc_df5$field = '5'
conc_df6$field = '6'
conc_df7$field = '7'
conc_df8$field = '8'
conc_df9$field = '9'
conc_df10$field = '10'
conc_df11$field = '11'
conc_df12$field = '12'
conc_df13_1$field = '13_1'
conc_df13_2$field = '13_2'
conc_df13_3$field = '13_3'
conc_df13_4$field = '13_4'
conc_df14$field = '14'


xddf = rbind(conc_df2,conc_df3,conc_df4,conc_df5,conc_df6)
xddf$rice_type = '黄华占'
nddf = rbind(conc_df7,conc_df8,conc_df9,conc_df11,conc_df12)
nddf$rice_type = '99-25'
jddf = rbind(conc_df1,conc_df10,conc_df13_1,conc_df13_2,conc_df13_3,
             conc_df13_4,conc_df14)
jddf$rice_type = '南粳9108'


# 选择展示天数
select_day = c(0,20,40,60,80,108)
selectday = function(df,day){
  day_colname_list = c()
  for (i in select_day){
    day_colname = paste( "day" , as.character(i) , "allconc",sep="")
    print(day_colname)
    day_colname_list = c(day_colname_list,day_colname)
  }
  day_colname_list = c(day_colname_list,'field')
  selectdf = subset(df,select = day_colname_list)
  selectdf$depth = c(0:100)
  selectdf$depth = selectdf$depth*3
  
  df = melt(selectdf,id.vars=c("depth",'field'),variable.name="day",value.name="conc")
  df = subset(df,depth<100)
  return(df)
}


peise = brewer.pal(9,'OrRd')
mycolor1 = peise[2:7]
mycolor2 = peise[2:9]
xddfsel = selectday(xddf,select_day)
figxd = ggplot(xddfsel,aes(depth,conc,color = day))+
  geom_line(alpha=0.8)+
  geom_vline(xintercept = 10)+
  geom_vline(xintercept = 20)+
  # geom_vline(xintercept = 60)+
  mytheme+ 
  coord_flip()+
  facet_grid(.~field)+
  scale_x_reverse()+
  scale_color_manual(values=mycolor1)+
  labs(x='depth(cm)',y='Zn concertration(mg/kg)')
figxd
# drawpdf(figxd,'籼稻的土壤剖面锌含量',12,3)

select_day = c(0,20,40,60,80,100,120,147)
nddfsel = selectday(nddf,select_day)
fignd = ggplot(nddfsel,aes(depth,conc,color = day))+
  geom_line(alpha=0.8)+
  geom_vline(xintercept = 10)+
  geom_vline(xintercept = 20)+
  # geom_vline(xintercept = 60)+
  mytheme+ 
  coord_flip()+
  facet_grid(.~field)+
  scale_x_reverse()+
  scale_color_manual(values=mycolor2)+
  labs(x='depth(cm)',y='Zn concertration(mg/kg)')
fignd
# drawpdf(fignd,'糯稻的土壤剖面锌含量',12,3)

select_day = c(0,20,40,60,80,100,120,147)
jddfsel = selectday(jddf,select_day)
figjd = ggplot(jddfsel,aes(depth,conc,color = day))+
  geom_line(alpha=0.8)+
  geom_vline(xintercept = 10)+
  geom_vline(xintercept = 20)+
  # geom_vline(xintercept = 60)+
  mytheme+ 
  coord_flip()+
  facet_grid(.~field)+
  scale_x_reverse()+
  scale_color_manual(values=mycolor2)+
  labs(x='depth(cm)',y='Zn concertration(mg/kg)')
figjd
# drawpdf(figjd,'粳稻的土壤剖面锌含量',12,3)



result =ggarrange(figxd,fignd,figjd,ncol = 1,nrow=3,
                  labels =c("(a)","(b)","(c)"),
                  common.legend = F,legend = "right")
drawpdf(result ,'三种水稻的土壤剖面锌含量',12,9)


