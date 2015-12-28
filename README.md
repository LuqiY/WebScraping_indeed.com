# WebScraping_indeed opening jobs

###Introduction
"Web scraping is a computer software technique of extracting information from websites. It focuses on the transformation 
of unstructured data on the web, typically in HTML format, into structured data that can be stored 
and analyzed in a central local database or spreadsheet." ----wikipedia

In this project, I am going to scrap job postings on indeed.com. The total number of opening jobs, the average salary and
the most popular skills for a particular kind of job is what I concerned. I am going to scrap the specifical information from thousands of 
Internet webpages by simply running some lines of python code. I will take Data Scientist positions as an example to do the further
data analysis and data visualization.

###Methodology
Code is here: [WebScraping.py](https://github.com/LuqiY/WebScraping_indeed.com/blob/master/WebScraping.py)

Now I am going to introduce the functions which together make the scraping work come true.

`clean(url)` is the function that clean the raw html--unstructured data. When called the function, input a url of a particular
opening position, it will return a list of words from the company overview, job description, requirement, etc. 

BeautifulSoup and Regular Expression package has been used to connect to the website, extract the useful text, removes blank space, 
removes unicode, keep the useful words and store in a list.

`get_job_urls(city = None, state = None)` is the function that search for Data Scientist opening jobs on indeed.com in a city or 
nationwide.

In this function, I construct the url of indeed searching result page, get the amount of pages in the searching result, and then 
loop indeed searching result pages, get all job urls. The function `clean(url)` has been called whenever a job url has been extracted.
Then a huge list which contain every words in all the urls has been constructed. Within the list, I calculate the frequency of 
important data science skills such Python, R, SAS, Java, etc. After that, save the result in dataframe, calculate the percentage and
draw the plot.

There are some outputs when input the city name and state:
![ScreenShot](http://i4.tietuku.com/24d640c98b506744.png)


![ScreenShot](http://i4.tietuku.com/9da8d66fd993fede.png)


![ScreenShot](http://i4.tietuku.com/33847c778c45ff07.png)

From the above pictures, we can easily find out that Python and R are the most popular skills. Beside that, there is also a great need 
in Hadoop, Java, SAS, SQL, C++.


`get_salaries(city = None, state = None)` is the function that crawling the salary information. It loops indeed searching result pages, 
gets all salary tags, and then use Regular Expression to get the right formatted data. Then a list contain all salaries has been 
constructed. The function returns the total number of opening jobs and average salary in a given city.

Then I compared the opening jobs and average salary of some big cities in US, tables and plots have been built to visualize the results:

![alt text](http://i4.tietuku.com/60dec64d487dad7e.png)

![alt text](http://i4.tietuku.com/31b8ac90d536100a.png)










