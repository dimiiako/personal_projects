q1
import pandas as pd, numpy as np
import csv
from datetime import datetime

#collect the data and order them by time of inspection date
#drop the  duplicates keeping the latest as the questions required
#
#
webextract = pd.read_csv('WebExtract.txt')
webextract['INSP_DATE'] = [pd.datetime.strptime(gd, "%Y-%m-%d %H:%M:%S") for gd in webextract['INSPDATE']]
sortedgrades = webextract.sort_values('INSP_DATE')
latestgrades = sortedgrades.drop_duplicates(subset = 'CAMIS', keep = 'last')
#keep the sipcode and the score
zips = latestgrades[["ZIPCODE", "SCORE"]]
#calculate the mean and std 
gzips = zips.groupby("ZIPCODE")
gzips_agg = gzips["SCORE"].agg({'mean': np.mean, 'std_dev': np.std, 'count': len})
gzips_agg['std_error'] = gzips_agg['std_dev']/np.sqrt(gzips_agg['count'])
final_gzips = gzips_agg.sort(columns = 'mean', ascending=False)
#keeping those with over 100 restaurants	
final_gzips = final_gzips[final_gzips['count'] > 100][["mean", "std_error", "count"]]

final_gzips.to_csv("rya1.csv", line_terminator="),(",quoting= csv.QUOTE_NONNUMERIC)

#
boro_names = pd.DataFrame({'boro_names' : pd.Series({1: "MANHATTAN", 2 : "THE BRONX", 3 : "BROOKLYN", 
                           4 : "QUEENS", 5 : "STATEN ISLAND"})} )
boro = latestgrades[['ZIPCODE', 'SCORE']].join(boro_names, on = ['BORO'])
_boro = boro.groupby('boro_names')

# do calculations per boro
boro_scores = g_boro['SCORE'].agg({'mean': np.mean, 'std_dev':np.std, 'count': len  })
boro_scores['std_error'] = boro_scores['std_dev']/np.sqrt(boro_scores['count'])
boro_scores = boro_scores[['mean', 'std_error', 'count']]

boro_score.to_csv('answertoboro.csv', line_terminator = '),(',quoting= csv.QUOTE_NONNUMERIC )






###########################question3

q4
webextract['INSP_DATE'] = [pd.datetime.strptime(gd, "%Y-%m-%d %H:%M:%S") for gd in webextract['INSPDATE']]
sortedgrades = webextract.sort_values('INSP_DATE')
latestgrades = sortedgrades.drop_duplicates(subset = 'CAMIS', keep = 'last')
#keep the sipcode and the score
zips = latestgrades[["BORO", "SCORE"]]
#calculate the mean and std 
gzips = zips.groupby("BORO")
gzips_agg = gzips["SCORE"].agg({'mean': np.mean, 'std_dev': np.std, 'count': len})
gzips_agg['std_error'] = gzips_agg['std_dev']/np.sqrt(gzips_agg['count'])
final_gzips = gzips_agg.sort(columns = 'mean', ascending=False)








violate_labels=violations


violate_labels['VIOLCODE'] = violate_labels['VIOLATIONCODE']
#violate_labels.drop('VIOLATIONCODE', axis=1, inplace=True)

violate_labels.head()

violate_labels['STARTDATE'] = pd.to_datetime(violate_labels['STARTDATE'])
violate_labels['ENDDATE'] = pd.to_datetime(violate_labels['ENDDATE'])
# merge the labels with the data
all_violate = pd.merge(violate_labels, violate)
all_violate = all_violate.drop(['index', 'CRITICALFLAG'],axis=1)
all_violate.head()
# select out inspection date that lies between start and end date
between = (all_violate['INSPDATE'] > all_violate['STARTDATE']) & (all_violate['INSPDATE'] < all_violate['ENDDATE'])
f_violate = all_violate[between]
# now restrict to VIOLATIONDESC, CUISINECODE
f_violate = f_violate[['VIOLATIONDESC', 'CUISINECODE', 'VIOLCODE']].reset_index(drop=True)
f_violate.shape
# ON to probabilities.....

x =f_violate
x['count'] = 1
np.sum(x['count'])

# The ratios don't mean much when the number of violations of a given type 
# and for a specific category are not large (why not?).  
#Be sure to filter these out.  We chose 100 as our cutoff.


startdate=datetime.datetime(2014,1,1)
all_violate["INSPDATE"]=pd.to_datetime[all_violate["INSPDATE"]
x=all_violate[all_violate["INSPDATE"]>startdate]

# violations per cuisine per description code
group_viol_cuis = x.groupby(["CUISINECODE", "VIOLATIONDESC"])['count']
x['viol_per'] = group_viol_cuis.transform(np.sum)

# drop the count variable
#x = x.drop_duplicates()
#x = x.drop('count', axis=1)
#x = x.reset_index()
                        
                        
x.head()
np.sum(x['count'])
# The ratios don't mean much when the number of violations of a given type 

group_cuisine = x.groupby(["CUISINECODE"])['count']
x['per_cuisine'] = group_cuisine.transform(np.sum) 
#total violations per violation description
group_violation = x.groupby(["VIOLATIONDESC"])['count']
x['per_violation'] = group_violation.transform(np.sum) 

# total violations
x['total_violation'] = np.sum(x['count'])

x['total_violation'][0]
Out[680]:
520720
In [681]:
# calculate conditional prob of violation per cusine code
x['prob_cuisine'] = x['viol_per']/ x['per_cuisine']

# calculat prob of violation
x['prob_viol'] = x['per_violation']/x['total_violation']

x['ratio'] = x['prob_cuisine']/x['prob_viol']
x.sort('CUISINECODE', ascending=False).reset_index().loc[[0,1,2,3,4,5]]

answer = x[['VIOLATIONDESC', 'ratio', 'viol_per', 'CUISINECODE']].merge(cuisine_labels)

	answer = answer.drop('CUISINECODE', axis=1)
	answer = answer[['CODEDESC', 'VIOLATIONDESC', 'ratio', 'viol_per']]
	answer = answer.sort('ratio', ascending=False)
	answer = answer.reset_index(drop=True)

f_answer = answer.drop_duplicates()


f_answer = f_answer[answer['viol_per'] > 100]
f_answer = f_answer[:20]
In [701]:
f_answer = [str(((
            row[1][0], 
            row[1][1]
            ), 
            row[1][2], 
            row[1][3]) )  for row in f_answer.iterrows()]


# with open('answers/violationratio.csv', 'wb') as f:
#         s = u"[" + y + u"]"
#         f.write(s)
q = ', '.join(f_answer).decode('string_escape').decode('iso-8859-1')
In [698]:
f = open('violationratio.csv', 'w')
f.write(q.encode('iso-8859-1'))
f.close()

#################


q5

import numpy as np

import pandas as pd

import datetime

#import webextract                                                                                                                                                                                                                           

df = pd.read_csv('../data/WebExtract_pipedelim.txt', delimiter="|")



#caluclate fraction of total violations for each cuisine                                                                                                                                                                                     
	
df         = df.dropna(subset=['VIOLCODE'])

n_cuis     = df.groupby(['CUISINECODE'])['CAMIS'].count()

n_rest     = len(df['CAMIS'])

f_cuis     = n_cuis/n_rest



#calculate fraction of each violation for each cuisine                                                                                                                                                                                       

nviol      = df.groupby(['VIOLCODE'])['CAMIS'].count()

nviol_cuis = df.groupby(['CUISINECODE','VIOLCODE'])['CAMIS'].count()

nvcg100    = nviol_cuis[nviol_cuis>100] #keep only when violations > 100                                                                                                                                                                     

viol_list  = pd.concat([((nvcg100/nviol)/f_cuis),nvcg100.rename('COUNT')],axis=1).sort_values(by='CAMIS',ascending=False)



#convert cuisine and violation codes                                                                                                                                                                                                         

cuis_desc  = pd.read_csv('Cuisine.txt')

startdate  = datetime.datetime(2014,1,1)

viol_desc  = pd.read_csv('../data/Violation_clean.txt', delimiter="|")

viol_desc['END_DT'] = pd.to_datetime(viol_desc['ENDDATE'])

viol_desc  = viol_desc[viol_desc['END_DT']>startdate]

cd         = cuis_desc.set_index('CUISINECODE').to_dict()

vd         = viol_desc.set_index('VIOLATIONCODE').to_dict()

cd         = cd['CODEDESC']

vd         = vd['VIOLATIONDESC']

vlr        = viol_list.rename(cd).rename(vd)



#print to csv                                                                                                                                                                                                                                

vlr.head(n=20).to_csv('prob5.dat',sep='|')



#print checkpoint                                                                                                                                                                                                                            

print vlr.head(n=20)['CAMIS'].sum()/20


















