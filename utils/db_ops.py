import sqlite3
import pandas as pd
import hashlib # Para hashing de contraseñas (simple para el demo)
import os

# --- Configuración de la Base de Datos SQLite para Usuarios ---
# Este archivo almacenará la información de los usuarios.
DB_FILE_USERS = 'users_db.db' 

def init_db():
    """
    Inicializa la base de datos de usuarios: crea la tabla 'users' si no existe.
    También asegura que un usuario 'admin' por defecto exista si la tabla está vacía.
    """
    with sqlite3.connect(DB_FILE_USERS) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                is_admin BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()

    # Asegurarse de que al menos un usuario admin exista si la base de datos está vacía
    # Esto se hace solo una vez al inicio para poblar la BD.
    if get_all_users().empty:
        try:
            # Crea un usuario administrador por defecto con contraseña "admin123"
            add_user("admin", "admin123", is_admin=True)
            # print("Base de datos inicializada y usuario 'admin' creado. ¡Contraseña: admin123!") # Para depuración
        except Exception as e:
            # En caso de que se intente crear múltiples veces o haya otro error
            # print(f"Error al crear admin inicial (posiblemente ya existe): {e}") # Para depuración
            pass # Ignorar si ya existe

def hash_password(password):
    """
    Genera un hash simple para la contraseña usando SHA256.
    NOTA: Para una aplicación de producción, se recomienda usar algoritmos más robustos
    como `bcrypt` o `Argon2` con una librería como `passlib`.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password, is_admin=False):
    """
    Agrega un nuevo usuario a la base de datos.
    Retorna True si el usuario fue añadido, False si ya existe o hay un error.
    """
    hashed_password = hash_password(password)
    with sqlite3.connect(DB_FILE_USERS) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                (username, hashed_password, is_admin)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Error si el username ya existe (UNIQUE constraint)
            return False 
        except Exception as e:
            # print(f"Error al añadir usuario {username}: {e}") # Para depuración
            return False

def verify_user(username, password):
    """
    Verifica las credenciales de un usuario.
    Retorna un diccionario con 'username' y 'is_admin' si las credenciales son correctas,
    None en caso contrario.
    """
    hashed_password = hash_password(password)
    with sqlite3.connect(DB_FILE_USERS) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, is_admin FROM users WHERE username = ? AND password = ?",
            (username, hashed_password)
        )
        user_data = cursor.fetchone()
        if user_data:
            return {"username": user_data[0], "is_admin": bool(user_data[1])}
        return None

def get_all_users():
    """
    Obtiene todos los usuarios de la base de datos.
    Retorna un pandas DataFrame. Útil para depuración o para un panel de administración.
    """
    with sqlite3.connect(DB_FILE_USERS) as conn:
        df = pd.read_sql_query("SELECT id, username, is_admin FROM users", conn)
        return df

