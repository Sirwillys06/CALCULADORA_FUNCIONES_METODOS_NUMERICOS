from sympy import symbols, sympify, lambdify



#Aqui lo hago es que el programa pueda aceptar texto comun porque lo transforma en texto matematico
x = symbols('x')

def convertir_funcion(expresion):

    expr = sympify(expresion)

    funcion = lambdify(x, expr, "numpy")

    return funcion