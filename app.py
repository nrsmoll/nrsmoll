from flask import Flask, render_template, flash, redirect, url_for, session, abort
from forms import CpetForm
from flask import request
import pickle
import numpy as np
from functions import create_cat



app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html', title='Home')

@app.route('/Publications')
def publications():
    return render_template('publications.html', title='Publications')

@app.route('/logbook')
def logbook():
    return render_template('logbookhome.html', title='Logbook Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error=None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            return redirect(url_for('logbook_data'))
    return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/logbook_data')
def logbook_data():
    if not session.get('logged_in'):
        error = 'Dude, you need to login to see this stuff!!'
        return render_template('login.html', error=error)
    else:
        return render_template('logbook_data.html')


@app.route('/Cpet', methods=('GET', 'POST'))
def cpetcalc():
    form = CpetForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('Cpet.html', form=form)
        else:
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            age = int(request.form['age'])
            bmi = int(request.form['bmi'])
            etco2 = int(request.form['etco2'])
            chronotropic = int(request.form['chronotropic'])

            # for pythonanywhere, the route has to be changed to '/home/nrsmoll/nrsmoll/static/models/'
            logreg_path = 'static/models/logistic_classifier_20181201.pkl'
            with open(logreg_path, 'rb') as f:
                logreg = pickle.load(f)
            svc_path = 'static/models/svc_classifier_20181201.pkl'
            with open(svc_path, 'rb') as f:
                svc = pickle.load(f)
            rf_path = 'static/models/rf_classifier_20181201.pkl'
            with open(rf_path, 'rb') as f:
                rf = pickle.load(f)
            linear_path = 'static/models/linear_regression_20181201.pkl'
            with open(linear_path, 'rb') as f:
                linear = pickle.load(f)
            svr_path = 'static/models/svr_regression_20181201.pkl'
            with open(svr_path, 'rb') as f:
                svr = pickle.load(f)
            rfr_path = 'static/models/rfr_regression_20181201.pkl'
            with open(rfr_path, 'rb') as f:
                rfr = pickle.load(f)

            mlist = np.array([[age, bmi, etco2, chronotropic]])
            logpred = int(list(logreg.predict(mlist))[0])
            svcpred = int(list(svc.predict(mlist))[0])
            rfpred = int(list(rf.predict(mlist))[0])
            svrpred = int(list(svr.predict(mlist))[0])
            linpred = int(list(linear.predict(mlist))[0])
            rfrpred = int(list(rfr.predict(mlist))[0])
            # Anaerobic modelling
            logpredat = 1
            linpredat = 22
            svcpredat = 1
            svrpredat = 21
            rfpredat = 0
            rfrpredat = 25
            mylist = [logpred, svcpred, rfpred, logpredat, svcpredat, rfpredat]
            logpred, svcpred, rfpred, logpredat, svcpredat, rfpredat = list(map(lambda x: create_cat(x), mylist))

            return render_template('Cpet_results.html',
                                   firstname=firstname, lastname=lastname, age=age, bmi=bmi, chronotropic=chronotropic, etco2=etco2,
                                   vo2maxcat1=logpred, atcat1=logpredat,
                                   vo2maxcat2=svcpred, atcat2=svcpredat,
                                   vo2maxcat3=rfpred, atcat3=rfpredat,
                                   vo2maxest1 = linpred, atest1 = linpredat,
                                   vo2maxest2 = svrpred, atest2 = svrpredat,
                                   vo2maxest3 = rfrpred, atest3 = rfrpredat
                                   )
    elif request.method == 'GET':
        return render_template('Cpet.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
