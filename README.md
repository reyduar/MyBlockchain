# MyBlockchain - Criptomoneda Recklion

## 📋 Descripción del Proyecto

Este proyecto implementa una **blockchain completa** y una **criptomoneda funcional** llamada **Recklion Coin** desde cero, utilizando Python. El sistema incluye todos los componentes fundamentales de una blockchain moderna: minería de bloques, transacciones, consenso distribuido y una API REST para interactuar con la red.

La implementación fue desarrollada con fines educativos para comprender a profundidad los mecanismos internos de las criptomonedas como Bitcoin y Ethereum, incluyendo el algoritmo de Proof of Work (PoW), la descentralización mediante nodos y el consenso de la cadena más larga.

---

## 🗂️ Estructura del Proyecto

```
MyBlockchain/
│
├── src/
│   ├── __init__.py
│   └── blockchain.py          # Clase principal Blockchain con toda la lógica
│
├── notebooks/
│   ├── 01_blockchain_basics.ipynb              # Fundamentos de blockchain
│   └── 02_blockchain_transactions.ipynb        # Implementación de la criptomoneda y API REST
│
├── requirements.txt           # Dependencias del proyecto
├── LICENSE                    # Licencia del proyecto
└── readme.md                  # Este archivo
```

### Descripción de los Componentes

- **`src/blockchain.py`**: Contiene la clase `Blockchain` con toda la lógica core de la blockchain, incluyendo creación de bloques, minería, validación, transacciones y consenso distribuido.

- **`notebooks/01_blockchain_basics.ipynb`**: Notebook introductorio que explica los conceptos fundamentales de blockchain y cómo funcionan los bloques.

- **`notebooks/02_blockchain_transactions.ipynb`**: Notebook principal que implementa la API REST completa para interactuar con la blockchain, permitiendo minar bloques, realizar transacciones y gestionar nodos.

---

## 🛠️ Tecnologías Utilizadas

### Lenguaje Principal

- **Python 3.x**: Lenguaje de programación principal del proyecto.

### Librerías y Frameworks

1. **Flask 3.1.2**: Framework web ligero para crear la API REST que permite interactuar con la blockchain.

2. **hashlib**: Librería estándar de Python para generar hashes SHA-256, utilizada para crear los hashes de los bloques.

3. **datetime**: Librería estándar para manejar timestamps en cada bloque.

4. **json**: Librería estándar para serializar y deserializar datos de los bloques.

5. **requests 2.31.0**: Cliente HTTP para la comunicación entre nodos de la red blockchain.

6. **uuid**: Librería estándar para generar identificadores únicos para las direcciones de los nodos.

7. **urllib.parse**: Librería estándar para parsear URLs de los nodos de la red.

8. **Jupyter / ipykernel**: Para desarrollo interactivo y documentación en notebooks.

---

## 🚀 Configuración del Entorno

### 1. Crear un Entorno Virtual de Python

Es altamente recomendable usar un entorno virtual para aislar las dependencias del proyecto.

#### En macOS/Linux:

```bash
# Navegar al directorio del proyecto
cd /Users/arielduarte/Workspaces/Recklion/MyBlockchain

# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate
```

#### En Windows:

```bash
# Navegar al directorio del proyecto
cd C:\ruta\a\MyBlockchain

# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
venv\Scripts\activate
```

Una vez activado, verás `(venv)` al inicio de tu línea de comando.

### 2. Instalar Dependencias con pip

Con el entorno virtual activado, instala todas las dependencias del proyecto:

```bash
# Instalar desde el archivo requirements.txt
pip install -r requirements.txt
```

Este comando instalará automáticamente:

- Flask 3.1.2
- requests 2.31.0
- ipykernel 6.29.5
- jupyter 1.1.1
- Y todas sus dependencias

### 3. Verificar la Instalación

Para verificar que todo se instaló correctamente:

```bash
# Ver todas las librerías instaladas
pip list

# Verificar versión de Flask
python -c "import flask; print(flask.__version__)"

# Verificar versión de requests
python -c "import requests; print(requests.__version__)"
```

### 4. Desactivar el Entorno Virtual

Cuando termines de trabajar:

```bash
deactivate
```

---

## 🔧 Cómo Funciona la Blockchain

### Arquitectura General

La blockchain de Recklion Coin está compuesta por una cadena de bloques enlazados criptográficamente, donde cada bloque contiene:

1. **Índice**: Posición del bloque en la cadena
2. **Timestamp**: Momento exacto de creación del bloque
3. **Transacciones**: Lista de transacciones incluidas en el bloque
4. **Proof (Nonce)**: Número obtenido mediante Proof of Work
5. **Previous Hash**: Hash del bloque anterior (enlace criptográfico)

### Componentes Principales

#### 1. **Creación de Bloques** (`create_block`)

Cada bloque nuevo se crea con:

- Un índice incremental
- Un timestamp del momento de creación
- Las transacciones pendientes en la mempool
- El proof (nonce) obtenido mediante minería
- El hash del bloque anterior

```python
block = {
    'index': len(self.chain) + 1,
    'timestamp': datetime.datetime.now().timestamp(),
    'proof': proof,
    'previous_hash': previous_hash,
    'transactions': self.transactions
}
```

#### 2. **Proof of Work (PoW)** - Algoritmo de Consenso

El sistema utiliza Proof of Work como mecanismo de consenso:

**Objetivo**: Encontrar un número (nonce) que, al combinarse con el nonce del bloque anterior, genere un hash que cumpla con cierta dificultad (número de ceros al inicio).

**Proceso**:

1. Se calcula: `new_nonce² - previous_nonce²`
2. Se genera el hash SHA-256 del resultado
3. Si el hash comienza con `N` ceros (dificultad = 4 por defecto), se acepta
4. Si no, se incrementa el nonce y se repite

**Dificultad Configurable**: El parámetro `difficulty` define cuántos ceros debe tener el hash (default: 4).

```python
target = '0' * self.difficulty  # Ej: "0000"
hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
```

Este proceso consume recursos computacionales, lo que hace extremadamente difícil alterar bloques antiguos.

#### 3. **Hashing Criptográfico** (`hash`)

Cada bloque genera un hash único usando SHA-256:

- Los datos del bloque se serializan a JSON ordenado
- Se codifican a bytes
- Se genera el hash SHA-256

Este hash sirve como:

- Identificador único del bloque
- Enlace con el siguiente bloque
- Mecanismo de detección de alteraciones

#### 4. **Validación de la Cadena** (`is_chain_valid`)

La blockchain se valida verificando:

1. **Integridad de enlaces**: Cada bloque debe tener el hash correcto del bloque anterior
2. **Validez del PoW**: Cada proof debe cumplir con la dificultad establecida

Si cualquier bloque se altera:

- Su hash cambia
- El siguiente bloque apunta a un hash incorrecto
- La cadena se vuelve inválida

#### 5. **Sistema de Transacciones** (`add_transaction`)

Las transacciones se almacenan en una mempool hasta que se minan:

```python
transaction = {
    'sender': 'Alice',
    'receiver': 'Bob',
    'amount': 50
}
```

Cuando se mina un bloque:

- Se incluyen todas las transacciones pendientes
- Se limpia la mempool
- Se agrega una recompensa de minería (10 Recklion Coins)

#### 6. **Descentralización y Nodos** (`add_node`, `replace_chain`)

**Red de Nodos**:

- Cada nodo mantiene una copia de la blockchain
- Los nodos pueden ejecutarse en diferentes puertos (5000, 5001, 5002, etc.)

**Algoritmo de Consenso - Cadena más Larga**:

1. Cada nodo consulta las blockchains de otros nodos
2. Si encuentra una cadena más larga **y válida**
3. Reemplaza su cadena local por la más larga

Este mecanismo asegura que todos los nodos converjan a la misma versión de la verdad.

---

## 🌐 API REST - Endpoints

La aplicación Flask expone una API REST completa para interactuar con la blockchain:

### 1. **Minar Bloque** - `GET /mine_block`

Mina un nuevo bloque y agrega una recompensa de 10 Recklion Coins al minero.

```bash
curl -X GET http://localhost:5000/mine_block
```

### 2. **Obtener Cadena** - `GET /get_chain`

Devuelve toda la blockchain con todos sus bloques.

```bash
curl -X GET http://localhost:5000/get_chain
```

### 3. **Validar Blockchain** - `GET /is_valid`

Verifica la integridad de toda la cadena.

```bash
curl -X GET http://localhost:5000/is_valid
```

### 4. **Agregar Transacción** - `POST /add_transaction`

Agrega una transacción a la mempool.

```bash
curl -X POST http://localhost:5000/add_transaction \
  -H "Content-Type: application/json" \
  -d '{"sender": "Alice", "receiver": "Bob", "amount": 50}'
```

### 5. **Conectar Nodo** - `POST /connect_node`

Conecta nuevos nodos a la red.

```bash
curl -X POST http://localhost:5000/connect_node \
  -H "Content-Type: application/json" \
  -d '{"nodes": ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]}'
```

### 6. **Reemplazar Cadena** - `GET /replace_chain`

Ejecuta el algoritmo de consenso y sincroniza con la cadena más larga.

```bash
curl -X GET http://localhost:5000/replace_chain
```

---

## 💻 Ejecución del Proyecto

### Opción 1: Desde Jupyter Notebook (Recomendado)

1. Activa el entorno virtual
2. Inicia Jupyter:
   ```bash
   jupyter notebook
   ```
3. Abre `notebooks/02_blockchain_transactions.ipynb`
4. Ejecuta las celdas secuencialmente

### Opción 2: Desde Script Python

Crea un archivo `run_server.py`:

```python
from src.blockchain import Blockchain
from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

node_address = str(uuid4()).replace('-', '')
blockchain = Blockchain()

# ... (copiar todos los endpoints del notebook)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Ejecutar:

```bash
python run_server.py
```

### Opción 3: Múltiples Nodos (Red Descentralizada)

Para simular una red descentralizada, ejecuta múltiples instancias en diferentes puertos:

**Terminal 1** (Nodo 5000):

```bash
python run_server.py
```

**Terminal 2** (Nodo 5001):
Modifica el puerto a 5001 y ejecuta otra instancia.

**Terminal 3** (Nodo 5002):
Modifica el puerto a 5002 y ejecuta otra instancia.

---

## 🧪 Pruebas y Ejemplos de Uso

### Ejemplo 1: Minar 3 Bloques

```bash
curl http://localhost:5000/mine_block
curl http://localhost:5000/mine_block
curl http://localhost:5000/mine_block
curl http://localhost:5000/get_chain
```

### Ejemplo 2: Crear Transacciones y Minar

```bash
# Agregar transacción 1
curl -X POST http://localhost:5000/add_transaction \
  -H "Content-Type: application/json" \
  -d '{"sender": "Alice", "receiver": "Bob", "amount": 100}'

# Agregar transacción 2
curl -X POST http://localhost:5000/add_transaction \
  -H "Content-Type: application/json" \
  -d '{"sender": "Bob", "receiver": "Charlie", "amount": 50}'

# Minar bloque con ambas transacciones
curl http://localhost:5000/mine_block

# Ver la blockchain
curl http://localhost:5000/get_chain
```

### Ejemplo 3: Red de Nodos

```bash
# En el nodo 5000, conectar otros nodos
curl -X POST http://localhost:5000/connect_node \
  -H "Content-Type: application/json" \
  -d '{"nodes": ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]}'

# Sincronizar con la cadena más larga
curl http://localhost:5000/replace_chain
```

---

## 🔐 Seguridad y Características

### ✅ Características Implementadas

- **Inmutabilidad**: Una vez que un bloque se mina, no puede alterarse sin invalidar toda la cadena posterior
- **Proof of Work**: Protección contra ataques de spam y generación masiva de bloques
- **Hashing SHA-256**: Estándar de seguridad criptográfica usado por Bitcoin
- **Validación de Cadena**: Verificación constante de la integridad de toda la blockchain
- **Descentralización**: Múltiples nodos pueden mantener copias de la blockchain
- **Consenso**: Algoritmo de la cadena más larga para resolver conflictos

### ⚠️ Limitaciones (Sistema Educativo)

Este proyecto es educativo y **NO está listo para producción**. Faltarían:

- Sistema de wallets y criptografía de claves públicas/privadas
- Verificación de firmas digitales
- Prevención de doble gasto
- Sistema de recompensas dinámico
- Optimización de almacenamiento
- Mecanismos de seguridad contra ataques Sybil
- Persistencia de datos en base de datos

---

## 📚 Conceptos Avanzados

### Dificultad Ajustable

La dificultad del PoW puede configurarse al crear la blockchain:

```python
# Fácil (2 ceros) - Minado rápido
blockchain = Blockchain(difficulty=2)

# Difícil (6 ceros) - Minado lento, más seguro
blockchain = Blockchain(difficulty=6)
```

### Por Qué Funciona el Proof of Work

1. **Difícil de crear**: Encontrar el nonce requiere miles/millones de intentos
2. **Fácil de verificar**: Verificar un nonce solo requiere un cálculo
3. **Costo computacional**: Atacar la red requeriría más del 51% del poder computacional

### Enlace Criptográfico

Cada bloque incluye el hash del anterior:

```
Bloque 1 → Hash: 0000a1b2c3...
Bloque 2 → Previous Hash: 0000a1b2c3... → Hash: 0000d4e5f6...
Bloque 3 → Previous Hash: 0000d4e5f6... → Hash: 0000g7h8i9...
```

Si alguien modifica el Bloque 1:

- Su hash cambia a `0000xyz123...`
- El Bloque 2 sigue apuntando a `0000a1b2c3...` (inválido)
- La cadena completa se invalida

---

## 🤝 Contribuciones

Este es un proyecto educativo. Si quieres extenderlo:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa mejoras
4. Envía un Pull Request

### Ideas de Mejoras

- Implementar wallets con claves públicas/privadas (ECDSA)
- Agregar persistencia con SQLite/MongoDB
- Implementar Merkle Trees para transacciones
- Crear un frontend web interactivo
- Implementar smart contracts básicos
- Optimizar el algoritmo PoW

---

## 📖 Recursos y Referencias

- [Bitcoin Whitepaper - Satoshi Nakamoto](https://bitcoin.org/bitcoin.pdf)
- [Documentación de Flask](https://flask.palletsprojects.com/)
- [SHA-256 Cryptographic Hash](https://en.wikipedia.org/wiki/SHA-2)
- [Proof of Work Explained](https://en.bitcoin.it/wiki/Proof_of_work)

---

## 📄 Licencia

Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

**Ariel Duarte**  
Proyecto de aprendizaje: Recklion Coin Blockchain

---

## 🎓 Aprendizajes Clave

Este proyecto enseña:

1. ✅ Cómo funciona una blockchain a nivel fundamental
2. ✅ Implementación de Proof of Work
3. ✅ Hashing criptográfico y seguridad
4. ✅ Descentralización y consenso distribuido
5. ✅ Creación de APIs REST con Flask
6. ✅ Arquitectura de criptomonedas como Bitcoin

---

**¡Disfruta explorando el mundo de las blockchains! 🚀**
