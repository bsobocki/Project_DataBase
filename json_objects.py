import json 

class JSON_Obj:
    def __init__(self):
        self.obj = None
        self.file = None
        self.src = None

    def read_obj(self, str):
        if str != '':
            self.obj = json.loads(str)
        else:
            self.obj = None

    def read_obj_from_file(self, src):
        if self.src != src:
            self.src = src
            self.file = open(self.src)

    def read_next_object(self):
        if self.file != None:
            str = self.file.readline()
            if str != '':
                self.obj = json.loads(str)
            else:
                self.obj = None
        else:
            self.obj = None

    def check_key(self, index,value):
        return list(self.obj.keys())[index]==value

    def get_current_Obj(self):
        return self.obj

    def get_values_as_dict(self):
        return self.obj[list(self.obj.keys())[0]]

    def get_values_as_list(self):
        return list(self.obj[list(self.obj.keys())[0]])


def json_OK_object(l):
    o = [] # create a new list to format data
    for i in l:
        i = list(i)
        i[0] = int(i[0]) # first objects is alvays 'Decimal('...')'
        o.append(i) # add to list
    obj = '{"status":"OK",\n  "data":' + str(o) + '}'
    return obj

OK_status = '{"status":"OK"}'

def ERROR_status(message):
    return '{"status":"ERROR", "message":'+message+'}'