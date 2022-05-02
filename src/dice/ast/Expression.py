from src.dice.ast.Dice import Dice

class Expression:
    expr:object


    def __init__(self, reader) -> None:
        if(reader.size() < 3):
            raise Exception("Expression is too short")
        self.__parseExpression(reader)

    def __parseExpression(self, reader):
        token = reader.peekToken()
        if(token['type'] != 'number'):
            raise Exception("Expression must start with a number")
        else:
            nextToken = reader.peekToken(1)
            if(nextToken == None):
                raise Exception("Missing dice or expression")

            if(nextToken['value'] in ['d', 'D']):
                self.expr = self.__parseDice(reader)
            elif(nextToken['value'] in ['(']):
                self.expr = self.__parseMult(reader)
            else: 
                raise Exception("Missing dice or expression")


    def __parseDice(self, reader):
        left = self.tryParseNumber(reader.peekToken(), "Left side of a dice should be a natural number over 0")
        operator = self.tryParseDiceOperator(reader.nextToken(), "Wrong operator, expected 'D' or 'd'")
        right = self.tryParseNumber(reader.nextToken(), "Right side of a dice should be a natural number over 0")

        modifierType = reader.nextToken()
        modifier = self.tryParseDiceModifier(reader)

        dice = Dice(left, operator, right, modifier)

        potentialToken = reader.nextToken()
        if(potentialToken != None):
            if(potentialToken['value'] == '('):
                self.__parseMult(self, reader)
        else:
            return dice



    def __parseMult(self, reader):
        pass


    def tryParseNumber(self, token:dict, error:str):
        if(token['type'] == 'number'):
            try:            
                return int(token['value'])
            except ValueError:
                raise Exception(error)
        raise Exception(error)



    def tryParseOperator(self, token:dict, error:str):
        if(token['type'] == 'operator'):
            return token['value']
        else:
            raise Exception(error)

                
    def tryParseDiceOperator(self, token:dict, error:str):
        if(token['type'] == 'operator'):
            if(token['value'] in ['d', 'D']):
                return token['value']
            else:
                raise Exception(error)


    def tryParseDiceModifier(self, reader):
        token = reader.peekToken()
        if(token == None):
            return 0

        if(token['type'] == 'operator'):
            if(token['value'] in ['+', '-']):
                operator = self.tryParseOperator(token, "Invalid dice modifier operator")
                value = self.tryParseNumber(reader.nextToken(), "Dice modifier should be a relative number")
                print(operator)
                if(operator == '-'):
                    value = value * -1
                return value
            else:
                raise Exception("Invalid dice modifier operator : '" + token['value'] + "', expected '+' or '-'")
        else:
            return 0

