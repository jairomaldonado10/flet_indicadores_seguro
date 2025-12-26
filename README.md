# Ecotech Solutions – Indicadores Económicos

Proyecto desarrollado en **Python + Flet + Oracle XE** que permite la **gestión segura de usuarios**, **consulta de indicadores económicos en tiempo real** y **persistencia de consultas** en base de datos Oracle.

Este sistema fue desarrollado como evidencia para la evaluación del ramo **TI3021**, cumpliendo la totalidad de los criterios de la rúbrica.

---

## 🎯 Funcionalidades principales

### 🔐 Registro de usuarios
- Registro mediante interfaz gráfica (Flet)
- Validaciones de campos obligatorios
- Control de usuarios duplicados
- Persistencia real en Oracle
- Contraseñas protegidas con **hash + salt (bcrypt)**

### 🔑 Inicio de sesión
- Login seguro con verificación de credenciales
- Manejo de errores (usuario inexistente / contraseña incorrecta)
- Gestión de sesión lógica

### 🧭 Pantalla principal
- Navegación clara entre módulos
- Visualización del usuario autenticado
- Opción de cierre de sesión

### 📊 Consulta de indicadores económicos
- Selección de indicador (UF, Dólar, Euro, UTM)
- Consumo de API pública **mindicador.cl**
- Visualización inmediata del resultado
- Manejo de excepciones ante errores de consulta

### 💾 Persistencia de consultas
- Registro automático de cada consulta
- Guarda: usuario, indicador, valor, fuente y fecha
- Persistencia en base de datos Oracle

### 🕘 Historial de consultas
- Visualización del historial por usuario
- Datos consistentes con la base de datos
- Ordenados por fecha descendente

---

## 🧱 Arquitectura del proyecto

- **POO (Programación Orientada a Objetos)**
- Separación por capas:
  - `ecotech.py`: lógica de negocio, seguridad, API y base de datos
  - `flet_ecotech.py`: interfaz gráfica y navegación
- Validaciones centralizadas
- Manejo controlado de excepciones

---

## 📁 Estructura del proyecto

```text
flet_indicadores_seguro/
│
├── ecotech.py
├── flet_ecotech.py
├── .env
└── venv/
