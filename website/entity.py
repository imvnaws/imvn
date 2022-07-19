from .object import Object

class Entity(Object):
    persistanceMapping = {
        "firstName" : "firstName",
        "lastName" : "lastName",
        "classCode" : "classCode",
        "createTime" : "createTime",
        "editTime" : "editTime",
        "dob" : "dob"
    }
    
    classCode = "ENT"
    tableName="CONTACTS"
    
    def __init__(self):
        super().__init__(True)

    def create(arg={}):
        obj = Entity()
        for x in arg.keys():
            setattr(obj, x, arg[x])
        return obj