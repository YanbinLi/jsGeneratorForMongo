class condition_transfer:
    def __init__(self, fields):
        self.fields = fields
        self.key_words = [">",">=", "<", "<=", "==", "!=", "and", "or", "(", ")", "in"]
        self.priority = {"#":0,
                         "or":1,
                         "and":2,
                         ">": 3,
                         ">=": 3,
                         "<":3,
                         "<=":3,
                         "==":3,
                         "!=":3,
                         "in":3,
                         "(":0,
                         ")":4,
                         "$":5  }
        self.mongo_map = {"or":"$or",
                         "and":"$and",
                         ">": "$gt",
                         ">=": "$gte",
                         "<":"$lt",
                         "<=":"$lte",
                         "==":":",
                         "!=" : "$ne",
                         "in":"$in"}

    def gen_conditon(self, condition):
        words = condition.split(" ")
        data = []
        oprs = ["#"]
        for word in words:
            if word == ")":
                while oprs[-1] != "(":
                    data.append(oprs.pop())
                oprs.pop()
                continue
                
            if word in self.key_words:
                if self.priority[word] > self.priority[oprs[-1]] or word == "(" :
                    oprs.append(word)
                else:
                    while self.priority[word] <= self.priority[oprs[-1]] and len(oprs) > 0:
                        data.append(oprs.pop())
                    oprs.append(word)
            else:
                data.append(word)
        data.extend(oprs[::-1])
        data.pop()

        self.translate(data)

    def translate(self, datas):
        result = []
        for data in datas:
            if data not in self.key_words:
                result.append(data)
            else:
                right = result.pop()
                left = result.pop()
                opr = self.mongo_map[data]
                if (data != "or" and data != "and"):
                    if (data != "=="):
                        result.append(left + ":{" + opr + ":" + right + "} " )
                    else:
                        result.append("{" + left + ":" + right + "} " )
                else:
                    
                    result.append(opr + ":[" + left + "," +  right + "]")
        print(result)



if __name__ == "__main__":
    jg = condition_transfer(None)
    jg.gen_conditon("( a < 1 or c > 1 and f == 1 ) and b > 2 and c in ['a','b']")

    


    
