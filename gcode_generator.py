"""Funciones puras para generar G-code de las operaciones CNC."""


def validar_parametros_corte(profundidad, paso_z):
    """Valida las convenciones principales usadas por la aplicación."""
    if profundidad >= 0:
        raise ValueError("La profundidad debe ser un valor negativo.")
    if paso_z >= 0:
        raise ValueError("El paso en Z debe ser un valor negativo.")


def _unir_lineas(lines):
    return "\n".join(lines)


def generar_barrido_gcode(ancho_x, alto_y, salto, profundidad, paso_z, velocidad_z, velocidad_xy):
    validar_parametros_corte(profundidad, paso_z)
    if salto <= 0:
        raise ValueError("El salto debe ser un valor positivo.")

    lines = [
        "S12000 M03 ; Velocidad de rotación de la herramienta",
        "G21 ; Unidades en mm",
        "G90 ; Posicionamiento absoluto",
        "",
        "G0 Z1 ; Subir herramienta",
        "G0 X0 Y0 ; Ir al punto de inicio",
        f"G1 Z{paso_z} F{velocidad_z} ; Bajar a profundidad de corte",
        "",
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
            "",
        ]
        lines.append(f"G1 Z{profundidad_actual:.3f} F{velocidad_z} ; Bajar a profundidad")
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
        "",
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
        "M30 ; Fin del programa",
    ]

    return _unir_lineas(lines)


def generar_corte_lateral_en_y(longitud, profundidad_final, paso_z, feed_z, feed_xy):
    validar_parametros_corte(profundidad_final, paso_z)

    lines = [
        "S12000 M03 ; Velocidad de la herramienta",
        "G21 ; Medida en mm",
        "G90 ; Posicionamiento Absoluto",
        "",
        "G0 Z1 ; Subir herramienta",
        "G0 X0 Y0 ; Ir al punto de inicio",
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
        "M30 ; Fin del programa",
    ]

    return _unir_lineas(lines)


def generar_corte_lateral_en_x(longitud, profundidad_final, paso_z, feed_z, feed_xy):
    validar_parametros_corte(profundidad_final, paso_z)

    lines = [
        "S12000 M03 ; Velocidad de la herramienta",
        "G21 ; Medida en mm",
        "G90 ; Posicionamiento Absoluto",
        "",
        "G0 Z1 ; Subir herramienta",
        "G0 X0 Y0 ; Ir al punto de inicio",
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
        "M30 ; Fin del programa",
    ]

    return _unir_lineas(lines)


def generar_corte_lateral_para_rectangulo(ancho_x, alto_y, profundidad_final, paso_z, feed_z, feed_xy):
    validar_parametros_corte(profundidad_final, paso_z)

    lines = [
        "S12000 M03 ; Velocidad de la herramienta",
        "G21 ; Medida en mm",
        "G90 ; Posicionamiento Absoluto",
        "",
        "G0 Z1 ; Subir herramienta",
        "G0 X0 Y0 ; Ir al punto de inicio",
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
        "M30 ; Fin del programa",
    ]

    return _unir_lineas(lines)


def guardar_gcode(filename, gcode):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(gcode)
