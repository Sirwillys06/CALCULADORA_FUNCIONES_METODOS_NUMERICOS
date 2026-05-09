import numpy as np
# Aqui estara toda la logica matematica de los metodos, definidos en una funcion para que sea mas facil llamarlos en la interfaz



def metodo_trapecio(funcion, a, b, n):

    delta = (b - a) / n

    x = np.linspace(a, b, n + 1)

    y = funcion(x)

    suma = y[0] + y[-1]

    for i in range(1, n):

        suma += 2 * y[i]

    resultado = (delta / 2) * suma

    return resultado, x, y, delta


# ---------------- SIMPSON 1/3 ----------------

def metodo_simpson_13(funcion, a, b, n):

    if n % 2 != 0:

        raise ValueError(
            "Para Simpson 1/3, n debe ser PAR."
        )

    h = (b - a) / n

    x = np.linspace(a, b, n + 1)

    y = funcion(x)

    suma = y[0] + y[-1]

    for i in range(1, n):

        if i % 2 == 0:

            suma += 2 * y[i]

        else:

            suma += 4 * y[i]

    resultado = (h / 3) * suma

    return resultado, x, y, h


# ---------------- JORGE BOOLE ----------------

def metodo_boole(funcion, a, b, n):

    if n % 4 != 0:

        raise ValueError(
            "Para Jorge Boole, n debe ser múltiplo de 4."
        )

    h = (b - a) / n

    x = np.linspace(a, b, n + 1)

    y = funcion(x)

    suma = 7 * (y[0] + y[-1])

    for i in range(1, n):

        if i % 4 == 0:

            suma += 14 * y[i]

        elif i % 2 == 0:

            suma += 12 * y[i]

        else:

            suma += 32 * y[i]

    resultado = (2 * h / 45) * suma

    return resultado, x, y, h


## ---------------- SIMPSON ABIERTO ----------------

def metodo_simpson_abierto(funcion, a, b, n):

    if n % 2 != 0:

        raise ValueError(
            "Para Simpson Abierto, n debe ser PAR."
        )

    h = (b - a) / n

    x = np.linspace(a, b, n + 1)

    y = funcion(x)

    suma = y[0] + y[-1]

    for i in range(1, n):

        if i % 2 == 0:

            suma += 2 * y[i]

        else:

            suma += 4 * y[i]

    resultado = (h / 3) * suma

    return resultado, x, y, h