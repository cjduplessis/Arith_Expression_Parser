INVALID_FORMULA_MESSAGE = "Invalid syntax!"

PRECEDENCE = {'^':1,'/':2,'|':2,'*':2,'%':2,'+':3,'-':3}

OPERATORS = ('+','-','*','/','|','%','^')

NUMBER_COMPONENTS = ('.','0','1','2','3','4','5','6','7','8','9')

MATH_FUNCTIONS = ('ln','log','exp','sin','cos','tan',
                  'asin','acos','atan','sinh','cosh',
                  'tanh','sqrt')

SYMBOL_FUNCTIONS = ('!')

HELP_TEXT = """
            HELP
            ----
              
            Every line labeled with a number <n> is where a calculation
            can be performed. All the usual rules for arithmatic count.
            
            Example:

            <22> (3 + 4) - (99*(1 - 3)*7)
                 = 1393 

            1. Arithmetic operations:
            
               +  addition
               -  subtraction
               *  multiplication
               /  regular division
               |  integer division
               %  modular division (both operands must be integers)
               ^  exponentiation
               
            2. Mathematical functions:

               Factorial: n! eg. 4! = 4*3*2*1
               Logarithms: ln(x), log(x)
               Exponent: exp(n). exp(x) = e^x, where e = 2.718281828...
               Trigonometric: sin(x), cos(x), tan(x)
               Inverse trig: asin(x), acos(x), atan(x)
               Hyperbolic: sinh(x), cosh(x), tanh(x)
               Square root: sqrt(x)          

            3. Referencing a previous line:
            
               You can reference a previous line on which a successfull
               calculation was performed by using the $ symbol with the line
               number directly next to it:

               Example:

               <1> 2*9
                   = 18
               <2> $1 + 100
                   = 118
            """
