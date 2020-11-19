from flask import Flask,jsonify,abort,render_template,url_for
import json
import http.client
import sys
from flask_cors import CORS
from user.models import User
from firbase.fire import fire

app = Flask(__name__)
cors = CORS(app)

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError



class mealDB:
    conn = http.client.HTTPSConnection("www.themealdb.com")


def data_transformation(data_dict):
    ingredients = []
    #print(data_dict['idMeal'])
    for i in range(20):
        if(not data_dict['strMeasure'+str(i+1)] or data_dict['strMeasure'+str(i+1)] is None):
            break
        mq = data_dict['strMeasure'+str(i+1)].split()
        while(len(mq)<2):
            mq.append('N/A')
        ingredients.append({
        "id":str(i),
        "item": data_dict['strIngredient'+str(i+1)],
        "measurement":mq[1] ,
        "quantity":mq[0],
        "gotten":False,
        "price":0
        }) 
            
        

    frontData={
        "instructions":[data_dict['strInstructions']],
        "servings":"2",
        "recipeId": data_dict['idMeal'],
        "cookTime": "10",
        "userId": "eu-west-1:1234abcd",
        "video": data_dict['strYoutube'], 
        "attachment": data_dict['strMealThumb'],
        "createdAt": data_dict['dateModified'],
        "ingredients":ingredients,
        "tag":{data_dict['strCategory'],data_dict['strArea']},
        "title":data_dict['strMeal']
    }
    return frontData


def process_data(data):
    #print(data.read().decode("utf-8"))
    y = json.loads(data.read().decode("utf-8"))
    print(type(y['meals'][0]))
    res = list()
    for x in y['meals']:
        res.append(data_transformation(x))
    return res

@app.route('/user/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        if fire().signup(user, password):
            return "Success"

    return 'Failed'

@app.route('/user/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        if fire().signin(user, password):
            return "Success"
    return 'Failed'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('/500.html'), 500

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/first/<string:fst>', methods=['GET'])
def requestFirst(fst):
        mealDB.conn.request("GET", "/api/json/v1/1/search.php?f=a"+fst)
        res = mealDB.conn.getresponse()
        return res.read().decode("utf-8")
        

@app.route('/search/<string:recipe>', methods=['GET'])
def requestMeal(recipe):
        mealDB.conn.request("GET", "/api/json/v1/1/search.php?s="+recipe)
        res = mealDB.conn.getresponse()
        #print(res.read().decode("utf-8"))
        res_list = process_data(res)
        res_json = json.dumps(res_list,default=set_default) 
        print(type(res_list[0]))
        return res_json
        #render_template('index.html', title="page", jsonfile=json.dumps(res.read().decode("utf-8")))

@app.route('/recipe/<string:id>', methods=['GET'])
def requestSpecific(id):
        mealDB.conn.request("GET", "/api/json/v1/1/lookup.php?i="+id)
        res = mealDB.conn.getresponse()
        #return res.read()
        #print(res.read().decode("utf-8"))
        res_list = process_data(res)
        res_json = json.dumps(res_list,default=set_default) 
        print(type(res_list[0]))
        return res_json

@app.route('/random/', methods=['GET'])
def random():
        mealDB.conn.request("GET", "/api/json/v1/1/random.php")
        res = mealDB.conn.getresponse()
        #return res.read()
        #print(res.read().decode("utf-8"))
        res_list = process_data(res)
        res_json = json.dumps(res_list,default=set_default) 
        print(type(res_list[0]))
        return res_json

@app.route('/search_main/<string:main>', methods=['GET'])
def requestMain(main):
        mealDB.conn.request("GET", "/api/json/v1/1/filter.php?i="+main)
        res = mealDB.conn.getresponse()
        #return res.read()
        #print(res.read().decode("utf-8"))
        return res.read().decode("utf-8")

@app.route('/list/<string:key>', methods=['GET'])
def listMeal(key):
    req = "/api/json/v1/1/list.php?"
    if(key == "area"):
        req += "a=list"
    elif(key == "categories"):
        req += "c=list"
    else:
         req += "i=list"
    mealDB.conn.request("GET", req)
    res = mealDB.conn.getresponse()
    return res.read().decode("utf-8")    

if __name__ == '__main__':
    app.run()

