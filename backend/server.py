from flask import Flask, render_template, request, redirect
from json import loads
import numpy as np
import pandas as pd

import math
import fict_api4 as environment
import numpy

a = dict()
a[40] = "Netherlands"
a[616] = "Poland"
a[36] = "Austria"
a[276] = "Germany"
a[56] = "Belgium"

event_cnt = 10
hour = pd.to_timedelta("0:1:0")

class item:
    cnt = 0
    rating = 0

class node:
    
    def __init__(self, arrive, depart, cash, counry_id):
        self.arrivial_time = arrive
        self.departure_time = depart
        self.cash = cash
        self.country_id = country_id
        
def radian(x):
    return (x * math.pi) / 180

def distance_from_points(f1, f2, q1, q2):
    f1 = radian(f1)
    f2 = radian(f2)
    q1 = radian(q1)
    q2 = radian(q2)
    temp1 = ((math.sin(f2 - f1) / 2)**2) + math.cos(f1) * math.cos(f2) * ((math.sin(q2 - q1) / 2)**2)
    return 2 * 6371 * math.asin(temp1**0.5)

def distance_from_areas(i1, i2):
    f1 = table.loc[i1].x
    f2 = table.loc[i2].x
    q1 = table.loc[i1].y
    q2 = table.loc[i2].y
    return distance_from_points(f1, f2, q1, q2)

def get_time_taxi(dist):
    return dist / 40.0

def get_time_fit(dist):
    return dist / 7

def taxi_count(dist):
    return (15 * 70 * dist) / 5

def id_to_sights(id):
    res = a[id]
    if (res == "Netherlands"):
        t = pd.read_json('Netherlands')
    if (res == "Poland"):
        t = pd.read_json('Poland')
    if (res == "Belgium"):
        t = pd.read_json('Belgium')
    if (res == "Austria"):
        t = pd.read_json('Austria')
    if (res == "Germany"):
        t = pd.read_json('Germany')
    t.time = pd.to_timedelta(t.time)
    return t

def get_random_ans(table, event_cnt):
    cur_rating = 0
    cur_cnt = 0
    cur_cash = 0
    cur_time = 0
    ans = []
    ids = list(range(event_cnt))
    weights = list(table.rating)
#     print(len(ids), len(weights))
    weights = [x / sum(weights) for x in weights]
    while(len(ids)):
        temp = numpy.random.choice(range(len(ids)), 1, p=weights)[0]
#         print(type(temp), temp)
        ans.append(ids[temp])
        ids.pop(temp)
        weights.pop(temp)
        weights = [x / sum(weights) for x in weights]
    return ans

def get_ans(table, event_cnt, max_cash, start_x, start_y):
    #print(start_x, start_y)
    #print(table)
    #print(event_cnt)
    cnt_1 = 0
    cnt_2 = 0
    hour = pd.to_timedelta("0:1:0")
    ans_rating = 0
    ans_cnt = 0
    ans_cash = 0
    ans = []
    ans_time = pd.to_timedelta("0:0:0")
    for _ in range(150):
        cur_rating = 0
        cur_cnt = 0
        cur_cash = 0
        cur_time = pd.to_timedelta("9:0:0")
        new_ans = get_random_ans(table, event_cnt)
        prev = -1
        for j,i in enumerate(new_ans):
            dist = 0
            if prev == -1:
                dist = distance_from_points(start_x, table.loc[i].x, start_y, table.loc[i].y)
            else:
                dist = distance_from_areas(prev, i)
            cur_cnt += 1
            cur_cash += table.loc[i].cost  
            cur_time += table.loc[i].time
            cur_rating += table.loc[i].rating
            if dist <= 0.8:
                needTime = get_time_fit(dist)
                cur_time += needTime * hour
            else:
                needTime = get_time_taxi(dist)
                cur_time += needTime * hour
                cur_cash += taxi_count(dist)
            if (cur_cash <= max_cash) and (cur_time < pd.to_timedelta("23:59:59")):
                if (cur_rating > ans_rating):
                    ans = new_ans[:j + 1]
                    ans_rating = cur_rating
                    ans_cash = cur_cash
                    ans_time = cur_time
                    ans_cnt = cur_cnt
            prev = i
    return (ans_cash, ans_time, ans)
            
    
def get_hotel(env, table):
    curK = 1e9
    num = 0
    for i in range(len(env)):
        curSum = 0
        for j in range (len(table)):
            curSum += distance_from_points(env.iloc[i].x, table.loc[j].x, env.iloc[i].y, table.loc[j].y)
        if (curSum < curK):
            curK = curSum
            num = i;
    #print(curSum)
    return num

env_ = environment.Environment()

user_is_new = True

app = Flask(__name__)

@app.route('/', methods = ["GET"])
def index_get():
    return render_template("index.html")

@app.route('/results', methods = ["GET"])
def results_get():
    return redirect("/")

@app.route('/results', methods = ["POST"])
def results_post():
    

    user_id = request.form.get("user_id")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    
    if not(user_id and start_date and end_date): 
        return redirect("/")

    date_s = start_date.split('-')
    date_s[0], date_s[1] =  date_s[1], date_s[0] 
   
    
    start_time = pd.to_datetime('/'.join(date_s)) 
    
    date_s = end_date.split('-')
    date_s[0], date_s[1] =  date_s[1], date_s[0]
    
    end_time = pd.to_datetime('/'.join(date_s))
    
    if user_is_new:
        li_o = [40, 616, 36, 276, 56]
        id_ = li_o[np.random.randint(5)]
        
    cash = 20000
    country = a[id_]
    table = id_to_sights(id_)
    env = env_.get_hotels(id_, start_time, end_time)
    temp = get_hotel(env, table)
    start_x = env.iloc[temp].x
    start_y = env.iloc[temp].y
    cur_time = pd.to_timedelta("5:30:0")
    k = get_ans(table, event_cnt, 20000, start_x, start_y)
    ans = []
    prev = -1
    ans.append({'type':'flight', 'name':'flight to' + country, 'time_in':(str(cur_time)), 'time_out':(str(cur_time + pd.to_timedelta("3:0:0")))})
    cur_time = "9:0:0"
    ans.append({'type':'hotel', 'name':'check in' + env.iloc[temp]['name'], 'time_in':(str(cur_time)), 'time_out':(str(cur_time + pd.to_timedelta("1:0:0")))})
    for i in k[2]:
        dist = 0
        time = "0:0:0"
        if prev == -1:
            dist = 1
        else:
            dist = distance_from_areas(i, prev)
        if dist <= 0.8:
            cur_time += get_time_fit(dist) * hour
        else:
            cur_time += get_time_taxi(dist) * hour
        prev = i
        ans.append({'type':'sightseeing', 'name': table.loc[i].name, 'time_in':(str(cur_time)), 'time_out':(str(cur_time + table.loc[i].time))})
        cur_time += table.loc[i].time 
    #print(ans)

    whole_pass = dict()
    whole_pass['name'] = country
    whole_pass['dates'] = str(start_time) + ' - ' + str(start_time + cur_time)
    whole_pass['cost'] = str(k[0])

    data = [[whole_dict] + ans]

    return render_template("results.html", data = data, start_date = start_date, end_date = end_date, cost = cost, country = country)


@app.route('/journey', methods = ["POST"])
def journey_post():

    data = request.form.get("data")

    if data:
        data = loads(data.replace("'", '"'))
        return render_template("journey.html", data = data)
    return redirect("/")

if __name__ == "__main__":
    app.run(threaded=True, host = "0.0.0.0", port = "80")
