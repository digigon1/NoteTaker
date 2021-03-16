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
    with open(file, 'r') as f:
        __config = yaml.load(f)
    print(__config)

def get(key):
    curr = __config
    for k in key.split('.'):
        curr = curr[k]
    return curr