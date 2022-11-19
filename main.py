import json,time,os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyperclip

url='https://www.luogu.com.cn'

with open('config.txt','r') as f:
    uid=f.readline().rstrip()
    path=f.readline().rstrip()
    
driver=webdriver.Chrome()
driver.get(url)
driver.delete_all_cookies()
with open('.\\data\\cookies.json','r') as f:
    cookie_list = json.loads(f.read())
for cookie in cookie_list:
    driver.add_cookie(cookie)

def download(problem):
    driver.get(url+'/record/list?user='+uid+'&pid='+problem+'&page=1')
    time.sleep(3)
    status_list=driver.find_elements(By.XPATH,'//div[@class="status"]/a[1]')
    for status in status_list:
        if status.text[0]=='A':
            href=status.get_attribute('href')
    driver.get(href)
    time.sleep(3)
    driver.find_element(By.XPATH,'//span[@class="entry"]').click()
    time.sleep(3)
    driver.find_element(By.XPATH,'//button[@class="copy-btn lfe-form-sz-small"]').click()
    with open(path+problem+'.cpp','w') as f:
        f.write(pyperclip.paste().replace('\r', ''))  

pblm=set()
do_not_download=set()
txt=''
with open('do_not_download.txt','r') as f:
    res=f.readlines()
    for line in res:
        line=line.rstrip()
        do_not_download.add(line)
problem_list=os.listdir(path)
for problem_id in problem_list:
    if problem_id[-4:]=='.cpp':
        pblm.add(problem_id[:-4])
            
driver.get(url+'/user/'+uid+'#practice')
time.sleep(3)
problem_list=driver.find_elements(By.XPATH,'//h3[text()="已通过的题目"]/..//a')
for problem in problem_list:
    problem_id=problem.text
    if(problem_id in pblm):
        pblm.remove(problem_id)
    elif problem_id not in do_not_download:
        download(problem_id)
        txt+=problem_id+'完成了下载\n'
        
txt+='未上传：\n'
for problem_id in pblm:
    txt+=problem_id+'\n'
driver.quit()
with open('.\\data\\logger.txt','w') as f:
    f.write(txt)
