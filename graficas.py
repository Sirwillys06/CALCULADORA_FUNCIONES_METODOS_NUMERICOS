import matplotlib.pyplot as plt
import numpy as np


def graficar_funcion(funcion, a, b):

    x = np.linspace(a, b, 500)

    y = funcion(x)

    plt.figure(figsize=(9, 5))

    # ---------------- CURVA ----------------

    plt.plot(
        x,
        y,
        linewidth=3,
        color="#0ea5e9",
        label="f(x)"
    )

    # ---------------- AREA SOMBREADA ----------------

    plt.fill_between(
        x,
        y,
        color="#38bdf8",
        alpha=0.35
    )

    # ---------------- EJES ----------------

    plt.axhline(
        0,
        color="black",
        linewidth=1
    )

    plt.axvline(
        0,
        color="black",
        linewidth=1
    )

    # ---------------- ESTILO ----------------

    plt.title(
        "Gráfica de la función",
        fontsize=16
    )

    plt.xlabel(
        "x",
        fontsize=12
    )

    plt.ylabel(
        "f(x)",
        fontsize=12
    )

    plt.grid(True, linestyle="--", alpha=0.6)

    plt.legend()

    plt.tight_layout()

    plt.show()