from flask import Flask,jsonify,abort,render_template,url_for
import requests, json
import http.client

app = Flask(__name__)

class mealDB:
    conn = http.client.HTTPSConnection("www.themealdb.com")

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
        #return res.read()
        #print(res.read().decode("utf-8"))
        return res.read().decode("utf-8")
        #render_template('index.html', title="page", jsonfile=json.dumps(res.read().decode("utf-8")))

@app.route('/recipe/<string:id>', methods=['GET'])
def requestSpecific(id):
        mealDB.conn.request("GET", "/api/json/v1/1/lookup.php?i="+id)
        res = mealDB.conn.getresponse()
        #return res.read()
        #print(res.read().decode("utf-8"))
        return res.read().decode("utf-8")
        #return render_template('index.html', title="page", jsonfile=json.dumps(res.read().decode("utf-8")))

@app.route('/random/', methods=['GET'])
def random():
        mealDB.conn.request("GET", "/api/json/v1/1/random.php")
        res = mealDB.conn.getresponse()
        #return res.read()
        #print(res.read().decode("utf-8"))
        return res.read().decode("utf-8")

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

