import sqlparse
from sql_syntax_error import SqlSyntaxError

class ConditionTransfer():
    def __init__(self):
        self.priority = {"#":0,
                    "or":1,
                    "and":2,
                    "not":3,
                    "in":4,
                    "$":5  }           
        self.mongo_map = {"or":"$or",
                        "and":"$and",
                        "not":"$not",
                        ">": "$gt",
                        ">=": "$gte",
                        "<":"$lt",
                        "<=":"$lte",
                        "=":":",
                        "!=" : "$ne",
                        "in":"$in"}
        self.key_words = [">",">=", "<", "<=", "==", "!=", "and", "or", "(", ")", "in", "not"]

    def __get_useful_token(self,tokens):
        return [i for i in tokens if i.ttype is None or( i.ttype.value not in sqlparse.tokens.Whitespace and i.ttype not in sqlparse.tokens.Punctuation)]


    def __to_mongo_comparison(self,comparison):
        if isinstance(comparison, sqlparse.sql.Comparison ):
                sub_tokens = self.__get_useful_token(comparison.tokens)
                if len(sub_tokens) != 3:
                    raise SqlSyntaxError("语法错误")
                left = sub_tokens[0].value
                opr = sub_tokens[1].value
                right = sub_tokens[2].value
                
                if opr in ("=", "==") :
                    return "{" + left + ":" + right + "}"
                else:
                    mongo_opr = self.mongo_map[opr]
                    return  left + ":{" + mongo_opr + ":" + right + "} " 
        return ""

    def __to_mongo_text(self, tokens):
        data = []
        opr = ["#"]
    
        for i in tokens:
            if isinstance(i, sqlparse.sql.Parenthesis):
                tmp = self.__get_useful_token(i)
                if len(tmp) == 1 and isinstance(tmp[0], sqlparse.sql.IdentifierList):
                    data.append("["  + ",".join( [indentifier.value for indentifier in self.__get_useful_token(tmp) ]  ) + "]" )
                else:
                    data.append(self.__to_mongo_text(tmp))
            
            elif isinstance(i, sqlparse.sql.Comparison):
                data.append(self.__to_mongo_comparison(i))
            elif i.ttype in sqlparse.tokens.Keyword:
                if self.priority[i.value] > self.priority[opr[-1]]:
                    opr.append(i.value)
                else:
                    while self.priority[i.value] <= self.priority[opr[-1]] and len(opr) > 0:
                        data.append(opr.pop())
                    opr.append(i.value)
            else:
                data.append(i.value) 
        data.extend(opr[::-1])
        data.pop()
        return data
    def __translate(self, datas):
        result = []
        for data in datas:
            if data not in self.key_words:
                result.append(data)
            else:
                if (data == "or" or data == "and" or data == "in"):
                    right = result.pop()
                    if isinstance(right, list):
                        right = self.__translate(right)
                    left = result.pop()
                    if isinstance(left, list):
                        left = self.__translate(left)
                    opr = self.mongo_map[data]
                    result.append(opr + ":[" + left + "," +  right + "]")   
                else:
                    right = result.pop()
                    if isinstance(right, list):
                        right = self.__translate(right)
                    opr = self.mongo_map[data]
                    result.append(opr + ":{" +   right + "}")
                   
        return result.pop()
    
    def gen_condition(self, condition):
        condition = condition.strip()
        condition = condition.lower()
        
        if not condition.startswith("where "):
            condition = "where " + condition
        where = None
        fields = sqlparse.parse(condition)
        for i in fields[0]:
            if isinstance(i, sqlparse.sql.Token ):
                where = i
        
        tmp = self.__to_mongo_text(self.__get_useful_token(where[1:]))
        return self.__translate(tmp)







if __name__ == '__main__':

    print("123123".startswith("123"))

    '''
    fields = sqlparse.parse("where ( not c == 'd' and d >= 1 and e not in (1, 2, 3) or h=1) or f = 2 and g<1")
    #fields = sqlparse.parse("where  not c == 'd' and d >= 1 and e not in ('1', '2', '3') ")
 
    where = None
    for i in fields[0]:
        if isinstance(i, sqlparse.sql.Token ):
            where = i
    transfer = ConditionTransfer()
    tmp = transfer.to_mongo_text(transfer.get_useful_token(where[1:]))


    print(tmp)
    print(transfer.translate(tmp))
    '''
