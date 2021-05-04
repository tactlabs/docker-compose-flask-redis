from redis import Redis

conn = Redis(host='redis', port=6379)
# conn.flushdb()

def store_words_for_user(username, word):
    v_word = conn.get(username)

    if(v_word):
        v_word = v_word.decode('UTF-8') + "," + word
    else:
        v_word = word

    conn.set(username, v_word)
    av_word = conn.get(username)

    return av_word
    
def startpy():
    result = store_words_for_user("talha", "Blr")
    print(result)