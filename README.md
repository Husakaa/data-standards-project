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

---

**Universidad de Málaga** - Ingeniería de la Salud  
**Asignatura**: Estándares de Datos en Bioinformática y Salud  
**Curso**: 2024/2025
