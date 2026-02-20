# PULSO — Historias de Usuario

**Proyecto:** Pulso | Sistema de Gestión de Personas  
**Versión:** 1.0  
**Fecha:** 2026-02-16  
**Fuente:** PROJECT.md v1.1, respuestas de Carolina, análisis del Excel  

> **Formato:** Cada historia tiene ID, rol, necesidad, beneficio, criterios de aceptación (CA) y sprint asignado.  
> **Roles del sistema:** Dirección (D), RRHH (R), Supervisor (S), Administrativo (A)

---

## SPRINT 1 — Setup + Auth

### US-1.1: Login al sistema
**Como** usuario del sistema  
**Quiero** ingresar con email y contraseña  
**Para** acceder a las funcionalidades según mi rol  

**CA:**
- [ ] Pantalla de login con campos email + contraseña
- [ ] Validación: email formato válido, contraseña mínimo 8 caracteres
- [ ] JWT access token (15min) + refresh token (7d en httpOnly cookie)
- [ ] Mensaje de error genérico en credenciales inválidas ("Email o contraseña incorrectos")
- [ ] Después de 5 intentos fallidos, bloquear cuenta 15 minutos
- [ ] Al loguearse exitosamente, redirigir al dashboard según rol
- [ ] bcrypt con salt rounds ≥ 12

### US-1.2: Logout
**Como** usuario logueado  
**Quiero** cerrar mi sesión  
**Para** proteger mi cuenta cuando dejo la computadora  

**CA:**
- [ ] Botón de logout visible en el header/sidebar
- [ ] Al hacer logout, invalidar refresh token en el servidor
- [ ] Redirigir a pantalla de login
- [ ] Limpiar datos del estado del cliente

### US-1.3: Refresh de sesión
**Como** usuario logueado  
**Quiero** que mi sesión se renueve automáticamente  
**Para** no tener que logearme cada 15 minutos  

**CA:**
- [ ] Cuando el access token expira, usar el refresh token para obtener uno nuevo automáticamente
- [ ] Si el refresh token expiró (7 días), redirigir a login
- [ ] El usuario no debe percibir el refresh (transparente)

### US-1.4: Protección de rutas por rol
**Como** administrador del sistema  
**Quiero** que cada rol tenga acceso solo a las pantallas que le corresponden  
**Para** proteger la información sensible  

**CA:**
- [ ] Middleware RBAC que valida rol + permiso en cada endpoint
- [ ] Roles: Dirección, RRHH, Supervisor, Administrativo
- [ ] Si un usuario intenta acceder a una ruta sin permiso: HTTP 403
- [ ] En el frontend, ocultar menús/opciones que no corresponden al rol
- [ ] La validación es server-side (no solo UI)
- [ ] Ver matriz de permisos en PROJECT.md §6

---

## SPRINT 2 — Catálogos + Empresas

### US-2.1: ABM de Empresas
**Como** usuario con rol Dirección  
**Quiero** dar de alta, editar y desactivar empresas  
**Para** gestionar las entidades empleadoras de forma dinámica  

**CA:**
- [ ] CRUD completo de empresas (crear, listar, editar, desactivar — NO eliminar)
- [ ] Campos: CUIT (único, formato XX-XXXXXXXX-X), razón social, tipo (SA/SAS/Persona Física/Monotributo), estado (activo/inactivo)
- [ ] Seed inicial con 4 empresas: NOR-PAN SA, Isabel Martinelli, Doña Carolina SAS, Carolina Zicovich
- [ ] No se puede eliminar una empresa que tenga empleados asignados
- [ ] Solo Dirección puede crear/editar empresas

### US-2.2: ABM de Unidades de Negocio
**Como** usuario con rol Dirección o RRHH  
**Quiero** gestionar las unidades de negocio por empresa  
**Para** organizar a los empleados por área operativa  

**CA:**
- [ ] CRUD: crear, editar, desactivar UNs
- [ ] Cada UN pertenece a una empresa (FK)
- [ ] Al seleccionar empresa, filtra las UNs de esa empresa
- [ ] No se puede desactivar una UN con empleados activos

### US-2.3: ABM de Áreas
**Como** usuario con rol Dirección o RRHH  
**Quiero** gestionar las áreas dentro de cada unidad de negocio  
**Para** agrupar empleados por sector  

**CA:**
- [ ] CRUD áreas con relación cascada: empresa → UN → área
- [ ] Selects dinámicos encadenados en el formulario

### US-2.4: ABM de Puestos
**Como** usuario con rol Dirección o RRHH  
**Quiero** mantener un catálogo de puestos  
**Para** asignar puestos a los empleados  

**CA:**
- [ ] CRUD de puestos: nombre, descripción, estado
- [ ] Catálogo global (no depende de empresa/UN)

### US-2.5: Gestión de Usuarios
**Como** usuario con rol Dirección  
**Quiero** crear usuarios y asignarles un rol  
**Para** controlar quién accede al sistema y qué puede hacer  

**CA:**
- [ ] CRUD usuarios: nombre, email, contraseña temporal, rol, estado
- [ ] Al crear usuario, enviar email con contraseña temporal (o permitir que Dirección la defina)
- [ ] Un usuario tiene un rol (no múltiples)
- [ ] Forzar cambio de contraseña en primer login
- [ ] Solo Dirección puede crear/editar usuarios
- [ ] No se puede eliminar, solo desactivar

### US-2.6: Auditoría de cambios
**Como** usuario con rol Dirección  
**Quiero** ver un registro de todos los cambios realizados en el sistema  
**Para** tener trazabilidad y detectar modificaciones indebidas  

**CA:**
- [ ] Cada operación de alta/edición/baja en entidades críticas genera un registro en audit_logs
- [ ] Campos: usuario, entidad, campo modificado, valor anterior, valor nuevo, timestamp
- [ ] Log inmutable (no se puede editar ni eliminar)
- [ ] Aplica a: empleados, contratos, liquidaciones, préstamos, asistencia, disciplina
- [ ] Vista de auditoría con filtros: entidad, usuario, rango de fechas

---

## SPRINT 3 — Legajo de Empleados

### US-3.1: Alta de empleado
**Como** usuario con rol RRHH  
**Quiero** dar de alta un nuevo empleado con todos sus datos  
**Para** registrar su ingreso a la empresa  

**CA:**
- [ ] Formulario con tabs/pasos: Datos Personales → Datos Contractuales → Datos Bancarios
- [ ] **Datos personales:** nombre y apellido, DNI (único), CUIL (único, formato validado), fecha nacimiento, domicilio, teléfono, email, estado civil, hijos, fecha ingreso, empresa (select dinámico), UN, área, puesto, supervisor, condición (FIJO/MÓVIL), foto DNI (sí/no o archivo), código sistema, observaciones generales
- [ ] **Datos contractuales:** tipo contratación (TC/Parcial/Eventual), categoría convenio, jornada (hs/día), días de trabajo (multiselect L-D), horario ingreso/egreso, modalidad (Presencial/Mixto/Remoto), sueldo básico, adicionales fijos, seguro contratado, obra social, ART, nro afiliado ART, sindicato, categoría sindical
- [ ] **Datos bancarios:** banco, nro cuenta, CBU, alias — tabla separada, visible solo por Dirección/RRHH
- [ ] Al guardar, asignar nro de legajo (autogenerado o manual)
- [ ] Estado inicial: Activo
- [ ] Registrar en auditoría

### US-3.2: Edición de empleado
**Como** usuario con rol RRHH  
**Quiero** editar los datos de un empleado existente  
**Para** mantener la información actualizada  

**CA:**
- [ ] Permitir editar todos los campos del legajo
- [ ] Cambios contractuales crean un nuevo registro con vigencia (fecha_desde/fecha_hasta) — no sobrescriben
- [ ] Registrar cada cambio en auditoría (campo, valor anterior, valor nuevo)
- [ ] No se puede cambiar el DNI una vez creado (solo Dirección con override)

### US-3.3: Listado y búsqueda de empleados
**Como** usuario del sistema  
**Quiero** ver un listado de empleados con filtros  
**Para** encontrar rápidamente al empleado que busco  

**CA:**
- [ ] Tabla paginada con columnas: legajo, nombre, empresa, UN, área, puesto, estado
- [ ] Filtros: empresa, UN, área, estado (activo/inactivo), condición (fijo/móvil)
- [ ] Búsqueda por texto: nombre, DNI, CUIL
- [ ] Búsqueda parcial (ej: escribir "Agu" encuentra "Aguirre")
- [ ] Click en fila → abre ficha/detalle del empleado
- [ ] Supervisor solo ve empleados de su equipo
- [ ] Administrativo ve datos limitados (sin bancarios)

### US-3.4: Ficha de empleado
**Como** usuario con rol RRHH  
**Quiero** ver la ficha completa de un empleado  
**Para** consultar toda su información en un solo lugar  

**CA:**
- [ ] Vista con secciones: datos personales, datos contractuales (actual + historial), datos bancarios (si tiene permiso)
- [ ] Historial contractual: tabla con todos los contratos/acuerdos con vigencias
- [ ] Mostrar antigüedad calculada automáticamente
- [ ] Mostrar días de vacaciones según antigüedad (tabla LCT)
- [ ] Estado visual: badge Activo (verde) / Inactivo (rojo)
- [ ] Botón "Editar" solo visible para roles autorizados

### US-3.5: Baja de empleado
**Como** usuario con rol RRHH  
**Quiero** registrar la baja de un empleado  
**Para** documentar su salida y disparar la liquidación final  

**CA:**
- [ ] Al dar de baja, pedir: fecha de baja + tipo de baja (Renuncia / Despido sin causa / Despido con causa / Jubilación / Mutuo acuerdo / Fin de contrato)
- [ ] Cambiar estado del empleado a Inactivo
- [ ] Crear registro en tabla terminations (tipo, fecha, usuario que procesó)
- [ ] No elimina el empleado — queda visible con filtro de inactivos
- [ ] Registrar en auditoría
- [ ] (Sprint 5) Disparar liquidación final si es despido sin causa

### US-3.6: Visibilidad de datos sensibles
**Como** administrador del sistema  
**Quiero** que los datos bancarios solo sean visibles por roles autorizados  
**Para** proteger información financiera de los empleados  

**CA:**
- [ ] Datos bancarios en tabla separada (employee_bank_info)
- [ ] Solo Dirección y RRHH pueden ver/editar
- [ ] El endpoint devuelve 403 si el rol no tiene permiso
- [ ] En el frontend, la tab de datos bancarios no se muestra si no tiene permiso

---

## SPRINT 4 — Motor de Liquidación

### US-4.1: Crear período de liquidación
**Como** usuario con rol RRHH  
**Quiero** crear un nuevo período de liquidación para una empresa  
**Para** iniciar el proceso mensual de cálculo de sueldos  

**CA:**
- [ ] Seleccionar empresa + mes + año
- [ ] No permitir duplicados (una empresa solo puede tener un período por mes)
- [ ] Estado inicial: Borrador
- [ ] Estados posibles: Borrador → Cerrado
- [ ] Una vez cerrado, no se puede editar (solo Dirección puede reabrir)
- [ ] Al crear, cargar automáticamente todos los empleados activos de esa empresa

### US-4.2: Calcular sueldo real (básico × porcentaje)
**Como** RRHH  
**Quiero** que el sistema calcule el sueldo real de cada empleado  
**Para** aplicar el modelo salarial de NORPAN correctamente  

**CA:**
- [ ] Fórmula: `sueldo_real = básico_del_mes × porcentaje_del_acuerdo`
- [ ] 3 tipos de composición salarial:
  - **Básico:** sueldo × porcentaje directo
  - **Producción:** calcular producción real; si es menor que básico×%, pagar básico×% (garantía mínima)
  - **Comisión:** solo cobran comisión, SIN garantía mínima
- [ ] El tipo de composición viene del contrato vigente del empleado
- [ ] Mostrar ambos valores por separado (declarado vs real)
- [ ] El sueldo declarado en el recibo es independiente del cálculo real

### US-4.3: Cargar conceptos remunerativos
**Como** RRHH  
**Quiero** cargar los conceptos remunerativos de cada empleado por período  
**Para** calcular el neto a cobrar  

**CA:**
- [ ] Conceptos disponibles: sueldo acordado, hs acordadas, hs extras (normales/50%/100%), feriados trabajados, comisiones, premios por objetivos, bonificaciones
- [ ] Cada concepto tiene: monto, auto/manual, observaciones
- [ ] Cálculos automáticos:
  - Valor hora = sueldo / hs del período
  - HE normales = valor_hora × cantidad_hs
  - HE 50% = valor_hora × 1.5 × cantidad_hs
  - HE 100% = valor_hora × 2 × cantidad_hs
  - Prorrateo = (sueldo/30) × días trabajados
- [ ] Subtotal remunerativo = Σ todos los conceptos

### US-4.4: Cargar descuentos
**Como** RRHH  
**Quiero** registrar los descuentos de cada empleado  
**Para** calcular el neto correcto  

**CA:**
- [ ] Descuentos internos (sobre sueldo real): embargos, adelantos, suspensiones, venta mercadería, faltante mercadería, otros configurables
- [ ] Descuentos legales (sobre sueldo DECLARADO): jubilación 11%, OS 3%, Ley 19032 3%, sindicato 2%
- [ ] Descuentos legales se calculan automáticamente al ingresar el sueldo declarado
- [ ] Porcentajes legales configurables en payroll_config (por si cambian)
- [ ] Neto real = Σ remunerativos - Σ descuentos internos
- [ ] Neto declarado = sueldo declarado - descuentos legales
- [ ] Los préstamos y ausencias se descuentan automáticamente (integración en sprints posteriores)

### US-4.5: Conceptos configurables
**Como** RRHH  
**Quiero** poder agregar nuevos conceptos de liquidación sin tocar código  
**Para** adaptarme a cambios normativos o de negocio  

**CA:**
- [ ] ABM de conceptos: nombre, tipo (remunerativo/descuento/legal), fórmula o porcentaje fijo, activo/inactivo
- [ ] Los nuevos conceptos aparecen automáticamente en la pantalla de liquidación
- [ ] No se pueden eliminar conceptos que ya se usaron en liquidaciones cerradas

### US-4.6: Vista de liquidación por período
**Como** RRHH  
**Quiero** ver un resumen de la liquidación de todos los empleados de un período  
**Para** revisar y aprobar antes de cerrar  

**CA:**
- [ ] Grilla con todos los empleados del período: nombre, sueldo real, subtotal remunerativo, descuentos, neto real, neto declarado
- [ ] Click en fila → detalle del empleado con todos los conceptos
- [ ] Totales al pie: total neto real, total neto declarado, costo total empresa
- [ ] Filtrable por tipo composición (básico/producción/comisión)
- [ ] Vista "declarada" vs "completa" según rol del usuario

---

## SPRINT 5 — Vacaciones + SAC + Liquidación Final

### US-5.1: Cálculo automático de días de vacaciones
**Como** RRHH  
**Quiero** que el sistema calcule los días de vacaciones de cada empleado automáticamente  
**Para** no tener que calcular manualmente la antigüedad  

**CA:**
- [ ] Cálculo basado en antigüedad desde fecha_ingreso (Art. 150 LCT):
  - <6 meses: 1 día cada 20 trabajados
  - 1-5 años: 14 días corridos
  - 5-10 años: 21 días corridos
  - 11-15 años: 28 días corridos
  - >15 años: 35 días corridos
- [ ] Tabla vacation_balances por empleado: días correspondientes, días tomados, saldo
- [ ] Actualización automática al cambiar de año

### US-5.2: Liquidación de vacaciones
**Como** RRHH  
**Quiero** liquidar las vacaciones de un empleado  
**Para** pagarle lo que corresponde cuando toma vacaciones  

**CA:**
- [ ] Fórmula: `(sueldo / 25) × días_de_vacaciones`
- [ ] Días trabajados del mes con vacaciones: `(sueldo / 30) × días_trabajados`
- [ ] Campo de observaciones por registro de vacaciones
- [ ] Descontar días del saldo de vacation_balances
- [ ] Integración con liquidación del período como concepto remunerativo

### US-5.3: Cálculo de aguinaldo (SAC)
**Como** RRHH  
**Quiero** que el sistema calcule el aguinaldo automáticamente en junio y diciembre  
**Para** cumplir con la ley sin errores de cálculo  

**CA:**
- [ ] Fórmula: `(mejor_remuneración_semestre / 2) × (meses_trabajados / 6)`
- [ ] Se calcula en períodos de junio y diciembre
- [ ] Proporcional si no completó 6 meses
- [ ] Pre-aguinaldo como concepto separado si aplica
- [ ] Tabla aguinaldo_calculations para registro

### US-5.4: Liquidación final por despido sin causa
**Como** RRHH  
**Quiero** generar la liquidación final de un empleado desvinculado  
**Para** calcular todo lo que se le debe legalmente  

**CA:**
- [ ] Solo se dispara para tipo de baja "Sin causa"
- [ ] Calcular automáticamente:
  - Sueldo proporcional del mes (preaviso)
  - Vacaciones proporcionales no gozadas
  - SAC proporcional
  - Indemnización Art. 245: `1 mes mejor remuneración × años de servicio` (fracción > 3 meses = 1 año)
  - Tope indemnización: 3× promedio CCT (configurable)
- [ ] Descontar pendientes: saldo préstamos, adelantos
- [ ] Concepto opcional: 1 mes adicional de preaviso (configurable)
- [ ] Registrar toda la liquidación final como un período especial
- [ ] Generar checklist de documentación: Certificado trabajo Art. 80 + Certificación servicios ANSES

### US-5.5: Empleados PPP (Programa Primer Paso)
**Como** RRHH  
**Quiero** configurar la proporción empresa/gobierno para empleados PPP  
**Para** calcular correctamente cuánto paga NORPAN y cuánto cubre el programa  

**CA:**
- [ ] Campos por empleado PPP: porcentaje_empresa (ej: 0.2), porcentaje_gobierno (ej: 0.8)
- [ ] Configurable globalmente (valor por defecto) y por empleado (override)
- [ ] En la liquidación, mostrar por separado: "Paga empresa: $X" / "Cubre gobierno: $Y"
- [ ] Los porcentajes deben poder editarse si cambian las reglas del programa

---

## SPRINT 6 — Pagos Parciales + Recibos PDF

### US-6.1: Registrar pagos parciales
**Como** RRHH  
**Quiero** registrar cada pago individual que se le hace a un empleado  
**Para** tener trazabilidad de cómo se le fue pagando y responder consultas  

**CA:**
- [ ] Por cada empleado y período, registrar múltiples pagos (hasta 4+)
- [ ] Campos por pago: monto, fecha de pago, medio (efectivo/transferencia/MercadoPago/depósito/otro), observaciones (texto libre)
- [ ] Saldo pendiente = neto_a_pagar - Σ pagos_realizados
- [ ] Saldo pendiente visible en la pantalla de liquidación
- [ ] Alerta visual si hay saldo pendiente al querer cerrar un período
- [ ] Ejemplo de observación: "Transferencia a cuenta Macro", "Efectivo en mano", "Pago a cuenta faltante agosto"

### US-6.2: Recibo de sueldo DECLARADO (PDF)
**Como** RRHH  
**Quiero** generar un recibo de sueldo con los montos declarados  
**Para** entregar al empleado el comprobante legal  

**CA:**
- [ ] PDF con:
  - Header: logo empresa + CUIT + razón social + período
  - Datos empleado: nombre, CUIL, legajo, puesto, categoría, fecha ingreso, obra social
  - Haberes: sueldo declarado + adicionales declarados
  - Descuentos legales desglosados: jubilación (11%), obra social (3%), PAMI (3%), sindicato (2%)
  - Neto declarado
  - Espacio para firma empleado + firma empleador
- [ ] Accesible por todos los roles
- [ ] Template configurable (logo, colores, estructura)
- [ ] Nombre archivo: APELLIDO_NOMBRE_MES_AÑO_declarado.pdf

### US-6.3: Recibo de sueldo REAL/COMPLETO (PDF)
**Como** usuario con rol Dirección  
**Quiero** generar un recibo con los montos reales  
**Para** tener un detalle interno de lo que efectivamente se paga  

**CA:**
- [ ] PDF con:
  - Básico del mes × porcentaje = sueldo real
  - Producción / Comisión si aplica
  - Horas extras desglosadas (normales/50%/100%)
  - Vacaciones, SAC
  - Descuentos internos (préstamos, adelantos, faltante, mercadería)
  - Detalle de pagos parciales: fecha + monto + medio + observación
  - Neto real + saldo pendiente
- [ ] **Solo accesible por Dirección** (RBAC enforced)
- [ ] Nombre archivo: APELLIDO_NOMBRE_MES_AÑO_completo.pdf

### US-6.4: Generación masiva de recibos
**Como** RRHH  
**Quiero** generar todos los recibos de un período de una vez  
**Para** no tener que generar uno por uno  

**CA:**
- [ ] Botón "Generar todos los recibos" en la vista de período
- [ ] Genera recibos declarados para todos los empleados del período
- [ ] Descarga como ZIP con un PDF por empleado
- [ ] Si el rol es Dirección, opción de generar también los completos
- [ ] Historial de generaciones previas (fecha, usuario, cantidad)

---

## SPRINT 7 — Préstamos y Adelantos

### US-7.1: Registrar préstamo
**Como** RRHH  
**Quiero** registrar un préstamo otorgado a un empleado  
**Para** controlar la deuda y descontarla automáticamente  

**CA:**
- [ ] Campos: empleado, monto total, cantidad de cuotas, fecha otorgamiento
- [ ] Al crear, generar automáticamente las N cuotas con montos iguales (monto/cuotas)
- [ ] Cuotas distribuidas en períodos futuros consecutivos
- [ ] Estado préstamo: Activo / Pagado / Cancelado
- [ ] Ver tabla de cuotas con estado de cada una
- [ ] Registrar en auditoría

### US-7.2: Descuento automático de cuota en liquidación
**Como** RRHH  
**Quiero** que al generar una liquidación se descuenten las cuotas pendientes automáticamente  
**Para** no tener que recordar descontar manualmente cada mes  

**CA:**
- [ ] Al crear/calcular un período, buscar cuotas pendientes del mes para cada empleado
- [ ] Agregar como concepto de descuento automático (tipo: "Cuota préstamo N/M")
- [ ] Al cerrar el período, marcar la cuota como pagada
- [ ] Si el empleado tiene baja, liquidar saldo completo en la liquidación final

### US-7.3: Registrar adelanto
**Como** Administrativo o RRHH  
**Quiero** registrar un adelanto de sueldo  
**Para** que se descuente en la liquidación del período  

**CA:**
- [ ] Campos: empleado, monto, fecha, período de descuento
- [ ] Se descuenta en la liquidación del período seleccionado
- [ ] También incluye: venta de mercadería y faltante de mercadería (conceptos separados)
- [ ] Rol Administrativo puede cargar adelantos (según RBAC §6)

### US-7.4: Dashboard de saldos pendientes
**Como** RRHH  
**Quiero** ver un resumen de todos los préstamos y saldos pendientes  
**Para** tener visibilidad del total adeudado por empleado y por empresa  

**CA:**
- [ ] Vista con 2 niveles:
  - Por empleado: préstamos activos, cuotas pendientes, saldo total, próxima cuota
  - Por empresa: total adeudado, cantidad de préstamos activos
- [ ] Filtros: empresa, estado (activo/pagado), empleado
- [ ] Exportable a Excel

---

## SPRINT 8 — Asistencia + Licencias + Feriados

### US-8.1: Registrar desvío de asistencia
**Como** Supervisor, Administrativo o RRHH  
**Quiero** registrar cuando un empleado falta, llega tarde o se retira antes  
**Para** tener control y que impacte automáticamente en la liquidación  

**CA:**
- [ ] Tipos: falta justificada, falta injustificada, llegada tarde, retiro temprano, ingreso anticipado
- [ ] Campos: empleado, fecha, tipo, hora (si aplica), observaciones (texto libre)
- [ ] Ej. observaciones: "Certificado médico presentado", "Aviso por teléfono"
- [ ] No se registra presentismo normal (solo desvíos)
- [ ] No permitir duplicar el mismo tipo en la misma fecha para el mismo empleado
- [ ] Supervisor carga para su equipo, RRHH para todos

### US-8.2: Registrar licencia
**Como** RRHH  
**Quiero** registrar una licencia para un empleado seleccionando el tipo legal  
**Para** cumplir con la LCT y que el impacto en sueldo sea automático  

**CA:**
- [ ] Catálogo de licencias (Art. 158 LCT):
  - Matrimonio: 10 días corridos
  - Nacimiento hijo: 2 días hábiles
  - Fallecimiento cónyuge/hijo/padre: 3 días corridos
  - Fallecimiento hermano: 1 día
  - Examen: 2 días por examen, máx 10/año
  - Mudanza: 1 día
  - Donación sangre: 1 día
  - Enfermedad inculpable: según antigüedad (3-12 meses)
- [ ] Campos: empleado, tipo licencia (select del catálogo), fecha desde/hasta, días, con goce (sí/no), certificado adjunto (archivo), observaciones
- [ ] Licencia con goce de sueldo: NO descuenta del neto
- [ ] Licencia sin goce: descuenta proporcional
- [ ] Catálogo extendible (para agregar licencias de CCT si aplica)

### US-8.3: Gestión de feriados
**Como** RRHH  
**Quiero** administrar el calendario de feriados y configurar quién trabaja  
**Para** calcular correctamente las compensaciones  

**CA:**
- [ ] CRUD feriados: fecha, nombre, tipo (nacional/provincial/especial)
- [ ] Importación masiva (lista de feriados del año)
- [ ] Config por empleado: marca si trabaja o no en cada feriado
- [ ] Registro de feriado trabajado: empleado, feriado, horas trabajadas
- [ ] Compensación configurable: pago doble (hs extras 100%) o franco compensatorio

### US-8.4: Impacto automático en liquidación
**Como** RRHH  
**Quiero** que las ausencias y licencias impacten automáticamente en la liquidación  
**Para** no tener que calcular descuentos manualmente  

**CA:**
- [ ] Faltas injustificadas del período → concepto descuento automático
- [ ] Licencias sin goce → descuento proporcional automático
- [ ] Feriados trabajados → concepto hs extras 100% automático
- [ ] Todo visible en el detalle de liquidación del empleado

### US-8.5: Alertas de desvíos reiterados
**Como** RRHH  
**Quiero** recibir alertas cuando un empleado acumula tardanzas o faltas  
**Para** tomar acción disciplinaria a tiempo  

**CA:**
- [ ] Umbrales configurables: ej. 3 tardanzas/mes → alerta, 2 faltas injustificadas → alerta
- [ ] Alerta visible en dashboard de RRHH
- [ ] Alerta al supervisor del empleado si aplica
- [ ] No bloquea ningún proceso, solo informa

---

## SPRINT 9 — Disciplina + Objetivos

### US-9.1: Registrar falta disciplinaria
**Como** RRHH o Supervisor  
**Quiero** registrar una advertencia, apercibimiento o suspensión  
**Para** documentar el historial disciplinario del empleado  

**CA:**
- [ ] Tipos: advertencia verbal, advertencia escrita, apercibimiento, suspensión
- [ ] Campos: empleado, tipo, fecha, descripción, días de suspensión (si aplica), adjuntos (PDF/imagen)
- [ ] Supervisor carga para su equipo, RRHH para todos
- [ ] Historial disciplinario visible en la ficha del empleado
- [ ] Registrar en auditoría

### US-9.2: Historial disciplinario
**Como** RRHH  
**Quiero** ver el historial disciplinario de un empleado  
**Para** evaluar su comportamiento en el tiempo  

**CA:**
- [ ] Timeline cronológico con tipo, fecha, descripción
- [ ] Filtros: tipo, rango de fechas
- [ ] Ver adjuntos asociados
- [ ] Exportable a PDF

### US-9.3: Asignar objetivos
**Como** RRHH o Supervisor  
**Quiero** asignar objetivos a empleados por período  
**Para** medir su desempeño  

**CA:**
- [ ] Campos: empleado, período, título, descripción, métrica, target numérico, peso (%)
- [ ] Un empleado puede tener múltiples objetivos por período
- [ ] La suma de pesos debe ser 100% (validar)
- [ ] Estado: pendiente / en progreso / completado

### US-9.4: Registrar resultado de objetivo
**Como** RRHH o Supervisor  
**Quiero** cargar el resultado de un objetivo  
**Para** calcular el % de cumplimiento  

**CA:**
- [ ] Cargar resultado numérico
- [ ] % cumplimiento = (resultado / target) × 100
- [ ] Cumplimiento ponderado = Σ (% cumplimiento × peso)
- [ ] Si hay premio por objetivos vinculado → concepto remunerativo en liquidación

### US-9.5: Ranking de desempeño
**Como** Dirección o RRHH  
**Quiero** ver un ranking de cumplimiento de objetivos  
**Para** identificar top performers y empleados que necesitan apoyo  

**CA:**
- [ ] Ranking por: área, UN, empresa
- [ ] Filtrable por período
- [ ] Promedio % cumplimiento ponderado por empleado
- [ ] Exportable a Excel

---

## SPRINT 10 — Tareas + Productividad

### US-10.1: Cargar tareas diarias
**Como** Administrativo (o el rol designado para carga)  
**Quiero** registrar las tareas realizadas en el día  
**Para** documentar la actividad y medir productividad  

**CA:**
- [ ] Campos: empleado, fecha, descripción de tarea, horas dedicadas
- [ ] Carga diaria, puede haber múltiples tareas por día
- [ ] Estado: pendiente de aprobación / aprobada / rechazada

### US-10.2: Aprobar/rechazar tareas
**Como** Supervisor  
**Quiero** aprobar o rechazar las tareas cargadas por mi equipo  
**Para** validar que el trabajo fue realizado  

**CA:**
- [ ] Vista de tareas pendientes de aprobación (filtrada por mi equipo)
- [ ] Acción: aprobar o rechazar con comentario
- [ ] Registro de quién aprobó/rechazó y cuándo

### US-10.3: Dashboard de productividad
**Como** Dirección, RRHH o Supervisor  
**Quiero** ver métricas de productividad por empleado  
**Para** evaluar rendimiento del equipo  

**CA:**
- [ ] Métricas:
  - Hs registradas vs jornada contractual
  - % tareas aprobadas
  - Tendencia semanal/mensual
- [ ] Indicador visual: verde (>90%), amarillo (70-90%), rojo (<70%)
- [ ] Gráficos con Recharts
- [ ] Filtros: empleado, equipo, período
- [ ] Supervisor solo ve su equipo

---

## SPRINT 11 — Reportes + Exportaciones

### US-11.1: Reporte liquidación mensual por CUIT
**Como** Dirección o RRHH  
**Quiero** exportar la liquidación mensual de una empresa  
**Para** tener el resumen completo para el estudio contable  

**CA:**
- [ ] Seleccionar empresa + período
- [ ] Reporte con todos los empleados: sueldo, conceptos, descuentos, neto
- [ ] Exportable a Excel y PDF
- [ ] Versión declarada (todos los roles) y completa (solo Dirección)

### US-11.2: Reporte costo laboral por UN
**Como** Dirección  
**Quiero** ver el costo laboral total por unidad de negocio  
**Para** tomar decisiones de asignación de presupuesto  

**CA:**
- [ ] Costo total = Σ sueldos reales por UN
- [ ] Desglose por área dentro de la UN
- [ ] Comparación mes a mes
- [ ] Exportable a Excel

### US-11.3: Reporte de ausentismo
**Como** RRHH  
**Quiero** ver un reporte de ausentismo por área  
**Para** detectar patrones y tomar medidas  

**CA:**
- [ ] Filtros: empresa, UN, área, período, tipo de ausencia
- [ ] Desglose: faltas justificadas vs injustificadas
- [ ] Licencias por tipo
- [ ] Exportable a Excel

### US-11.4: Reporte de horas extras
**Como** RRHH  
**Quiero** ver un reporte de horas extras por empleado  
**Para** controlar costos y detectar excesos  

**CA:**
- [ ] Filtros: empresa, período, empleado
- [ ] Desglose: normales, 50%, 100%
- [ ] Total en horas y en pesos
- [ ] Exportable a Excel

### US-11.5: Visibilidad por rol
**Como** administrador del sistema  
**Quiero** que los reportes respeten los permisos del usuario  
**Para** que nadie vea datos que no le corresponden  

**CA:**
- [ ] Dirección: ve todo (versión completa)
- [ ] RRHH: ve todo (versión completa)
- [ ] Supervisor: solo su equipo, solo versión declarada
- [ ] Administrativo: solo versión declarada
- [ ] Filtrado server-side, no solo ocultando en UI

---

## SPRINT 12-13 — QA + Deploy

### US-12.1: Migración de datos desde Excel
**Como** RRHH  
**Quiero** que los datos actuales del Excel se migren al sistema  
**Para** no tener que cargar 80 empleados manualmente  

**CA:**
- [ ] Script que lee el Excel de Carolina (Liquidación Sueldo 11 02 26.xlsb)
- [ ] Migrar: empleados (~80), datos contractuales (acuerdos con vigencias), empresas
- [ ] Idempotente: puede ejecutarse múltiples veces sin duplicar datos
- [ ] Reporte de migración: cuántos registros migrados, errores encontrados
- [ ] Validación post-migración: comparar totales del Excel vs sistema

### US-12.2: Backup automático
**Como** administrador del sistema  
**Quiero** que la base de datos se resguarde diariamente  
**Para** no perder información en caso de fallo  

**CA:**
- [ ] Cron job diario: pg_dump → compresión → upload a almacenamiento remoto
- [ ] Retención: 30 días diarios + 12 meses mensuales
- [ ] Alerta si el backup falla (email o notificación)
- [ ] Documentar proceso de restore

---

## M14 — Recursos y Accesos (Opcional)

### US-14.1: Asignar recurso a empleado
**Como** RRHH  
**Quiero** registrar qué herramientas, accesos y equipos tiene cada empleado  
**Para** saber qué recursos devolver/revocar cuando se va  

**CA:**
- [ ] Categorías: Cuentas digitales, Apps/Sistemas, Equipamiento físico, Llaves/Accesos, Vehículos
- [ ] Campos: nombre recurso, categoría, estado (Activo/Inactivo/Pendiente), nro serie (si aplica), fecha asignación, asignado por, notas
- [ ] Vista por empleado: listado con badges de estado (verde/rojo/amarillo)
- [ ] Historial de cambios por recurso

### US-14.2: Checklist de onboarding/offboarding
**Como** RRHH  
**Quiero** que al dar de alta/baja un empleado se genere un checklist de recursos  
**Para** no olvidar provisionar o revocar nada  

**CA:**
- [ ] Onboarding: checklist de recursos a provisionar según puesto/área
- [ ] Offboarding: checklist de recursos a revocar/devolver
- [ ] Cada ítem se marca como completado
- [ ] Alerta si quedan ítems pendientes

### US-14.3: Inventario global de recursos
**Como** Dirección o RRHH  
**Quiero** ver un reporte de todos los recursos activos  
**Para** tener visibilidad del inventario de la empresa  

**CA:**
- [ ] Filtros: categoría, empleado, UN, estado
- [ ] Exportable a Excel
- [ ] Total de recursos por categoría

---

*Documento generado el 2026-02-16. Basado en PROJECT.md v1.1, ARCHITECTURE.md, SPRINTS.md v2, respuestas de Carolina y análisis del Excel de liquidación.*
