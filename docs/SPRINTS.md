# NORPAN RRHH - Plan de Desarrollo (Sprints)

## Metodología
- **Sprints de 2 semanas**
- **Estimación core:** 13 sprints (~6.5 meses)
- **Entrega incremental:** cada sprint produce funcionalidad usable
- **Demos:** al final de cada sprint el equipo de NORPAN puede probar lo entregado
- **M14 (Recursos y Accesos):** módulo opcional, se planifica por separado

---

## Hitos de Prueba para el Negocio

> Momentos clave donde Carolina y el equipo pueden empezar a probar/cargar datos reales.

| Hito | Sprint | Qué puede probar Carolina |
|------|--------|---------------------------|
| 🟢 **Carga de legajos** | Sprint 3 | Cargar los ~80 empleados reales, ver fichas, validar datos |
| 🟢 **Primera liquidación** | Sprint 5 | Correr una liquidación de prueba con datos reales y comparar con el Excel |
| 🟢 **Recibos PDF** | Sprint 6 | Generar recibos de sueldo (declarado + real) y revisar pagos parciales |
| 🟢 **Préstamos cargados** | Sprint 7 | Cargar préstamos actuales y ver descuento automático en liquidación |
| 🟢 **Control diario** | Sprint 8 | Registrar desvíos de asistencia, licencias y feriados trabajados |
| 🟢 **Gestión de equipo** | Sprint 10 | Supervisores pueden cargar tareas y objetivos, ver productividad |
| 🟢 **Reportes finales** | Sprint 11 | Exportar liquidación por CUIT, costo por UN, reportes completos |
| 🚀 **Go-live** | Sprint 13 | Sistema en producción reemplazando el Excel |

---

## FASE 1: FUNDACIÓN (Sprints 1-2) — 4 semanas

### Sprint 1 — Setup + Auth + Catálogos
**Objetivo:** Base técnica funcional con login y catálogos

| Tarea | Estimación |
|-------|-----------|
| Setup proyecto: monorepo, linting, CI/CD básico | 2d |
| Modelo de datos inicial (Prisma schema) | 2d |
| Migraciones iniciales PostgreSQL | 1d |
| Auth: registro, login, JWT, refresh token | 2d |
| RBAC middleware (roles + permisos) | 1d |
| Frontend: layout base, navegación, login | 2d |
| **Total** | **10d** |

### Sprint 2 — Catálogos + CRUD Empresas
**Objetivo:** ABM de entidades maestras (empresas dinámicas, no hardcodeadas)

| Tarea | Estimación |
|-------|-----------|
| ABM Empresas (CUIT, razón social, tipo) — dinámico | 2d |
| ABM Unidades de negocio | 1d |
| ABM Áreas | 1d |
| ABM Puestos | 1d |
| ABM Usuarios + asignación de roles | 2d |
| Seed data para testing (4 empresas iniciales + monotributo) | 1d |
| Auditoría: middleware de logging | 2d |
| **Total** | **10d** |

---

## FASE 2: LEGAJO (Sprint 3) — 2 semanas

### Sprint 3 — Módulo de Empleados
**Objetivo:** Alta, edición, búsqueda y visualización de legajos completos

| Tarea | Estimación |
|-------|-----------|
| API CRUD empleados (personales + condición FIJO/MÓVIL + observaciones) | 2d |
| API datos contractuales con vigencias (+ ART, sindicato, categoría) | 2d |
| Datos bancarios (tabla separada + permisos) | 1d |
| Registro de baja (motivo, tipo, fecha) + entidad `terminations` | 1d |
| Frontend: formulario alta/edición empleado (campos ampliados) | 2d |
| Frontend: listado con filtros y búsqueda + vista ficha | 1d |
| Validaciones (DNI único, CUIL formato, empresa obligatoria) | 1d |
| **Total** | **10d** |

> 🟢 **DEMO Sprint 3:** Carolina puede empezar a cargar los ~80 empleados reales. Validar legajos completos (datos personales, contractuales, condición, empresa asignada) antes de avanzar con liquidación.

---

## FASE 3: LIQUIDACIÓN CORE (Sprints 4-5) — 4 semanas

### Sprint 4 — Motor de Liquidación + Modelo Salarial
**Objetivo:** Motor salarial confirmado (básico × porcentaje) + conceptos + cálculos

| Tarea | Estimación |
|-------|-----------|
| Modelo períodos de liquidación (por empresa) | 1d |
| Motor salarial: básico × porcentaje, 3 tipos composición (básico/producción/comisión) | 2d |
| API conceptos remunerativos por período (con observaciones) | 2d |
| API descuentos internos + descuentos legales sobre declarado (§5.2b) | 2d |
| Motor de cálculo: valor hora, prorrateo, neto real vs neto declarado | 2d |
| Conceptos configurables (tabla dinámica) | 1d |
| **Total** | **10d** |

### Sprint 5 — Vacaciones + Aguinaldo + Liquidación Final
**Objetivo:** Reglas de negocio complejas + liquidación final con indemnización

| Tarea | Estimación |
|-------|-----------|
| Cálculo automático de días de vacaciones por antigüedad (tabla LCT) | 2d |
| Fórmula vacaciones: sueldo/25 × días + observaciones | 1d |
| Cálculo SAC automático (jun/dic + proporcional) | 2d |
| Liquidación final ampliada: indemnización Art. 245, tipos de baja, preaviso | 2d |
| Config PPP: porcentaje empresa/gobierno por empleado, cálculo separado | 1d |
| Frontend: pantalla de liquidación por período + detalle conceptos | 2d |
| **Total** | **10d** |

> 🟢 **DEMO Sprint 5:** Carolina puede correr una liquidación de prueba y compararla contra su Excel. Verificar modelo salarial (básico × porcentaje), vacaciones, aguinaldo. **Punto de control crítico.**

---

## FASE 4: PAGOS Y RECIBOS (Sprint 6) — 2 semanas

### Sprint 6 — Pagos Parciales + Recibos PDF
**Objetivo:** Registrar pagos detallados y generar recibos en dos versiones

| Tarea | Estimación |
|-------|-----------|
| API pagos parciales (monto + fecha + medio + observaciones) | 2d |
| Saldo pendiente por período (total - Σ pagos) | 1d |
| Template recibo **declarado** PDF (sueldo + descuentos legales + neto) | 2d |
| Template recibo **real/completo** PDF (básico×%, pagos parciales, descuentos internos) | 2d |
| Generación masiva + descarga ZIP por período | 1d |
| Frontend: detalle pagos por empleado + historial recibos generados | 2d |
| **Total** | **10d** |

> 🟢 **DEMO Sprint 6:** Carolina puede generar recibos para un período y comparar ambas versiones (declarado vs real). Revisar que los pagos parciales con observaciones estén completos.

---

## FASE 5: PRÉSTAMOS Y ADELANTOS (Sprint 7) — 2 semanas

### Sprint 7 — Módulo de Préstamos
**Objetivo:** Control de préstamos con cuotas automáticas

| Tarea | Estimación |
|-------|-----------|
| API CRUD préstamos (monto, cuotas, estado) | 2d |
| Generación automática de cuotas | 1d |
| Integración con liquidación (descuento automático) | 2d |
| API adelantos + venta/faltante de mercadería | 1d |
| Dashboard saldo pendiente (por empleado y total empresa) | 2d |
| Frontend: pantalla préstamos + adelantos | 2d |
| **Total** | **10d** |

---

## FASE 6: ASISTENCIA, LICENCIAS Y FERIADOS (Sprint 8) — 2 semanas

### Sprint 8 — Asistencia + Licencias LCT + Feriados
**Objetivo:** Registro de desvíos, licencias especiales y gestión de feriados

| Tarea | Estimación |
|-------|-----------|
| API registro de desvíos (faltas, tardes, etc.) + campo observaciones | 1d |
| Catálogo tipos de licencia (Art. 158 LCT: matrimonio, nacimiento, etc.) | 1d |
| API licencias: tipo, días, goce/sin goce, adjunto certificado | 2d |
| Calendario de feriados (CRUD + importación) + config por empleado | 1d |
| Registro feriados trabajados + compensación | 1d |
| Integración con liquidación (ausencias injust. → descuento, licencias s/goce → descuento) | 1d |
| Alertas automáticas (tardanzas reiteradas, etc.) | 1d |
| Frontend: pantallas asistencia + licencias + feriados | 2d |
| **Total** | **10d** |

> 🟢 **DEMO Sprint 8:** Carolina puede registrar desvíos de asistencia, cargar licencias con certificados y ver el impacto automático en liquidación.

---

## FASE 7: DISCIPLINA + OBJETIVOS + TAREAS (Sprints 9-10) — 4 semanas

### Sprint 9 — Disciplina y Objetivos
**Objetivo:** Registro disciplinario y gestión de objetivos

| Tarea | Estimación |
|-------|-----------|
| API registro disciplinario + adjuntos | 2d |
| Historial disciplinario con filtros | 1d |
| API objetivos (CRUD + cálculo % cumplimiento) | 3d |
| Ranking por área/unidad de negocio | 1d |
| Frontend: pantallas disciplina + objetivos | 3d |
| **Total** | **10d** |

### Sprint 10 — Tareas y Productividad
**Objetivo:** Registro de tareas con validación de supervisor

| Tarea | Estimación |
|-------|-----------|
| API tareas (CRUD + validación supervisor) | 2d |
| Reportes de productividad (semanal/mensual) | 2d |
| Frontend: carga de tareas + aprobación | 2d |
| Frontend: dashboard productividad | 2d |
| Medición automatizada (hs registradas vs jornada) | 2d |
| **Total** | **10d** |

---

## FASE 8: REPORTES Y EXPORTACIONES (Sprint 11) — 2 semanas

### Sprint 11 — Reportes
**Objetivo:** Todos los reportes solicitados + exportaciones

| Tarea | Estimación |
|-------|-----------|
| Liquidación mensual por CUIT (Excel/PDF) | 2d |
| Detalle individual exportable | 1d |
| Costo laboral por Unidad de Negocio | 1d |
| Exportación contable por UN (CSV/Excel — formato a confirmar con estudio) | 1d |
| Reportes: disciplinario, ausentismo, licencias, HE, productividad | 3d |
| Ranking objetivos exportable | 1d |
| Visibilidad por rol (declarado vs completo) | 1d |
| **Total** | **10d** |

> 🟢 **DEMO Sprint 11:** Carolina y el equipo pueden exportar todas las liquidaciones, ver costos por UN, reportes completos. Validar formatos de exportación.

---

## FASE 9: PULIDO Y DEPLOY (Sprints 12-13) — 4 semanas

### Sprint 12 — QA + Ajustes
| Tarea | Estimación |
|-------|-----------|
| Testing e2e de flujos críticos (liquidación, recibos, préstamos) | 3d |
| Corrección de bugs | 3d |
| Optimización de queries y rendimiento | 2d |
| Backup automático (pg_dump + storage) | 1d |
| Documentación de usuario básica | 1d |
| **Total** | **10d** |

### Sprint 13 — Deploy + Go-live
| Tarea | Estimación |
|-------|-----------|
| Setup servidor producción (HTTPS, dominio, DNS) | 2d |
| Deploy CI/CD completo | 1d |
| Script migración datos del Excel actual (~80 empleados + histórico) | 2d |
| Capacitación usuarios (Dirección, RRHH, Supervisores) | 2d |
| Soporte post-lanzamiento (2 semanas) | 3d |
| **Total** | **10d** |

---

## Resumen de Timeline

```
Feb 2026  ████████ Sprint 1-2: Fundación + Auth + Catálogos
Mar 2026  ████     Sprint 3: Legajo ← 🟢 Carolina carga empleados
Mar-Abr   ████████ Sprint 4-5: Liquidación Core ← 🟢 Primera liquidación de prueba
Abr 2026  ████     Sprint 6: Pagos Parciales + Recibos PDF ← 🟢 Recibos para revisar
May 2026  ████     Sprint 7: Préstamos y Adelantos
May 2026  ████     Sprint 8: Asistencia + Licencias LCT + Feriados ← 🟢 Control diario
Jun 2026  ████████ Sprint 9-10: Disciplina + Objetivos + Tareas
Jul 2026  ████     Sprint 11: Reportes ← 🟢 Exportaciones completas
Jul-Ago   ████████ Sprint 12-13: QA + Deploy ← 🚀 Go-live
```

**Go-live estimado: Agosto 2026**

**Estimación core: 13 sprints × 10d = 130 días-dev (~520 horas con AI)**

---

## MÓDULO OPCIONAL: Recursos y Accesos (M14)

> Módulo independiente, no afecta liquidación ni el resto del sistema. Se puede desarrollar en cualquier momento post-Sprint 3 (necesita legajo de empleados). Carolina no confirmó prioridad, queda como add-on.

### Sprint M14 — Recursos y Accesos (~1 sprint, 10d)

| Tarea | Estimación |
|-------|-----------|
| Modelo DB: employee_resources + seeders categorías | 1d |
| API CRUD recursos (asignar, revocar, editar) | 2d |
| API historial de cambios por recurso | 1d |
| Frontend: vista por empleado (listado + badges estado) | 2d |
| Frontend: vista global con filtros (categoría, UN, estado) | 1d |
| Checklists onboarding/offboarding automáticos | 2d |
| Exportación Excel inventario de recursos | 1d |
| **Total** | **10d** |

**Opciones de planificación:**
- **Opción A:** Hacerlo en paralelo durante Sprint 9-10 (si hay capacidad)
- **Opción B:** Hacerlo post go-live como mejora
- **Opción C:** Intercalarlo como Sprint 3.5 (si Carolina lo prioriza)

---

## Riesgos Identificados

| Riesgo | Impacto | Mitigación |
|--------|---------|-----------|
| Formato exportación contable desconocido | Medio | Pedir ejemplo al estudio laboral antes de Sprint 11 (pregunta 9). No bloquea desarrollo |
| Cambios de requisitos durante desarrollo | Medio | Sprints cortos + demos quincenales |
| Migración de datos del Excel | Medio | Diseñar script de migración durante Sprint 5 (cuando se valida con datos reales) |
| CCT sin definir | Bajo | Si aplica un CCT específico, puede agregar licencias extra y tope indemnización. Preguntar a Carolina (post-MVP) |
| Template recibo PDF | Bajo | Empezar con template genérico, iterar con feedback de Carolina en Sprint 6 |

---

## Dependencias Externas

1. **Carolina:** Todas las preguntas bloqueantes resueltas (§11 del PROJECT.md). Solo queda formato contable (pregunta 9), que no bloquea desarrollo
2. **Estudio laboral:** Pedir formato de exportación contable antes de Sprint 11
3. **Infraestructura:** Definir hosting antes de Sprint 12 (VPS o cloud)
4. **Datos:** Acceso al Excel actualizado para diseñar migración (Sprint 5-6)

---

## Changelog del Plan

| Fecha | Cambio |
|-------|--------|
| 2026-02-16 | Plan inicial: 12 sprints, go-live julio 2026 |
| 2026-02-16 | Modelo salarial confirmado (básico × porcentaje) → Sprint 4 actualizado |
| 2026-02-16 | Recibos PDF (2 versiones) → Nuevo Sprint 6, total 13 sprints |
| 2026-02-16 | Licencias LCT (Art. 158) → Sprint 8 ampliado |
| 2026-02-16 | Indemnización Art. 245 + tipos de baja → Sprint 5 ampliado |
| 2026-02-16 | Descuentos legales sobre declarado → Sprint 4 incluido |
| 2026-02-16 | Campos legajo ampliados (condición, motivo baja, ART, sindicato) → Sprint 3 |

---

*Plan generado el 2026-02-16. v2 — incorpora recibos PDF, licencias LCT, indemnización, descuentos legales y observaciones.*
