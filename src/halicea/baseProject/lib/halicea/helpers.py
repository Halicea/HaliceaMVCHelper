__author__ = 'KMihajlov'

def get_pager(params, limit=20, offset=0, limitName='limit', offsetName='offset'):
    try:
        limit = int(params[limitName])
        offset = int(params['offsetName'])
    except:
        pass
    return limit, offset

def get_model(params, modelClass):
    raise NotImplementedError('IMPLEMENT ME FIRST')
