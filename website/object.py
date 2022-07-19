from .persistance import PersistanceManager
import datetime

class Object(PersistanceManager):
    persistanceMapping = {
        "classCode" : "classCode",
        "createTime" : "createTime",
        "editTime" : "editTime"
    }
    id = ''
    classCode = "OBJ"
    def __init__(self, autoGenID=True):
        super().__init__(autoGenID=autoGenID)
        self.isNew=True
        self.createTime = datetime.datetime.now()
        self.editTime = datetime.datetime.now()
        self.classCode = self.classCode

    def read(self, where=''):
        resultDict = {}
        resultSet = []
        attrs = self.dbMap.keys()
        statement = self.createSelectStatement(attrs, where)
        result = self.runSelectStatement(statement)
        self.debug(result)
        for x in result:
            resultDict = {}
            inst = x
            i = 1
            resultDict['id'] = inst[0]
            for y in attrs:
                resultDict[y] = inst[i]
                i = i + 1
            resultSet.append(resultDict)
        self.debug(resultSet)
        return tuple(resultSet)

    def create(arg):
        obj = Object()
        for x in arg.keys():
            setattr(obj, x, arg[x])
        return obj
    
    def update(self, newSelf):
        for x in newSelf.keys():
            setattr(self, x, newSelf[x])
        self.isNew = False
        return self
    
    def commit(self):
        attributeMapping = {}
        for x in self.dbMap.keys():
            attributeMapping[x] = getattr(self, x)
        if self.isNew == True:
            query = self.createInsertStatement(attributeMapping)
        else:
            query = self.createUpdateByIDStatement(attributeMapping, self.id)

        self.runStatement(query)
    
    def deleteById(self, id):
        stmt = self.createDeleteByIDStatement(id)
        self.runStatement(stmt)
    
    def getAttrs(self):
        return self.persistanceMapping.keys()
    def getClass():
        return Object.classCode