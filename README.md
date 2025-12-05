# T1-MongoDB - Base de Datos de Bioinformática

## Descripción del Proyecto

Base de datos MongoDB diseñada para almacenar y gestionar información de experimentos bioinformáticos, incluyendo experimentos de secuenciación (RNA-seq), muestras clínicas, datos genéticos, investigadores y publicaciones científicas.

Este proyecto forma parte de la asignatura de Estándares de Datos en Bioinformática y Salud, implementando una arquitectura de base de datos NoSQL con múltiples colecciones interrelacionadas.

## Estructura del Proyecto

```
T1-MongoDB/
├── data/               # Datos poblados de las colecciones
├── docs/              # Documentación del proyecto
├── schemas/           # Esquemas JSON de las colecciones
│   ├── experiments.json
│   ├── samples.json
│   ├── genes.json
│   ├── researchers.json
│   └── publications.json
└── src/               # Scripts de población y consultas
```

## Arquitectura de la Base de Datos

### Colecciones Principales

La base de datos consta de **5 colecciones interconectadas**:

1. **experiments** - Experimentos de secuenciación y análisis genómico
2. **samples** - Muestras biológicas y datos clínicos
3. **genes** - Información genética y expresión génica
4. **researchers** - Investigadores y grupos de investigación
5. **publications** - Publicaciones científicas y métricas

### Características Técnicas

- Mínimo de **3 colecciones interconectadas** (implementadas 5)
- Mínimo de **3 niveles de anidamiento** por colección (implementados 4)
- **Relaciones entre colecciones** mediante ObjectId
- **Datos realistas** del ámbito bioinformático
- **Validación mediante JSON Schema**

## Relaciones entre Colecciones

```
experiments ←→ samples
     ↓            ↓
researchers   genes
     ↓            ↓
publications ←────┘
```

### Detalle de Relaciones

- **experiments** → researchers (1:1), samples (1:N), publications (N:M)
- **samples** → experiments (N:M), genes (N:M)
- **genes** → samples (N:M), publications (N:M)
- **researchers** → experiments (1:N), publications (N:M)
- **publications** → researchers (N:M), experiments (N:M), genes (N:M)

## Esquema de Colección: Experiments

Cada colección implementa **4 niveles de anidamiento**:

**Nivel 1**: Campos principales del experimento
```javascript
{
  experiment_id: "EXP_001",
  title: "RNA-seq analysis of cancer cells",
  type: "RNA-seq",
  status: "completed"
}
```

**Nivel 2**: Metadata del experimento
```javascript
methodology: {
  platform: "Illumina NovaSeq",
  library_prep: "TruSeq stranded mRNA"
}
```

**Nivel 3**: Parámetros técnicos
```javascript
sequencing_params: {
  read_length: 150,
  coverage: "30X"
}
```

**Nivel 4**: Control de calidad
```javascript
quality_control: {
  q30_percentage: 92.5,
  adapter_contamination: 0.3,
  duplication_rate: 15.2
}
```

## Instalación y Uso

### Prerrequisitos

- MongoDB 6.0 o superior
- Python 3.8+ (para scripts de población)
- MongoDB Compass (opcional, para visualización)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/data-standards-project.git
cd data-standards-project/T1-MongoDB

# Importar esquemas a MongoDB
mongoimport --db bioinformatics --collection experiments --file schemas/experiments.json
```

### Población de Datos

```bash
# Ejecutar script de población automática
python src/populate_db.py

```

## Consultas de Ejemplo

### Se encuentran en la carpeta querys

## 👥 Equipo de Desarrollo

- **Aissa Omar El Hammouti Chachoui**
- **Hugo Salas Calderón**
- **Patricia Rodríguez Lidueña**
- ** Luis Miguel Parrado Navarro**
- **Neja KaŠman**

## Documentación Adicional

- Ver `docs/T1-Explicacion.pdf` para más detalles sobre el diseño
- Ver `schemas/` para los esquemas JSON completos
- Ver `src/` para scripts de población

## Tecnologías Utilizadas

- **MongoDB** - Base de datos NoSQL
- **JSON Schema** - Validación de documentos
- **Python** - Scripts de automatización

## Notas sobre el Desarrollo

Este proyecto fue desarrollado con asistencia de IA Generativa (Claude) para:
- Diseño de esquemas JSON
- Estructura de las colecciones
- Generación de datos realistas
- Optimización de consultas

## Licencia

Este proyecto es material académico de la Universidad de Málaga.

## Contacto

Para dudas o sugerencias sobre el proyecto, contactar a través del repositorio de GitHub.

-------------------------------------------------------------------------------------------------------

# T2-XML - Transformación de Datos Bioinformáticos a Estándares Abiertos

## Descripción del Proyecto

Este proyecto completa la transición del modelo de base de datos MongoDB (JSON) diseñado en **T1-MongoDB** a un conjunto de estándares abiertos y validados (XML, XSD, XSLT).

El objetivo principal es garantizar la interoperabilidad y claridad estructural de los datos bioinformáticos mediante un flujo de trabajo automatizado en Python que transforma la información para su visualización en HTML.

Este proyecto forma parte de la asignatura de Estándares de Datos en Bioinformática y Salud.

## Estructura del Proyecto

```
T2-XML/
├── docs/              # Documentación del proyecto (explicación en PDF)
├── xsd/               # Esquemas XSD de validación
├── xml/               # Documentos XML generados
├── xslt/              # Plantillas XSLT para transformar de XML a HTML
├── html/              # Documentos HTML resultantes
└── src/               # Script de población
```

---

## Arquitectura del Sistema

El flujo de trabajo implementado reproduce y valida la estructura diseñada en la T1:

1. **Diseño de Esquemas XSD**  
   Se definen los tipos de datos, la jerarquía de elementos y las relaciones entre entidades bioinformáticas.  
   Cada XSD describe la estructura esperada del XML equivalente a las colecciones MongoDB.

2. **Generación de XML**  
   A partir del modelo JSON de T1, se generan documentos XML que mantienen la estructura con **cuatro niveles de anidamiento**.

3. **Script Python de Transformación**  
   El script `json_to_xml.py` permite:
   - Conectarse a MongoDB mediante credenciales
   - Leer consultas desde un archivo `.txt`
   - Ejecutarlas usando PyMongo
   - Transformar el resultado JSON a XML válido
   - Validarlo frente a su XSD
   - Aplicar una plantilla XSLT
   - Producir un documento HTML

4. **Transformación XSLT a HTML**  
   Las plantillas permiten visualizar la información en HTML de forma clara, ordenada y legible.

---

## Componentes Técnicos

### Esquemas XSD

Definen:

- Tipos de cada elemento  
- Jerarquía estructural  
- Relaciones entre datos  
- Campos obligatorios y opcionales  

### Documentos XML

Reproducen la estructura de las colecciones de T1:

- experiments  
- samples  
- genes  
- researchers  
- publications  

### Plantillas XSLT

Permiten transformar los XML en páginas HTML mediante reglas de estilo y selección de contenido.

### Script Python (`json_to_xml.py`)

Incluye:

- Uso de `argparse`  
- Gestión de errores  
- Conversión JSON a XML  
- Validación XSD  
- Transformación XSLT  
- Generación de HTML final  

---

## Instalación y Uso

### Prerrequisitos

- Python 3.8+  
- Librerías: `lxml`, `pymongo`  
- Acceso a la base de datos MongoDB creada en T1  

### Ejecución del Script

```bash
python src/json_to_xml.py \
    --db_uri <URI_MONGODB> \
    --query_spec queries/query1.txt \
    --xslt_template xslt/template1.xslt \
    --output_file html/result1.html
```

## 👥 Equipo de Desarrollo

- **Aissa Omar El Hammouti Chachoui**
- **Hugo Salas Calderón**
- **Patricia Rodríguez Lidueña**
- ** Luis Miguel Parrado Navarro**
- **Neja KaŠman**

## Licencia

Este proyecto es material académico de la Universidad de Málaga.

## Contacto

Para dudas o sugerencias sobre el proyecto, contactar a través del repositorio de GitHub.

***

**Universidad de Málaga** - Ingeniería de la Salud  
**Asignatura**: Estándares de Datos en Bioinformática y Salud  
**Curso**: 2024/2025


