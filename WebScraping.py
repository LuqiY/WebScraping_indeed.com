import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from time import sleep
from collections import Counter
from compiler.ast import flatten
import numpy as np


############################################
# clean the raw html, return a list of words
############################################
def clean(url):
    
# connect to the website, extract the useful text
    try:
        sub_site = requests.get(url).text
        sub_site = BeautifulSoup(sub_site)
    except:
        return
    
    for script in sub_site(["script", "style"]):
        script.extract()
        
    sub_text = sub_site.get_text()
    
# use regular expression to do the text clearning work
    sub_text = sub_text.encode('utf-8')
    sub_text = re.sub("[^a-zA-Z+]"," ", sub_text)
    sub_text = sub_text.lower()
    filtered_text = re.split(' +',sub_text)
    
# return a list
    return filtered_text


####################################################################
# for a given city, extract all the data scientist opening job urls
####################################################################
def get_job_urls(city = None, state = None):
    
    if city is not None:
        
        city_1 = re.sub(' ','+',city)
        
# construct the url of indeed searching result page (first page)
        search_site =''.join(['http://www.indeed.com/jobs?q=data+scientist&l=',city_1,'%2C+',state])

# if city = None, then return all data scientist position all over the country   
    else:
        search_site = 'http://www.indeed.com/jobs?q=data+scientist'
    
# download the front page
    text = requests.get(search_site).text
    text = BeautifulSoup(text)
    
    total_amount_text = text.find_all('meta',{'name':"description"})
    a=[tag.get('content') for tag in total_amount_text]
    
# the number of jobs available on indeed
    total_amount = int(''.join(a[0].split(' ')[0].split(',')))
    print 'There are %s jobs in %s!' %(total_amount, city)
    
# the amount of pages in the searching result
    num_pages = total_amount/10 +1
    
    job_descriptions = []

# loop indeed searching result pages, get all job urls
    for i in xrange(num_pages):
        
        url_number = str(i*10)
        
        #the url of each result page
        page = ''.join([search_site,'&start=',url_number])
        
        #get the raw html of current page 
        page_text = requests.get(page).text
        page_text = BeautifulSoup(page_text)
        
        #extract the job urls on current page
        job_link_area = page_text.find(id = 'resultsCol')
        jobs = job_link_area.find_all('a',{'data-tn-element':"jobTitle"})
        urls = [tag.get('href') for tag in jobs]
        urls = ['http://www.indeed.com'+ i for i in urls]
        
        for j in xrange(len(urls)):
            
            description = clean(urls[j])
            
            # append the description which has been successfully parsed. 
            if description: 
                job_descriptions.append(description)
            sleep(1) 

    print 'Done with collecting the data scientist jobs!'    
    print 'There were', len(job_descriptions), 'jobs successfully found (including ads).'
    
# count the frequency of each key word
    doc_frequency = Counter()  
    [doc_frequency.update(item) for item in job_descriptions]
    
# calculate the frequency of important data science skills
    Programming = Counter({'R':doc_frequency['r'], 'Python':doc_frequency['python'],
                           'Java':doc_frequency['java'], 'C++':doc_frequency['c++'],
                           'Linux':doc_frequency['linux'],'Perl':doc_frequency['perl'], 
                           'Matlab':doc_frequency['matlab'],'JavaScript':doc_frequency['javascript'], 
                           'Scala': doc_frequency['scala']})

    analysis_tool = Counter({'Excel':doc_frequency['excel'],  'Tableau':doc_frequency['tableau'],
                             'SAS':doc_frequency['sas'], 'SPSS':doc_frequency['spss']})  

    big_data = Counter({'Hadoop':doc_frequency['hadoop'], 'MapReduce':doc_frequency['mapreduce'],
                        'Spark':doc_frequency['spark'], 'Pig':doc_frequency['pig'],
                        'Hive':doc_frequency['hive'], 'Mahout':doc_frequency['mahout']})

    database = Counter({'SQL':doc_frequency['sql'], 'NoSQL':doc_frequency['nosql'],
                        'HBase':doc_frequency['hbase'],'MongoDB':doc_frequency['mongodb']})


    total_skills = Programming + analysis_tool + big_data + database
    
# save the result in dataframe
    DF_skills = pd.DataFrame(total_skills.items(),columns = ['skill', 'freq'])
    
# according to the frequency of each skill, calculate the percentage
    DF_skills['percentage'] = (DF_skills['freq'])/(sum(DF_skills['freq']))
    
#sorted the dataframe in local files and keep the top ten records
    DF_skills.sort(columns = 'percentage', ascending = False, inplace = True)
    
    print DF_skills
    
    top_ten = DF_skills.head(10).reset_index(drop=True)
    
    data_file = city + ".csv"
    DF_skills.to_csv(data_file)
    
#draw plot
    title_plot = 'Percentage of Top-Ten Data Scientist Skills in '+city
    top_ten.plot(x = 'skill', y = 'percentage', kind = 'bar',legend = None)
    plt.title(title_plot, fontsize = 15)
    plt.xticks(fontsize=10,rotation=20)
    plt.ylabel('Percentage', fontsize = 12)
    plt.show()

    
##################################
# crawling the salary information
##################################
def get_salaries(city = None, state = None):
    
    if city is not None:
        
        city_1 = re.sub(' ','+',city)
        
# construct the url of indeed searching result page (first page)
        search_site =''.join(['http://www.indeed.com/jobs?q=data+scientist&l=',city_1,'%2C+',state])
    else:
        search_site = 'http://www.indeed.com/jobs?q=data+scientist'
    
# download the front page
    text = requests.get(search_site).text
    text = BeautifulSoup(text)
    
    total_amount_text = text.find_all('meta',{'name':"description"})
    a=[tag.get('content') for tag in total_amount_text]
    
# the total amount of jobs available on indeed
    total_amount = int(''.join(a[0].split(' ')[0].split(',')))
    print 'There are %s jobs in %s!' %(total_amount, city)
    
# the amount of pages in the searching result
    num_pages = total_amount/10 +1
    
    total_salaries = []
    
# loop indeed searching result pages, get all job urls
    for i in xrange(num_pages):
        
        url_number = str(i*10)
        
        # the url of each result page
        page = ''.join([search_site,'&start=',url_number])
        
        # get the raw html of current page 
        page_text = requests.get(page).text
        page_text = BeautifulSoup(page_text)
        
        #extract the job urls on current page
        job_link_area = page_text.find(id = 'resultsCol')
        salaries = job_link_area.find_all('nobr')
        salaries = [tag.get_text() for tag in salaries]
        
        # format cleaning
        for j in xrange(len(salaries)):
            salaries[j] = salaries[j].encode('utf-8')
            salaries[j] = re.sub("[^\d-]+","",salaries[j])
            salaries[j] = salaries[j].split('-')
            
        # convert a nested list into a one-dimensional list
        # then convert the whole list from str to int
        salaries = map(int, flatten(salaries))
        total_salaries.append(salaries)
    
    total_salaries = flatten(total_salaries)
    
    # get rid of salaries which are not annual salary
    total_salaries = filter(lambda x : x>10000, total_salaries)
    
    # if you want to get the list of total_salaries to do further analysis
    # print total_salaries
    total_salaries_mean = np.mean(total_salaries)
    
    return [total_amount, total_salaries_mean]


########################################################################
# compare the salaries in some big cities and show the results in plots
########################################################################
city_list = ['New York','Boston','Bay Area','Philadelphia','Austin','Princeton','Chicago','Seattle']
state_list = ['NY','MA','CA','PA','TX','NJ','IL','WA']

compare_city = []

for i in range(len(city_list)):
    compare_city.append(get_salaries(city = city_list[i], state = state_list[i]))

# construct a data frame for the number of jobs and average salaries in each city
df1 = pd.DataFrame(city_list,columns = ['CITY'])
df2 = pd.DataFrame(compare_city,columns = ['Total Jobs','Average Salary'])
df_total = pd.concat([df1,df2],axis = 1)

# results visualization
plot_salary = df_total.sort('Average Salary', ascending = False)
plot_job = df_total.sort('Total Jobs', ascending = False)

df_total.plot(x = 'CITY', y = 'Total Jobs', kind = 'bar',legend = None)
plt.title('The Number of Openning Jobs in Popular Cities', fontsize = 15)
plt.xticks(fontsize=10,rotation=20)
plt.ylabel('Number of Jobs', fontsize = 12)
plt.show()

plot_salary.plot(x = 'CITY', y = 'Average Salary', kind = 'bar',legend = None)
plt.title('Average Salaries in Popular Cities', fontsize = 15)
plt.xticks(fontsize=10,rotation=20)
plt.ylabel('Dollar', fontsize = 12)
plt.show()
