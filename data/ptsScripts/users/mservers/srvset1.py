'''
Created on 10-Mar-2025

@author: kayma
'''

def ACTION(request):
    print("----okok---")
    print(request)
    print(PROPS)
    return {'out':"nothing"}
    
    
if __name__ == "__main__":
    
    PROPS = {'Node Script': 'rough.servers.srvset1', 'STYLE': '1'}
    PROPS['STYLE'] = 0
    
    REQUEST = {"in1":890}
    ret = ACTION(REQUEST)
    
    print(ret)
    