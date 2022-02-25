
import time
from flask import Flask, request, abort, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


    
app = Flask(__name__)   

@app.route("/", methods=["GET"])
def loby():
    return render_template("loby.html")

@app.route("/index.html", methods=["GET"])                            
def greet():
    number = request.args.get("number")
    all=[]
    pc = pchome(number)
    mo =momo(number)
    all += pc
    all += mo
    all = sorted(all, key=lambda s: int(s[3]))
    return render_template("index.html",pc=all)



def pchome(number):
    information = [[] for _ in range(20)]
    i=0
    chrome_options = Options()
    chrome_options.page_load_strategy = 'none'
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://shopping.pchome.com.tw/')
    time.sleep(1.5)
    driver.find_element_by_xpath('//*[@id="keyword"]').send_keys(number)
    driver.find_element_by_xpath('//*[@id="doSearch"]/span').click()
    time.sleep(1)

    herfs = driver.find_elements_by_xpath('//*/dd[2]/h5/a')
    for herf in herfs :
        buy_link = herf.get_attribute('href')
        information[i].append(herf.text)
        information[i].append(buy_link)
        i+=1
    i=0

    jpgs = driver.find_elements_by_xpath('//*/dd[1]/a/img')
    for jpg in jpgs :
        image_link = jpg.get_attribute('src')
        information[i].append(image_link)
        i+=1
    i=0

    values = driver.find_elements_by_class_name('value')
    for val in values:
        v =val.text
        if i >=5:
            information[i-5].append(v)
        i+=1
    return information

def momo(number):
    information = [[] for _ in range(20)]
    i=0
    chrome_options = Options()
    chrome_options.page_load_strategy = 'none'
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://www.momoshop.com.tw/main/Main.jsp')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="keyword"]').send_keys(number)
    driver.find_element_by_xpath('//*[@id="topSchFrm"]/p/button').click()
    time.sleep(5)

    herfs = driver.find_elements_by_class_name('prdName')
    for herf in herfs[:20] :
        information[i].append(herf.text)
        i+=1
    i=0

    herfs = driver.find_elements_by_class_name('goodsUrl')
    for herf in herfs[:20] :
        buy_herf = herf.get_attribute('href')
        information[i].append(buy_herf)
        i+=1
    i=0


    jpgs = driver.find_elements_by_class_name('lazy-loaded')
    for jpg in jpgs[:20] :
        image_link = jpg.get_attribute('src')
        information[i].append(image_link)
        i+=1
    i=0

    values = driver.find_elements_by_class_name('price')
    for val in values[:20]:
        v =val.text
        information[i].append(v)
        i+=1
    i = 0
    for j in range(20):
        information[i][3]=information[i][3][1:]
        ad = list(information[i][3])
        if "," in ad:
            while "," in ad:
                ad.remove(",")
            information[i][3] = "".join(ad)
        i+=1
    return information


if __name__ == "__main__":
    app.run(debug=True)

