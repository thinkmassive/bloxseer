from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloxseer.db'
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    metric = db.Column(db.String(255))
    begin = db.Column(db.Integer)
    end = db.Column(db.Integer)
    comparison = db.Column(db.String(32))
    value = db.Column(db.Integer)

# Not currently used, served by Aperture static files
@app.route('/')
def index():
    return "Bloxseer API\n"

@app.route('/health')
def health():
    return "OK\n"

@app.route('/event', methods=['GET', 'POST'])
def event():
    if request.method == 'POST':
        name = request.form['name']
        metric = request.form['metric']
        begin = request.form['begin']
        end = request.form['end']
        comparison = request.form['comparison']
        value = request.form['value']
        new_event = Event(name=name,metric=metric,begin=begin,end=end,comparison=comparison,value=value)
        db.session.add(new_event)
        db.session.commit()
        return 'Event added: {}'.format(name)
    elif request.method == 'GET':
        events = Event.query.all()
        event_list = []
        for event in events:
            event_list.append("Name: {} Metric: {} Begin: {} End: {} Comparison: {} Value: {}".format(event.name,event.metric,event.begin,event.end,event.comparison,event.value))
        return '<br>'.join(event_list)

@app.route('/new')
def new():
    return render_template('new.html', action_url='/events')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)
