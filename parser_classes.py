import math
import constants as const

class Symbol_Function:

    """The class represents a mathematical function in a formula"""
   
    def __init__(self, name):
        self.name = name

    def calculate(self, x):
        if self.name == '!':
            return math.factorial(x)
        else:
            return

class Function:

    """The class represents a mathematical function in a formula"""
   
    def __init__(self, name):
        self.name = name

    def calculate(self, x):
        if self.name == 'log':
            return math.log10(x)
        elif self.name == 'ln':
            return math.log(x)
        elif self.name == 'exp':
            return math.exp(x)
        elif self.name == 'sin':
            return math.sin(x)
        elif self.name == 'cos':
            return math.cos(x)
        elif self.name == 'tan':
            return math.tan(x)
        elif self.name == 'asin':
            return math.asin(x)
        elif self.name == 'acos':
            return math.acos(x)
        elif self.name == 'atan':
            return math.atan(x)
        elif self.name == 'sinh':
            return math.sinh(x)
        elif self.name == 'cosh':
            return math.cosh(x)
        elif self.name == 'tanh':
            return math.tanh(x)
        elif self.name == 'sqrt':
            return math.sqrt(x)
        else:
            return
        
class Operator:

    """The class represents an operation in a formula"""
   
    def __init__(self, symbol):
        self.symbol = symbol
        self._prec = const.PRECEDENCE.get(symbol, 0)

    def prec(self):
        return self._prec

    def calculate(self, x, y):
        if self.symbol == '|':
            return x//y
        if self.symbol == '^':
            return x**y
        if self.symbol == '/':
            return x/y
        if self.symbol == '*':
            return x*y
        if self.symbol == '%':
            return x%y
        if self.symbol == '+':
            return x+y
        if self.symbol == '-':
            return x-y
        return

			
class Stack:
    def __init__(self):
        self._elements = []

    def __str__(self):
        s = ""
        for element in self._elements:
            if isinstance(element, int):
                s += str(element)
            else:
                s += "'" + element + "'"
            s += " "
        return s

    def push(self, item):
        self._elements.append(item)

    def pop(self, index = -1):
        if index == -1:
            self._elements.pop()
        else:
            self._elements.pop(index)

    def peek(self, index = -1):
        if index == -1:
            return self._elements[len(self._elements) - 1]
        
        return self._elements[index]

    def size(self):
        return len(self._elements)

    def is_empty(self):
        return len(self._elements) == 0
