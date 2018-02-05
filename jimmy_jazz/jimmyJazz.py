import requests
from bs4 import BeautifulSoup as bs
import random
import threading

def get_size_in_stock(session):
    endpoint="http://www.jimmyjazz.com/mens/footwear/adidas-i-5923-sneaker/BB2091?color=Red"
    response=session.get(endpoint)
    
    soup=bs(response.text,"html.parser")
    
    div=soup.find("div",{"class":"box_wrapper"})
    all_sizes=div.find_all("a")
    size_in_stock=[]
    for size in all_sizes:
        if("piunavaliable" not in size("class")):
            size_id=size["id"]
            size_in_stock.append(size_id.split("_")[1])
    return size_in_stock

def add_to_cart(session):
    size_in_stock=get_size_in_stock(session)
    size_chosen=random.choice(size_in_stock);
    endpoint="http://www.jimmyjazz.com/cart-request/cart/add/%s/1"%(size_chosen)
    response=session.get(endpoint)
    print '"success":1' in response.text
def checkout(session):
    endpoint0="https://www.jimmyjazz.com/cart/checkout"
    response0=session.get(endpoint0)
    soup=bs(response0.text,"html.parser")
    inputs=soup.find_all("input",{"name":"form_build_id","type":"hidden"})
    if(len(inputs)>1):
        form_build_id=inputs[1]["value"]
    else:
        form_build_id=inputs[0]["value"]
    print(form_build_id)
    
   
    '''
    #untested code
    endpoint1="https://www.jimmyjazz.com/cart/checkout"
    payload1={
        "billing_email":"",
        "billing_email_confirm":"",
        "billing_phone":"",
        "email_opt_in":"1",
        "shipping_first_name":"",
        "shipping_last_name":"",
        "shipping_address1":"",
        "shipping_address2":"",
        "shipping_city":"",
        "shipping_state":"",
        "shipping_zip":"",
        "shipping_method":"1",
        "billing_first_name":"",
        "billing_last_name":"",
        "billing_country":"",
        "billing_address1":"",
        "billing_address2":"",
        "billing_city":"",
        "billing_state":"",
        "billing_zip":"",
        "cc_type":"",
        "cc_number":"",
        "cc_exp_month":"",
        "cc_exp_year":"",
        "cc_cvv":"",
        "gc_num":"",
        "form_build_id":form_build_id,
        "form_id":"cart_checkout_form"
    }
    response1=session.post(endpoint1,data=payload1)
    
    soup=bs(response1.text,"html.parser")
    inputs=soup.find_all("input",{"name":"form_build_id"})
    form_build_id=inputs[1]["value"]
    endpoint2="https://www.jimmyjazz.com/cart/confirm"
    payload2={
        "form_build_id":form_build_id,
        "form_id":"cart_confirm_form"
    }
    response1=session.post(endpoint2,data=payload2)
    '''
 
def multiple_execution(): 
    session=requests.session()
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"}
    session.headers.update(headers)
    add_to_cart(session)
    checkout(session)

threads=[]
for i in range(5):
    t = threading.Thread(target=multiple_execution)
    threads.append(t)
    t.start()
   