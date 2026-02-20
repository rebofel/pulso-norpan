# Consultas para Carolina — Proyecto App RRHH

**De:** Feli (Tech Lead)  
**Para:** Carolina  
**Fecha:** 16/02/2026  
**Asunto:** Definiciones necesarias para arrancar el desarrollo + propuesta de módulo nuevo  

---

Caro, analicé todo lo que me mandaste: el mail, la conversación con GPT y la planilla Excel de liquidación. El Excel me sirvió mucho porque tiene la lógica real de cómo se liquida hoy (porcentajes, cuotas, producción, comisiones, pagos parciales, etc.).

Ya armé la documentación técnica del proyecto. Antes de arrancar a programar necesito que me confirmes algunas cosas. Las ordeno por urgencia:

---

## PREGUNTAS BLOQUEANTES (las necesito sí o sí para empezar)

### 1. El "Porcentaje" del acuerdo
En la planilla cada empleado tiene un Porcentaje (0.5, 0.9, 1.0, 1.2, 2.0, etc.) que multiplica el sueldo básico del mes. 

**Pregunta:** ¿Este es el mecanismo para manejar la diferencia entre lo que se declara y lo que realmente se paga? Es decir, ¿el básico de "Tabla Sueldos" es el valor de referencia y el Porcentaje define lo que realmente cobra cada uno?

### 2. ¿Cuántos empleadores son?
En la planilla encontré: NOR-PAN SA, ISABEL MARTINELLI, LUCILA CASTRILLO, DOÑA CAROLINA SAS, CAROLINA ZICOVICH, "SIN EMPLEADOR", MONOTRIBUTO y PPP.

**Pregunta:** ¿Son todos? ¿Pueden aparecer más? ¿"SIN EMPLEADOR" es una categoría informal? Necesito saber esto para configurar bien el sistema multiempresa.

### 3. Composición del sueldo
Veo que hay 3 formas de armar el sueldo: por básico, por producción, o por comisión (definido en los acuerdos).

**Pregunta:** ¿Es correcto? ¿El sistema debe saber de entrada cuál aplica a cada empleado, o es algo que se define mes a mes?

### 4. Pagos parciales
La planilla muestra hasta 4 pagos por período (efectivo, transferencia, MercadoPago, etc.) con fechas distintas.

**Pregunta:** ¿El sistema tiene que registrar cada pago parcial (monto + fecha + medio de pago) hasta completar el saldo? ¿O solo importa el total?

### 5. ¿Cómo se liquida hoy?
Veo que hoy la liquidación se resuelve con la planilla Excel.

**Pregunta:** Además del Excel, ¿usan alguna otra plantilla, programa o sistema para liquidar? ¿Lo hace alguien internamente o lo tercerizan al estudio contable? Necesito entender bien el flujo actual para que el sistema nuevo lo reemplace correctamente y no nos falte nada.

---

## PREGUNTAS IMPORTANTES (las necesito antes de llegar al módulo de liquidación)

### 6. Descuentos legales
En la planilla no aparecen aportes patronales (jubilación, obra social, ley 19032, sindicato).

**Pregunta:** ¿Se calculan por separado? ¿Ya están incluidos en el "acordado"? ¿No se muestran intencionalmente?

### 7. Recibos de sueldo
**Pregunta:** ¿El sistema tiene que generar recibos PDF descargables? ¿Se necesitan dos versiones (una "declarada" y una "real")? ¿O solo es un detalle interno tipo Excel?

### 8. Empleados PPP (Programa Primer Paso)
Veo varios en la planilla.

**Pregunta:** ¿Tienen reglas especiales? ¿Subsidio del gobierno? ¿Se liquidan distinto?

### 9. Formato para el estudio contable
**Pregunta:** ¿El estudio contable que les hace los números tiene un formato específico de archivo que necesiten recibir? Si tienen un ejemplo, me sirve.

---

## PREGUNTAS QUE PUEDEN ESPERAR (las definimos mientras avanzamos)

### 10. Notificaciones
¿Querés que el sistema avise por email o dentro de la app cuando pasa algo? (ej: se carga una sanción, vencen vacaciones, vence un préstamo)

### 11. Convenio colectivo
Algunos empleados tienen "COMERCIO" como convenio. ¿Se aplican escalas salariales obligatorias del CCT?

### 12. Acceso de empleados
¿A futuro los empleados podrían tener su propio login para ver sus recibos/datos?

### 13. Cambio de obra social
Mencionaste "cambio de obra social" como un movimiento registrable. ¿Solo se registra como dato o tiene algún impacto en la liquidación?

---

## PROPUESTA EXTRA: Módulo de Recursos y Accesos del Empleado

Además de todo lo que hablamos, te propongo agregar un módulo para **centralizar qué herramientas y accesos tiene cada empleado**. La idea:

**¿Qué resuelve?**
- Saber de un vistazo qué tiene asignado cada persona: mail de la empresa, acceso a apps, llaves, herramientas, uniformes, vehículos, etc.
- Cuando alguien se va, tener un checklist automático de todo lo que hay que dar de baja o recuperar
- Cuando entra alguien nuevo, saber qué hay que darle de alta

**Ejemplos de lo que se cargaría:**

| Empleado | Recurso | Tipo | Estado | Fecha alta |
|----------|---------|------|--------|-----------|
| López, Santiago | email slopez@norpan.com | Cuenta digital | Activo | 01/03/2022 |
| López, Santiago | Acceso sistema facturación | App/Sistema | Activo | 15/03/2022 |
| López, Santiago | Celular Samsung A54 | Equipo físico | Activo | 01/06/2023 |
| López, Santiago | Llave depósito JM | Llave/Acceso físico | Activo | 01/03/2022 |
| Robles, Hector | email hrobles@norpan.com | Cuenta digital | **Baja** | 01/02/2024 |

**No afecta en nada** al módulo de sueldos ni al resto — es independiente, pero está vinculado al legajo del empleado. Es algo simple de desarrollar y muy útil para el día a día.

¿Te parece? Si te gusta lo incluyo en el plan.

---

Cualquier duda me avisás. Con las respuestas a las primeras 4 preguntas ya puedo arrancar a codear.

Saludos,  
Feli
