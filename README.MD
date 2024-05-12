# API de Usuarios

Esta es una API básica para administrar usuarios utilizando Flask y SQLAlchemy.

## Configuración del Proyecto

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias del proyecto utilizando el siguiente comando:

```bash
pip install -r requirements.txt
```

## Funcionalidades

### 1. Crear Usuario

- **Endpoint:** `/users`
- **Método HTTP:** POST
- **Descripción:** Crea un nuevo usuario con los datos proporcionados.
- **Cuerpo de la Solicitud:**

```json
{
    "name": "Nombre",
    "apellido": "Apellido",
    "correo": "correo@example.com",
    "status": 1
}
```

- **Respuesta Exitosa:**

```json
{
    "message": "Usuario creado exitosamente",
    "usuario": {
        "id": 1,
        "name": "Nombre",
        "apellido": "Apellido",
        "correo": "correo@example.com",
        "status": 1
    }
}
```

### 2. Obtener Usuarios Activos

- **Endpoint:** `/users`
- **Método HTTP:** GET
- **Descripción:** Obtiene una lista de usuarios activos.
- **Parámetros de la Solicitud:** (Opcional)

    - `page`: Número de página (por defecto 1).
    - `per_page`: Usuarios por página (por defecto 20).

- **Respuesta Exitosa:**

```json
[
    {
        "id": 1,
        "name": "Nombre",
        "apellido": "Apellido",
        "correo": "correo@example.com",
        "status": 1
    },
    {
        "id": 2,
        "name": "Nombre2",
        "apellido": "Apellido2",
        "correo": "correo2@example.com",
        "status": 1
    }
]
```

### 3. Obtener Usuario por ID

- **Endpoint:** `/users/<id>`
- **Método HTTP:** GET
- **Descripción:** Obtiene los detalles de un usuario específico por su ID.

- **Respuesta Exitosa:**

```json
{
    "id": 1,
    "name": "Nombre",
    "apellido": "Apellido",
    "correo": "correo@example.com",
    "status": 1
}
```

### 4. Actualizar Usuario

- **Endpoint:** `/users/<id>`
- **Método HTTP:** PUT
- **Descripción:** Actualiza los detalles de un usuario específico por su ID.
- **Cuerpo de la Solicitud:**

```json
{
    "name": "Nuevo Nombre",
    "apellido": "Nuevo Apellido",
    "correo": "nuevo_correo@example.com"
}
```

- **Respuesta Exitosa:**

```json
{
    "message": "Usuario actualizado exitosamente",
    "usuario": {
        "id": 1,
        "name": "Nuevo Nombre",
        "apellido": "Nuevo Apellido",
        "correo": "nuevo_correo@example.com",
        "status": 1
    }
}
```

### 5. Eliminar Usuario

- **Endpoint:** `/users/<id>`
- **Método HTTP:** DELETE
- **Descripción:** Elimina un usuario específico por su ID.

- **Respuesta Exitosa:**

```json
{
    "message": "Usuario eliminado exitosamente",
    "usuario": {
        "id": 1,
        "name": "Nombre",
        "apellido": "Apellido",
        "correo": "correo@example.com",
        "status": 0
    }
}
```

## Registro de Cambios

- **v1.0:** Implementación inicial de la API de Usuarios.
