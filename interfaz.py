import tkinter as tk
from tkinter import ttk, messagebox

from utils import convertir_funcion
from graficas import graficar_funcion
from metodos import (
    metodo_trapecio,
    metodo_simpson_13,
    metodo_boole,
    metodo_simpson_abierto
)


def iniciar_interfaz():

    # ---------------- VENTANA PRINCIPAL ----------------

    ventana = tk.Tk()

    ventana.title("Calculadora de Métodos Numéricos")

    ventana.geometry("1000x1500")

    ventana.configure(bg="#0f172a")

    ventana.resizable(False, False)

    # ---------------- ESTILOS COMBOBOX ----------------

    style = ttk.Style()

    style.theme_use("clam")

    style.configure(
        "TCombobox",
        fieldbackground="#1e293b",
        background="#1e293b",
        foreground="white",
        bordercolor="#38bdf8",
        lightcolor="#38bdf8",
        darkcolor="#38bdf8",
        arrowcolor="white",
        padding=8
    )

    # ---------------- TITULO ----------------

    titulo = tk.Label(
        ventana,
        text="CALCULADORA DE MÉTODOS NUMÉRICOS",
        font=("Segoe UI", 24, "bold"),
        bg="#0f172a",
        fg="#38bdf8"
    )

    titulo.pack(pady=(25, 5))

    # ---------------- SUBTITULO ----------------

    subtitulo = tk.Label(
        ventana,
        text="Software de Integración Numérica",
        font=("Segoe UI", 11),
        bg="#0f172a",
        fg="#94a3b8"
    )

    subtitulo.pack()

    # ---------------- FRAME PRINCIPAL ----------------

    frame_principal = tk.Frame(
        ventana,
        bg="#111827"
    )

    frame_principal.pack(
        pady=25,
        padx=30,
        fill="both",
        expand=True
    )

    # ---------------- METODOS ----------------

    label_metodo = tk.Label(
        frame_principal,
        text="Seleccione un método:",
        font=("Segoe UI", 12, "bold"),
        bg="#111827",
        fg="white"
    )

    label_metodo.pack(pady=(20, 10))

    metodos = [
        "Trapecio",
        "Jorge Boole",
        "Simpson 3/8",
        "Simpson 1/3",
        "Simpson Abierto"
    ]

    combo_metodos = ttk.Combobox(
        frame_principal,
        values=metodos,
        font=("Segoe UI", 11),
        width=35,
        state="readonly"
    )

    combo_metodos.pack()

    combo_metodos.current(0)

    # ---------------- FRAME DATOS ----------------

    frame_datos = tk.Frame(
        frame_principal,
        bg="#111827"
    )

    frame_datos.pack(pady=30)

    # ---------------- ESTILOS ----------------

    estilo_label = {
        "font": ("Segoe UI", 11),
        "bg": "#111827",
        "fg": "white"
    }

    estilo_entry = {
        "font": ("Segoe UI", 11),
        "bg": "#1e293b",
        "fg": "white",
        "insertbackground": "white",
        "relief": "flat",
        "width": 35,
        "bd": 8
    }

    # ---------------- FUNCION ----------------

    label_funcion = tk.Label(
        frame_datos,
        text="Función f(x):",
        **estilo_label
    )

    label_funcion.grid(
        row=0,
        column=0,
        padx=15,
        pady=15,
        sticky="w"
    )

    entrada_funcion = tk.Entry(
        frame_datos,
        **estilo_entry
    )

    entrada_funcion.grid(
        row=0,
        column=1,
        pady=15
    )

    # ---------------- LIMITE A ----------------

    label_a = tk.Label(
        frame_datos,
        text="Límite inferior (a):",
        **estilo_label
    )

    label_a.grid(
        row=1,
        column=0,
        padx=15,
        pady=15,
        sticky="w"
    )

    entrada_a = tk.Entry(
        frame_datos,
        **estilo_entry
    )

    entrada_a.grid(
        row=1,
        column=1
    )

    # ---------------- LIMITE B ----------------

    label_b = tk.Label(
        frame_datos,
        text="Límite superior (b):",
        **estilo_label
    )

    label_b.grid(
        row=2,
        column=0,
        padx=15,
        pady=15,
        sticky="w"
    )

    entrada_b = tk.Entry(
        frame_datos,
        **estilo_entry
    )

    entrada_b.grid(
        row=2,
        column=1
    )

    # ---------------- PARTICIONES ----------------

    label_n = tk.Label(
        frame_datos,
        text="Número de particiones (n):",
        **estilo_label
    )

    label_n.grid(
        row=3,
        column=0,
        padx=15,
        pady=15,
        sticky="w"
    )

    entrada_n = tk.Entry(
        frame_datos,
        **estilo_entry
    )

    entrada_n.grid(
        row=3,
        column=1
    )

    # ---------------- FUNCION INSERTAR ----------------

    def insertar_funcion(texto):

        entrada_funcion.insert(tk.END, texto)

    # ---------------- CONTROL GRAFICA ----------------

    grafica_habilitada = False

    # ---------------- FUNCION CALCULAR ----------------

    def calcular():

        nonlocal grafica_habilitada

        try:

            metodo = combo_metodos.get()

            expresion = entrada_funcion.get()

            if expresion == "":

                messagebox.showerror(
                    "Error",
                    "Debe ingresar una función."
                )

                return

            funcion = convertir_funcion(expresion)

            a = float(entrada_a.get())

            b = float(entrada_b.get())

            n = int(entrada_n.get())

            if n <= 0:

                messagebox.showerror(
                    "Error",
                    "n debe ser mayor que cero."
                )

                return

            texto_resultados.delete(1.0, tk.END)

            # ---------------- TRAPECIO ----------------

            if metodo == "Trapecio":

                resultado, x, y, h = metodo_trapecio(
                    funcion,
                    a,
                    b,
                    n
                )

                texto_resultados.insert(
                    tk.END,
                    "========== MÉTODO TRAPECIO ==========\n\n"
                )

                texto_resultados.insert(
                    tk.END,
                    f"h = {h}\n\n"
                )

                for i in range(len(x)):

                    texto_resultados.insert(
                        tk.END,
                        f"x{i} = {x[i]:.6f}      "
                        f"f(x{i}) = {y[i]:.6f}\n"
                    )

                texto_resultados.insert(
                    tk.END,
                    "\n-------------------------------------\n"
                )

                texto_resultados.insert(
                    tk.END,
                    f"Resultado aproximado = {resultado}"
                )

                grafica_habilitada = True

                boton_grafica.config(
                    state="normal",
                    bg="#22c55e"
                )
                
            # ---------------- SIMPSON 1/3 ----------------

            elif metodo == "Simpson 1/3":

                resultado, x, y, h = metodo_simpson_13(
                    funcion,
                    a,
                    b,
                    n
                )

                texto_resultados.insert(
                    tk.END,
                    "========== MÉTODO SIMPSON 1/3 ==========\n\n"
                )

                texto_resultados.insert(
                    tk.END,
                    f"h = {h}\n\n"
                )

                for i in range(len(x)):

                    texto_resultados.insert(
                        tk.END,
                        f"x{i} = {x[i]:.6f}      "
                        f"f(x{i}) = {y[i]:.6f}\n"
                    )

                texto_resultados.insert(
                    tk.END,
                    "\n-------------------------------------\n"
                )

                texto_resultados.insert(
                    tk.END,
                    f"Resultado aproximado = {resultado}"
                )

                grafica_habilitada = True

                boton_grafica.config(
                    state="normal",
                    bg="#22c55e"
                )
                
                
            # ---------------- JORGE BOOLE ----------------

            elif metodo == "Jorge Boole":

                resultado, x, y, h = metodo_boole(
                    funcion,
                    a,
                    b,
                    n
                )

                texto_resultados.insert(
                    tk.END,
                    "========== MÉTODO JORGE BOOLE ==========\n\n"
                )

                texto_resultados.insert(
                    tk.END,
                    f"h = {h}\n\n"
                )

                for i in range(len(x)):

                    texto_resultados.insert(
                        tk.END,
                        f"x{i} = {x[i]:.6f}      "
                        f"f(x{i}) = {y[i]:.6f}\n"
                    )

                texto_resultados.insert(
                    tk.END,
                    "\n-------------------------------------\n"
                )

                texto_resultados.insert(
                    tk.END,
                    f"Resultado aproximado = {resultado}"
                )

                grafica_habilitada = True

                boton_grafica.config(
                    state="normal",
                    bg="#22c55e"
                )
                
                
            # ---------------- SIMPSON ABIERTO ----------------

            elif metodo == "Simpson Abierto":

                resultado, x, y, h = metodo_simpson_abierto(
                    funcion,
                    a,
                    b,
                    n
                )

                texto_resultados.insert(
                    tk.END,
                    "========== SIMPSON ABIERTO ==========\n\n"
                )

                texto_resultados.insert(
                    tk.END,
                    f"h = {h}\n\n"
                )

                for i in range(len(x)):

                    texto_resultados.insert(
                        tk.END,
                        f"x{i} = {x[i]:.6f}      "
                        f"f(x{i}) = {y[i]:.6f}\n"
                    )

                texto_resultados.insert(
                    tk.END,
                    "\n-------------------------------------\n"
                )

                texto_resultados.insert(
                    tk.END,
                    f"Resultado aproximado = {resultado}"
                )

                grafica_habilitada = True

                boton_grafica.config(
                    state="normal",
                    bg="#22c55e"
                )

            # ---------------- SIMPSON 3/8 ----------------

            elif metodo == "Simpson 3/8":

                texto_resultados.insert(
                    tk.END,
                    "Este método será implementado "
                    "por otro integrante del equipo."
                )

            else:

                texto_resultados.insert(
                    tk.END,
                    "Método aún no implementado."
                )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Ocurrió un problema:\n\n{error}"
            )

    # ---------------- FUNCION GRAFICAR ----------------

    def mostrar_grafica():

        if not grafica_habilitada:
            return

        expresion = entrada_funcion.get()

        funcion = convertir_funcion(expresion)

        a = float(entrada_a.get())

        b = float(entrada_b.get())

        graficar_funcion(
            funcion,
            a,
            b
        )
        
    def limpiar():

        nonlocal grafica_habilitada

        entrada_funcion.delete(0, tk.END)

        entrada_a.delete(0, tk.END)

        entrada_b.delete(0, tk.END)

        entrada_n.delete(0, tk.END)

        texto_resultados.delete(1.0, tk.END)

        grafica_habilitada = False

        boton_grafica.config(
            state="disabled",
            bg="#334155"
        )


    # ---------------- FRAME BOTONES ----------------

    frame_botones = tk.Frame(
        frame_principal,
        bg="#111827"
    )

    frame_botones.pack(pady=10)
    
        # ---------------- FUNCION LIMPIAR ----------------


    # ---------------- HOVER ----------------

    def on_enter(e):
        e.widget["bg"] = "#0ea5e9"

    def on_leave(e):
        e.widget["bg"] = "#1d4ed8"

    # ---------------- ESTILO BOTONES ----------------

    estilo_boton = {
        "width": 9,
        "font": ("Segoe UI", 10, "bold"),
        "bg": "#1d4ed8",
        "fg": "white",
        "activebackground": "#0ea5e9",
        "activeforeground": "white",
        "relief": "flat",
        "cursor": "hand2",
        "bd": 0,
        "pady": 8
    }

    # ---------------- BOTONES MATEMATICOS ----------------

    botones = [
        ("sin", "sin(x)", 0, 0),
        ("cos", "cos(x)", 0, 1),
        ("tan", "tan(x)", 0, 2),
        ("√", "sqrt(x)", 0, 3),
        ("log", "log(x)", 0, 4),
        ("exp", "exp(x)", 1, 0),
        ("π", "pi", 1, 1),
        ("x²", "x**2", 1, 2)
    ]

    for texto, valor, fila, columna in botones:

        boton = tk.Button(
            frame_botones,
            text=texto,
            command=lambda v=valor: insertar_funcion(v),
            **estilo_boton
        )

        boton.grid(
            row=fila,
            column=columna,
            padx=8,
            pady=8
        )

        boton.bind("<Enter>", on_enter)

        boton.bind("<Leave>", on_leave)

    # ---------------- FRAME ACCIONES ----------------

    frame_acciones = tk.Frame(
        frame_principal,
        bg="#111827"
    )

    frame_acciones.pack(pady=(15, 25))

    # ---------------- BOTON CALCULAR ----------------

    boton_calcular = tk.Button(
        frame_acciones,
        text="CALCULAR",
        bg="#0ea5e9",
        fg="white",
        activebackground="#38bdf8",
        activeforeground="white",
        font=("Segoe UI", 12, "bold"),
        width=18,
        relief="flat",
        bd=0,
        pady=10,
        cursor="hand2",
        command=calcular
    )

    boton_calcular.grid(
        row=0,
        column=0,
        padx=10
    )

    # ---------------- BOTON GRAFICAR ----------------

    boton_grafica = tk.Button(
        frame_acciones,
        text="GRAFICAR",
        bg="#334155",
        fg="white",
        activebackground="#22c55e",
        activeforeground="white",
        font=("Segoe UI", 12, "bold"),
        width=18,
        relief="flat",
        bd=0,
        pady=10,
        cursor="hand2",
        state="disabled",
        command=mostrar_grafica
    )

    boton_grafica.grid(
        row=0,
        column=1,
        padx=10
    )
    
        # ---------------- BOTON LIMPIAR ----------------

    boton_limpiar = tk.Button(
        frame_acciones,
        text="LIMPIAR",
        bg="#ef4444",
        fg="white",
        activebackground="#f87171",
        activeforeground="white",
        font=("Segoe UI", 12, "bold"),
        width=18,
        relief="flat",
        bd=0,
        pady=10,
        cursor="hand2",
        command=limpiar
    )

    boton_limpiar.grid(
        row=0,
        column=2,
        padx=10
    )

    # ---------------- RESULTADOS ----------------

    label_resultados = tk.Label(
        frame_principal,
        text="Resultados",
        font=("Segoe UI", 15, "bold"),
        bg="#111827",
        fg="#38bdf8"
    )

    label_resultados.pack(pady=(10, 10))

    texto_resultados = tk.Text(
        frame_principal,
        width=95,
        height=14,
        font=("Consolas", 11),
        bg="#0f172a",
        fg="#e2e8f0",
        insertbackground="white",
        relief="flat",
        bd=10
    )

    texto_resultados.pack(pady=10)

    # ---------------- MAINLOOP ----------------

    ventana.mainloop()