# App Fresadora - Generador de G-code

Aplicacion de escritorio en Python para generar archivos G-code orientados a cortes milimetricos en una fresadora CNC, originalmente pensada para una **Genmitsu 4040 Pro**. El objetivo principal del proyecto es facilitar la generacion de trayectorias repetibles para cortar o rebajar piezas de grafito, como paletas, teniendo en cuenta dimensiones, profundidad de corte, paso vertical y velocidades de avance.

La aplicacion genera archivos `.nc` que luego pueden cargarse en el software de control de la fresadora.

## Estado del proyecto

El funcionamiento base de la aplicacion esta implementado en `app_final_dark.py`. La interfaz permite seleccionar un tipo de operacion, ingresar parametros de corte y guardar el G-code resultante en un archivo `.nc`.

El repositorio tambien contiene:

- `app_final_dark.py`: codigo principal de la aplicacion.
- `app_final_dark.spec`: configuracion usada por PyInstaller para crear un ejecutable.
- `dist/app_final_dark.exe`: ejecutable generado previamente en Windows.
- `build/`: archivos internos generados por PyInstaller.

> Nota: el archivo `.exe` incluido fue generado en Windows y no se ejecuta nativamente en macOS. Para usar la app en Mac se recomienda ejecutarla con Python o generar un nuevo binario desde macOS.

## Funcionalidades principales

La aplicacion ofrece cuatro modos de generacion de G-code:

### 1. Barrido rectangular

Genera una trayectoria de barrido sobre un area rectangular definida por ancho en X y alto en Y. Esta operacion es util para rebajes superficiales o limpieza de una zona rectangular.

Parametros:

- `Ancho X (mm)`: longitud del area en el eje X.
- `Alto Y (mm)`: longitud del area en el eje Y.
- `Salto (mm)`: separacion entre pasadas.
- `Profundidad (Z negativa)`: profundidad final de trabajo.
- `Paso en Z (negativo)`: incremento vertical por pasada.
- `Velocidad Z (F)`: avance para movimientos verticales.
- `Velocidad XY (F)`: avance para movimientos horizontales.

### 2. Corte lateral en Y

Genera un corte lineal de ida y regreso sobre el eje Y, bajando progresivamente en Z hasta alcanzar la profundidad final.

Parametros:

- `Longitud Y (mm)`: distancia del corte en el eje Y.
- `Profundidad Final (Z negativa)`: profundidad final del corte.
- `Paso en Z (negativo)`: profundidad adicional por pasada.
- `Velocidad Z (F)`: avance en el eje Z.
- `Velocidad XY (F)`: avance de corte en XY.

### 3. Corte lateral en X

Genera un corte lineal de ida y regreso sobre el eje X, bajando progresivamente en Z hasta alcanzar la profundidad final.

Parametros:

- `Longitud X (mm)`: distancia del corte en el eje X.
- `Profundidad Final (Z negativa)`: profundidad final del corte.
- `Paso en Z (negativo)`: profundidad adicional por pasada.
- `Velocidad Z (F)`: avance en el eje Z.
- `Velocidad XY (F)`: avance de corte en XY.

### 4. Corte lateral para rectangulo

Genera el contorno de un rectangulo con pasadas progresivas en Z. En el codigo actual, la operacion suma 2 mm al ancho y 2 mm al alto antes de generar la trayectoria, lo cual funciona como compensacion o margen adicional de corte segun el flujo de trabajo usado originalmente.

Parametros:

- `Ancho X (mm)`: ancho base del rectangulo.
- `Alto Y (mm)`: alto base del rectangulo.
- `Profundidad Final (Z negativa)`: profundidad final del corte.
- `Paso en Z (negativo)`: profundidad adicional por pasada.
- `Velocidad Z (F)`: avance en el eje Z.
- `Velocidad XY (F)`: avance de corte en XY.

## Formato general del G-code generado

Los archivos generados siguen una estructura simple y compatible con flujos CNC comunes:

- `S12000 M03`: enciende el husillo a 12000 RPM.
- `G21`: configura unidades en milimetros.
- `G90`: usa posicionamiento absoluto.
- `G0 Z1`: eleva la herramienta antes de desplazamientos iniciales o finales.
- `G0 X0 Y0`: regresa al origen.
- `G1`: genera movimientos de corte con avance definido por `F`.
- `M30`: finaliza el programa.

La aplicacion guarda los archivos con extension `.nc` por defecto.

## Requisitos

### Requisitos minimos

- Python 3.10 o superior.
- Tkinter disponible en la instalacion de Python.
- Paquete `customtkinter`.

El proyecto fue probado originalmente en Windows. En macOS tambien puede ejecutarse, siempre que Python tenga soporte para Tkinter.

## Instalacion y ejecucion en macOS

Desde la raiz del proyecto:

```bash
cd /Users/jsob/Documents/Insutec/GitHub/App_Fresadora
```

Se recomienda crear un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install customtkinter
```

Ejecutar la aplicacion:

```bash
python app_final_dark.py
```

Si se desea probar rapidamente sin entorno virtual:

```bash
python3 -m pip install customtkinter
python3 app_final_dark.py
```

## Instalacion y ejecucion en Windows

Con Python instalado:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install customtkinter
python app_final_dark.py
```

Tambien se puede usar el ejecutable existente en `dist/app_final_dark.exe`, siempre que se este en Windows y el archivo corresponda a la version deseada del codigo.

## Generar un ejecutable

Para crear un ejecutable nuevo se puede usar PyInstaller.

Instalar dependencias:

```bash
python -m pip install pyinstaller customtkinter
```

### macOS

```bash
python -m PyInstaller --windowed --name App_Fresadora app_final_dark.py
```

El resultado quedara en la carpeta `dist/`.

### Windows

```powershell
python -m PyInstaller --onefile --windowed --name app_final_dark app_final_dark.py
```

Tambien puede usarse el archivo `.spec` existente:

```bash
python -m PyInstaller app_final_dark.spec
```

> Importante: PyInstaller genera ejecutables para el sistema operativo donde se ejecuta. Para generar un `.exe`, debe correrse en Windows. Para generar una app/binario de macOS, debe correrse en macOS.

## Uso recomendado

1. Abrir la aplicacion.
2. Seleccionar el tipo de G-code requerido.
3. Ingresar las dimensiones y parametros de corte.
4. Usar valores negativos para profundidad y paso en Z.
5. Generar el archivo `.nc`.
6. Revisar o simular el G-code antes de enviarlo a la fresadora.
7. Cargar el archivo en el software de control CNC.

## Convenciones de parametros

- Las dimensiones estan en milimetros.
- Las profundidades en Z deben ser negativas.
- El paso en Z debe ser negativo.
- Las velocidades `F` deben ser positivas.
- El origen de trabajo esperado es `X0 Y0`.
- La herramienta se eleva a `Z1` para movimientos rapidos iniciales y finales.

Ejemplo conceptual:

```text
Profundidad final: -1.0
Paso en Z: -0.2
```

Esto genera pasadas progresivas en Z hasta acercarse a la profundidad final.

## Seguridad y verificacion CNC

Antes de ejecutar cualquier archivo generado en la fresadora:

- Verificar que las dimensiones correspondan a la pieza real.
- Confirmar el diametro/radio de la herramienta usada.
- Confirmar que la compensacion aplicada sea la esperada.
- Revisar que el cero de trabajo este correctamente definido.
- Simular el G-code cuando sea posible.
- Hacer una prueba en aire o sobre material de descarte antes del corte final.
- Verificar que las velocidades de avance sean adecuadas para grafito, herramienta y maquina.

El G-code generado por esta aplicacion no reemplaza la revision del operador. El usuario debe validar que los parametros sean seguros para su maquina, material, herramienta y montaje.

## Notas tecnicas

- La interfaz esta construida con `customtkinter`.
- `tkinter` se usa para dialogos de archivo y mensajes.
- No hay dependencias externas adicionales para la generacion del G-code.
- El codigo escribe directamente el archivo seleccionado por el usuario.
- El proyecto no requiere conexion a internet para ejecutarse, salvo para instalar paquetes inicialmente.

## Posibles mejoras futuras

- Separar la logica de generacion de G-code de la interfaz grafica.
- Agregar pruebas automaticas para validar salidas G-code.
- Incluir previsualizacion de trayectoria.
- Permitir configurar RPM del husillo desde la interfaz.
- Permitir configurar altura segura en Z.
- Documentar formalmente la compensacion de herramienta.
- Crear instaladores separados para Windows y macOS.
- Agregar ejemplos de archivos `.nc` generados.

## Licencia

No se ha definido una licencia formal para este proyecto. Antes de distribuirlo publicamente, se recomienda agregar una licencia acorde al uso esperado.
