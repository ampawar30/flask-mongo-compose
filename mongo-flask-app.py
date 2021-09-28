from flask import Flask,jsonify,redirect, url_for, request, render_template
from flask_pymongo import PyMongo,MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import os
app=Flask(__name__)

app.config['MONGO_DBNAME']='mongotask'
app.config['MONGO_URI']='mongodb://127.0.0.1:27017/mongotask'

#create object for connection between flask and monogdb
mongo=PyMongo(app)

#cross orgin resource sharing for all origin
CORS(app)

@app.route('/api/tasks',methods=['GET'])
def get_all_tasks():
    tasks=mongo.db.tasks
    result=[]
    for field in tasks.find():
        result.append({'_id':str(field['_id']),'title':field['title']})

    return render_template('api.html',result=result)

@app.route('/api/task',methods=['POST'])
def add_task():
    tasks=mongo.db.tasks
    title=request.get_json()
    title=title['title']
    task_id=tasks.insert({'title':title})
    new_task=tasks.find_one({'_id':task_id})
    result={'title':new_task['title']}
    print(result)
    return jsonify({'result':result})

@app.route('/api/task/<new>',methods=['POST'])
def update_task(new):
    tasks=mongo.db.tasks
    new_title = {
        'title': request.form['title']
            }
    task_id=tasks.insert(new_title)
    new_task=tasks.find_one({'_id':task_id})
    print(new_task)
    return redirect(url_for('get_all_tasks'))


if __name__ == "__main__":
    env = os.environ.get('APP_ENV', 'development')
    port = int(os.environ.get('PORT', 5000))
    debug = False if env == 'production' else True
    app.run(host='0.0.0.0', port=port, debug=debug)