from datetime import datetime
from .audit import Audit
import mysql.connector
import os
import time

class PersistanceManager(Audit):
    persistanceMapping = {
        "createTime" : "createTime",
        "editTime" : "editTime"
    }

    tableName = ''
    def __init__(self, autoGenID=True, delimitor=";", autocommit=True):
        super().__init__()
        self.dbMap = {}
        for x in self.persistanceMapping.keys():
            self.dbMap[x] = self.persistanceMapping[x]
        if not self.tableName:
            self.persisted = False
        else:
            if isinstance(self.tableName, str):
                self.tableName = self.tableName.upper()
                self.persisted = True
            else:
                error = "Table name " + str(self.tableName) + " is not of type String."
                Audit.raiseCustomError(error)
        self.autoGenID = autoGenID
        self.className = 'PersistanceManager'
        self.delimitor = delimitor
        self.autocommit = autocommit
    
    def createConn(self):
        connection = mysql.connector.connect(
            host=os.environ['RDS_HOSTNAME'], user=os.environ['RDS_USERNAME'], password=os.environ['RDS_PASSWORD'], database=os.environ['RDS_DB_NAME'], autocommit=self.autocommit
        )
        return connection
    def brStr(self, str):
        return "(" + str + ")"

    def prepValues(self, attr):
        if isinstance(attr, datetime):
            return attr.strftime("%m/%d/%Y, %H:%M:%S")
        else:
            return attr
    def createInsertStatement(self, attributeMap):
        columns = ""
        values = []
        valueStr = ""
        statement = ""
        #Create a list of values to be added to the execute statement. List will converted into tuple upon return
        for x in attributeMap.keys():
            if not values or not columns:
                values.append(self.prepValues(attributeMap[x]))
                valueStr = "%s"
                columns = x.upper()
            else:
                valueStr = valueStr + ", " + "%s"
                columns = columns + ", " + x.upper()
                values.append(self.prepValues(attributeMap[x]))
        statement = "INSERT INTO " + self.tableName + " " + self.brStr(columns) + " VALUES " + self.brStr(valueStr)
        self.debug("SQL: " + statement)
        return {"stmt" : statement, "data" : tuple(values)}

    def createUpdateByIDStatement(self, attributeMap, id):
        statement = ""
        values = []
        #Create a list of values to be added to the execute statement. List will converted into tuple upon return
        for x in attributeMap.keys():
            if not statement:
                values.append(self.prepValues(attributeMap[x]))
                statement = x.upper() + " = %s"
            else:
                statement = statement + ", " + x.upper() + " = %s"
                values.append(self.prepValues(attributeMap[x]))
        statement = "UPDATE " + self.tableName + " SET " + statement + " WHERE ID = " + str(id)
        return {"stmt" : statement, "data" : tuple(values)}
    
    def createDeleteByIDStatement(self, id):
        statement = "DELETE FROM " + self.tableName + " WHERE ID = " + str(id)
        return {"stmt" : statement, "data" : tuple([])}
    
    def createSelectStatement(self, attrs='*', where=''):
        statement = ""
        if attrs == '*':
            statement = '*'
        else:
            if self.autoGenID == True:
                statement = "ID"
            for x in attrs:
                if not statement:
                    statement = x
                else:
                    statement = statement + ", " + x
        if where:
            where = " WHERE " + where
        statement = "SELECT " + statement + " FROM " + self.tableName + where
        self.debug("SQL: " + statement)
        return statement
    def runSelectStatement(self, sql):
        self.logger.debug('SQL: ' + sql)
        #Set autocommit to false. Environment variables are pulled from Elastic Beanstalk
        connection = self.createConn()
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            self.error(e)
            raise e
        finally:
            try:
                cursor.close()
            except Exception as e:
                self.error(e)
                raise e
            try:
                connection.close()
            except Exception as e:
                self.error(e)
                raise e
        return result
    def runStatement(self, sql):
        self.debug(sql)
        #Set autocommit to false. Environment variables are pulled from Elastic Beanstalk
        connection = self.createConn()
        try:
            cursor = connection.cursor()
            cursor.execute(sql["stmt"], sql["data"])
            if self.autocommit == False:
                connection.commit()
        except Exception as e:
            if not self.autocommit:
                connection.rollback()
            self.error(e)
            raise e
        finally:
            try:
                cursor.close()
            except Exception as e:
                self.error(e)
                raise e
            try:
                connection.close()
            except Exception as e:
                self.error(e)
                raise e
    def executeSQLFile(self, filename):
        self.debug("Running script " + filename)
        try:
            conn = self.createConn()
        except Exception as e:
            self.error(e)
            raise e
        else:
            try:
                with open(filename, 'r') as f:
                    with conn.cursor() as cursor:
                        for _ in cursor.execute(f.read(), multi=True): pass
                        #cursor.execute(f.read(), multi=True)
                    conn.commit()
            except Exception as e:
                self.error(e)
                raise e
            finally:
                try:
                    cursor.close()
                except Exception as e:
                    self.error(e)
                    raise e
                try:
                    conn.close()
                except Exception as e:
                    self.error(e)
                    raise e