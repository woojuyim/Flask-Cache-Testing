from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_cors import cross_origin, CORS

app = Flask("Cache Testing")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

cacheData = {}
cacheTime = {}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/cache')
def currentCache():
    return render_template('cache.html')


# Cache expire in 30 minutes
def checkTimeLimit(key):
    current_time = datetime.now()
    diff = current_time - cacheTime[key]
    if(diff.total_seconds() > 1800):
        del cacheData[key]
        del cacheTime[key]


@app.route('/getCache', methods=['GET', 'POST'])
def getCache():
    key = request.args['key']
    if key is not "":
        try: 
            checkTimeLimit(key)
            pair = {key: cacheData[key]}
            return render_template('view.html', data = pair)
        except KeyError:
            return render_template('cache.html', failure = "failure")
    else:
        return render_template('cache.html', failure = "parameter")

@app.route('/newcache')
def newcache():
    return render_template('newcache.html')


@app.route('/allcache')
def allcache():
    for key in list(cacheTime):
        checkTimeLimit(key)
    return render_template('view.html', data=cacheData)


@app.route('/addCache')
def addCache():
    key = request.args['key']
    value = request.args['value']
    if key is not "" and value is not "":
        cacheData[key] = value
        cacheTime[key] = datetime.now()
        jsonvalue = {'Key': key, 'Value': value}
        return render_template('newcache.html', success = "success")

    else:
        return render_template('newcache.html', success = "failure")


if __name__ == "__main__":
    app.run(debug=False)
