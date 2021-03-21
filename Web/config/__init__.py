import yaml

__config = {
    'app': {
        'debug': False
    },
    'db': {
        'type': 'file',
        'file': 'files.db'
    }
}

def init(file='config/default.yaml'):
    global __config

    with open(file, 'r') as f:
        __config = yaml.load(f, Loader=yaml.FullLoader)

def get(key):
    global __config
    
    curr = __config
    for k in key.split('.'):
        curr = curr.get(k)
        if not curr:
            return None
    return curr