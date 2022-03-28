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
library(RColorBrewer)
display.brewer.all()  #显示所有可用颜色
brewer.pal(4,"RdYlGn")


# NJ9108
solute_df1 = read.csv('main_result/field1_solutedata.csv')
fig1 = ggplot(solute_df1)+
  geom_line(aes(das,solute_uptake))+
  mytheme

solute_df10 = read.csv('main_result/field10_solutedata.csv')
fig10 = ggplot(solute_df10)+
  geom_line(aes(das,solute_uptake))+
  mytheme

solute_df13_1 = read.csv('main_result/field13_1_solutedata.csv')
fig13_1 = ggplot(solute_df13_1)+
  geom_line(aes(das,solute_uptake))+
  mytheme

solute_df13_2 = read.csv('main_result/field13_2_solutedata.csv')
fig13_2 = ggplot(solute_df13_2)+
  geom_line(aes(das,solute_uptake))+
  mytheme

solute_df13_3 = read.csv('main_result/field13_3_solutedata.csv')
fig13_3 = ggplot(solute_df13_3)+
  geom_line(aes(das,solute_uptake))+
  mytheme

solute_df13_4 = read.csv('main_result/field13_4_solutedata.csv')
fig13_4 = ggplot(solute_df13_4)+
  geom_line(aes(das,solute_uptake))+
  mytheme

solute_df14 = read.csv('main_result/field14_solutedata.csv')
fig14 = ggplot(solute_df14)+
  geom_line(aes(das,solute_uptake))+
  mytheme


#  hhz
solute_df2 = read.csv('main_result/field2_solutedata.csv')
fig2 = ggplot(solute_df2)+
  geom_line(aes(das,solute_uptake))+
  mytheme

solute_df3 = read.csv('main_result/field3_solutedata.csv')
fig3 = ggplot(solute_df3)+
  geom_line(aes(das,solute_uptake))+
  mytheme

solute_df4 = read.csv('main_result/field4_solutedata.csv')
fig4 = ggplot(solute_df4)+
  geom_line(aes(das,solute_uptake))+
  mytheme

solute_df5 = read.csv('main_result/field5_solutedata.csv')
fig5 = ggplot(solute_df5)+
  geom_line(aes(das,solute_uptake))+
  mytheme

solute_df6 = read.csv('main_result/field6_solutedata.csv')
fig6 = ggplot(solute_df6)+
  geom_line(aes(das,solute_uptake))+
  mytheme

# 99-25
solute_df7 = read.csv('main_result/field7_solutedata.csv')
fig7 = ggplot(solute_df7)+
  geom_line(aes(das,solute_uptake))+
  mytheme

solute_df8 = read.csv('main_result/field8_solutedata.csv')
fig8 = ggplot(solute_df8)+
  geom_line(aes(das,solute_uptake))+
  mytheme

solute_df9 = read.csv('main_result/field9_solutedata.csv')
fig9 = ggplot(solute_df9)+
  geom_line(aes(das,solute_uptake))+
  mytheme

solute_df11 = read.csv('main_result/field11_solutedata.csv')
fig11 = ggplot(solute_df11)+
  geom_line(aes(das,solute_uptake))+
  mytheme

solute_df12= read.csv('main_result/field12_solutedata.csv')
fig12 = ggplot(solute_df12)+
  geom_line(aes(das,solute_uptake))+
  mytheme



zn_handle = read.csv('zn_handle.csv')



melt_df2 = melt(solute_df2,id.vars='das',variable.name='type',value.name = 'value')
melt_df2$field='2'
melt_df3 = melt(solute_df3,id.vars='das',variable.name='type',value.name = 'value')
melt_df3$field='3'
melt_df4 = melt(solute_df4,id.vars='das',variable.name='type',value.name = 'value')
melt_df4$field='4'
melt_df5 = melt(solute_df5,id.vars='das',variable.name='type',value.name = 'value')
melt_df5$field='5'
melt_df6 = melt(solute_df6,id.vars='das',variable.name='type',value.name = 'value')
melt_df6$field='6'
xd_df = rbind(melt_df2,melt_df3,melt_df4,melt_df5,melt_df6)
xd_df$value = xd_df$value*10000*666.67/1000
xd_df = left_join(xd_df,zn_handle,by='field')
xd_df$soil_zn = factor(xd_df$soil_zn,levels = c(0,1,2,3))
xd_df$sprinkle_zn = factor(xd_df$sprinkle_zn,levels = c(0,3))
xd_df_day = subset(xd_df,type == 'solute_uptake')
xd_df_all = subset(xd_df,type == 'all_solute_uptake')
fig_xdzn = ggplot(xd_df_day ,aes(das,value,color=soil_zn))+
  geom_line(aes(linetype=zn_type,size=sprinkle_zn))+
  mytheme+
  scale_color_brewer(palette = 'RdYlGn')+
  labs(x='DAS(d)',y='Absorbed Zn(g/mu)',color='Soil Zn',size='Sprinkle Zn',linetype="Zn type")+
  scale_size_manual(values=c(0.2,0.4))+
  scale_linetype_manual(values=c('solid'))+
  scale_color_manual(values=c("#D7191C", "#FDAE61", "#A6D96A", "#1A9641"))+
  ylim(0,1.2)+
  xlim(0,150)
fig_xdzn
fig_xdznall = ggplot(xd_df_all ,aes(das,value,color =soil_zn))+
  geom_line(aes(linetype=zn_type,size=sprinkle_zn))+
  mytheme+
  scale_color_brewer(palette = 'RdYlGn')+
  labs(x='DAS(d)',y='Absorbed Zn(g/mu)',color='Soil Zn',size='Sprinkle Zn',linetype="Zn type")+
  scale_size_manual(values=c(0.2,0.4))+
  scale_linetype_manual(values=c('solid'))+
  scale_color_manual(values=c("#D7191C", "#FDAE61", "#A6D96A", "#1A9641"))+
  xlim(0,150)+
  ylim(0,60)
fig_xdznall
drawpdf(fig_xdzn,"籼稻每日吸锌速率",6,4)
drawpdf(fig_xdznall,"籼稻吸锌量",6,4)


# --------------------nj9108
meltdf = function(solute_df2,field){
  melt_df2 = melt(solute_df2,id.vars='das',variable.name='type',value.name = 'value')
  melt_df2$field=field
  return(melt_df2)
}
melt_df1 = meltdf(solute_df1,'1')
melt_df10 = meltdf(solute_df10,'10')
melt_df13_1 = meltdf(solute_df13_1,'13_1')
melt_df13_2 = meltdf(solute_df13_2,'13_2')
melt_df13_3 = meltdf(solute_df13_3,'13_3')
melt_df13_4 = meltdf(solute_df13_4,'13_4')
melt_df14 = meltdf(solute_df14,'14')
jd_df = rbind(melt_df1,melt_df10,melt_df13_1,melt_df13_2,melt_df13_3,melt_df13_4,melt_df14)
jd_df$value = jd_df$value*10000*666.67/1000
jd_df = left_join(jd_df,zn_handle,by='field')
jd_df$soil_zn = factor(jd_df$soil_zn,levels = c(0,1,2,3))
jd_df$sprinkle_zn = factor(jd_df$sprinkle_zn,levels = c(0,3))
jd_df$zn_type =factor(jd_df$zn_type,levels = c('znso4','EDTA','Sugar alcohol zinc'))
jd_df_day = subset(jd_df,type == 'solute_uptake')
jd_df_all = subset(jd_df,type == 'all_solute_uptake')
fig_jdzn = ggplot(jd_df_day ,aes(das,value,color=soil_zn))+
  geom_line(aes(linetype=zn_type,size=sprinkle_zn))+
  mytheme+
  scale_color_brewer(palette = 'RdYlGn')+
  labs(x='DAS(d)',y='Absorbed Zn(g/mu)',color='Soil Zn',size='Sprinkle Zn',linetype="Zn type")+
  scale_size_manual(values=c(0.2,0.4))+
  scale_linetype_manual(values=c('solid','dashed','dotdash'))+
  scale_color_manual(values=c("#D7191C",  "#A6D96A", "#1A9641"))+
  ylim(0,1.2)+
  xlim(0,150)
fig_jdzn
fig_jdznall = ggplot(jd_df_all ,aes(das,value,color =soil_zn))+
  geom_line(aes(linetype=zn_type,size=sprinkle_zn))+
  mytheme+
  scale_color_brewer(palette = 'RdYlGn')+
  labs(x='DAS(d)',y='Absorbed Zn(g/mu)',color='Soil Zn',size='Sprinkle Zn',linetype="Zn type")+
  scale_size_manual(values=c(0.2,0.4))+
  scale_linetype_manual(values=c('solid','dashed','dotdash'))+
  scale_color_manual(values=c("#D7191C",  "#A6D96A", "#1A9641"))+
  xlim(0,150)+
  ylim(0,60)
fig_jdznall
drawpdf(fig_jdzn,"粳稻每日吸锌速率",6,4)
drawpdf(fig_jdznall,"粳稻吸锌量",6,4)


# ----------------99-25-------------------
melt_df7 = meltdf(solute_df7,'7')
melt_df8 = meltdf(solute_df8,'8')
melt_df9 = meltdf(solute_df9,'9')
melt_df11 = meltdf(solute_df11,'11')
melt_df12 = meltdf(solute_df12,'12')
nd_df = rbind(melt_df7,melt_df8,melt_df9,melt_df11,melt_df12)
nd_df$value = nd_df$value*10000*666.67/1000
nd_df = left_join(nd_df,zn_handle,by='field')
nd_df$soil_zn = factor(nd_df$soil_zn,levels = c(0,1,2,3))
nd_df$sprinkle_zn = factor(nd_df$sprinkle_zn,levels = c(0,3))
nd_df_day = subset(nd_df,type == 'solute_uptake')
nd_df_all = subset(nd_df,type == 'all_solute_uptake')
fig_ndzn = ggplot(nd_df_day ,aes(das,value,color=soil_zn))+
  geom_line(aes(linetype=zn_type,size=sprinkle_zn))+
  mytheme+
  scale_color_brewer(palette = 'RdYlGn')+
  labs(x='DAS(d)',y='Absorbed Zn(g/mu)',color='Soil Zn',size='Sprinkle Zn',linetype="Zn type")+
  scale_size_manual(values=c(0.2,0.4))+
  scale_linetype_manual(values=c('solid'))+
  scale_color_manual(values=c("#D7191C", "#FDAE61", "#A6D96A", "#1A9641"))+
  ylim(0,1.2)+
  xlim(0,150)
fig_ndzn
fig_ndznall = ggplot(nd_df_all ,aes(das,value,color =soil_zn))+
  geom_line(aes(linetype=zn_type,size=sprinkle_zn))+
  mytheme+
  scale_color_brewer(palette = 'RdYlGn')+
  labs(x='DAS(d)',y='Absorbed Zn(g/mu)',color='Soil Zn',size='Sprinkle Zn',linetype="Zn type")+
  scale_size_manual(values=c(0.2,0.4))+
  scale_linetype_manual(values=c('solid'))+
  scale_color_manual(values=c("#D7191C", "#FDAE61", "#A6D96A", "#1A9641"))+
  xlim(0,150)+
  ylim(0,60)
fig_ndznall
drawpdf(fig_ndzn,"糯稻每日吸锌速率",6,4)
drawpdf(fig_ndznall,"糯稻吸锌量",6,4)



common_legend = get_legend(fig_jdznall)
figzn = ggarrange(fig_xdzn,fig_ndzn,fig_jdzn,ncol = 3,nrow=1,
                  labels =c("(a)","(b)","(c)"),
                  common.legend = T,legend = "right",legend.grob=common_legend)
figzn
drawpdf(figzn,"三种水稻每日吸锌速率",10,3.5)
figznall = ggarrange(fig_xdznall,fig_ndznall,fig_jdznall,ncol = 3,nrow=1,
                  labels =c("(a)","(b)","(c)"),
                  common.legend = T,legend = "right",legend.grob=common_legend)
figznall
drawpdf(figznall,"三种水稻吸锌量",10,3.5)


# ---------------查看为什么没有EDTA的线--------------
chakan = subset(jd_df,field=='13_3'|field=='13_2')
chakan = subset(chakan,type=='solute_uptake')

ggplot(chakan,aes(das,value,color=field))+
  geom_line()






