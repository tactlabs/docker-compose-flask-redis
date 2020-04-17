'''
    Source:
    https://realpython.com/python-redis/
'''

from flask import Flask, jsonify, request
from redis import Redis
import random as rd
import logging

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

'''
    http://0.0.0.0:5000/
'''
@app.route('/')
def home():
    
    count = redis.incr('hits')

    result  = {
        'count' : count
    }

    return jsonify(result)

'''
    http://0.0.0.0:5000/name?name=one
'''
@app.route('/name')
def name_score():

    # logging.debug('Debug')
    # logging.info('reached name api')
    # logging.warning('Warning')
    # logging.error('Error')
    # logging.critical('Critical')

    logging.info('reached name api')

    name = request.values.get('name')

    score_from_cache = redis.get(name)

    if(score_from_cache):
        print('score got from cache')

        score_from_cache = int(score_from_cache.decode("utf-8"))

        result  = {
            'name' : name,
            'score' : score_from_cache
        }

        return jsonify(result) 

    score = get_name_score()
    count = redis.set(name, score)

    result = {
        'name' : name,
        'score' : score
    }

    return jsonify(result) 

def get_name_score():

    logging.info('get score fresh')

    return rd.randint(1, 1000)


if __name__ == "__main__":
    logging.basicConfig(filename='out.log',level=logging.INFO)
    app.run(host="0.0.0.0", debug=True)