import requests
import time
import math
import os
import sys
import socket
from multiprocessing import Process

HOST = 'api.sconce.prontotype.us'
if 'SCONCE_HOST' in os.environ:
    HOST = os.environ['SCONCE_HOST']

# Helpers

def time_since(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

def req(method, path, json):
    return requests.request(method, 'http://%s/%s.json' % (HOST, path), json=json)

# Start a job

class Job:
    def __init__(self, name, params={}, hostname=None):
        self.name = name
        self.params = params
        self.hostname = hostname or socket.gethostname()

        self.start()

    def start(self):
        r = req('post', 'jobs', {'name': self.name, 'params': self.params, 'hostname': self.hostname})
        body = r.json()

        if r.status_code != 200:
            print("JOB CLAIMED", r.status_code, r.content)
            sys.exit()

        self.job_id = body['id']
        print("Starting job %s at %s" % (self.job_id, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        self.start_time = time.time()

        self.log_every = 50
        self.plot_every = 50
        self.loss_avg = 0

    def stop(self, ):
        req('put', 'jobs/%s' % self.job_id, {'status': 'done'})

    def log(self, l):
        print('[log] %s' % time_since(self.start_time), l)
        Process(target=req, args=('post', 'jobs/%s/logs' % self.job_id, {'body': l})).start()

    def plot(self, x, y):
        Process(target=req, args=('post', 'jobs/%s/points' % self.job_id, {'x': x, 'y': y})).start()

    def record(self, e, loss):
        self.loss_avg += loss

        if e > 0 and e % self.log_every == 0:
            self.log('(%s) %.4f' % (e, loss))

        if e > 0 and e % self.plot_every == 0:
            self.plot(e, self.loss_avg / self.plot_every)
            self.loss_avg = 0

