import os


def load_topics(directory=None):
    if directory is None:
        directory = os.path.join(os.path.dirname(__file__), 'topics')

    topics = {}
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            topic_name = filename[:-4]
            with open(os.path.join(directory, filename), 'r') as file:
                words = file.read().splitlines()
                topics[topic_name] = words
    return topics
