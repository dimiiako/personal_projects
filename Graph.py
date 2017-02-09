	
# coding: utf-8

# In[1]:

from collections import namedtuple
from datetime import datetime
import requests
from bs4 import BeautifulSoup


# In[2]:

def get_index_urls():
    '''  
    
    Make a list of the index page urls.  The first page is specified by
    `url_stub`.  subsequent pages have `?page=X` appended, where X is an
    integer from 1 to 24. 
    '''
    url_stub = 'http://www.newyorksocialdiary.com/party-pictures'
    index_urls = []
    for x in range(0,28):
        index_urls.append(url_stub + '?page=' + str(x))
    return index_urls


# In[3]:

def get_album_urls(index_url):
   '''
   From a single index page, scrape out all the urls corresponding
   to an album before Dec 1, 2014.  
   '''
   # load the page
   r = requests.get(index_url)
   soup = BeautifulSoup(r.text)

   # select the chunk of html corresponding to each album listing
   album_divs = soup.select('div.view-content > div')

   # function for getting the url and year from this html chunk 
   AlbumInfo = namedtuple('AlbumInfo', 'date, url')
   def get_info(ad):
       # get year and date     
       l_date = ad.select('span.views-field-created > span')
       l_url = ad.select('span.views-field-title > span > a')
       if len(l_url)!=1 or len(l_date)!=1:
           print 'DID SOMETHING WRONG!!!'
           return None
       
       # extract year and date and return
       date = datetime.strptime(l_date[0].text, '%A, %B %d, %Y')
       url = l_url[0]['href']
       return AlbumInfo(date=date, url=url)
           
   album_infos = [get_info(ad) for ad in album_divs]

   refdate = datetime(2014, 12, 1) # Dec 1, 2014
   return [ai.url for ai in album_infos if ai.date<refdate]


# In[4]:

final_all_list = []
final_all_list_with_url = []
for ele in get_index_urls():
    final_all_list.extend(get_album_urls(ele))

for ele in (final_all_list):
    final_all_list_with_url.append('http://www.newyorksocialdiary.com' + ele)


# In[5]:

del final_all_list
print final_all_list_with_url


# In[6]:

caption_list = []
for test in final_all_list_with_url:
    r = requests.get(test)
    soup = BeautifulSoup(r.text)
    z = soup.select('.photocaption')
    parent_div = soup.find_all('font', attrs={'size':1})
    leng = 0
    flag = 0
    if z != []:
        leng = len(z)
        flag = 1
    else:
        leng = len(parent_div)
    for i in range(leng):
        if flag ==1:
            caption_list.append(z[i].text)
        else:
            caption_list.append(parent_div[i].text)


# In[7]:

#save caption list
thefile = open('captionfile.txt', 'w')
for item in caption_list:
  thefile.write("%s\n" % item.encode('ascii', 'ignore'))
print len(caption_list)


# In[164]:

#extract caption list
caption_list = []
f = open('captionfile.txt', 'r')
for lines in f:
    if lines == '\n':
        continue
    caption_list.append(lines)
print len(caption_list)


# In[7]:

#clean up caption list
for i,ele in enumerate(caption_list):
    if len(ele)>250:
        del caption_list[i]
print len(caption_list)
        


# In[8]:

name_list = []
final_list = []

for ele in caption_list:
    if 'and' in list(ele.split(' ')):
        name_list.append(ele.split(','))    
          
for i,elle in enumerate(name_list):
    if len(elle)>2:
        for j,mini_li in enumerate(elle):
            if 'and' in mini_li:
                z = name_list[i].pop(j)
                name_list[i].insert(j,z.split('and')[1])
                final_list.append(name_list[i])
    
    if len(elle)<2:
        if 'and' in elle[0]:
            z = name_list[i].pop()
            a =  z.split('and')

            if len(a[0].split()) == 1:
                if len(a[1].split())>1:
                    a.insert(-1,a[0].split()[0] +" "+ a[1].split()[-1]) 
                    a.pop(0)
                    
                
            for z,mini_li in enumerate(a):
                if 'Dr.' in mini_li:
                    temp = a.pop(z)
                    a.insert(z,temp.replace('Dr. ',''))
                if 'Mr.' in mini_li:
                    temp = a.pop(z)
                    a.insert(z,temp.replace('Mr. ',''))                    
                if 'Ms.' in mini_li:
                    temp = a.pop(z)
                    a.insert(z,temp.replace('Ms. ',''))  
                if 'Mrs.' in mini_li:
                    temp = a.pop(z)
                    a.insert(z,temp.replace('Mrs. ',''))                     
                if 'Mayor' in mini_li:
                    temp = a.pop(z)
                    a.insert(z,temp.replace('Mayor ',''))   
                if 'Ambassador ' in mini_li:
                    temp = a.pop(z)
                    a.insert(z,temp.replace('Ambassador ',''))                     
                if '\n' in mini_li:
                    temp = a.pop(z)
                    a.insert(z,temp.replace('\n',''))
            final_list.append(a)    
               
                
            #name_list[i].insert(0,a)
            
last_list = []          
for li in final_list:
    temp_li = []
    for ele in li:
        temp_li.append(" ".join(ele.split()))
    last_list.append(temp_li)
    
  
print (last_list[:100])    


# In[22]:

import networkx as nx
import itertools as it
G=nx.Graph()

for lis in last_list:
    G.add_nodes_from(lis)

for lis in last_list:   
    combos = list(it.combinations(lis,2))
    for singlecombos in combos:
        flag = 0
        if singlecombos[0] not in G.neighbors(singlecombos[1]):
            for name in singlecombos:
                if name == '':
                    flag = 1
                if name == 'er':
                    flag = 1
                if name == 'ez':
                    flag = 1
                if name == 'MD':
                    flag = 1
                if name == 'M.D':
                    flag = 1
                if name == 'Alex':
                    flag = 1
                if name == 'ra Lebenthal':
                    flag = 1
                if name == 'S':
                    flag = 1
                if name == 'ler':
                    flag = 1
                if name == 'ers':
                    flag = 1
                if name == 'Am':
                    flag = 1
                if name == 'Jr.':
                    flag = 1
                if name == 'friend':
                    #print 'YES'
                    flag = 1
                if name == 'a':
                    flag = 1
                if name == 'a Kellogg':
                    flag = 1 
                if name == 'PhD':
                    flag = 1 
                if name == 'y':
                    flag = 1      
                if name == 's':
                    flag = 1 
                if name == 'C':
                    flag = 1  
                if name == 'M.D.':
                    flag = 1
                if name == 't':
                    flag = 1 
                if name == 'i':
                    flag = 1  
                if name == 'R':
                    flag = 1 
                if name == 'ra Seidenfeld':
                    flag = 1
                if name == 'ra Lind Rose':
                    flag = 1 
                if name == 'Fern':
                    flag = 1  
                if name == 'CEO':
                    flag = 1 
                if name == 'is':
                    flag = 1 
                if name == 'friends':
                    flag = 1  
                if name == 'a Hearst':
                    flag = 1
                if name == 'ra McConnell':
                    flag = 1
                if name == 'el':
                    flag = 1
                if name == '-Hermes':
                    flag = 1
                    
                if name == 'Ph.D.':
                    flag = 1
                if name == 'all':
                    flag = 1
                if name == 'ra':
                    flag = 1
                if name == 'olph':
                    flag = 1 
                if name == 'o':
                    flag = 1
                if name == 'ell':
                    flag = 1
                if name == 'President':
                    flag = 1
                if name == 'e Shuman':
                    flag = 1   
                if name == 'a Ross':
                    flag = 1  
                    
                if name == 'ish':
                    flag = 1
                if name == 'ra Seidenfeld Lyster':
                    flag = 1   
                if name == 'ys':
                    flag = 1 
                    
                if name == 'Guest':
                    flag = 1
                if name == 'ra Porter':
                    flag = 1   
                if name == 'hi':
                    flag = 1  
                if name == 'ra Papanicolaou':
                    flag = 1  
                if name == 'egger':
                    flag = 1     
            if flag == 0:
                G.add_edge(singlecombos[0],singlecombos[1], weight=0)
        else:
            #print G[singlecombos[0]][singlecombos[1]]['weight']
            G[singlecombos[0]][singlecombos[1]]['weight']+=1


# In[23]:

import operator
print len(G.edges())
node_degree_list = []

#n = G.nodes()

n = nx.degree(G)

sorted_x = sorted(n.items(), key=operator.itemgetter(1),reverse=True)

best_list = []
for ele in sorted_x:
    if len(ele[0].split())>1:
        best_list.append(ele[0])


# In[24]:

for ele in best_list[:100]:
    print G[ele]


# In[25]:

print G['Jean Shafiroff'] #in G.neighbors('Debbie Bancroft')


# In[ ]:

pg_rank = nx.pagerank(G,alpha=0.85)


# In[ ]:

rank = nx.pagerank(G)
ans = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[:100]
#pickle.dump(ans, open('q2.p', 'wb')) 

#print 'PAGERANK:\n'
#print ans


# In[26]:

rank = nx.pagerank(G,alpha=0.85)
ans = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[:500]
for tups in ans[:290]:
    #if len(tups[0].split())>1:
        print tups


# In[27]:

def q3(g):
    def getKey(item):
        return item[1]
    edg = [((node1, node2), int(data['weight'])) for node1, node2, data in g.edges_iter(data=True)] 
    ans = sorted(edg, key=getKey, reverse=True)[:300]
    return ans


# In[28]:

print q3(G)


# In[ ]:



