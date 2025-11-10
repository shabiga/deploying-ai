def block_topics(msg):
    banned = ["cat", "dog", "taylor swift", "horoscope", "zodiac"]
    for w in banned:
        if w in msg.lower():
            return True
    return False
