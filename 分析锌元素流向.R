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

tran = function(df){
  df = melt(df,id.vars = 'day',variable.name = 'zncontent_type',value.name = 'value')
  return(df)
}


# 首先，读取作物中锌元素的数据、土壤中的锌元素数据、下边界流出的锌元素数据
# ----------------------根据田块和天数来计算------------
field  = '1'


readreult = function(field){
  #先读取作物数据
  field1_df =read.csv('main_result/field1_zn_contentdata.csv')
}


# crop
field1crop_df = read.csv('main_result/field1_zndata.csv')
# soil
field1soil_df = read.csv('main_result/field1_soildata.csv')
# flow
field1flow_df = read.csv('main_result/field1_sumZnbotdata.csv')












