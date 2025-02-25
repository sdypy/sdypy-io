import numpy as np

def get_meta_data(filename):
    """
    Function to open sfmov image sequences (exported from FLIR ResearchIR) and obtain metadata
    
    Arguments:
        filename {str} -- path to the file
    
    Returns:
        dict -- a dictionary of metadata
    """
    with open(filename, 'rt', errors='ignore') as f:
        meta = {}
        for line in f:
            if line[:11] == 'saf_padding':
                break
            a = line[:-1].split(' ')
            meta[a[0]] = a[1]

    int_values = ['xPixls', 'yPixls', 'NumDPs']

    for i in int_values:
        meta[i] = int(meta[i])

    return meta

    
def get_data(filename):
    """
    Function to open sfmov image sequences (exported from FLIR ResearchIR) and obtain raw data
    
    Arguments:
        filename {str} -- path to the file
    
    Returns:
        data -- raw data
    """
    meta = get_meta_data(filename=filename)
    f = open(filename,'rb') 
    f.seek(f.read().find(b'DATA')+6)
    
    if meta['DaType'] == 'Flt32':
        ty = np.float32
    else:
        ty = np.uint16
        
    data = np.fromfile(f, dtype=ty).reshape(-1, meta['yPixls'], meta['xPixls'])
    return data