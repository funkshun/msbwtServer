import os
import json
import sys
import requests
import sqlite3
import secrets
import string
import msbwtServer.db as db_ops
from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing.pool import ThreadPool


def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'msbwt.sqlite'),
    )

    app.config.from_object('config')
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    scheduler = BackgroundScheduler()
    alive, bwts = _checkHosts()
    job = scheduler.add_job(_checkHosts, 'interval', minutes=5)
    
    jobs = {}
    


    @app.route('/')
    def index():
        return render_template('index.html', res=bwts)

    @app.route('/hosts')
    def listHosts():
        return Response(json.dumps(alive), status=200)

    @app.route('/functions')
    def functions():
        return render_template('functions.html')

    @app.route('/results/<phrase>')
    def results(phrase):
        res = jobs[phrase]
        
        for re in res:
            r = requests.get(bwts[re['data']['name']] + '/results/' + re['token'])
            print(re['token'])
            if r.status_code == 200:
                rj = r.json()
                print(rj['status'])
                re['date'] = rj['date']
                re['status'] = rj['status']
                if re['status'] == 'RUNNING':
                    re['result'] = 'In Progress'
                elif re['status'] == 'FAILED':
                    re['result'] = 'Query Failed'
                else:
                    re['result'] = rj['result']

        return render_template('results.html', vals = res)


    
    @app.route('/<func_call>')
    def functionCaller(func_call):
            
        args = request.args.get('args', None).encode('ascii', 'ignore')
        names = [x.encode('ascii', 'ignore') for x in request.args.getlist('names')]
        

        rets = []
        for name in names:
            r = makeRequest(name, func_call, args, bwts)
            a = r.json()
            a['status_code'] = r.status_code
            rets.append(a)
        loc_tok = getToken()
        jobs[loc_tok] = rets

        return render_template('job.html', func_call=func_call, res=rets, ar=args, token = loc_tok)
    


    def _checkHosts():
        try:
            with open(os.path.join(app.config['HOST_ROOT']), 'r') as f:
                host_lst = f.read()
            hosts = [x.strip() for x in host_lst.split("\n")]
            
        except Exception as e:
            print("Error opening hosts file. Ensure file exists and is populated")
            print(e)
            sys.exit(1)

        alive = {}
        bwts = {}
        for h in hosts:
            try:
                r = requests.get('http://' + h + '/checkAlive')
                j = r.json()
                
                if r.status_code == 200:
                    
                    alive[h] = j
                
                for key in alive.keys():
                   
                    bwts[alive[key]['name']] = 'http://' + key

            except:
                pass
        return (alive, bwts)

    


    return app


def makeRequest(name, func, args, maps):
    target = maps[name]
    para = {
                'args' : args
    }
    r = requests.get(target + '/' + func, params = para)
    return r

def getToken():
    alphabet = string.ascii_letters + string.digits
    t = ""
    for i in range(15):
        t = t + secrets.choice(alphabet)
    return t


    


    
