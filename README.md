* Guide created with chatgpt


# 🚗 Car Settings Automation with Raspberry Pi Pico RP2040-Zero

> **ES:** Automatización de configuraciones de un sistema multimedia de vehículo mediante emulación USB HID (mouse + teclado).  
> **EN:** Vehicle infotainment settings automation through USB HID emulation (mouse + keyboard).

---

## Table of Contents

- [🇪🇸 Español](#-español)
  - [1. Resumen](#1-resumen)
  - [2. Objetivo del proyecto](#2-objetivo-del-proyecto)
  - [3. Cómo funciona](#3-cómo-funciona)
  - [4. Arquitectura](#4-arquitectura)
  - [5. Estructura del repositorio](#5-estructura-del-repositorio)
  - [6. Requisitos](#6-requisitos)
  - [7. Instalación y despliegue](#7-instalación-y-despliegue)
  - [8. Formato del archivo `macro.json`](#8-formato-del-archivo-macrojson)
  - [9. Configuración global](#9-configuración-global)
  - [10. Secciones](#10-secciones)
  - [11. Tipos de pasos soportados](#11-tipos-de-pasos-soportados)
  - [12. Flujo interno de ejecución](#12-flujo-interno-de-ejecución)
  - [13. Cómo interpretar las coordenadas](#13-cómo-interpretar-las-coordenadas)
  - [14. Buenas prácticas para crear macros](#14-buenas-prácticas-para-crear-macros)
  - [15. Ejemplo de uso real](#15-ejemplo-de-uso-real)
  - [16. Limitaciones](#16-limitaciones)
  - [17. Seguridad y responsabilidad](#17-seguridad-y-responsabilidad)
  - [18. Posibles mejoras](#18-posibles-mejoras)
  - [19. Licencia](#19-licencia)
- [🇺🇸 English](#-english)
  - [1. Overview](#1-overview)
  - [2. Project goal](#2-project-goal)
  - [3. How it works](#3-how-it-works)
  - [4. Architecture](#4-architecture)
  - [5. Repository structure](#5-repository-structure)
  - [6. Requirements](#6-requirements)
  - [7. Installation and deployment](#7-installation-and-deployment)
  - [8. `macro.json` file format](#8-macrojson-file-format)
  - [9. Global configuration](#9-global-configuration)
  - [10. Sections](#10-sections)
  - [11. Supported step types](#11-supported-step-types)
  - [12. Internal execution flow](#12-internal-execution-flow)
  - [13. How to interpret coordinates](#13-how-to-interpret-coordinates)
  - [14. Best practices for writing macros](#14-best-practices-for-writing-macros)
  - [15. Real-world usage example](#15-real-world-usage-example)
  - [16. Limitations](#16-limitations)
  - [17. Safety and responsibility](#17-safety-and-responsibility)
  - [18. Possible improvements](#18-possible-improvements)
  - [19. License](#19-license)

---

# 🇪🇸 Español

## 1. Resumen

Este proyecto automatiza acciones repetitivas dentro del sistema multimedia de un vehículo utilizando una **Raspberry Pi Pico RP2040-Zero** como dispositivo **USB HID**.  
En la práctica, la placa se presenta ante el vehículo como si fuera un **mouse USB** y un **teclado USB**, permitiendo ejecutar una secuencia programada de movimientos, clicks, scrolls y combinaciones de teclas.

La lógica de automatización está separada en dos partes:

- **`code.py`**: motor de ejecución
- **`macro.json`**: definición declarativa de las acciones a realizar

Esto permite cambiar el comportamiento del sistema sin tocar el código principal, simplemente editando el archivo de configuración.

## 🚗 Vehículo objetivo

Esta implementación fue probada en:

- **Vehículo:** Ora 03 GT
- **Sistema multimedia:** basado en Android

## 🔧 Personalizaciones

Este repositorio incluye macros específicas para este vehículo, incluyendo:

- activación de e-pedal
- modo eco+ (opcional)
- configuración de asistencia de carril
- **masaje del asiento del conductor (modo bajo únicamente)**

> ⚠️ Nota: Solo se implementó y calibró el masaje del conductor en modo "bajo".
No incluye el asiento del pasajero ni otros niveles.

---

## 2. Objetivo del proyecto

El objetivo es recuperar automáticamente configuraciones del vehículo que no quedan guardadas de forma persistente o que requieren demasiados pasos manuales cada vez que el sistema arranca.

Ejemplos típicos:

- activar un modo específico;
- desactivar asistencias que vuelven a encenderse solas;
- navegar hasta un menú determinado;
- volver a Android Auto o Apple CarPlay;
- aplicar varias preferencias de forma secuencial.

La idea central es simple: **si una persona puede hacerlo con clicks y teclas, este sistema puede reproducirlo**.

---

## 3. Cómo funciona

Cuando la placa arranca, el script:

1. inicializa la interfaz HID;
2. carga el archivo `macro.json`;
3. lee la configuración global;
4. recorre todas las secciones declaradas;
5. ejecuta únicamente las que estén marcadas como activas;
6. procesa los pasos uno por uno respetando tiempos y orden;
7. queda en espera permanente al finalizar.

Las acciones disponibles son:

- esperar una cantidad de segundos;
- volver a la pantalla principal;
- mover el mouse y hacer click;
- ejecutar múltiples clicks;
- hacer scroll.

Todo el flujo está pensado para operar sobre interfaces gráficas que no ofrecen API ni integración directa, por lo que la automatización se resuelve **simulando interacción humana**.

---

## 4. Arquitectura

### 4.1 `code.py`: motor de automatización

El archivo `code.py` implementa toda la lógica operativa. Sus responsabilidades principales son:

- inicializar el teclado y mouse HID;
- cargar y parsear el archivo JSON;
- convertir valores tipo “si/no” a booleanos reales;
- reiniciar el puntero cuando corresponda;
- ejecutar clicks relativos;
- hacer scroll;
- simular la combinación de teclas para volver a Home;
- recorrer secciones y pasos en orden;
- ignorar secciones inactivas;
- ignorar pasos desconocidos sin detener toda la macro;
- escribir mensajes de log por consola serie.

### 4.2 `macro.json`: definición de la macro

El archivo `macro.json` describe **qué** debe hacerse, mientras que `code.py` define **cómo** se ejecuta.

Ese diseño tiene varias ventajas:

- separar lógica de ejecución y contenido;
- facilitar cambios sin editar el programa principal;
- permitir activar o desactivar bloques enteros;
- simplificar pruebas y calibraciones;
- hacer el proyecto más mantenible.

### 4.3 Enfoque general

La automatización está basada en coordenadas relativas y secuencias temporizadas.  
No existe lectura del estado real de la pantalla ni validación visual, por lo que el comportamiento es determinista: el sistema “asume” que cada paso produjo el efecto esperado antes de avanzar al siguiente.

---

## 5. Estructura del repositorio

```text
.
├── code.py
├── macro.json
└── README.md
```

### Descripción de archivos

- **`code.py`**  
  Script principal que se ejecuta en la placa y procesa la macro.

- **`macro.json`**  
  Archivo de configuración con secciones, pasos y parámetros globales.

- **`README.md`**  
  Documentación del proyecto.

---

## 6. Requisitos

Para ejecutar este proyecto se necesita:

- una **Raspberry Pi Pico RP2040-Zero** o placa compatible con RP2040;
- un entorno de ejecución compatible con `usb_hid` y `adafruit_hid` (habitualmente **CircuitPython**);
- la librería `adafruit_hid` instalada en la placa;
- un cable USB de datos;
- acceso al sistema del vehículo que acepte un dispositivo HID por USB;
- calibración previa de coordenadas y tiempos.

### Dependencias observables en el código

El script usa:

- `time`
- `json`
- `usb_hid`
- `adafruit_hid.keyboard`
- `adafruit_hid.keycode`
- `adafruit_hid.mouse`

---

## 7. Instalación y despliegue

## 7.1 Preparar la placa

Cargar en la placa un firmware compatible con el script, normalmente CircuitPython.

## 7.2 Copiar archivos

Copiar al almacenamiento visible de la placa:

- `code.py`
- `macro.json`

## 7.3 Instalar librerías necesarias

Asegurarse de que la librería `adafruit_hid` esté disponible en la carpeta `lib/` de la placa.

## 7.4 Ajustar la macro

Editar `macro.json` con:

- los tiempos adecuados;
- las secciones que se quieran activar;
- las coordenadas correctas para la interfaz del vehículo.

## 7.5 Conectar al vehículo

Al alimentar la placa y ser detectada como HID, comenzará a ejecutar la macro automáticamente.

> **Importante:** este proyecto depende completamente del layout y del comportamiento exacto de la interfaz objetivo.

---

## 8. Formato del archivo `macro.json`

La estructura general es:

```json
{
  "configuracion": {
    "reiniciar_puntero_al_inicio": "no",
    "reiniciar_puntero_antes_de_cada_click": "si",
    "delay_entre_pasos_ms": 150
  },
  "secciones": [
    {
      "descripcion": "Activar eco+",
      "activo": "si",
      "pasos": [
        { "tipo": "esperar", "segundos": 10 },
        { "tipo": "ir_a_home", "veces": 1 },
        { "tipo": "click", "dx": 50, "dy": 150 }
      ]
    }
  ]
}
```

Tiene dos bloques principales:

- **`configuracion`**: parámetros globales
- **`secciones`**: conjunto de macros o grupos de pasos

---

## 9. Configuración global

### 9.1 `reiniciar_puntero_al_inicio`

```json
"reiniciar_puntero_al_inicio": "no"
```

Si está activo, al inicio de la ejecución el sistema mueve el cursor fuertemente hacia `(-3000, -3000)` para intentar llevarlo a una esquina de referencia.

Esto ayuda a partir de una posición conocida antes de ejecutar la primera acción.

### 9.2 `reiniciar_puntero_antes_de_cada_click`

```json
"reiniciar_puntero_antes_de_cada_click": "si"
```

Si está activo, antes de cada click el puntero vuelve a la posición de referencia.  
Esto evita que pequeños errores acumulados terminen desplazando toda la macro con el paso del tiempo.

En la práctica, esta opción suele ser muy útil cuando las acciones están pensadas como coordenadas relativas desde una base fija.

### 9.3 `delay_entre_pasos_ms`

```json
"delay_entre_pasos_ms": 150
```

Define el delay base entre pasos consecutivos, expresado en milisegundos.

Este parámetro impacta directamente en:

- estabilidad de la secuencia;
- tolerancia de la interfaz a entradas rápidas;
- confiabilidad general de la macro.

---

## 10. Secciones

Cada objeto dentro de `secciones` representa una macro independiente.

Ejemplo:

```json
{
  "descripcion": "Volver a Android Auto - Apple Car Play",
  "activo": "si",
  "pasos": [
    { "tipo": "esperar", "segundos": 1 },
    { "tipo": "ir_a_home", "veces": 1 },
    { "tipo": "click", "dx": 50, "dy": 310 }
  ]
}
```

### Campos de una sección

#### `descripcion`
Texto descriptivo para identificar la intención de esa sección.

#### `activo`
Permite habilitar o deshabilitar la ejecución de la sección sin borrarla.

#### `pasos`
Lista ordenada de acciones a ejecutar.

### Comportamiento en ejecución

- Si `activo` es falso, la sección se omite.
- Si `activo` es verdadero, se ejecuta completa en el orden declarado.
- No existe validación de resultados intermedios.

---

## 11. Tipos de pasos soportados

## 11.1 `esperar`

```json
{ "tipo": "esperar", "segundos": 10 }
```

Suspende la ejecución la cantidad de segundos indicada.

Uso típico:

- esperar que el sistema multimedia termine de iniciar;
- dejar tiempo entre pantallas;
- sincronizar la macro con animaciones o cargas lentas.

---

## 11.2 `ir_a_home`

```json
{ "tipo": "ir_a_home", "veces": 1 }
```

Ejecuta la función `ir_a_home()`, que internamente llama a `alt_esc()` una o más veces.

En el código, `alt_esc()` presiona:

- `LEFT_ALT`
- `ESCAPE`

Esto simula una combinación de teclado que, en la interfaz objetivo, sirve para volver a una pantalla anterior o principal.

> El efecto exacto depende de cómo responda el sistema receptor a esa combinación.

---

## 11.3 `click`

```json
{ "tipo": "click", "dx": 300, "dy": 280, "nota": "Entrar a Configuración" }
```

Realiza un movimiento relativo del mouse y luego hace click izquierdo.

### Campos relevantes

- `dx`: desplazamiento horizontal
- `dy`: desplazamiento vertical
- `nota`: comentario opcional para documentar la intención

### Detalle de ejecución

1. opcionalmente reinicia puntero;
2. mueve el mouse a `(dx, dy)` respecto del punto base actual;
3. espera el delay configurado;
4. ejecuta click izquierdo;
5. espera una pequeña pausa adicional.

---

## 11.4 `clicks`

```json
{
  "tipo": "clicks",
  "lista": [
    { "dx": 400, "dy": 210 },
    { "dx": 450, "dy": 250 }
  ]
}
```

Permite agrupar múltiples clicks dentro de un mismo paso.

Cada elemento de `lista` se ejecuta como un click independiente y respeta la lógica de reinicio de puntero si esa opción está activa.

Es útil cuando varias acciones consecutivas forman parte de una misma intención lógica.

---

## 11.5 `scroll`

```json
{ "tipo": "scroll", "direccion": "abajo", "ticks": 800 }
```

Realiza scroll mediante la rueda virtual del mouse.

### Campos

- `direccion`: `arriba` / `abajo` (también acepta `up`)
- `ticks`: magnitud del scroll

### Implementación

En el código:

- `arriba` / `up` → wheel negativo
- cualquier otro valor → wheel positivo

Esto se adapta a la convención habitual de muchos sistemas, pero puede variar según el receptor.

---

## 11.6 Pasos desconocidos

Si un paso tiene un `tipo` no soportado, el script no se detiene.  
Simplemente registra un mensaje de log y continúa.

Eso vuelve al motor relativamente tolerante a errores de edición o extensiones futuras.

---

## 12. Flujo interno de ejecución

El flujo real del programa puede resumirse así:

```text
Inicio
 ├─ Inicializar teclado y mouse HID
 ├─ Cargar macro.json
 ├─ Leer configuración global
 ├─ Reiniciar puntero al inicio (opcional)
 ├─ Recorrer secciones
 │   ├─ ¿Está activa?
 │   │   ├─ No → saltar
 │   │   └─ Sí → ejecutar pasos
 │   │       ├─ esperar
 │   │       ├─ ir_a_home
 │   │       ├─ click
 │   │       ├─ clicks
 │   │       └─ scroll
 ├─ Log "Macro finalizado"
 └─ Espera infinita
```

### Detalles importantes del flujo

- El orden de los pasos importa totalmente.
- No hay paralelismo.
- No hay reintentos automáticos.
- No hay detección de error visual.
- El programa termina la macro y luego queda en un loop infinito de espera.

Ese loop final evita que el script “salga” y mantiene la placa estable una vez completada la automatización.

---

## 13. Cómo interpretar las coordenadas

Las coordenadas `dx` y `dy` son **relativas**, no absolutas.

Eso significa que cada click parte desde:

- la posición actual del cursor; o
- la posición de referencia, si se reinicia el puntero antes de cada click.

### Consecuencia práctica

La precisión depende mucho de:

- usar siempre el mismo layout de pantalla;
- que el cursor comience desde una posición consistente;
- que no haya elementos emergentes o cambios inesperados;
- que las pantallas carguen en tiempos similares.

### Estrategia habitual

Una estrategia común y robusta es:

1. reiniciar puntero antes de cada click;
2. usar siempre coordenadas calibradas desde esa base;
3. agregar esperas donde la interfaz sea lenta;
4. validar paso a paso durante el ajuste inicial.

---

## 14. Buenas prácticas para crear macros

- Empezar con una sola sección pequeña.
- Activar una sección a la vez.
- Usar descripciones claras y específicas.
- Agregar notas en pasos críticos.
- Incluir esperas generosas durante la calibración.
- Recién después optimizar tiempos.
- Evitar depender de animaciones largas o variables.
- Revisar la macro después de cualquier cambio de software del vehículo.
- Mantener una copia de seguridad de configuraciones que funcionen.

---

## 15. Ejemplo de uso real

Con la estructura actual del proyecto se pueden automatizar tareas como:

- activar **eco+**;
- activar **e-pedal**;
- desactivar una asistencia de carril;
- volver a **Android Auto / Apple CarPlay**.

El archivo `macro.json` de este repositorio demuestra justamente ese enfoque: cada comportamiento está encapsulado en una sección separada y puede activarse o desactivarse individualmente.

Esto hace posible:

- probar funciones por separado;
- encadenar varias preferencias;
- mantener una macro modular y entendible.

---

## 16. Limitaciones

Este proyecto tiene varias limitaciones importantes que deben entenderse antes de usarlo:

### 16.1 No existe feedback del sistema

La placa no “ve” la pantalla ni recibe confirmaciones de éxito.  
Solo envía eventos HID.

### 16.2 Dependencia total del layout

Si cambia cualquier cosa de la interfaz:

- posición de botones;
- resolución;
- escalado;
- menús;
- tiempos de carga;

la macro puede fallar o ejecutar acciones incorrectas.

### 16.3 Dependencia temporal

Si una pantalla tarda más de lo esperado, los pasos siguientes pueden quedar desfasados.

### 16.4 No hay validación contextual

El script no sabe en qué pantalla está.  
Simplemente ejecuta el siguiente paso.

### 16.5 No hay recuperación automática

Si algo sale mal a mitad de la secuencia, el programa no corrige el estado ni vuelve atrás por sí mismo.

---

## 17. Seguridad y responsabilidad

Este proyecto debe usarse con criterio.  
La automatización interactúa con funciones del vehículo y puede modificar ajustes del sistema.

Recomendaciones básicas:

- calibrar siempre con el vehículo detenido;
- probar en un entorno controlado;
- no ajustar coordenadas ni tiempos mientras se conduce;
- validar cada sección por separado antes de usar una secuencia larga;
- asumir que cualquier actualización del sistema puede requerir recalibración.

Este repositorio documenta un enfoque técnico de automatización HID.  
Cada usuario es responsable de evaluar su conveniencia, seguridad y compatibilidad con su entorno.

---

## 18. Posibles mejoras

Algunas extensiones futuras interesantes serían:

- herramienta de calibración visual de coordenadas;
- perfiles por vehículo o versión de software;
- macros condicionales;
- soporte para pasos reutilizables;
- logs más detallados;
- sistema de abortado manual;
- selección de macros por botón físico;
- archivo de configuración más expresivo;
- documentación de pruebas y troubleshooting.

---

## 19. Licencia

Podés publicar este proyecto bajo la licencia que prefieras.

Opciones habituales:

- **MIT** si querés máxima simplicidad;
- **Apache-2.0** si querés una licencia más explícita;
- **GPL** si querés obligar a compartir derivados bajo la misma licencia.

Si no tenés una preferencia definida, **MIT** suele ser una buena opción para proyectos de este estilo.

---

# 🇺🇸 English

## 1. Overview

This project automates repetitive actions inside a vehicle infotainment system using a **Raspberry Pi Pico RP2040-Zero** as a **USB HID** device.  
In practice, the board presents itself to the vehicle as a **USB mouse** and a **USB keyboard**, allowing it to execute a programmed sequence of movements, clicks, scrolls, and key combinations.

The automation logic is split into two parts:

- **`code.py`**: execution engine
- **`macro.json`**: declarative definition of the actions to perform

This makes it possible to change the system behavior without touching the main code, simply by editing the configuration file.

## 🚗 Target Vehicle

This implementation was tested on:

- **Vehicle:** Ora 03 GT
- **Infotainment system:** Android-based OEM system

## 🔧 Customizations

This repository includes custom macros specifically developed for this vehicle, including:

- e-pedal activation
- eco+ mode (optional)
- lane assist configuration
- **driver seat massage (low mode only)**

> ⚠️ Note: Only the driver seat massage in **low** mode was implemented and calibrated.  
> Passenger seat massage and other massage levels are not included yet.

---

## 2. Project goal

The goal is to automatically restore vehicle settings that are not persistently saved or that require too many manual steps every time the system starts.

Typical examples:

- enabling a specific mode;
- disabling driver assistance features that turn themselves back on;
- navigating to a specific menu;
- returning to Android Auto or Apple CarPlay;
- applying multiple preferences in sequence.

The core idea is simple: **if a person can do it with clicks and keys, this system can replay it**.

---

## 3. How it works

When the board starts, the script:

1. initializes the HID interface;
2. loads the `macro.json` file;
3. reads the global configuration;
4. iterates through all declared sections;
5. executes only the ones marked as active;
6. processes steps one by one while preserving timing and order;
7. remains in an infinite idle state after completion.

The available actions are:

- wait for a number of seconds;
- return to the main screen;
- move the mouse and click;
- execute multiple clicks;
- scroll.

The whole flow is designed for graphical interfaces that do not provide an API or direct integration, so automation is solved by **simulating human interaction**.

---

## 4. Architecture

### 4.1 `code.py`: automation engine

The `code.py` file implements the full operational logic. Its main responsibilities are:

- initialize HID keyboard and mouse devices;
- load and parse the JSON file;
- convert “yes/no” style values into actual booleans;
- reset the pointer when required;
- execute relative clicks;
- perform scrolling;
- simulate the key combination used to return Home;
- iterate over sections and steps in order;
- skip inactive sections;
- ignore unknown step types without stopping the full macro;
- print log messages to the serial console.

### 4.2 `macro.json`: macro definition

The `macro.json` file describes **what** must be done, while `code.py` defines **how** it is executed.

That design provides several benefits:

- separating execution logic from content;
- simplifying changes without editing the main program;
- allowing entire blocks to be enabled or disabled;
- making testing and calibration easier;
- improving maintainability.

### 4.3 General approach

The automation is based on relative coordinates and timed sequences.  
There is no real screen-state reading or visual validation, so the behavior is deterministic: the system “assumes” each step had the expected effect before moving to the next one.

---

## 5. Repository structure

```text
.
├── code.py
├── macro.json
└── README.md
```

### File descriptions

- **`code.py`**  
  Main script executed on the board that processes the macro.

- **`macro.json`**  
  Configuration file containing sections, steps, and global parameters.

- **`README.md`**  
  Project documentation.

---

## 6. Requirements

To run this project you need:

- a **Raspberry Pi Pico RP2040-Zero** or compatible RP2040 board;
- a runtime environment compatible with `usb_hid` and `adafruit_hid` (commonly **CircuitPython**);
- the `adafruit_hid` library installed on the board;
- a USB data cable;
- access to the vehicle system that accepts a USB HID device;
- prior calibration of coordinates and timings.

### Dependencies visible in the code

The script uses:

- `time`
- `json`
- `usb_hid`
- `adafruit_hid.keyboard`
- `adafruit_hid.keycode`
- `adafruit_hid.mouse`

---

## 7. Installation and deployment

## 7.1 Prepare the board

Flash the board with firmware compatible with the script, usually CircuitPython.

## 7.2 Copy files

Copy these files to the board storage:

- `code.py`
- `macro.json`

## 7.3 Install required libraries

Make sure the `adafruit_hid` library is available in the board’s `lib/` folder.

## 7.4 Adjust the macro

Edit `macro.json` with:

- suitable timing values;
- the sections you want to enable;
- the correct coordinates for the vehicle UI.

## 7.5 Connect to the vehicle

When the board is powered and detected as an HID device, it will automatically start executing the macro.

> **Important:** this project depends entirely on the exact layout and behavior of the target interface.

---

## 8. `macro.json` file format

The general structure is:

```json
{
  "configuracion": {
    "reiniciar_puntero_al_inicio": "no",
    "reiniciar_puntero_antes_de_cada_click": "si",
    "delay_entre_pasos_ms": 150
  },
  "secciones": [
    {
      "descripcion": "Enable eco+",
      "activo": "yes",
      "pasos": [
        { "tipo": "esperar", "segundos": 10 },
        { "tipo": "ir_a_home", "veces": 1 },
        { "tipo": "click", "dx": 50, "dy": 150 }
      ]
    }
  ]
}
```

It contains two main blocks:

- **`configuracion`**: global parameters
- **`secciones`**: collection of macros or step groups

---

## 9. Global configuration

### 9.1 `reiniciar_puntero_al_inicio`

```json
"reiniciar_puntero_al_inicio": "no"
```

If enabled, at startup the system moves the pointer strongly toward `(-3000, -3000)` to try to force it into a reference corner.

This helps begin from a known position before executing the first action.

### 9.2 `reiniciar_puntero_antes_de_cada_click`

```json
"reiniciar_puntero_antes_de_cada_click": "si"
```

If enabled, before every click the pointer is returned to the reference position.  
This prevents small accumulated errors from shifting the whole macro over time.

In practice, this option is usually very useful when actions are designed as relative coordinates from a fixed base position.

### 9.3 `delay_entre_pasos_ms`

```json
"delay_entre_pasos_ms": 150
```

Defines the base delay between consecutive steps, expressed in milliseconds.

This parameter directly affects:

- sequence stability;
- interface tolerance to rapid input;
- overall macro reliability.

---

## 10. Sections

Each object inside `secciones` represents an independent macro.

Example:

```json
{
  "descripcion": "Return to Android Auto - Apple Car Play",
  "activo": "yes",
  "pasos": [
    { "tipo": "esperar", "segundos": 1 },
    { "tipo": "ir_a_home", "veces": 1 },
    { "tipo": "click", "dx": 50, "dy": 310 }
  ]
}
```

### Section fields

#### `descripcion`
Descriptive text used to identify the purpose of the section.

#### `activo`
Allows the section to be enabled or disabled without deleting it.

#### `pasos`
Ordered list of actions to execute.

### Runtime behavior

- If `activo` is false, the section is skipped.
- If `activo` is true, the section runs completely in the declared order.
- There is no validation of intermediate results.

---

## 11. Supported step types

## 11.1 `esperar`

```json
{ "tipo": "esperar", "segundos": 10 }
```

Pauses execution for the specified number of seconds.

Typical usage:

- waiting for the infotainment system to finish booting;
- leaving time between screens;
- synchronizing the macro with animations or slow loading screens.

---

## 11.2 `ir_a_home`

```json
{ "tipo": "ir_a_home", "veces": 1 }
```

Calls the `ir_a_home()` function, which internally invokes `alt_esc()` one or more times.

In the code, `alt_esc()` presses:

- `LEFT_ALT`
- `ESCAPE`

This simulates a key combination that, on the target interface, is used to return to a previous or main screen.

> The exact effect depends on how the receiving system responds to that key combination.

---

## 11.3 `click`

```json
{ "tipo": "click", "dx": 300, "dy": 280, "nota": "Open Settings" }
```

Performs a relative mouse movement and then executes a left click.

### Relevant fields

- `dx`: horizontal offset
- `dy`: vertical offset
- `nota`: optional comment documenting the intention

### Execution detail

1. optionally reset pointer;
2. move the mouse to `(dx, dy)` relative to the current base point;
3. wait for the configured delay;
4. perform a left click;
5. wait for a small additional pause.

---

## 11.4 `clicks`

```json
{
  "tipo": "clicks",
  "lista": [
    { "dx": 400, "dy": 210 },
    { "dx": 450, "dy": 250 }
  ]
}
```

Allows grouping multiple clicks into a single step.

Each item in `lista` is executed as an independent click and follows the same pointer reset behavior if that option is enabled.

It is useful when several consecutive actions belong to the same logical intent.

---

## 11.5 `scroll`

```json
{ "tipo": "scroll", "direccion": "down", "ticks": 800 }
```

Performs scrolling through the virtual mouse wheel.

### Fields

- `direccion`: `arriba` / `abajo` (also accepts `up`)
- `ticks`: scroll magnitude

### Implementation

In the code:

- `arriba` / `up` → negative wheel movement
- any other value → positive wheel movement

This follows the common convention of many systems, but behavior may vary depending on the receiver.

---

## 11.6 Unknown steps

If a step has an unsupported `tipo`, the script does not stop.  
It simply logs a message and continues.

That makes the engine relatively tolerant to editing mistakes or future extensions.

---

## 12. Internal execution flow

The actual program flow can be summarized as follows:

```text
Start
 ├─ Initialize HID keyboard and mouse
 ├─ Load macro.json
 ├─ Read global configuration
 ├─ Reset pointer at startup (optional)
 ├─ Iterate through sections
 │   ├─ Is it active?
 │   │   ├─ No → skip
 │   │   └─ Yes → execute steps
 │   │       ├─ esperar
 │   │       ├─ ir_a_home
 │   │       ├─ click
 │   │       ├─ clicks
 │   │       └─ scroll
 ├─ Log "Macro finalizado"
 └─ Infinite idle loop
```

### Important flow details

- Step order matters completely.
- There is no parallelism.
- There are no automatic retries.
- There is no visual error detection.
- The program finishes the macro and then remains in an infinite idle loop.

That final loop prevents the script from “exiting” and keeps the board stable once the automation has completed.

---

## 13. How to interpret coordinates

The `dx` and `dy` coordinates are **relative**, not absolute.

That means every click starts from:

- the current pointer position; or
- the reference position, if pointer reset is enabled before each click.

### Practical consequence

Accuracy depends heavily on:

- always using the same screen layout;
- ensuring the cursor starts from a consistent position;
- preventing popups or unexpected UI changes;
- having similar screen loading times.

### Common strategy

A common and robust strategy is to:

1. reset the pointer before each click;
2. always use calibrated coordinates from that base;
3. add waits where the interface is slow;
4. validate step by step during initial tuning.

---

## 14. Best practices for writing macros

- Start with a single small section.
- Enable one section at a time.
- Use clear and specific descriptions.
- Add notes to critical steps.
- Use generous waits during calibration.
- Only optimize timings afterward.
- Avoid depending on long or variable animations.
- Review the macro after any vehicle software update.
- Keep a backup of known-good configurations.

---

## 15. Real-world usage example

With the current project structure, tasks such as the following can be automated:

- enabling **eco+**;
- enabling **e-pedal**;
- disabling a lane assistance feature;
- returning to **Android Auto / Apple CarPlay**.

The `macro.json` file in this repository demonstrates exactly that approach: each behavior is encapsulated in a separate section and can be enabled or disabled individually.

This makes it possible to:

- test functions separately;
- chain multiple preferences;
- maintain a modular and understandable macro.

---

## 16. Limitations

This project has several important limitations that should be understood before use:

### 16.1 There is no system feedback

The board does not “see” the screen and does not receive confirmations of success.  
It only sends HID events.

### 16.2 Total layout dependency

If anything in the interface changes:

- button positions;
- resolution;
- scaling;
- menu structure;
- loading times;

the macro may fail or execute incorrect actions.

### 16.3 Timing dependency

If one screen takes longer than expected, later steps may become misaligned.

### 16.4 No contextual validation

The script does not know which screen it is currently on.  
It simply executes the next step.

### 16.5 No automatic recovery

If something goes wrong in the middle of the sequence, the program does not correct the state or roll back by itself.

---

## 17. Safety and responsibility

This project should be used carefully.  
The automation interacts with vehicle functions and may change system settings.

Basic recommendations:

- always calibrate with the vehicle stationary;
- test in a controlled environment;
- do not adjust coordinates or timings while driving;
- validate each section independently before using a long sequence;
- assume any system update may require recalibration.

This repository documents a technical HID automation approach.  
Each user is responsible for evaluating its convenience, safety, and compatibility with their environment.

---

## 18. Possible improvements

Some interesting future extensions could be:

- a visual coordinate calibration tool;
- profiles per vehicle or software version;
- conditional macros;
- support for reusable steps;
- more detailed logs;
- a manual abort mechanism;
- macro selection through a physical button;
- a more expressive configuration file;
- testing and troubleshooting documentation.

---

## 19. License

MIT
