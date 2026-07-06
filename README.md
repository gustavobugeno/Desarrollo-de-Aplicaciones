# CBC E.I.R.L. - Sistema Web de Gestión de Servicios

## Acceso al Proyecto

🌐 **Sitio Web:** https://desarrollo-de-aplicaciones-d7hl.onrender.com/

💻 **Repositorio:** https://github.com/gustavobugeno/Desarrollo-de-Aplicaciones
## Descripción

Este proyecto corresponde al desarrollo de una aplicación web para la empresa **CBC E.I.R.L.**, dedicada a la prestación de servicios de construcción, obras civiles, montajes, mantenciones y servicios industriales.

El sistema fue desarrollado utilizando **Django** bajo una arquitectura en capas (Modelo-Vista-Template), permitiendo administrar los servicios ofrecidos por la empresa y gestionar las solicitudes de información realizadas por los clientes.

---

# Tecnologías utilizadas

- Python 3.14
- Django 5
- PostgreSQL
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Git
- GitHub
- Render

---

# Arquitectura del Proyecto (Modelo N-Capas)

La aplicación fue diseñada siguiendo una arquitectura en capas.

## Capa de Presentación

Encargada de mostrar la información al usuario mediante:

- Templates HTML
- Bootstrap
- CSS
- JavaScript

## Capa de Lógica de Negocio

Implementada mediante:

- Views
- Formularios
- Validaciones
- Gestión de solicitudes
- Administración de servicios

## Capa de Datos

Compuesta por:

- Modelos Django
- PostgreSQL
- Migraciones

Esta separación facilita el mantenimiento, escalabilidad y reutilización del código.

---

# Módulos del Sistema

## Inicio

- Presentación de la empresa.
- Información institucional.

---

## Servicios

Permite visualizar todos los servicios registrados desde el panel administrativo.

Funciones:

- Mostrar imagen principal.
- Mostrar descripción.
- Mostrar galería.
- Solicitar información.

---

## Solicitudes de Información

Los clientes pueden enviar consultas sobre un servicio.

Información solicitada:

- Nombre
- Correo electrónico
- Teléfono
- Mensaje

Las solicitudes quedan almacenadas en la base de datos.

---

## Administración de Servicios

Disponible únicamente para administradores.

Permite realizar operaciones CRUD:

- Crear servicio
- Editar servicio
- Eliminar servicio
- Publicar servicio

---

## Panel de Solicitudes

Permite:

- Visualizar solicitudes
- Marcar como revisadas
- Administrar consultas

---

# CRUD Implementados

## Servicios

✔ Crear

✔ Leer

✔ Actualizar

✔ Eliminar

---

## Solicitudes

✔ Crear

✔ Leer

✔ Actualizar estado

---

# Validación de Datos

El sistema realiza validaciones para garantizar la integridad de la información.

Ejemplos:

- Campos obligatorios.
- Validación de correo electrónico.
- Restricción de longitud.
- Protección CSRF.
- Validaciones del ORM de Django.

---

# Pruebas Realizadas

## Prueba 1

Objetivo:

Registrar un nuevo servicio.

Resultado:

Correcto.

---

## Prueba 2

Objetivo:

Enviar una solicitud de información.

Resultado:

La información se almacena correctamente en PostgreSQL.

---

## Prueba 3

Objetivo:

Modificar un servicio.

Resultado:

Actualización exitosa.

---

## Prueba 4

Objetivo:

Eliminar un servicio.

Resultado:

Registro eliminado correctamente.

---

## Prueba 5

Objetivo:

Marcar solicitud como revisada.

Resultado:

Estado actualizado correctamente.

---

# Documentación de Clases

Principales clases desarrolladas.

## Servicio

Representa los servicios ofrecidos por la empresa.

Responsabilidades:

- almacenar información
- imágenes
- descripción

---

## SolicitudInformacion

Representa las solicitudes realizadas por los clientes.

Responsabilidades:

- almacenar datos del cliente
- estado de revisión
- fecha de envío

---

## Views

Responsables de:

- lógica de negocio
- consultas
- renderizado
- procesamiento de formularios

---

# Manual de Usuario

## Cliente

1. Ingresar al sitio web.
2. Revisar los servicios.
3. Seleccionar un servicio.
4. Completar el formulario.
5. Enviar la solicitud.
6. Revisar seguimiento.

---

## Administrador

1. Iniciar sesión.
2. Acceder al panel administrativo.
3. Gestionar servicios.
4. Revisar solicitudes.
5. Cambiar estado de las solicitudes.
6 Administrar seguimiento.
---

# Manual de Instalación

## Clonar el proyecto

```bash
git clone https://github.com/gustavobugeno/Desarrollo-de-Aplicaciones.git
```

Entrar al proyecto

```bash
cd Desarrollo-de-Aplicaciones
```

Crear entorno virtual

```bash
python -m venv venv
```

Activar entorno

Windows

```bash
venv\Scripts\activate
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

Aplicar migraciones

```bash
python manage.py migrate
```

Crear superusuario

```bash
python manage.py createsuperuser
```

Ejecutar servidor

```bash
python manage.py runserver
```

---

# Términos y Condiciones

- El sitio tiene fines informativos y comerciales.
- La información enviada por los clientes será utilizada únicamente para responder solicitudes relacionadas con los servicios de CBC E.I.R.L.
- Los datos personales no serán compartidos con terceros.
- El usuario acepta proporcionar información veraz.
- CBC E.I.R.L. podrá actualizar los contenidos del sitio sin previo aviso.

---

# Estado del Proyecto

Proyecto Finalizado.

Cumple con:

- Arquitectura en capas
- CRUD completo
- Validaciones
- PostgreSQL
- Django
- Bootstrap
- Manual de Usuario
- Manual de Instalación
- Documentación técnica

---

# Autores

Gustavo Bugueño
Benjamin Morales
