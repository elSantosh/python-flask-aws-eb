from flask import Flask, render_template, abort, jsonify, request, make_response, url_for
from application import db
from application.models import Data
from application.forms import EnterDBInfo, RetrieveDBInfo

# Elastic Beanstalk initialization
application = Flask(__name__)
application.debug = True
application.secret_key = 'oJuy3vDaEnnKLjfEYZ88lJtt4wDEBvmfFTLBbnjU'

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Bread, Fruit',
        'done': False
    },
    {
        'id': 2,
        'title': u'Goto Gym',
        'description': u'Lets goto the gym on saturday mrng',
        'done': False
    }
]
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task
@application.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    try:
        # num_return = int(form2.numRetrieve.data)
        query_db = Data.query.order_by(Data.id.desc()).limit(100)
        for q in query_db:
            print(q.notes)
        db.session.close()
    except:
        db.session.rollback()
        return jsonify({'tasks': [i.serialize for i in query_db]})
@application.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    # data_entered = Data(task)
    ed_user = Data(notes = task.title)
    try:
        db.session.add(ed_user)
        db.session.commit()
        db.session.close()
    except:
        db.session.rollback()
    # return render_template('thanks.html', notes=form1.dbNotes.data)
    return jsonify({'task': task}), 201

@application.route('/', methods=['GET', 'POST'])

@application.route('/index', methods=['GET', 'POST'])

def index():
    form1 = EnterDBInfo(request.form)
    form2 = RetrieveDBInfo(request.form)

    if request.method == 'POST' and form1.validate():
        data_entered = Data(notes=form1.dbNotes.data)
        try:
            db.session.add(data_entered)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()
        return render_template('thanks.html', notes=form1.dbNotes.data)

    if request.method == 'POST' and form2.validate():
        try:
            num_return = int(form2.numRetrieve.data)
            query_db = Data.query.order_by(Data.id.desc()).limit(num_return)
            for q in query_db:
                print(q.notes)
            db.session.close()
        except:
            db.session.rollback()
        return render_template('results.html', results=query_db, num_return=num_return)

    return render_template('index.html', form1=form1, form2=form2)

if __name__ == '__main__':
    application.run(host='0.0.0.0')
