# NORPAN RRHH - Propuesta de Arquitectura Técnica

## Stack Tecnológico Propuesto

### Frontend
| Tecnología | Justificación |
|------------|---------------|
| **React + TypeScript** | Tipado fuerte, ecosistema maduro, componentización |
| **Vite** | Build rápido, HMR, configuración simple |
| **TailwindCSS + shadcn/ui** | UI consistente, componentes accesibles, rápido de prototipar |
| **TanStack Query** | Cache de datos, sincronización server-state |
| **React Router v7** | Navegación SPA |
| **React Hook Form + Zod** | Formularios complejos con validación tipada |
| **Recharts** | Gráficos para reportes/dashboards |
| **xlsx / jsPDF** | Exportación Excel y PDF del lado cliente |

### Backend
| Tecnología | Justificación |
|------------|---------------|
| **Node.js + Express/Fastify** | Mismo lenguaje front/back, equipo unificado |
| **TypeScript** | Consistencia con frontend, tipado e2e |
| **Prisma ORM** | Type-safe queries, migraciones, introspección |
| **PostgreSQL** | Robusta, relacional, soporte multitenancy, JSON nativo |
| **JWT + bcrypt** | Autenticación stateless con refresh tokens |
| **Zod** | Validación compartida front/back |
| **node-cron** | Tareas programadas (backups, alertas) |

### Infraestructura
| Componente | Opción |
|------------|--------|
| **Hosting** | VPS (ej: DigitalOcean/Hetzner) o cloud (Railway/Render) |
| **DB hosting** | Managed PostgreSQL o self-hosted |
| **CI/CD** | GitHub Actions |
| **Backup DB** | pg_dump automático diario + storage (S3/Backblaze) |
| **Monitoreo** | Sentry (errores) + uptime check |

---

## Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────┐
│                   FRONTEND                       │
│          React + TypeScript + Vite               │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │ Auth     │ │ Legajo   │ │ Liquidación      │ │
│  │ Module   │ │ Module   │ │ Module           │ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │ Discipl. │ │ Objetivos│ │ Asistencia       │ │
│  │ Module   │ │ & Tareas │ │ & Feriados       │ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
│  ┌──────────┐ ┌──────────────────────────────┐   │
│  │ Reportes │ │ Admin (Users/Roles/Catálogos) │  │
│  └──────────┘ └──────────────────────────────┘   │
└──────────────────────┬──────────────────────────┘
                       │ REST API (JSON)
                       ▼
┌─────────────────────────────────────────────────┐
│                   BACKEND                        │
│          Node.js + TypeScript + Fastify           │
│  ┌──────────────────────────────────────────┐    │
│  │  Middleware: Auth (JWT) + RBAC + Audit    │   │
│  └──────────────────────────────────────────┘    │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │ Employees│ │ Payroll  │ │ Loans/Advances   │ │
│  │ Service  │ │ Engine   │ │ Service          │ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │ Discipl. │ │ Goals    │ │ Attendance       │ │
│  │ Service  │ │ & Tasks  │ │ Service          │ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
│  ┌──────────┐ ┌──────────────────────────────┐   │
│  │ Reports  │ │ Admin Service                 │  │
│  │ Engine   │ │ (Users/Roles/Companies/Audit) │  │
│  └──────────┘ └──────────────────────────────┘   │
└──────────────────────┬──────────────────────────┘
                       │ Prisma ORM
                       ▼
┌─────────────────────────────────────────────────┐
│              PostgreSQL Database                 │
│  ┌──────────────────────────────────────────┐    │
│  │  Multi-empresa via company_id (soft MT)   │   │
│  └──────────────────────────────────────────┘    │
│  Schemas: employees, payroll, loans, discipline, │
│           goals, tasks, attendance, holidays,    │
│           audit, auth, catalogs                  │
└─────────────────────────────────────────────────┘
```

---

## Modelo de Base de Datos (Entidades Principales)

### Core
- `companies` — Empresas (5 CUIT)
- `business_units` — Unidades de negocio (por empresa)
- `areas` — Áreas (por unidad de negocio)
- `positions` — Puestos

### Auth & Permisos
- `users` — Usuarios del sistema
- `roles` — Dirección, RRHH, Supervisor, Administrativo
- `permissions` — Permisos granulares por módulo/acción
- `user_roles` — Asignación usuario-rol

### Empleados
- `employees` — Datos personales (incluye notes/observaciones generales)
- `employee_contracts` — Datos contractuales con vigencias (desde/hasta)
- `employee_bank_info` — Datos bancarios (tabla separada por seguridad)
- `employee_family` — Grupo familiar (para SUAF/asignaciones, post-MVP)
- `terminations` — Registro de baja (tipo, fecha, indemnización calculada, documentación emitida)

### Liquidación
- `payroll_periods` — Períodos de liquidación (mes/año + empresa)
- `payroll_items` — Conceptos por empleado por período
- `payroll_config` — Conceptos configurables (nombre, tipo, fórmula)
- `payroll_payments` — Pagos parciales por período (monto, fecha, medio_pago, notes)

### Préstamos y Adelantos
- `loans` — Préstamos (monto, cuotas, tasa, estado)
- `loan_installments` — Cuotas (monto, período, pagada sí/no)
- `advances` — Adelantos (vinculados a período)

### Vacaciones y Aguinaldo
- `vacation_requests` — Solicitudes de vacaciones (días, fechas, notes)
- `vacation_balances` — Saldos de días por empleado
- `aguinaldo_calculations` — Cálculos SAC por semestre

### Disciplina
- `disciplinary_records` — Registros disciplinarios
- `disciplinary_attachments` — Adjuntos

### Objetivos y Tareas
- `goals` — Objetivos por empleado/período
- `tasks` — Tareas diarias
- `task_validations` — Aprobaciones de supervisor

### Asistencia
- `attendance_deviations` — Solo desvíos (falta, tarde, retiro temprano, ingreso anticipado, notes)
- `leave_types` — Catálogo de tipos de licencia (LCT + CCT: matrimonio, nacimiento, fallecimiento, etc.)
- `leaves` — Licencias (tipo, días, certificado, notes)
- `holidays` — Feriados del calendario
- `employee_holiday_config` — Config de feriados por empleado
- `holiday_work_records` — Registro de feriados trabajados

### Auditoría
- `audit_logs` — Log inmutable (usuario, entidad, campo, valor_anterior, valor_nuevo, timestamp)

### Recursos y Accesos (M14)
- `resource_categories` — Catálogo de categorías (Cuenta digital, App/Sistema, Equipo físico, Llave/Acceso, Vehículo)
- `employee_resources` — Recurso asignado a empleado (nombre, category_id, status, serial_number, assigned_date, revoked_date, assigned_by, notes)
- `resource_history` — Log de cambios por recurso (asignación, revocación, cambio estado)

---

## Seguridad

1. **Autenticación:** JWT con access token (15min) + refresh token (7d)
2. **Autorización:** Middleware RBAC que valida rol + permiso por endpoint
3. **Datos sensibles:** Tabla separada para info bancaria con permisos estrictos
4. **Auditoría:** Trigger/middleware que loguea cambios en tablas críticas
5. **Passwords:** bcrypt con salt rounds ≥ 12
6. **Rate limiting:** En endpoints de login y exportación
7. **HTTPS:** Obligatorio en producción

---

## Estrategia Multiempresa

Se usa **soft multi-tenancy**: todas las empresas comparten la misma base de datos, cada registro relevante tiene un `company_id`. Los queries siempre filtran por empresa activa del usuario.

Un empleado pertenece a **una empresa (CUIT)** pero un usuario admin puede ver todas las empresas.

---

## Alternativas Evaluadas

| Decisión | Opción elegida | Alternativa descartada | Motivo |
|----------|---------------|----------------------|--------|
| Framework backend | Fastify | NestJS | Más ligero, suficiente para este scope |
| ORM | Prisma | TypeORM / Drizzle | Mejor DX, migraciones más simples |
| DB | PostgreSQL | MySQL | Mejor soporte JSON, CTEs, constraints |
| Frontend | React + Vite | Next.js | No necesitamos SSR, es una app interna |
| UI Kit | shadcn/ui | MUI / Ant Design | Más liviano, customizable, moderno |

---

*Documento generado el 2026-02-16. Sujeto a revisión con el equipo.*
