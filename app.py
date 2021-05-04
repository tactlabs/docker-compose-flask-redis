'''
    Source:
    
    https://realpython.com/python-redis/

    https://medium.com/better-programming/tips-and-tricks-for-handling-logging-files-in-python-b48be3d553ad
'''

from flask import Flask, jsonify, request
from redis import Redis
import random as rd
import store_redis as sr
import logging

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

'''
    http://0.0.0.0:5000/
'''
@app.route('/')
def home():
    
    count = redis.incr('apikey')

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

'''
    http://0.0.0.0:5000/api?api_key=one
'''
@app.route('/api')
def get_api_hit_count():

    api_key = request.values.get('api_key')

    api_hit_count = redis.get(api_key)

    if(not api_hit_count):
        api_hit_count = 0
    else:
        api_hit_count = int(api_hit_count)

    api_hit_count = api_hit_count + 1

    redis.set(api_key, api_hit_count)

    result = {
        'api_key' : api_key,
        'api_hit_count' : int(api_hit_count)
    }

    return jsonify(result) 

'''
    http://0.0.0.0:5000/api/reset?api_key=one
'''
@app.route('/api/reset')
def reset_api_hit_count():

    api_key = request.values.get('api_key')

    api_hit_count = redis.get(api_key)

    if(not api_hit_count):
        print('Is not available, so no need to reset')
    else:
        redis.set(api_key, 0)
        print('hard reset done on ', api_key)

    result = {
        'api_key' : api_key,
        'result' : 'reset done'
    }

    return jsonify(result) 

'''
    http://0.0.0.0:5000/api/user/<username>/<word>
'''
@app.route('/api/user/<username>/<word>')
def api_store_user_word(username, word):

    result = sr.store_words_for_user(username, word)

    result = result.decode('UTF-8')

    word_list = result.split(',')

    word_dict = {
        username : word_list
    }

    return jsonify(word_dict) 



def get_name_score():

    logging.info('get score fresh')

    name = request.values.get('name')

    return rd.randint(1, 1000)


if __name__ == "__main__":

    logging.basicConfig(filename = 'out.log', level = logging.INFO)
    app.run(host = "0.0.0.0", debug = True)