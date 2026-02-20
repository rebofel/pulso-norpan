# NORPAN - Sistema Integral de Gestión de RRHH y Liquidación

**Proyecto:** NORPAN RRHH  
**Tech Lead:** Feli  
**Stakeholder:** Carolina (CEO)  
**Fecha inicio análisis:** 2026-02-16  
**Versión documento:** 1.1  

---

## 1. RESUMEN EJECUTIVO

Sistema web para la **gestión integral de empleados, liquidación de haberes, control disciplinario, desempeño, tareas, asistencia y reportes**. Opera en entorno **multiempresa (4 empresas + monotributos)** con control de acceso por roles.

### Fuentes de requisitos consolidadas
- Mail de Carolina (CEO)
- Conversación GPT adjunta (`gpt.json`)
- Planilla Excel de liquidación (`Liquidación Sueldo 11 02 26.xlsb`)

---

## 2. MÓDULOS DEL SISTEMA

| # | Módulo | Descripción |
|---|--------|-------------|
| M1 | Legajo de Empleados | Alta, baja, modificación de datos personales y contractuales |
| M2 | Liquidación de Haberes | Conceptos remunerativos, descuentos, cálculos automáticos |
| M3 | Préstamos y Adelantos | Control de préstamos con cuotas, saldos y descuento automático |
| M4 | Vacaciones | Cálculo de días según antigüedad, liquidación proporcional |
| M5 | Aguinaldo (SAC) | Cálculo automático semestral y proporcional |
| M6 | Liquidación Final | Preaviso, vacaciones y aguinaldo proporcionales, pendientes |
| M7 | Registro Disciplinario | Advertencias, suspensiones, historial |
| M8 | Objetivos y Desempeño | Asignación, seguimiento, ranking por área |
| M9 | Registro de Tareas | Carga diaria, validación por supervisor, productividad |
| M10 | Control de Asistencia | Desvíos de horario, faltas, llegadas tarde, alertas |
| M11 | Gestión de Feriados | Configuración por empleado, compensación |
| M12 | Reportes | Liquidación, costos, ausentismo, horas extras, productividad |
| M13 | Administración | Usuarios, roles, catálogos, empresas, auditoría |
| M14 | Recursos y Accesos | Tracking de herramientas, cuentas digitales, equipos y accesos físicos por empleado |

---

## 3. REGLAS DE NEGOCIO CRÍTICAS (del mail de Carolina)

### 3.1 Aguinaldo (SAC)
- **Fórmula:** Medio sueldo cada 6 meses trabajados
- **Pago:** Con sueldo de junio y diciembre
- **Proporcional:** Si no se completan 6 meses → `(Mejor remuneración del semestre / 2) × (meses trabajados / 6)`
- Debe calcularse automáticamente en cada liquidación de junio y diciembre

### 3.2 Vacaciones
- **Fórmula de liquidación:** `SUELDO / 25 × DÍAS DE VACACIONES`
- **Días trabajados del mes:** `SUELDO / 30 × DÍAS TRABAJADOS`
- **Tabla de días por antigüedad:**

| Antigüedad | Días de vacaciones |
|------------|-------------------|
| Menos de 6 meses | 1 día cada 20 días trabajados |
| 1 a 5 años | 14 días corridos |
| 5 a 10 años | 21 días corridos |
| 11 a 15 años | 28 días corridos |
| Más de 15 años | 35 días corridos |

### 3.3 Liquidación Final (sin causa)
- **Obligatorio:**
  - Completar sueldo del mes (concepto preaviso)
  - Liquidar vacaciones proporcionales no gozadas
  - Liquidar aguinaldo proporcional
  - Liquidar todos los pendientes del empleado (préstamos, adelantos, etc.)
- **Opcional:**
  - Ingresar pago adicional de 1 mes de preaviso (configurable)
- **Indemnización por antigüedad (Art. 245 LCT):**
  - `1 mes de mejor remuneración × años de servicio` (o fracción > 3 meses)
  - Tope: 3 veces el promedio CCT aplicable (configurable)
  - Solo aplica en despido sin causa; registrar tipo de baja (renuncia, sin causa, con causa, jubilación, mutuo acuerdo, fin contrato)
- **Documentación de baja:**
  - Certificado de trabajo (Art. 80 LCT) — obligatorio emitir
  - Certificación de servicios y remuneraciones (ANSES)
  - Checklist de offboarding (recursos, accesos, uniforme) — integra con M14

### 3.4 Préstamos
- Registro del monto total y cantidad de cuotas
- Descuento automático de cuota en cada liquidación
- Visualización de saldo pendiente por empleado y total empresa
- Los adelantos también muestran saldo total pendiente

### 3.5 Asistencia (solo desvíos)
- No se registra asistencia normal
- Solo se registran:
  - **Faltas** (justificadas/injustificadas)
  - **Llegadas tarde**
  - **Retiros más tarde de lo establecido**
  - **Ingresos más tempranos**
- **Cada registro lleva un campo `Observaciones`** (texto libre) — Ej: "Certificado médico presentado", "Aviso por teléfono"
- Las ausencias injustificadas impactan como descuento automático en liquidación (Col 34 del Excel)

### 3.5b Licencias Especiales (LCT + CCT)
- Licencias obligatorias por ley (Art. 158 LCT):

| Licencia | Días | Observación |
|----------|:----:|-------------|
| Matrimonio | 10 | Corridos |
| Nacimiento hijo | 2 | Hábiles |
| Fallecimiento cónyuge/hijo/padre | 3 | Corridos |
| Fallecimiento hermano | 1 | |
| Examen (empleado estudiante) | 2 | Por examen, hasta 10/año |
| Mudanza | 1 | Según CCT |
| Donación de sangre | 1 | Con certificado |
| Enfermedad inculpable | Según antigüedad | 3-12 meses s/ carga familiar |

- **El tipo de licencia se selecciona al cargar la ausencia** justificada
- **Licencia con goce de sueldo:** no descuenta del neto
- **Licencia sin goce de sueldo:** descuenta proporcional
- Posibilidad de adjuntar certificado médico/documentación

### 3.6 Visibilidad de datos
- **Parte "declarada" por empresa:** descargable por todos los usuarios
- **Parte "completa" (real):** solo acceso administrador/dirección

### 3.7 Modelo Salarial ✅ (confirmado por Carolina)
- **Sueldo básico** = unidad de medida sobre lo que se paga en realidad (NO es lo declarado en recibo)
- **Porcentaje** (del acuerdo) = multiplicador individual que define cuánto cobra realmente cada empleado
- **Sueldo real** = `Sueldo básico del mes × Porcentaje del empleado`
- Lo declarado en el recibo de sueldo es independiente de este cálculo
- **3 tipos de composición salarial:**
  - **Básico** (sueldo × porcentaje)
  - **Producción** — se define al ingreso, pero si producción es menor que el básico, se paga el básico (garantía mínima)
  - **Comisión** — cobran SOLO comisión, sin garantía mínima. Posiblemente bajo modalidad monotributo. En el Excel tienen `Sueldo_Básico=False`
- El tipo se define al ingresar al empleado pero puede cambiar

### 3.8 Pagos Parciales ✅ (confirmado por Carolina)
- El sistema **DEBE registrar cada pago individual**: monto + fecha + medio de pago (efectivo, transferencia, MercadoPago, etc.)
- **Cada pago lleva un campo `Observaciones`** (texto libre) — en el Excel Carolina usa hasta 4 campos de observaciones por período, uno por pago
- Hasta 4+ pagos por período
- Objetivo: poder detallarle al empleado cómo se le fue pagando ante cualquier consulta

### 3.9 Empresas / Empleadores ✅ (confirmado por Carolina)
- **4 empresas iniciales:**
  1. NOR-PAN SA
  2. Isabel Martinelli
  3. Doña Carolina SAS
  4. Carolina Zicovich
- **Monotributos:** empleados que deben facturar como monotributista (antes figuraban como "SIN EMPLEADOR")
- Todos deben estar registrados en alguno de estos formatos
- **El sistema debe permitir dar de alta nuevas empresas dinámicamente** (ABM de empresas, no hardcodeado)
- PPP = programa gobierno, ver §3.11

### 3.10 Proceso Actual de Liquidación ✅ (confirmado por Carolina)
- **Estudio laboral externo:** se encarga de lo fiscal y legal
- **Guardia (acceso oficinas):** controla los horarios de ingreso/egreso
- **Carolina (Excel):** lleva TODO el detalle real de sueldos. Es la única fuente de verdad
- **ERP "Rojo":** registra anticipos a nombre de cada empleado, pero el pago final es un solo movimiento a la cuenta madre "Sueldos" (sin desglose)
- **Conclusión:** el sistema reemplaza principalmente el Excel de Carolina. No se requiere integración con ERP Rojo por ahora

### 3.11 Empleados PPP (Programa Primer Paso - Gobierno de Córdoba)
- La empresa paga un porcentaje del sueldo y el Gobierno de Córdoba aporta el resto
- En el Excel, los PPP tienen `Porcentaje=0.2` (20% del básico)
- **La proporción puede cambiar** según políticas del programa
- **Diseño:** dejar configurable:
  - `porcentaje_empresa` (ej: 0.2) — lo que paga NORPAN
  - `porcentaje_gobierno` (ej: 0.8) — lo que cubre el programa
  - Estos valores deben poder editarse por empleado PPP o globalmente
- El sistema debe calcular y mostrar ambas partes por separado

---

## 4. DATOS DEL EMPLEADO (LEGAJO)

### 4.1 Datos Personales

| Campo | Tipo | Obligatorio | Único | Visibilidad | Observaciones |
|-------|------|:-----------:|:-----:|-------------|---------------|
| Nro Legajo | Numérico | ✓ | ✓ | Todos | Autogenerado o manual |
| Nombre y Apellido | Texto | ✓ | | Todos | |
| DNI | Numérico | ✓ | ✓ | Todos | |
| CUIL | Numérico | ✓ | ✓ | Todos | Validar formato |
| Fecha Nacimiento | Fecha | ✓ | | RRHH+ | |
| Domicilio | Texto | ✓ | | RRHH+ | |
| Teléfono | Texto | ✓ | | Todos | |
| Email | Email | ✓ | | Todos | Validar formato |
| Estado Civil | Select | | | RRHH+ | |
| Hijos (cantidad) | Numérico | | | RRHH+ | |
| Fecha Ingreso | Fecha | ✓ | | Todos | Base para antigüedad |
| Empresa (CUIT) | Select | ✓ | | Todos | Catálogo multiempresa |
| Unidad de Negocio | Select | ✓ | | Todos | |
| Área | Select | ✓ | | Todos | |
| Puesto | Select | ✓ | | Todos | |
| Supervisor | Select | ✓ | | Todos | |
| Banco | Texto | | | Dirección/RRHH | Dato sensible |
| Nro Cuenta | Texto | | | Dirección/RRHH | Dato sensible |
| CBU | Numérico | | | Dirección/RRHH | Dato sensible |
| Alias | Texto | | | Dirección/RRHH | |
| Fecha Baja | Fecha | | | RRHH+ | Pasa a estado Inactivo |
| Motivo baja | Select | | | RRHH+ | Renuncia/Sin causa/Con causa/Jubilación/Mutuo acuerdo/Fin contrato |
| Foto DNI | Booleano/Archivo | | | RRHH+ | Del Excel: campo 'FOTO DNI' |
| Condición | Select | | | RRHH+ | FIJO/MÓVIL (del Excel) |
| Código sistema | Texto | | | RRHH+ | 'CODIGO SIST' del Excel |
| Observaciones generales | Texto largo | | | RRHH+ | Notas libres sobre el empleado |

### 4.2 Datos Contractuales

| Campo | Tipo | Obligatorio |
|-------|------|:-----------:|
| Tipo contratación | Select (TC/Parcial/Eventual) | ✓ |
| Categoría convenio | Texto | ✓ |
| Jornada laboral (hs/día) | Numérico | ✓ |
| Días de trabajo | Multiselect (L-D) | ✓ |
| Horario ingreso | Hora | ✓ |
| Horario egreso | Hora | ✓ |
| Modalidad | Select (Presencial/Mixto/Remoto) | ✓ |
| Sueldo básico | Numérico | ✓ |
| Adicionales fijos | Numérico | |
| Seguro contratado | Texto | |
| Obra social | Select | ✓ |
| ART | Select | | Aseguradora de Riesgos del Trabajo |
| Número afiliado ART | Texto | |
| Sindicato | Select | | Si adhiere a algún gremio |
| Categoría sindical | Texto | | Del CCT aplicable |

> **Historial:** Todo cambio contractual debe registrarse con vigencia (fecha desde/hasta) para auditoría y liquidaciones retroactivas.

---

## 5. LIQUIDACIÓN DE HABERES

### 5.1 Conceptos Remunerativos (por período)

| Concepto | Tipo | Auto/Manual |
|----------|------|-------------|
| Sueldo acordado | Numérico | Manual |
| Horas acordadas | Numérico | Manual |
| Horas extras normales | Numérico | Manual (cálculo asistido) |
| Horas extras 50% | Numérico | Manual (cálculo asistido) |
| Observaciones horas extras | Texto | Manual |
| Feriados trabajados | Numérico | Manual / Automático |
| Comisiones | Numérico | Manual |
| Premios por objetivos | Numérico | Manual / desde M8 |
| Bonificaciones | Numérico | Manual |
| Vacaciones | Numérico | **Automático** (S/25 × días) |
| Observaciones vacaciones | Texto | Manual |
| Aguinaldo | Numérico | **Automático** (jun/dic) |

### 5.2 Descuentos (por período)

| Concepto | Tipo | Auto/Manual |
|----------|------|-------------|
| Embargos | Numérico | Manual |
| Adelantos | Numérico | **Automático** (desde M3) |
| Ausencias injustificadas | Numérico | **Automático** (desde M10) |
| Suspensiones | Numérico | Manual |
| Préstamos (cuota) | Numérico | **Automático** (desde M3) |
| Venta de mercadería | Numérico | Manual |
| Faltante de mercadería | Numérico | Manual |
| Otros configurables | Numérico | Manual |

### 5.2b Descuentos Legales (solo aplican sobre sueldo DECLARADO)

| Concepto | Porcentaje | Aplicación |
|----------|:----------:|------------|
| Jubilación (SIPA) | 11% | Automático |
| Obra social | 3% | Automático |
| Ley 19.032 (PAMI) | 3% | Automático |
| Sindicato | 2% | Automático (si aplica) |

> Estos descuentos se muestran en el **recibo declarado**. El estudio laboral los deposita fiscalmente. Los porcentajes son configurables en caso de cambio normativo.

### 5.4 Recibos de Sueldo (PDF)

El sistema genera **dos versiones** de recibo por empleado por período:

| Versión | Contenido | Acceso | Formato |
|---------|-----------|--------|---------|
| **Declarado** | Sueldo registrado + descuentos legales desglosados + neto declarado | Todos los roles | PDF |
| **Real/Completo** | Básico×%, producción, comisión, pagos parciales con observaciones, descuentos internos, neto real | Solo Dirección | PDF |

- Generación individual o masiva (todos los empleados de un período)
- Descarga individual o ZIP con todos los recibos del período
- Historial de recibos generados por empleado
- Template configurable (logo empresa, datos CUIT, firma)

### 5.3 Cálculos Automáticos

| Cálculo | Fórmula |
|---------|---------|
| Valor hora | `Sueldo acordado / Horas acordadas del período` |
| HE normales | `Valor hora × cantidad horas extras` |
| HE 50% | `Valor hora × 1.5 × cantidad horas extras` |
| HE 100% | `Valor hora × 2 × cantidad horas extras` |
| Prorrateo sueldo | `(Sueldo / 30) × días trabajados` |
| Vacaciones | `(Sueldo / 25) × días de vacaciones` |
| Días trabajados del mes (con vac.) | `(Sueldo / 30) × días trabajados` |
| Aguinaldo | `(Mejor rem. semestre / 2) × (meses / 6)` |
| Neto a cobrar | `Σ Remunerativos - Σ Descuentos` |
| Costo total empresa | `Σ Remunerativos (+ cargas futuras)` |

---

## 6. NIVELES DE ACCESO (RBAC)

| Permiso / Módulo | Dirección | RRHH | Supervisor | Administrativo |
|-------------------|:---------:|:----:|:----------:|:--------------:|
| Legajo (ver todo) | ✓ | ✓ | Parcial | Parcial |
| Legajo (editar) | ✓ | ✓ | ✗ | ✗ |
| Datos bancarios | ✓ | ✓ | ✗ | ✗ |
| Liquidación completa | ✓ | ✓ | ✗ | ✗ |
| Liquidación declarada | ✓ | ✓ | ✓ | ✓ |
| Préstamos/Adelantos | ✓ | ✓ | ✗ | Carga |
| Disciplina | ✓ | ✓ | Carga | ✗ |
| Objetivos | ✓ | ✓ | ✓ (equipo) | ✗ |
| Tareas | ✓ | ✓ | ✓ (equipo) | ✗ |
| Asistencia | ✓ | ✓ | ✓ (equipo) | Carga |
| Feriados | ✓ | ✓ | ✗ | ✗ |
| Reportes | ✓ | ✓ | Equipo | ✗ |
| Admin sistema | ✓ | ✗ | ✗ | ✗ |
| Recursos y Accesos | ✓ | ✓ | Lectura (equipo) | ✗ |
| Exportar declarada | ✓ | ✓ | ✓ | ✓ |
| Exportar completa | ✓ | ✗ | ✗ | ✗ |

> **Dato clave de Carolina:** "Que la parte declarada de cada empresa, se pueda descargar por todos los usuarios. Que la parte completa solo tenga acceso el administrador."

---

## 7. REPORTES

| Reporte | Exportable | Roles |
|---------|:----------:|-------|
| Liquidación mensual por empresa (CUIT) | Excel/PDF | Dirección, RRHH |
| Detalle individual por empleado | Excel/PDF | Dirección, RRHH |
| Costo laboral por Unidad de Negocio | Excel | Dirección, RRHH |
| Ranking cumplimiento de objetivos | Excel | Dirección, RRHH, Supervisor |
| Reporte disciplinario por período | Excel | Dirección, RRHH |
| Ausentismo por área | Excel | Dirección, RRHH |
| Horas extras por empleado | Excel | Dirección, RRHH |
| Productividad por empleado | Excel | Dirección, RRHH, Supervisor |
| Saldos pendientes préstamos/adelantos | Excel | Dirección, RRHH |
| Exportación contable por UN | CSV/Excel | Dirección, RRHH |

---

## 8. AUDITORÍA

- **Registrar en:** Legajo, Liquidación, Disciplina, Objetivos, Asistencia, Préstamos
- **Campos:** Usuario, Fecha/Hora, Acción (Alta/Edición/Baja), Valor anterior, Valor nuevo
- **Historial no editable**

---

## 9. REQUISITOS TÉCNICOS

| Requisito | Detalle |
|-----------|---------|
| Tipo | Aplicación web |
| Base de datos | Centralizada, relacional |
| Multiempresa | 4 empresas + monotributos (confirmado por Carolina) |
| Autenticación | Login con roles |
| Auditoría | Por tabla/campo crítico |
| Exportaciones | Excel (obligatorio), PDF (deseable), CSV |
| Backup | Automático diario |
| Historial contractual | Vigencias con fecha desde/hasta |

---

## 10. MÓDULO RECURSOS Y ACCESOS (M14)

> Módulo independiente que no afecta la liquidación de sueldos. Permite gestionar el inventario de herramientas, cuentas digitales, equipos físicos y accesos asignados a cada empleado.

### 10.1 Categorías de Recursos

| Categoría | Ejemplos |
|-----------|----------|
| Cuentas digitales | Email corporativo, Slack, Google Workspace |
| Apps / Sistemas | Acceso al sistema RRHH, ERP, facturación |
| Equipamiento físico | Notebook, celular, herramientas, uniforme |
| Llaves / Accesos físicos | Llave oficina, tarjeta acceso, alarma |
| Vehículos | Vehículo empresa, tag peaje |

### 10.2 Datos por Recurso Asignado

| Campo | Tipo | Obligatorio | Observaciones |
|-------|------|:-----------:|---------------|
| Empleado | FK | ✓ | Referencia al legajo |
| Nombre del recurso | Texto | ✓ | Ej: "Notebook Lenovo", "Email trabajo" |
| Categoría | Select | ✓ | De las categorías definidas arriba |
| Estado | Select | ✓ | Activo / Inactivo / Pendiente |
| Fecha asignación | Fecha | ✓ | |
| Fecha revocación | Fecha | | Se completa al dar de baja |
| Asignado por | FK usuario | ✓ | Quién asignó el recurso |
| Número de serie | Texto | | Para equipos con identificador |
| Notas | Texto largo | | Observaciones adicionales |

### 10.3 Funcionalidades Clave

- **Vista por empleado:** Listado de todos los recursos asignados con estado visual (badge verde/rojo/amarillo)
- **Onboarding checklist:** Al dar de alta un empleado, generar checklist de recursos a provisionar
- **Offboarding checklist:** Al dar de baja, generar checklist de recursos a revocar/devolver
- **Vista global:** Reporte de todos los recursos activos, filtrable por categoría, empleado, unidad de negocio
- **Historial:** Log de cambios (asignación, revocación, cambio de estado)
- **Exportación:** Excel con inventario completo

---

## 11. PUNTOS A CONFIRMAR CON CAROLINA

> Estos puntos surgieron del análisis cruzado entre el mail y la conversación GPT. Requieren definición antes de implementar.

### ✅ RESUELTOS (respuestas de Carolina + decisiones de diseño - 16/02/2026)

1. ~~**Sueldo básico × Porcentaje:**~~ Confirmado. Básico es unidad de medida, Porcentaje define pago real. No tiene relación con lo declarado. → Ver §3.7
2. ~~**Empleadores:**~~ Son 4 empresas + monotributos. "SIN EMPLEADOR" = monotributo. Sistema permite crear nuevas empresas dinámicamente. → Ver §3.9
3. ~~**Composición salarial:**~~ 3 tipos. Producción tiene garantía mínima (básico×%). Comisión NO tiene garantía (cobran solo comisión, posible monotributo). → Ver §3.7
4. ~~**Pagos parciales:**~~ Sí, registrar cada movimiento (monto + fecha + medio). → Ver §3.8
5. ~~**Proceso actual:**~~ Excel de Carolina = fuente de verdad. Estudio laboral externo hace lo fiscal. ERP Rojo solo anticipos. → Ver §3.10
6. ~~**PPP:**~~ Empresa paga un porcentaje, Gobierno de Córdoba aporta el resto. Dejar configurable. → Ver §3.11
7. ~~**Descuentos legales:**~~ Se aplican sobre el sueldo DECLARADO (jubilación 11%, OS 3%, Ley 19032 3%, sindicato 2%). Los calcula el sistema y se muestran en el recibo declarado. El estudio laboral los deposita fiscalmente. → Ver §5.2b
8. ~~**Recibos de sueldo:**~~ Sí, generar PDF. Dos versiones: declarado (con descuentos legales, accesible por todos) y real/completo (solo Dirección). → Ver §5.4

### Pendientes — Definir antes de Sprint 4

9. **Formato de exportación contable:**  
   ¿El estudio contable/laboral necesita un formato específico? Pedir ejemplo a Carolina. No bloquea el desarrollo del motor de liquidación, se puede agregar el export después.

### Pendientes — Pueden esperar (post-MVP)

10. **Notificaciones:**  
    ¿Notificar por email/in-app sanciones, vacaciones, vencimiento cuotas?

11. **Convenio colectivo:**  
    ¿Se aplica un CCT específico? ¿Hay escalas salariales obligatorias? Esto afecta categorías, tope indemnización y licencias adicionales.

12. **Acceso empleado:**  
    ¿Portal para que cada empleado vea sus recibos?

13. **Cambio de obra social:**  
    ¿Solo registro o impacta liquidación?

14. **AFIP / Libro de sueldos digital:**  
    ¿El estudio laboral maneja todo lo de AFIP (F931, altas/bajas, libro sueldos digital) o necesitan exportar algo desde el sistema? (Probablemente sí según §3.10)

15. **Familiares a cargo:**  
    ¿Registrar grupo familiar (para SUAF/asignaciones familiares) o ANSES lo gestiona directo?

16. **ART:**  
    ¿Qué aseguradora usan? ¿Registrar accidentes en el sistema o lo gestiona la ART directamente?

---

*Documento generado el 2026-02-16, actualizado el 2026-02-16 con respuestas de Carolina, hallazgos del Excel, módulo M14, observaciones, licencias LCT, indemnización y análisis de gaps para RRHH argentino.*
