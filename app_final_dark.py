import customtkinter as ctk
from tkinter import messagebox, filedialog


# --------------------- Configuración global --------------------- #
ctk.set_appearance_mode("dark")  # Opciones: "dark", "light", "system"
ctk.set_default_color_theme("blue")




# --------------------- Función: Barrido --------------------- #
def generar_barrido_gcode(ancho_x, alto_y, salto, profundidad, paso_z, velocidad_z, velocidad_xy, filename):

    #Esta seccion sirve para evitar que el paso en Z sea mayor a la profundidad
    #Servia para no tener que cambiar el paso en Z manualmente, pero ahora no es necesario por comodidad del usuario
    #Ya que se esta acostumbrando a que el paso en Z sea negativo y se debe cambiar manualmente
    """
    if profundidad <= -0.2:
        paso_z = -0.2
    else:
        paso_z = profundidad
    """

    lines = [
        "S12000 M03 ; Velocidad de rotación de la herramienta",
        "G21 ; Unidades en mm",
        "G90 ; Posicionamiento absoluto",
        "",
        "G0 Z1 ; Subir herramienta",
        "G0 X0 Y0 ; Ir al punto de inicio",
        f"G1 Z{paso_z} F{velocidad_z} ; Bajar a profundidad de corte",
        ""
    ]


    profundidad_actual = paso_z
    while profundidad_actual >= profundidad + 0.2:
        lines.append(f"G1 Z{profundidad_actual:.3f} F{velocidad_z} ; Bajar a profundidad")
        y = 0.0
        toggle = True
        while y <= alto_y:
            if toggle:
                lines.append(f"G1 X{ancho_x:.3f} Y{y:.3f} F{velocidad_xy}")
            else:
                lines.append(f"G1 X0.000 Y{y:.3f} F{velocidad_xy}")
            y += salto
            if y <= alto_y:
                lines.append(f"G1 Y{y:.3f}")
            toggle = not toggle

        lines += [
            "",
            "G0 X0 Y0",
            ""
        ]
        lines.append(f"G1 Z{profundidad_actual:.3f} F{velocidad_z} ; Bajar a profundidad")

        """
        x = 0.0
        toggle = True
        while x <= ancho_x:
            if toggle:
                lines.append(f"G1 Y{alto_y:.3f} X{x:.3f} F{velocidad_xy}")
            else:
                lines.append(f"G1 Y0.000 X{x:.3f} F{velocidad_xy}")
            x += salto
            if x <= ancho_x:
                lines.append(f"G1 X{x:.3f}")
            toggle = not toggle

        lines += [
            "",
            "G0 X0 Y0",
            ""
        ]
        """
        profundidad_actual += paso_z
        


    lines.append(f"G1 Z{profundidad_actual:.3f} F{velocidad_z} ; Bajar a profundidad")
    y = 0.0
    toggle = True
    while y <= alto_y:
        if toggle:
            lines.append(f"G1 X{ancho_x:.3f} Y{y:.3f} F{velocidad_xy}")
        else:
            lines.append(f"G1 X0.000 Y{y:.3f} F{velocidad_xy}")
        y += salto
        if y <= alto_y:
            lines.append(f"G1 Y{y:.3f}")
        toggle = not toggle

    lines += [
        "",
        "G0 X0 Y0",
        ""
    ]

    x = 0.0
    toggle = True
    while x <= ancho_x:
        if toggle:
            lines.append(f"G1 Y{alto_y:.3f} X{x:.3f} F{velocidad_xy}")
        else:
            lines.append(f"G1 Y0.000 X{x:.3f} F{velocidad_xy}")
        x += salto
        if x <= ancho_x:
            lines.append(f"G1 X{x:.3f}")
        toggle = not toggle

    lines += [
        "",
        "G0 Z1 ; Subir herramienta",
        "G0 X0 Y0 ; Volver al inicio",
        "",
        "M30 ; Fin del programa"
    ]

    if profundidad >= 0:
        messagebox.showerror("Error", "La profundidad debe ser un valor negativo.")
        return
        

    if paso_z >= 0:
        messagebox.showerror("Error", "El paso en Z debe ser un valor negativo.")
        return

    with open(filename, "w") as f:
        f.write("\n".join(lines))
    messagebox.showinfo("Éxito", f"Archivo G-code generado:\n{filename}")


# --------------------- Función: Corte lateral en Y --------------------- #
def generar_corte_lateral_en_Y(longitud, profundidad_final, paso_z, feed_z, feed_xy, filename):

    lines = [
        "S12000 M03 ; Velocidad de la herramienta",
        "G21 ; Medida en mm",
        "G90 ; Posicionamiento Absoluto",
        "",
        "G0 Z1 ; Subir herramienta",
        "G0 X0 Y0 ; Ir al punto de inicio"
    ]

    profundidad_actual = paso_z
    while profundidad_actual >= profundidad_final:
        lines.append(f"G1 Z{profundidad_actual:.3f} F{feed_z} ; Bajar a profundidad")
        lines.append(f"G1 X0.000 Y{longitud:.3f} F{feed_xy} ; Corte de ida")
        profundidad_actual += paso_z
        lines.append(f"G1 Z{profundidad_actual:.3f} F{feed_z} ; Bajar a profundidad")
        lines.append(f"G1 X0.000 Y0.000 F{feed_xy} ; Corte de regreso")
        profundidad_actual += paso_z

    lines += [
        "",
        "G0 Z1 ; Subir herramienta",
        "G0 X0 Y0 ; Volver al inicio",
        "M30 ; Fin del programa"
    ]

    with open(filename, "w") as f:
        f.write("\n".join(lines))
    messagebox.showinfo("Éxito", f"Archivo G-code generado:\n{filename}")



# --------------------- Función: Corte lateral en X --------------------- #
def generar_corte_lateral_en_X(longitud, profundidad_final, paso_z, feed_z, feed_xy, filename):

    lines = [
        "S12000 M03 ; Velocidad de la herramienta",
        "G21 ; Medida en mm",
        "G90 ; Posicionamiento Absoluto",
        "",
        "G0 Z1 ; Subir herramienta",
        "G0 X0 Y0 ; Ir al punto de inicio"
    ]

    profundidad_actual = paso_z
    while profundidad_actual >= profundidad_final:
        lines.append(f"G1 Z{profundidad_actual:.3f} F{feed_z} ; Bajar a profundidad")
        lines.append(f"G1 X{longitud:.3f} Y0.000 F{feed_xy} ; Corte de ida")
        profundidad_actual += paso_z
        lines.append(f"G1 Z{profundidad_actual:.3f} F{feed_z} ; Bajar a profundidad")
        lines.append(f"G1 X0.000 Y0.000 F{feed_xy} ; Corte de regreso")
        profundidad_actual += paso_z


    lines += [
        "",
        "G0 Z1 ; Subir herramienta",
        "G0 X0 Y0 ; Volver al inicio",
        "M30 ; Fin del programa"
    ]

    with open(filename, "w") as f:
        f.write("\n".join(lines))
    messagebox.showinfo("Éxito", f"Archivo G-code generado:\n{filename}")



# --------------------- Función: Corte lateral para rectangulo --------------------- #
def generar_corte_lateral_para_rectangulo(ancho_x, alto_y, profundidad_final, paso_z, feed_z, feed_xy, filename):

    lines = [
        "S12000 M03 ; Velocidad de la herramienta",
        "G21 ; Medida en mm",
        "G90 ; Posicionamiento Absoluto",
        "",
        "G0 Z1 ; Subir herramienta",
        "G0 X0 Y0 ; Ir al punto de inicio"
    ]

    ancho_x += 2
    alto_y += 2
    
    profundidad_actual = paso_z
    while profundidad_actual >= profundidad_final:
        lines.append(f"G1 Z{profundidad_actual:.3f} F{feed_z} ; Bajar a profundidad")
        lines.append(f"G1 X{ancho_x:.3f} Y0.000 F{feed_xy} ; Corte de ida x")
        lines.append(f"G1 X{ancho_x:.3f} Y{alto_y:.3f} F{feed_xy} ; Corte de ida x")
        lines.append(f"G1 X0.000 Y{alto_y:.3f} F{feed_xy} ; Corte de regreso x")
        lines.append(f"G1 X0.000 Y0.000 F{feed_xy} ; Corte de regreso y")
        profundidad_actual += paso_z


    lines += [
        "",
        "G0 Z1 ; Subir herramienta",
        "G0 X0 Y0 ; Volver al inicio",
        "M30 ; Fin del programa"
    ]

    with open(filename, "w") as f:
        f.write("\n".join(lines))
    messagebox.showinfo("Éxito", f"Archivo G-code generado:\n{filename}")


# --------------------- Interfaces --------------------- #
def crear_interfaz_campos(campos, titulo, funcion_final):
    ventana = ctk.CTkToplevel()
    ventana.title(titulo)
    ventana.geometry("450x600")

    entradas = {}

    for texto in campos:
        label = ctk.CTkLabel(ventana, text=texto)
        label.pack(pady=5)
        entrada = ctk.CTkEntry(ventana, placeholder_text=texto, width=155)
        entrada.pack(pady=3)
        entradas[texto] = entrada

    def ejecutar():
        try:
            args = [float(entradas[c].get()) for c in campos]
            if paso_z := args[-2] <= 0:
                messagebox.showerror("Error", "El paso en Z debe ser un valor negativo.")
                return
            if profundidad := args[-3] >= 0:
                messagebox.showerror("Error", "La profundidad debe ser un valor negativo.")
                return
            if prfundidad_final := args[-3] >= 0:
                messagebox.showerror("Error", "La profundidad final debe ser un valor negativo.")
                return
            

            filename = filedialog.asksaveasfilename(
                defaultextension=".nc",
                filetypes=[("Archivos G-code", "*.nc"), ("Todos los archivos", "*.*")],
                title="Guardar G-code como..."
            )
            if not filename:
                return
            funcion_final(*args, filename)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    boton = ctk.CTkButton(ventana, text="Generar G-code", command=ejecutar)
    boton.pack(pady=20)


def interfaz_barrido():
    campos = [
        "Ancho X (mm)",
        "Alto Y (mm)",
        "Salto (mm)",
        "Profundidad (Z negativa)",
        "Paso en Z (negativo)",
        "Velocidad Z (F)",
        "Velocidad XY (F)"
    ]
    crear_interfaz_campos(campos, "Barrido Rectangular", generar_barrido_gcode)


def interfaz_lateral_y():
    campos = [
        "Longitud Y (mm)",
        "Profundidad Final (Z negativa)",
        "Paso en Z (negativo)",
        "Velocidad Z (F)",
        "Velocidad XY (F)"
    ]
    crear_interfaz_campos(campos, "Corte Lateral en Y", generar_corte_lateral_en_Y)


def interfaz_lateral_x():
    campos = [
        "Longitud X (mm)",
        "Profundidad Final (Z negativa)",
        "Paso en Z (negativo)",
        "Velocidad Z (F)",
        "Velocidad XY (F)"
    ]
    crear_interfaz_campos(campos, "Corte Lateral en X", generar_corte_lateral_en_X)


def interfaz_corte_rectangulo():
    campos = [
        "Ancho X (mm)",
        "Alto Y (mm)",
        "Profundidad Final (Z negativa)",
        "Paso en Z (negativo)",
        "Velocidad Z (F)",
        "Velocidad XY (F)"
    ]
    crear_interfaz_campos(campos, "Corte Lateral para Rectángulo", generar_corte_lateral_para_rectangulo)

# --------------------- Menú principal --------------------- #
def menu_principal():
    root = ctk.CTk()
    root.title("Generador de G-code")
    root.geometry("500x400")

    titulo = ctk.CTkLabel(root, text="Selecciona el tipo de G-code que deseas generar", font=ctk.CTkFont(size=20))
    titulo.pack(pady=25)

    ctk.CTkButton(root, width=200, height=40, text="Barrido rectangular", font=ctk.CTkFont(size=15), command=interfaz_barrido).pack(pady=15)
    ctk.CTkButton(root, width=200, height=40, text="Corte lateral en Y", font=ctk.CTkFont(size=15), command=interfaz_lateral_y).pack(pady=15)
    ctk.CTkButton(root, width=200, height=40, text="Corte lateral en X", font=ctk.CTkFont(size=15), command=interfaz_lateral_x).pack(pady=15)
    ctk.CTkButton(root, width=200, height=40, text="Corte lateral para rectángulo", font=ctk.CTkFont(size=15), command=interfaz_corte_rectangulo).pack(pady=15)

    root.mainloop()


# --------------------- Ejecutar --------------------- #
menu_principal()
