import pytest

from gcode_generator import (
    generar_barrido_gcode,
    generar_corte_lateral_en_x,
    generar_corte_lateral_en_y,
    generar_corte_lateral_para_rectangulo,
    guardar_gcode,
)


def lineas(gcode):
    return gcode.splitlines()


@pytest.mark.parametrize(
    "generador,args,primera_linea",
    [
        (
            generar_barrido_gcode,
            (10, 5, 1, -0.4, -0.2, 100, 200),
            "S12000 M03 ; Velocidad de rotación de la herramienta",
        ),
        (
            generar_corte_lateral_en_x,
            (10, -0.4, -0.2, 100, 200),
            "S12000 M03 ; Velocidad de la herramienta",
        ),
        (
            generar_corte_lateral_en_y,
            (10, -0.4, -0.2, 100, 200),
            "S12000 M03 ; Velocidad de la herramienta",
        ),
        (
            generar_corte_lateral_para_rectangulo,
            (10, 5, -0.4, -0.2, 100, 200),
            "S12000 M03 ; Velocidad de la herramienta",
        ),
    ],
)
def test_programas_inician_configuran_unidades_y_finalizan(generador, args, primera_linea):
    codigo = generador(*args)
    resultado = lineas(codigo)

    assert resultado[0] == primera_linea
    assert any(linea.startswith("G21") for linea in resultado)
    assert any(linea.startswith("G90") for linea in resultado)
    assert resultado[-1] == "M30 ; Fin del programa"


def test_corte_lateral_x_genera_ida_y_regreso_con_profundidades():
    codigo = generar_corte_lateral_en_x(
        longitud=10,
        profundidad_final=-0.4,
        paso_z=-0.2,
        feed_z=100,
        feed_xy=200,
    )
    resultado = lineas(codigo)

    assert "G1 Z-0.200 F100 ; Bajar a profundidad" in resultado
    assert "G1 X10.000 Y0.000 F200 ; Corte de ida" in resultado
    assert "G1 Z-0.400 F100 ; Bajar a profundidad" in resultado
    assert "G1 X0.000 Y0.000 F200 ; Corte de regreso" in resultado


def test_corte_lateral_y_genera_ida_y_regreso_con_profundidades():
    codigo = generar_corte_lateral_en_y(
        longitud=12,
        profundidad_final=-0.4,
        paso_z=-0.2,
        feed_z=90,
        feed_xy=180,
    )
    resultado = lineas(codigo)

    assert "G1 Z-0.200 F90 ; Bajar a profundidad" in resultado
    assert "G1 X0.000 Y12.000 F180 ; Corte de ida" in resultado
    assert "G1 Z-0.400 F90 ; Bajar a profundidad" in resultado
    assert "G1 X0.000 Y0.000 F180 ; Corte de regreso" in resultado


def test_barrido_genera_pasadas_en_x_y_y():
    codigo = generar_barrido_gcode(
        ancho_x=4,
        alto_y=2,
        salto=1,
        profundidad=-0.4,
        paso_z=-0.2,
        velocidad_z=100,
        velocidad_xy=200,
    )
    resultado = lineas(codigo)

    assert "G1 X4.000 Y0.000 F200" in resultado
    assert "G1 X0.000 Y1.000 F200" in resultado
    assert "G1 Y2.000 X0.000 F200" in resultado
    assert "G1 Y0.000 X1.000 F200" in resultado


def test_rectangulo_aplica_compensacion_de_dos_milimetros():
    codigo = generar_corte_lateral_para_rectangulo(
        ancho_x=10,
        alto_y=5,
        profundidad_final=-0.2,
        paso_z=-0.2,
        feed_z=100,
        feed_xy=200,
    )
    resultado = lineas(codigo)

    assert "G1 X12.000 Y0.000 F200 ; Corte de ida x" in resultado
    assert "G1 X12.000 Y7.000 F200 ; Corte de ida x" in resultado
    assert "G1 X0.000 Y7.000 F200 ; Corte de regreso x" in resultado


@pytest.mark.parametrize(
    "generador,args",
    [
        (generar_barrido_gcode, (10, 5, 1, 0.4, -0.2, 100, 200)),
        (generar_corte_lateral_en_x, (10, 0.4, -0.2, 100, 200)),
        (generar_corte_lateral_en_y, (10, 0.4, -0.2, 100, 200)),
        (generar_corte_lateral_para_rectangulo, (10, 5, 0.4, -0.2, 100, 200)),
    ],
)
def test_rechaza_profundidades_positivas(generador, args):
    with pytest.raises(ValueError, match="profundidad"):
        generador(*args)


@pytest.mark.parametrize(
    "generador,args",
    [
        (generar_barrido_gcode, (10, 5, 1, -0.4, 0.2, 100, 200)),
        (generar_corte_lateral_en_x, (10, -0.4, 0.2, 100, 200)),
        (generar_corte_lateral_en_y, (10, -0.4, 0.2, 100, 200)),
        (generar_corte_lateral_para_rectangulo, (10, 5, -0.4, 0.2, 100, 200)),
    ],
)
def test_rechaza_paso_z_positivo(generador, args):
    with pytest.raises(ValueError, match="paso en Z"):
        generador(*args)


def test_barrido_rechaza_salto_cero_para_evitar_ciclos_infinitos():
    with pytest.raises(ValueError, match="salto"):
        generar_barrido_gcode(10, 5, 0, -0.4, -0.2, 100, 200)


def test_guardar_gcode_escribe_archivo_nc(tmp_path):
    destino = tmp_path / "corte.nc"
    codigo = generar_corte_lateral_en_x(10, -0.2, -0.2, 100, 200)

    guardar_gcode(destino, codigo)

    assert destino.read_text(encoding="utf-8") == codigo
