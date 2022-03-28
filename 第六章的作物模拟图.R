library(ggplot2);library(reshape2);library(dplyr);library(scales)
library(lmtest)
library(hydroGOF)
library(patchwork)
library(ggpubr)
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

# 作物数据
# 读取模拟数据
field_list = c('1','2','3','4','5','6','7','8','9','10','11','12','13_1',
               '13_2','13_3','13_4','14')
xdsimdf = read.csv('main_result/field2_cropdata.csv')
ndsimdf = read.csv('main_result/field7_cropdata.csv')
jdsimdf = read.csv('main_result/field1_cropdata.csv')
xdsimdf$day = as.Date(xdsimdf$day)
xdsimdf$das = xdsimdf$day-as.Date('2020-5-30')+1
ndsimdf$day = as.Date(ndsimdf$day)
ndsimdf$das = ndsimdf$day-as.Date('2020-5-30')+1
jdsimdf$day = as.Date(jdsimdf$day)
jdsimdf$das = jdsimdf$day-as.Date('2020-5-30')+1
xd2simdf = xdsimdf
xd3simdf = xdsimdf
xd4simdf = xdsimdf
xd5simdf = xdsimdf
xd6simdf = xdsimdf
xd2simdf$field = '2'
xd3simdf$field = '3'
xd4simdf$field = '4'
xd5simdf$field = '5'
xd6simdf$field = '6'
xdsumsimdf = rbind(xd2simdf,xd3simdf,xd4simdf,xd5simdf,xd6simdf)
nd7simdf = ndsimdf
nd8simdf = ndsimdf
nd9simdf = ndsimdf
nd11simdf = ndsimdf
nd12simdf = ndsimdf
nd7simdf$field = '7'
nd8simdf$field = '8'
nd9simdf$field = '9'
nd11simdf$field = '11'
nd12simdf$field = '12'
ndsumsimdf = rbind(nd7simdf,nd8simdf,nd9simdf,nd11simdf,nd12simdf)
jd1simdf = jdsimdf
jd10simdf = jdsimdf
jd13_1simdf = jdsimdf
jd13_2simdf = jdsimdf
jd13_3simdf = jdsimdf
jd13_4simdf = jdsimdf
jd14simdf = jdsimdf
jd1simdf$field = '1'
jd10simdf$field = '10'
jd13_1simdf$field = '13_1'
jd13_2simdf$field = '13_2'
jd13_3simdf$field = '13_3'
jd13_4simdf$field = '13_4'
jd14simdf$field = '14'
jdsumsimdf = rbind(jd1simdf,jd10simdf,jd13_1simdf,jd13_2simdf,jd13_3simdf,jd13_4simdf,jd14simdf)

# 读取原始数据
xddf = read.csv('清洗后的数据20220218/籼稻干重.csv')
names(xddf) = c('field','repeatt','2020/6/12','2020/6/21','2020/6/26',
                '2020/7/1','2020/7/6','2020/7/13','2020/7/20','2020/8/2',
                '2020/8/14','2020/8/25','type')
nddf = read.csv('清洗后的数据20220218/糯稻干重.csv')
names(nddf) = c('field','repeatt','2020/6/12','2020/6/21','2020/6/26',
                '2020/7/1','2020/7/6','2020/7/13','2020/7/20','2020/8/2',
                '2020/8/14','2020/8/25','2020/9/17','2020/10/23','type')
jddf = read.csv('清洗后的数据20220218/粳稻干重.csv')
names(jddf) = c('field','repeatt','2020/6/12','2020/6/21','2020/6/26',
                '2020/7/1','2020/7/6','2020/7/13','2020/7/20','2020/8/2',
                '2020/8/14','2020/8/25','2020/9/17','2020/10/23','type')
laidf = read.csv('清洗后的数据20220218/lai_remote_delnan.csv')
laidf =subset(laidf,select=c('date','filed','obs_lai'))
names(laidf) = c('date','field','obs_lai')
laidf$date = as.Date(laidf$date)
xdmeltdf = melt(xddf,id.vars = c('field','repeatt','type'),
                variable.name="date",value.name="weight")
ndmeltdf = melt(nddf,id.vars = c('field','repeatt','type'),
                variable.name="date",value.name="weight")
jdmeltdf = melt(jddf,id.vars = c('field','repeatt','type'),
                variable.name="date",value.name="weight")
xdmeltdf$rice_type = "黄华占"
ndmeltdf$rice_type = "99-25"
jdmeltdf$rice_type = "南粳9108"
ricedf = rbind(xdmeltdf,ndmeltdf,jdmeltdf)
zn_handle = read.csv('清洗后的数据20220218/zn_handle.csv')
ricedf = left_join(ricedf,zn_handle,by='field')
# ------预处理结束，开始正式处理------
df = ricedf
lfdf = subset(df,type=='叶干重',select=c('field','repeatt','date','weight','rice_type'))
names(lfdf) = c('field','repeatt','date','leaf_weight','rice_type')
stdf = subset(df,type=='茎干重',select=c('field','repeatt','date','weight','rice_type'))
names(stdf) = c('field','repeatt','date','stem_weight','rice_type')
erdf = subset(df,type=='穗干重',select=c('field','repeatt','date','weight','rice_type'))
names(erdf) = c('field','repeatt','date','ear_weight','rice_type')
aggdf = left_join(lfdf,stdf,by=c('field','repeatt','date','rice_type'))
aggdf = left_join(aggdf,erdf,by=c('field','repeatt','date','rice_type'))
aggdf = left_join(aggdf,zn_handle,by='field')
aggdf$date = as.Date(aggdf$date)
plant_density = read.csv('清洗后的数据20220218/plant_density.csv')
aggdf = left_join(aggdf,plant_density,by='field')
aggdf$leaf_weight_perha = aggdf$leaf_weight*aggdf$plant_density*10000/1000
aggdf$stem_weight_perha = aggdf$stem_weight*aggdf$plant_density*10000/1000
aggdf$ear_weight_perha = aggdf$ear_weight*aggdf$plant_density*10000/1000
aggdf = left_join(aggdf,laidf,by=c('date','field'))
myvars = c('leaf_weight_perha','stem_weight_perha','ear_weight_perha','obs_lai')
df = aggregate(aggdf[myvars],by=list(field = aggdf$field,date = aggdf$date), mean,na.rm=T)
df$total_weight_perha = df$leaf_weight_perha+df$stem_weight_perha+df$ear_weight_perha
rice_type = read.csv('main_result/real_data/rice_type.csv')
df = left_join(df,rice_type,by='field')
df$rice_type[df$rice_type=='籼稻'] = '黄华占'
df$rice_type[df$rice_type=='糯稻'] = '99-25'
df$rice_type[df$rice_type=='粳稻'] = '南粳9108'

# -----单位转化为ha--------
xddf = subset(df,rice_type=='黄华占')
xddf = xddf[order(xddf$field),]
xddf$DVS = c(0.3507 ,0.4551 ,0.5130 ,0.5710 ,0.6290 ,0.7101 ,0.7913,0.9420 ,1.1842,1.4737 )
nddf = subset(df,rice_type=='99-25')
nddf = nddf[order(nddf$field),]
nddf$DVS = c(0.3333,0.4256,0.4769,0.5282 ,0.5795 ,0.6513 ,0.7231 ,0.8564 ,0.9795 ,1.1324 ,1.4706,2.0000 )
jddf = subset(df,rice_type=='南粳9108')
jddf = jddf[order(jddf$field),]
jddf$DVS = c(0.3316 ,0.4228 ,0.4734 ,0.5241 ,0.5747 ,0.6456,0.7165 ,0.8481 ,0.9696,1.1194 ,1.4627,2.0000  )
xddf_py=xddf[,c("field","date","obs_lai","DVS",'total_weight_perha','ear_weight_perha',
                'leaf_weight_perha','stem_weight_perha')]
names(xddf_py) = c("field",'day',	'observed_lai',	'observed_DVS',	'observed_TAGP',
                   'observed_TWSO',	'observed_WLV',	'observed_TWST')
nddf_py=nddf[,c("field","date","obs_lai","DVS",'total_weight_perha','ear_weight_perha',
                'leaf_weight_perha','stem_weight_perha')]
names(nddf_py) = c("field",'day',	'observed_lai',	'observed_DVS',	'observed_TAGP',
                   'observed_TWSO',	'observed_WLV',	'observed_TWST')
jddf_py=jddf[,c("field","date","obs_lai","DVS",'total_weight_perha','ear_weight_perha',
                'leaf_weight_perha','stem_weight_perha')]
names(jddf_py) = c("field",'day',	'observed_lai',	'observed_DVS',	'observed_TAGP',
                   'observed_TWSO',	'observed_WLV',	'observed_TWST')


write.csv(xddf_py, file = "xddf_py.csv", row.names = FALSE)
write.csv(nddf_py, file = "nddf_py.csv", row.names = FALSE)
write.csv(jddf_py, file = "jddf_py.csv", row.names = FALSE)


# 开始画图
xddf = left_join(xdsumsimdf,xddf_py,by=c('day','field'))
xddf$das = as.integer(xddf$das)
nddf = left_join(ndsumsimdf,nddf_py,by=c('day','field'))
nddf$das = as.integer(nddf$das)
jddf = left_join(jdsumsimdf,jddf_py,by=c('day','field'))
jddf$das = as.integer(jddf$das)


# 我觉得应该只画散点图就行了
xddf = subset(xddf,observed_DVS!="NA")
nddf = subset(nddf,observed_DVS!="NA")
jddf = subset(jddf,observed_DVS!="NA")

xddf=xddf[,c("field","day",'das','DVS','LAI','TWST','WLV','TWSO','TAGP',
             'observed_DVS','observed_lai','observed_TWST','observed_WLV',
             'observed_TWSO','observed_TAGP')]
names(xddf) = c("field","day",'das','DVS','LAI','TWST','WLV','TWSO','TAGP',
                'obsDVS','obsLAI','obsTWST','obsWLV',
                'obsTWSO','obsTAGP')
nddf=nddf[,c("field","day",'das','DVS','LAI','TWST','WLV','TWSO','TAGP',
             'observed_DVS','observed_lai','observed_TWST','observed_WLV',
             'observed_TWSO','observed_TAGP')]
names(nddf) = c("field","day",'das','DVS','LAI','TWST','WLV','TWSO','TAGP',
                'obsDVS','obsLAI','obsTWST','obsWLV',
                'obsTWSO','obsTAGP')
jddf=jddf[,c("field","day",'das','DVS','LAI','TWST','WLV','TWSO','TAGP',
             'observed_DVS','observed_lai','observed_TWST','observed_WLV',
             'observed_TWSO','observed_TAGP')]
names(jddf) = c("field","day",'das','DVS','LAI','TWST','WLV','TWSO','TAGP',
                'obsDVS','obsLAI','obsTWST','obsWLV',
                'obsTWSO','obsTAGP')

evaluate_sim = function(seldf){
  # seldf = subset(df,obsLAI!='NA')
  
  r1=cor(seldf$DVS,seldf$obsDVS)
  r21=round(r1*r1,3)
  rmse1=round(rmse(seldf$DVS,seldf$obsDVS),3)
  nse1 = round(NSE(seldf$DVS,seldf$obsDVS),3)
  r2=cor(seldf$LAI,seldf$obsLAI)
  r22=round(r2*r2,3)
  rmse2=round(rmse(seldf$LAI,seldf$obsLAI),3)
  nse2 = round(NSE(seldf$LAI,seldf$obsLAI),3)
  r3=cor(seldf$TWST,seldf$obsTWST)
  r23=round(r3*r3,3)
  rmse3=round(rmse(seldf$TWST,seldf$obsTWST),3)
  nse3 = round(NSE(seldf$TWST,seldf$obsTWST),3)
  r4=cor(seldf$WLV,seldf$obsWLV)
  r24=round(r4*r4,3)
  rmse4=round(rmse(seldf$WLV,seldf$obsWLV),3)
  nse4 = round(NSE(seldf$WLV,seldf$obsWLV),3)
  r5=cor(seldf$TWSO,seldf$obsTWSO)
  r25=round(r5*r5,3)
  rmse5=round(rmse(seldf$TWSO,seldf$obsTWSO),3)
  nse5 = round(NSE(seldf$TWSO,seldf$obsTWSO),3)
  r6=cor(seldf$TAGP,seldf$obsTAGP)
  r26=round(r6*r6,3)
  rmse6=round(rmse(seldf$TAGP,seldf$obsTAGP),3)
  nse6 = round(NSE(seldf$TAGP,seldf$obsTAGP),3)
  
  label11 = paste("R^2:",r21)
  label12 = paste("RMSE:",rmse1)
  label13 = paste("NSE:",nse1)
  label21 = paste("R^2:",r22)
  label22 = paste("RMSE:",rmse2)
  label23 = paste("NSE:",nse2)
  label31 = paste("R^2:",r23)
  label32 = paste("RMSE:",rmse3)
  label33 = paste("NSE:",nse3)
  label41 = paste("R^2:",r24)
  label42 = paste("RMSE:",rmse4)
  label43 = paste("NSE:",nse4)
  label51 = paste("R^2:",r25)
  label52 = paste("RMSE:",rmse5)
  label53 = paste("NSE:",nse5)
  label61 = paste("R^2:",r26)
  label62 = paste("RMSE:",rmse6)
  label63 = paste("NSE:",nse6)
  fig1 = ggplot(seldf,aes(obsDVS,DVS))+
    geom_point(aes(color = field),position = 'jitter')+
    stat_smooth(method = lm)+
    mytheme+
    coord_fixed()+
    xlim(0,2)+
    ylim(0,2)+
    labs(x='obsDVS',y="simDVS")+
    scale_color_brewer(palette = 'Set2')
  fig1
  fig2 = ggplot(seldf,aes(obsLAI,LAI))+
    geom_point(aes(color = field),position = 'jitter')+
    stat_smooth(method = lm)+
    mytheme+
    coord_fixed()+
    xlim(0,6)+
    ylim(0,6)+
    labs(x='obsLAI',y="simLAI")+
    scale_color_brewer(palette = 'Set2')
  fig2
  fig3 = ggplot(seldf,aes(obsTWST,TWST))+
    geom_point(aes(color = field),position = 'jitter')+
    stat_smooth(method = lm)+
    mytheme+
    coord_fixed()+
    xlim(0,6000)+
    ylim(0,6000)+
    labs(x='obsTWST(kg/ha)',y="simTWST(kg/ha)")+
    scale_color_brewer(palette = 'Set2')
  fig3
  fig4 = ggplot(seldf,aes(obsWLV,WLV))+
    geom_point(aes(color = field),position = 'jitter')+
    stat_smooth(method = lm)+
    mytheme+
    coord_fixed()+
    xlim(0,4000)+
    ylim(0,4000)+
    labs(x='obsWLV(kg/ha)',y="simWLV(kg/ha)")+
    scale_color_brewer(palette = 'Set2')
  fig4
  fig5 = ggplot(seldf,aes(obsTWSO,TWSO))+
    geom_point(aes(color = field),position = 'jitter')+
    stat_smooth(method = lm)+
    mytheme+
    coord_fixed()+
    xlim(0,7500)+
    ylim(0,7500)+
    labs(x='obsTWSO(kg/ha)',y="simTWSO(kg/ha)")+
    scale_color_brewer(palette = 'Set2')
  fig5
  fig6 = ggplot(seldf,aes(obsTAGP,TAGP))+
    geom_point(aes(color = field),position = 'jitter')+
    stat_smooth(method = lm)+
    mytheme+
    coord_fixed()+
    xlim(0,16000)+
    ylim(0,16000)+
    labs(x='obsTAGP(kg/ha)',y="simTAGP(kg/ha)")+
    scale_color_brewer(palette = 'Set2')
  fig6
  layout <- '
ABC
DEF
'
  result =fig1+fig2+fig3+fig4+fig5+fig6+ plot_layout(design = layout)+ plot_annotation(tag_levels = 'A')
  
  return(result)
}

evaluate_fun = function(seldf){
  r1=cor(seldf$DVS,seldf$obsDVS)
  r21=round(r1*r1,3)
  rmse1=round(rmse(seldf$DVS,seldf$obsDVS),3)
  nse1 = round(NSE(seldf$DVS,seldf$obsDVS),3)
  r2=cor(seldf$LAI,seldf$obsLAI,use="complete.obs")
  r22=round(r2*r2,3)
  rmse2=round(rmse(seldf$LAI,seldf$obsLAI),3)
  nse2 = round(NSE(seldf$LAI,seldf$obsLAI),3)
  r3=cor(seldf$TWST,seldf$obsTWST)
  r23=round(r3*r3,3)
  rmse3=round(rmse(seldf$TWST,seldf$obsTWST),3)
  nse3 = round(NSE(seldf$TWST,seldf$obsTWST),3)
  r4=cor(seldf$WLV,seldf$obsWLV)
  r24=round(r4*r4,3)
  rmse4=round(rmse(seldf$WLV,seldf$obsWLV),3)
  nse4 = round(NSE(seldf$WLV,seldf$obsWLV),3)
  r5=cor(seldf$TWSO,seldf$obsTWSO)
  r25=round(r5*r5,3)
  rmse5=round(rmse(seldf$TWSO,seldf$obsTWSO),3)
  nse5 = round(NSE(seldf$TWSO,seldf$obsTWSO),3)
  r6=cor(seldf$TAGP,seldf$obsTAGP)
  r26=round(r6*r6,3)
  rmse6=round(rmse(seldf$TAGP,seldf$obsTAGP),3)
  nse6 = round(NSE(seldf$TAGP,seldf$obsTAGP),3)
  evaluate_re = data.frame(
    r2 = c(r21,r22,r23,r24,r25,r26),
    rmse= c(rmse1,rmse2,rmse3,rmse4,rmse5,rmse6),
    nse= c(nse1,nse2,nse3,nse4,nse5,nse6)
  )
  return(evaluate_re )
}




ggarange_draw = function(seldf){
  # seldf = subset(df,obsLAI!='NA')
  
  r1=cor(seldf$DVS,seldf$obsDVS)
  r21=round(r1*r1,3)
  rmse1=round(rmse(seldf$DVS,seldf$obsDVS),3)
  nse1 = round(NSE(seldf$DVS,seldf$obsDVS),3)
  r2=cor(seldf$LAI,seldf$obsLAI)
  r22=round(r2*r2,3)
  rmse2=round(rmse(seldf$LAI,seldf$obsLAI),3)
  nse2 = round(NSE(seldf$LAI,seldf$obsLAI),3)
  r3=cor(seldf$TWST,seldf$obsTWST)
  r23=round(r3*r3,3)
  rmse3=round(rmse(seldf$TWST,seldf$obsTWST),3)
  nse3 = round(NSE(seldf$TWST,seldf$obsTWST),3)
  r4=cor(seldf$WLV,seldf$obsWLV)
  r24=round(r4*r4,3)
  rmse4=round(rmse(seldf$WLV,seldf$obsWLV),3)
  nse4 = round(NSE(seldf$WLV,seldf$obsWLV),3)
  r5=cor(seldf$TWSO,seldf$obsTWSO)
  r25=round(r5*r5,3)
  rmse5=round(rmse(seldf$TWSO,seldf$obsTWSO),3)
  nse5 = round(NSE(seldf$TWSO,seldf$obsTWSO),3)
  r6=cor(seldf$TAGP,seldf$obsTAGP)
  r26=round(r6*r6,3)
  rmse6=round(rmse(seldf$TAGP,seldf$obsTAGP),3)
  nse6 = round(NSE(seldf$TAGP,seldf$obsTAGP),3)
  
  label11 = paste("R^2:",r21)
  label12 = paste("RMSE:",rmse1)
  label13 = paste("NSE:",nse1)
  label21 = paste("R^2:",r22)
  label22 = paste("RMSE:",rmse2)
  label23 = paste("NSE:",nse2)
  label31 = paste("R^2:",r23)
  label32 = paste("RMSE:",rmse3)
  label33 = paste("NSE:",nse3)
  label41 = paste("R^2:",r24)
  label42 = paste("RMSE:",rmse4)
  label43 = paste("NSE:",nse4)
  label51 = paste("R^2:",r25)
  label52 = paste("RMSE:",rmse5)
  label53 = paste("NSE:",nse5)
  label61 = paste("R^2:",r26)
  label62 = paste("RMSE:",rmse6)
  label63 = paste("NSE:",nse6)
  fig1 = ggplot(seldf,aes(obsDVS,DVS))+
    geom_point(aes(color = field),position = 'jitter')+
    stat_smooth(method = lm)+
    mytheme+
    coord_fixed()+
    xlim(0,2)+
    ylim(0,2)+
    labs(x='obsDVS',y="simDVS",color="Field")+
    scale_color_brewer(palette = 'Set2')
  fig1
  fig2 = ggplot(seldf,aes(obsLAI,LAI))+
    geom_point(aes(color = field),position = 'jitter')+
    stat_smooth(method = lm)+
    mytheme+
    coord_fixed()+
    xlim(0,6)+
    ylim(0,6)+
    labs(x='obsLAI',y="simLAI",color="Field")+
    scale_color_brewer(palette = 'Set2')
  fig2
  fig3 = ggplot(seldf,aes(obsTWST,TWST))+
    geom_point(aes(color = field),position = 'jitter')+
    stat_smooth(method = lm)+
    mytheme+
    coord_fixed()+
    xlim(0,6000)+
    ylim(0,6000)+
    labs(x='obsTWST(kg/ha)',y="simTWST(kg/ha)",color="Field")+
    scale_color_brewer(palette = 'Set2')
  fig3
  fig4 = ggplot(seldf,aes(obsWLV,WLV))+
    geom_point(aes(color = field),position = 'jitter')+
    stat_smooth(method = lm)+
    mytheme+
    coord_fixed()+
    xlim(0,4000)+
    ylim(0,4000)+
    labs(x='obsWLV(kg/ha)',y="simWLV(kg/ha)",color="Field")+
    scale_color_brewer(palette = 'Set2')
  fig4
  fig5 = ggplot(seldf,aes(obsTWSO,TWSO))+
    geom_point(aes(color = field),position = 'jitter')+
    stat_smooth(method = lm)+
    mytheme+
    coord_fixed()+
    xlim(0,7500)+
    ylim(0,7500)+
    labs(x='obsTWSO(kg/ha)',y="simTWSO(kg/ha)",color="Field")+
    scale_color_brewer(palette = 'Set2')
  fig5
  fig6 = ggplot(seldf,aes(obsTAGP,TAGP))+
    geom_point(aes(color = field),position = 'jitter')+
    stat_smooth(method = lm)+
    mytheme+
    coord_fixed()+
    xlim(0,16000)+
    ylim(0,16000)+
    labs(x='obsTAGP(kg/ha)',y="simTAGP(kg/ha)",color="Field")+
    scale_color_brewer(palette = 'Set2')
  fig6
  
  result =ggarrange(fig1,fig2,fig3,fig4,fig5,fig6,ncol = 3,nrow=2,
                    labels =c("(a)","(b)","(c)","(d)","(e)","(f)"),
                    common.legend = T,legend = "right")
  
  return(result)
}






pdf('评价hhz模拟效果.pdf',width=10,height=6)
xdevfig = evaluate_sim(xddf)
xdevfig  
dev.off()
pdf('评价hhz模拟效果1.pdf',width=10,height=7)
xdevfig = ggarange_draw(xddf)
xdevfig  
dev.off()
xdevfigdata = evaluate_fun(xddf)
xdevfigdata

pdf('评价9925模拟效果.pdf',width=10,height=6)
ndevfig = evaluate_sim(nddf)
ndevfig  
dev.off()
pdf('评价9925模拟效果1.pdf',width=10,height=7)
ndevfig = ggarange_draw(nddf)
ndevfig  
dev.off()
ndevfigdata = evaluate_fun(nddf)
ndevfigdata


pdf('评价nj9108模拟效果.pdf',width=10,height=6)
jdevfig = evaluate_sim(jddf)
jdevfig  
dev.off()
pdf('评价nj9108模拟效果1.pdf',width=10,height=7)
jdevfig = ggarange_draw(jddf)
jdevfig  
dev.off()
jdevfigdata = evaluate_fun(jddf)
jdevfigdata







