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

# ────────────────────────────────────────────────
#  PALETA DE COLORES — TECH DARK / NEON CYAN
# ────────────────────────────────────────────────
C = {
    # Fondos
    "bg_app":         "#060a0f",   # negro casi puro con tinte azul
    "bg_card":        "#0a1018",   # card ligeramente más clara
    "bg_input":       "#060a0f",   # input igual que fondo app
    "bg_result":      "#040709",   # consola / resultado

    # Bordes
    "border":         "#111d2b",
    "border_hi":      "#1b2e45",
    "border_accent":  "#0e4a6e",   # borde activo/focus

    # Acento principal — cian eléctrico
    "accent":         "#00d4ff",
    "accent_dim":     "#0099cc",
    "accent_glow":    "#003d5c",   # fondo sutil detrás del acento

    # Texto
    "text_hi":        "#e8f4ff",
    "text_mid":       "#7fa8cc",
    "text_low":       "#2e4a63",

    # Verde para estado habilitado
    "green":          "#00ff88",
    "green_dim":      "#003d20",
    "green_border":   "#00663a",

    # Rojo para limpiar
    "red_text":       "#ff4d6a",
    "red_border":     "#3d1220",
    "red_hover":      "#ff7088",

    # Chips / pills
    "chip_bg":        "#080e16",
    "chip_border":    "#111d2b",
    "chip_active_bg": "#071828",
    "chip_active_fg": "#00d4ff",
    "chip_active_bd": "#0e4a6e",

    # Separador decorativo
    "sep_line":       "#0d1e30",
}


def iniciar_interfaz():

    # ────────────────────────────────────────────────
    #  VENTANA PRINCIPAL
    # ────────────────────────────────────────────────

    ventana = tk.Tk()
    ventana.title("Métodos Numéricos — Integración")
    ventana.geometry("860x960")
    ventana.configure(bg=C["bg_app"])
    ventana.resizable(False, False)

    # ────────────────────────────────────────────────
    #  ESTILO COMBOBOX
    # ────────────────────────────────────────────────

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Dark.TCombobox",
        fieldbackground=C["bg_input"],
        background=C["bg_input"],
        foreground=C["text_mid"],
        bordercolor=C["border_accent"],
        lightcolor=C["border_accent"],
        darkcolor=C["border_accent"],
        arrowcolor=C["accent_dim"],
        selectbackground=C["bg_input"],
        selectforeground=C["accent"],
        padding=10,
        relief="flat"
    )
    style.map(
        "Dark.TCombobox",
        fieldbackground=[("readonly", C["bg_input"])],
        foreground=[("readonly", C["text_mid"])],
        background=[("readonly", C["bg_input"])]
    )

    # ────────────────────────────────────────────────
    #  HELPER: separador decorativo con línea
    # ────────────────────────────────────────────────

    def separador(parent, pady=(0, 0)):
        linea = tk.Frame(parent, bg=C["sep_line"], height=1)
        linea.pack(fill="x", padx=0, pady=pady)

    # ────────────────────────────────────────────────
    #  HELPER: card con borde izquierdo accent
    # ────────────────────────────────────────────────

    def card(parent, pady=(0, 10), accent_left=False):
        outer = tk.Frame(
            parent,
            bg=C["border_hi"],       # borde exterior (1 px)
            bd=0
        )
        outer.pack(fill="x", padx=26, pady=pady)

        if accent_left:
            # Barra cian de 3 px a la izquierda
            accent_bar = tk.Frame(outer, bg=C["accent"], width=3)
            accent_bar.pack(side="left", fill="y")

        marco = tk.Frame(outer, bg=C["bg_card"], bd=0)
        marco.pack(fill="x", expand=True)

        inner = tk.Frame(marco, bg=C["bg_card"])
        inner.pack(fill="x", padx=22, pady=18)
        return inner

    # ────────────────────────────────────────────────
    #  HELPER: micro-etiqueta de sección
    # ────────────────────────────────────────────────

    def section_label(parent, texto, icon=""):
        row = tk.Frame(parent, bg=C["bg_card"])
        row.pack(fill="x", pady=(0, 8))

        if icon:
            tk.Label(
                row,
                text=icon,
                font=("Consolas", 9),
                bg=C["bg_card"],
                fg=C["accent_dim"],
                padx=0
            ).pack(side="left")

        tk.Label(
            row,
            text=f"  {texto}" if icon else texto,
            font=("Consolas", 8, "bold"),
            bg=C["bg_card"],
            fg=C["text_low"]
        ).pack(side="left")

        # línea decorativa después del texto
        tk.Frame(row, bg=C["sep_line"], height=1).pack(
            side="left", fill="x", expand=True, padx=(10, 0), pady=1
        )

    # ────────────────────────────────────────────────
    #  HELPER: campo de entrada estándar
    # ────────────────────────────────────────────────

    def make_entry(parent, placeholder=""):
        e = tk.Entry(
            parent,
            font=("Consolas", 12),
            bg=C["bg_input"],
            fg=C["text_mid"],
            insertbackground=C["accent"],
            relief="flat",
            bd=0,
            highlightbackground=C["border_hi"],
            highlightthickness=1,
            highlightcolor=C["accent"]
        )
        e.configure(width=1)

        # Focus glow
        e.bind("<FocusIn>",  lambda ev, w=e: w.config(highlightbackground=C["border_accent"], fg=C["text_hi"]))
        e.bind("<FocusOut>", lambda ev, w=e: w.config(highlightbackground=C["border_hi"],     fg=C["text_mid"]))
        return e

    # ────────────────────────────────────────────────
    #  ENCABEZADO
    # ────────────────────────────────────────────────

    header_wrap = tk.Frame(ventana, bg=C["bg_app"])
    header_wrap.pack(fill="x", padx=26, pady=(28, 18))

    # Línea superior decorativa
    top_bar = tk.Frame(header_wrap, bg=C["accent"], height=2)
    top_bar.pack(fill="x")

    header = tk.Frame(header_wrap, bg=C["bg_card"],
                      highlightbackground=C["border_hi"], highlightthickness=1)
    header.pack(fill="x")

    inner_h = tk.Frame(header, bg=C["bg_card"])
    inner_h.pack(fill="x", padx=22, pady=18)

    # Columna izquierda (textos)
    left_h = tk.Frame(inner_h, bg=C["bg_card"])
    left_h.pack(side="left", fill="both", expand=True)

    badge_row = tk.Frame(left_h, bg=C["bg_card"])
    badge_row.pack(anchor="w")

    tk.Label(
        badge_row,
        text="◆",
        font=("Consolas", 8),
        bg=C["accent_glow"],
        fg=C["accent"],
        padx=6, pady=4,
        relief="flat"
    ).pack(side="left")

    tk.Label(
        badge_row,
        text="  INTEGRACIÓN NUMÉRICA  v1.0",
        font=("Consolas", 8, "bold"),
        bg=C["accent_glow"],
        fg=C["accent"],
        padx=8, pady=4,
        relief="flat"
    ).pack(side="left")

    tk.Label(
        left_h,
        text="Calculadora de Métodos Numéricos",
        font=("Segoe UI", 21, "bold"),
        bg=C["bg_card"],
        fg=C["text_hi"]
    ).pack(anchor="w", pady=(10, 2))

    tk.Label(
        left_h,
        text="Trapecio  ·  Simpson 1/3  ·  Simpson 3/8  ·  Boole  ·  Abierto",
        font=("Consolas", 9),
        bg=C["bg_card"],
        fg=C["text_low"]
    ).pack(anchor="w")

    # Columna derecha (indicador live)
    right_h = tk.Frame(inner_h, bg=C["bg_card"])
    right_h.pack(side="right", anchor="ne")

    tk.Label(
        right_h,
        text="● SISTEMA ACTIVO",
        font=("Consolas", 8),
        bg=C["bg_card"],
        fg=C["green"]
    ).pack(anchor="e")

    tk.Label(
        right_h,
        text="CÁLCULO NUMÉRICO",
        font=("Consolas", 8),
        bg=C["bg_card"],
        fg=C["text_low"]
    ).pack(anchor="e", pady=(4, 0))

    # ────────────────────────────────────────────────
    #  CARD 1 — MÉTODO + FUNCIÓN
    # ────────────────────────────────────────────────

    c1 = card(ventana, pady=(0, 8), accent_left=True)

    section_label(c1, "MÉTODO DE INTEGRACIÓN", icon="⚙")

    metodos = [
        "Trapecio",
        "Simpson 1/3",
        "Simpson 3/8",
        "Jorge Boole",
        "Simpson Abierto"
    ]

    combo_metodos = ttk.Combobox(
        c1,
        values=metodos,
        font=("Consolas", 11),
        state="readonly",
        style="Dark.TCombobox"
    )
    combo_metodos.pack(fill="x")
    combo_metodos.current(0)

    # — Función f(x)
    tk.Frame(c1, bg=C["bg_card"], height=16).pack()
    section_label(c1, "FUNCIÓN  f(x)", icon="ƒ")

    # Marco con borde accent para el entry de función
    func_frame = tk.Frame(
        c1,
        bg=C["border_accent"],
        highlightbackground=C["accent"],
        highlightthickness=0,
        bd=1
    )
    func_frame.pack(fill="x")

    entrada_funcion = tk.Entry(
        func_frame,
        font=("Consolas", 14),
        bg=C["accent_glow"],
        fg=C["accent"],
        insertbackground=C["accent"],
        relief="flat",
        bd=0,
    )
    entrada_funcion.pack(fill="x", ipady=10, padx=2, pady=2)

    tk.Label(
        c1,
        text="Sintaxis Python  ·  x**2  ·  sin(x)  ·  sqrt(x)  ·  pi  ·  exp(x)",
        font=("Consolas", 8),
        bg=C["bg_card"],
        fg=C["text_low"],
        anchor="w"
    ).pack(fill="x", pady=(6, 0))

    # — Chips de funciones
    def insertar_funcion(texto):
        entrada_funcion.insert(tk.END, texto)

    chips_frame = tk.Frame(c1, bg=C["bg_card"])
    chips_frame.pack(fill="x", pady=(10, 0))

    chips_data = [
        ("sin",  "sin(x)"),
        ("cos",  "cos(x)"),
        ("tan",  "tan(x)"),
        ("√",    "sqrt(x)"),
        ("ln",   "log(x)"),
        ("eˣ",   "exp(x)"),
        ("π",    "pi"),
        ("x²",   "x**2"),
        ("x³",   "x**3"),
    ]

    for label, valor in chips_data:
        btn = tk.Button(
            chips_frame,
            text=label,
            font=("Consolas", 10),
            bg=C["chip_bg"],
            fg=C["text_mid"],
            activebackground=C["chip_active_bg"],
            activeforeground=C["chip_active_fg"],
            relief="flat",
            bd=0,
            pady=6,
            padx=12,
            cursor="hand2",
            highlightbackground=C["chip_border"],
            highlightthickness=1,
            command=lambda v=valor: insertar_funcion(v)
        )
        btn.pack(side="left", padx=(0, 5))

        def _enter(e, b=btn):
            b.config(bg=C["chip_active_bg"], fg=C["chip_active_fg"],
                     highlightbackground=C["chip_active_bd"])

        def _leave(e, b=btn):
            b.config(bg=C["chip_bg"], fg=C["text_mid"],
                     highlightbackground=C["chip_border"])

        btn.bind("<Enter>", _enter)
        btn.bind("<Leave>", _leave)

    # ────────────────────────────────────────────────
    #  CARD 2 — PARÁMETROS
    # ────────────────────────────────────────────────

    c2 = card(ventana, pady=(0, 8), accent_left=True)
    section_label(c2, "PARÁMETROS DE INTEGRACIÓN", icon="∫")

    params_frame = tk.Frame(c2, bg=C["bg_card"])
    params_frame.pack(fill="x")
    params_frame.columnconfigure(0, weight=1)
    params_frame.columnconfigure(1, weight=1)
    params_frame.columnconfigure(2, weight=1)

    def param_field(parent, col, label_text, symbol=""):
        wrap = tk.Frame(parent, bg=C["bg_card"])
        wrap.grid(row=0, column=col, sticky="ew",
                  padx=(0, 12) if col < 2 else (0, 0))

        lbl_row = tk.Frame(wrap, bg=C["bg_card"])
        lbl_row.pack(fill="x", pady=(0, 6))

        if symbol:
            tk.Label(
                lbl_row,
                text=symbol,
                font=("Consolas", 10),
                bg=C["bg_card"],
                fg=C["accent_dim"],
            ).pack(side="left")

        tk.Label(
            lbl_row,
            text=f" {label_text}",
            font=("Consolas", 8, "bold"),
            bg=C["bg_card"],
            fg=C["text_low"],
        ).pack(side="left")

        e = tk.Entry(
            wrap,
            font=("Consolas", 13),
            bg=C["bg_input"],
            fg=C["text_hi"],
            insertbackground=C["accent"],
            relief="flat",
            bd=0,
            highlightbackground=C["border_hi"],
            highlightthickness=1,
            highlightcolor=C["accent"]
        )
        e.pack(fill="x", ipady=9)

        # Focus glow
        e.bind("<FocusIn>",  lambda ev, w=e: w.config(highlightbackground=C["border_accent"], fg=C["accent"]))
        e.bind("<FocusOut>", lambda ev, w=e: w.config(highlightbackground=C["border_hi"],     fg=C["text_hi"]))
        return e

    entrada_a = param_field(params_frame, 0, "LÍMITE INFERIOR  (a)", symbol="α")
    entrada_b = param_field(params_frame, 1, "LÍMITE SUPERIOR  (b)", symbol="β")
    entrada_n = param_field(params_frame, 2, "PARTICIONES  (n)",     symbol="n")

    # ────────────────────────────────────────────────
    #  BOTONES DE ACCIÓN
    # ────────────────────────────────────────────────

    btn_outer = tk.Frame(ventana, bg=C["bg_app"])
    btn_outer.pack(fill="x", padx=26, pady=(4, 10))

    btn_frame = tk.Frame(btn_outer, bg=C["bg_app"])
    btn_frame.pack(fill="x")
    btn_frame.columnconfigure(0, weight=3)
    btn_frame.columnconfigure(1, weight=2)
    btn_frame.columnconfigure(2, weight=2)

    grafica_habilitada = False

    def _set_grafica(activo):
        nonlocal grafica_habilitada
        grafica_habilitada = activo
        if activo:
            boton_grafica.config(
                bg=C["green_dim"],
                fg=C["green"],
                highlightbackground=C["green_border"],
                state="normal"
            )
        else:
            boton_grafica.config(
                bg=C["bg_card"],
                fg=C["text_low"],
                highlightbackground=C["border_hi"],
                state="disabled"
            )

    def _make_action_btn(parent, col, text, color_fg, color_bd,
                         color_bg=None, cmd=None, state="normal", padx_extra=(0, 8)):
        bg = color_bg or C["bg_card"]
        b = tk.Button(
            parent,
            text=text,
            font=("Consolas", 10, "bold"),
            bg=bg,
            fg=color_fg,
            activebackground=C["bg_input"],
            activeforeground=color_fg,
            relief="flat",
            bd=0,
            pady=12,
            cursor="hand2",
            state=state,
            highlightbackground=color_bd,
            highlightthickness=1,
            command=cmd
        )
        b.grid(row=0, column=col, sticky="ew",
               padx=padx_extra)
        return b

    # ────────────────────────────────────────────────
    #  LÓGICA: CALCULAR
    # ────────────────────────────────────────────────

    def calcular():
        nonlocal grafica_habilitada
        try:
            metodo    = combo_metodos.get()
            expresion = entrada_funcion.get().strip()

            if not expresion:
                messagebox.showerror("Error", "Debe ingresar una función.")
                return

            funcion = convertir_funcion(expresion)
            a = float(entrada_a.get())
            b = float(entrada_b.get())
            n = int(entrada_n.get())

            if n <= 0:
                messagebox.showerror("Error", "n debe ser mayor que cero.")
                return

            texto_resultados.config(state="normal")
            texto_resultados.delete(1.0, tk.END)

            mapa = {
                "Trapecio":        (metodo_trapecio,        "MÉTODO TRAPECIO"),
                "Simpson 1/3":     (metodo_simpson_13,      "MÉTODO SIMPSON 1/3"),
                "Jorge Boole":     (metodo_boole,           "MÉTODO JORGE BOOLE"),
                "Simpson Abierto": (metodo_simpson_abierto, "SIMPSON ABIERTO"),
            }

            if metodo in mapa:
                fn_metodo, titulo = mapa[metodo]
                resultado, x, y, h = fn_metodo(funcion, a, b, n)

                texto_resultados.insert(tk.END, f"\n  ◆ {titulo}\n",  "header")
                texto_resultados.insert(tk.END,  "  " + "─" * 46 + "\n", "dim")
                texto_resultados.insert(tk.END, f"  h  =  {h}\n\n",   "sub")

                # ── Tabla de valores
                texto_resultados.insert(tk.END, "   i      xi              f(xi)\n", "col_header")
                texto_resultados.insert(tk.END, "  " + "─" * 46 + "\n", "dim")

                for i in range(len(x)):
                    texto_resultados.insert(tk.END, f"  {i:<5}", "key")
                    texto_resultados.insert(tk.END, f"  {x[i]:<16.6f}", "val")
                    texto_resultados.insert(tk.END, f"  {y[i]:.6f}\n",  "val")

                texto_resultados.insert(tk.END,  "  " + "─" * 46 + "\n\n", "dim")
                texto_resultados.insert(tk.END,  "  RESULTADO  ≈  ", "sub")
                texto_resultados.insert(tk.END, f"{resultado}\n\n", "result")

                _set_grafica(True)
                indicador.config(text="● calculado", fg=C["green"])

            elif metodo == "Simpson 3/8":
                texto_resultados.insert(
                    tk.END,
                    "\n  Simpson 3/8 — pendiente de implementación.\n", "sub")
                _set_grafica(False)
                indicador.config(text="● en espera", fg=C["text_low"])
            else:
                texto_resultados.insert(
                    tk.END, "\n  Método aún no implementado.\n", "sub")
                _set_grafica(False)
                indicador.config(text="● sin datos", fg=C["text_low"])

            texto_resultados.config(state="disabled")

        except Exception as error:
            messagebox.showerror("Error", f"Ocurrió un problema:\n\n{error}")
            indicador.config(text="● error", fg=C["red_text"])

    # ────────────────────────────────────────────────
    #  LÓGICA: GRAFICAR
    # ────────────────────────────────────────────────

    def mostrar_grafica():
        if not grafica_habilitada:
            return
        expresion = entrada_funcion.get()
        funcion   = convertir_funcion(expresion)
        a = float(entrada_a.get())
        b = float(entrada_b.get())
        graficar_funcion(funcion, a, b)

    # ────────────────────────────────────────────────
    #  LÓGICA: LIMPIAR
    # ────────────────────────────────────────────────

    def limpiar():
        entrada_funcion.delete(0, tk.END)
        entrada_a.delete(0, tk.END)
        entrada_b.delete(0, tk.END)
        entrada_n.delete(0, tk.END)
        texto_resultados.config(state="normal")
        texto_resultados.delete(1.0, tk.END)
        texto_resultados.config(state="disabled")
        _set_grafica(False)
        indicador.config(text="● listo", fg=C["text_low"])

    # ── Crear botones
    boton_calcular = _make_action_btn(
        btn_frame, 0, "⬡  CALCULAR",
        C["accent"], C["border_accent"],
        color_bg=C["accent_glow"],
        cmd=calcular,
        padx_extra=(0, 8)
    )
    boton_grafica = _make_action_btn(
        btn_frame, 1, "◈  GRAFICAR",
        C["text_low"], C["border_hi"],
        cmd=mostrar_grafica, state="disabled",
        padx_extra=(0, 8)
    )
    boton_limpiar = _make_action_btn(
        btn_frame, 2, "✕  LIMPIAR",
        C["red_text"], C["red_border"],
        cmd=limpiar,
        padx_extra=(0, 0)
    )

    # Hover effects
    def _hover(btn, fg_in, bd_in, fg_out, bd_out, bg_in=None, bg_out=None):
        def on_enter(e):
            btn.config(fg=fg_in, highlightbackground=bd_in)
            if bg_in:
                btn.config(bg=bg_in)
        def on_leave(e):
            btn.config(fg=fg_out, highlightbackground=bd_out)
            if bg_out:
                btn.config(bg=bg_out)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    _hover(boton_calcular, C["text_hi"], C["accent"],
           C["accent"], C["border_accent"],
           bg_in=C["accent_glow"], bg_out=C["accent_glow"])
    _hover(boton_limpiar,  C["red_hover"], C["red_hover"],
           C["red_text"], C["red_border"])

    # ────────────────────────────────────────────────
    #  CARD 3 — RESULTADOS
    # ────────────────────────────────────────────────

    c3_outer = tk.Frame(
        ventana,
        bg=C["border_hi"],
        bd=0
    )
    c3_outer.pack(fill="x", padx=26, pady=(0, 22))

    # Barra cian izquierda
    tk.Frame(c3_outer, bg=C["accent"], width=3).pack(side="left", fill="y")

    c3_inner = tk.Frame(c3_outer, bg=C["bg_card"])
    c3_inner.pack(fill="x", expand=True)

    c3 = tk.Frame(c3_inner, bg=C["bg_card"])
    c3.pack(fill="x", padx=22, pady=18)

    # Fila título + indicador
    res_header = tk.Frame(c3, bg=C["bg_card"])
    res_header.pack(fill="x", pady=(0, 10))

    tk.Label(
        res_header,
        text="▸ CONSOLA DE RESULTADOS",
        font=("Consolas", 9, "bold"),
        bg=C["bg_card"],
        fg=C["text_low"]
    ).pack(side="left")

    indicador = tk.Label(
        res_header,
        text="● listo",
        font=("Consolas", 9),
        bg=C["bg_card"],
        fg=C["text_low"]
    )
    indicador.pack(side="right")

    # Marco del text widget
    text_frame = tk.Frame(
        c3,
        bg=C["border_hi"],
        highlightbackground=C["border_hi"],
        highlightthickness=1,
        bd=0
    )
    text_frame.pack(fill="both", expand=True)

    texto_resultados = tk.Text(
        text_frame,
        width=1,
        height=15,
        font=("Consolas", 11),
        bg=C["bg_result"],
        fg=C["text_mid"],
        insertbackground=C["accent"],
        relief="flat",
        bd=0,
        selectbackground=C["accent_glow"],
        selectforeground=C["text_hi"],
        spacing1=3,
        spacing3=3,
        state="disabled",
        padx=8,
        pady=8
    )
    texto_resultados.pack(fill="both", expand=True)

    # Tags de color para el texto de resultados
    texto_resultados.tag_configure("header",
                                   foreground=C["accent"],
                                   font=("Consolas", 12, "bold"))
    texto_resultados.tag_configure("col_header",
                                   foreground=C["text_low"],
                                   font=("Consolas", 10, "bold"))
    texto_resultados.tag_configure("sub",
                                   foreground=C["text_low"],
                                   font=("Consolas", 11))
    texto_resultados.tag_configure("key",
                                   foreground=C["accent_dim"],
                                   font=("Consolas", 11))
    texto_resultados.tag_configure("val",
                                   foreground=C["text_mid"],
                                   font=("Consolas", 11))
    texto_resultados.tag_configure("result",
                                   foreground=C["accent"],
                                   font=("Consolas", 14, "bold"))
    texto_resultados.tag_configure("dim",
                                   foreground=C["border_hi"],
                                   font=("Consolas", 10))

    # ────────────────────────────────────────────────
    #  FOOTER
    # ────────────────────────────────────────────────

    footer = tk.Frame(ventana, bg=C["bg_app"])
    footer.pack(fill="x", padx=26, pady=(0, 14))

    tk.Frame(footer, bg=C["sep_line"], height=1).pack(fill="x", pady=(0, 8))

    tk.Label(
        footer,
        text="Métodos Numéricos  ·  Cálculo Diferencial e Integral  ·  2025",
        font=("Consolas", 8),
        bg=C["bg_app"],
        fg=C["text_low"]
    ).pack(side="left")

    tk.Label(
        footer,
        text="Python  +  Tkinter",
        font=("Consolas", 8),
        bg=C["bg_app"],
        fg=C["text_low"]
    ).pack(side="right")

    # ────────────────────────────────────────────────
    #  MAINLOOP
    # ────────────────────────────────────────────────

    ventana.mainloop()