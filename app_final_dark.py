import customtkinter as ctk
from tkinter import filedialog, messagebox

from gcode_generator import (
    generar_barrido_gcode,
    generar_corte_lateral_en_x,
    generar_corte_lateral_en_y,
    generar_corte_lateral_para_rectangulo,
    guardar_gcode,
)


# --------------------- Configuración global --------------------- #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def _leer_valores(campos, entradas):
    valores = []
    for campo in campos:
        texto = entradas[campo].get().strip()
        if not texto:
            raise ValueError(f"El campo '{campo}' no puede estar vacío.")
        valores.append(float(texto))
    return valores


def _seleccionar_archivo_salida():
    return filedialog.asksaveasfilename(
        defaultextension=".nc",
        filetypes=[("Archivos G-code", "*.nc"), ("Todos los archivos", "*.*")],
        title="Guardar G-code como...",
    )


def crear_interfaz_campos(campos, titulo, funcion_generadora):
    ventana = ctk.CTkToplevel()
    ventana.title(titulo)
    ventana.geometry("450x600")

    entradas = {}

    for texto in campos:
        label = ctk.CTkLabel(ventana, text=texto)
        label.pack(pady=5)
        entrada = ctk.CTkEntry(ventana, placeholder_text=texto, width=180)
        entrada.pack(pady=3)
        entradas[texto] = entrada

    def ejecutar():
        try:
            args = _leer_valores(campos, entradas)
            filename = _seleccionar_archivo_salida()
            if not filename:
                return

            gcode = funcion_generadora(*args)
            guardar_gcode(filename, gcode)
            messagebox.showinfo("Éxito", f"Archivo G-code generado:\n{filename}")
        except ValueError as error:
            messagebox.showerror("Error", str(error))
        except Exception as error:
            messagebox.showerror("Error inesperado", str(error))

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
        "Velocidad XY (F)",
    ]
    crear_interfaz_campos(campos, "Barrido Rectangular", generar_barrido_gcode)


def interfaz_lateral_y():
    campos = [
        "Longitud Y (mm)",
        "Profundidad Final (Z negativa)",
        "Paso en Z (negativo)",
        "Velocidad Z (F)",
        "Velocidad XY (F)",
    ]
    crear_interfaz_campos(campos, "Corte Lateral en Y", generar_corte_lateral_en_y)


def interfaz_lateral_x():
    campos = [
        "Longitud X (mm)",
        "Profundidad Final (Z negativa)",
        "Paso en Z (negativo)",
        "Velocidad Z (F)",
        "Velocidad XY (F)",
    ]
    crear_interfaz_campos(campos, "Corte Lateral en X", generar_corte_lateral_en_x)


def interfaz_corte_rectangulo():
    campos = [
        "Ancho X (mm)",
        "Alto Y (mm)",
        "Profundidad Final (Z negativa)",
        "Paso en Z (negativo)",
        "Velocidad Z (F)",
        "Velocidad XY (F)",
    ]
    crear_interfaz_campos(campos, "Corte Lateral para Rectángulo", generar_corte_lateral_para_rectangulo)


def menu_principal():
    root = ctk.CTk()
    root.title("Generador de G-code")
    root.geometry("500x400")

    titulo = ctk.CTkLabel(
        root,
        text="Selecciona el tipo de G-code que deseas generar",
        font=ctk.CTkFont(size=20),
    )
    titulo.pack(pady=25)

    botones = [
        ("Barrido rectangular", interfaz_barrido),
        ("Corte lateral en Y", interfaz_lateral_y),
        ("Corte lateral en X", interfaz_lateral_x),
        ("Corte lateral para rectángulo", interfaz_corte_rectangulo),
    ]

    for texto, comando in botones:
        ctk.CTkButton(
            root,
            width=220,
            height=40,
            text=texto,
            font=ctk.CTkFont(size=15),
            command=comando,
        ).pack(pady=15)

    root.mainloop()


if __name__ == "__main__":
    menu_principal()
