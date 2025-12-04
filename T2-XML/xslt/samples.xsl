<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" indent="yes" encoding="UTF-8"/>

    <!-- Raíz -->
    <xsl:template match="/">
        <html>
            <head>
                <title>Samples</title>
                <meta charset="UTF-8"/>
                <style>
                    table { border-collapse: collapse; width: 100%; margin-bottom: 1.5em; }
                    th, td { border: 1px solid #ccc; padding: 4px 6px; vertical-align: top; }
                    th { background-color: #f0f0f0; }
                    h1 { font-family: sans-serif; }
                    .subtable { width: 100%; font-size: 0.9em; }
                </style>
            </head>
            <body>
                <h1>Listado de muestras</h1>
                <table>
                    <tr>
                        <th>Sample ID</th>
                        <th>Fuente</th>
                        <th>Organismo</th>
                        <th>Paciente</th>
                        <th>Diagnóstico / Estadio</th>
                        <th>Tratamiento</th>
                        <th>Biomarcadores</th>
                        <th>Procesado / RNA</th>
                        <th>Experimentos</th>
                        <th>Genes detectados</th>
                    </tr>
                    <xsl:apply-templates select="samples/sample"/>
                </table>
            </body>
        </html>
    </xsl:template>

    <!-- Cada sample -->
    <xsl:template match="sample">
        <tr>
            <td><xsl:value-of select="sample_id"/></td>
            <td><xsl:value-of select="source"/></td>
            <td><xsl:value-of select="organism"/></td>

            <!-- Paciente -->
            <td><xsl:value-of select="clinical_data/patient_id"/></td>

            <!-- Diagnóstico y estadio -->
            <td>
                <div><strong>Dx:</strong> <xsl:value-of select="clinical_data/diagnosis"/></div>
                <div><strong>Stage:</strong> <xsl:value-of select="clinical_data/stage"/></div>
            </td>

            <!-- Tratamiento -->
            <td>
                <div><strong>Terapia:</strong> <xsl:value-of select="clinical_data/treatment/therapy_type"/></div>
                <div><strong>Fármacos:</strong></div>
                <ul>
                    <xsl:for-each select="clinical_data/treatment/drugs/drug">
                        <li><xsl:value-of select="."/></li>
                    </xsl:for-each>
                </ul>
                <div><strong>Respuesta:</strong> <xsl:value-of select="clinical_data/treatment/response/status"/></div>
                <div><strong>Fecha eval:</strong> <xsl:value-of select="clinical_data/treatment/response/evaluation_date"/></div>
            </td>

            <!-- Biomarcadores -->
            <td>
                <ul>
                    <li>Ki67: <xsl:value-of select="clinical_data/treatment/response/biomarkers/ki67"/></li>
                    <li>HER2: <xsl:value-of select="clinical_data/treatment/response/biomarkers/her2"/></li>
                </ul>
            </td>

            <!-- Procesado / RNA -->
            <td>
                <div><strong>Fecha colección:</strong> <xsl:value-of select="processing/collection_date"/></div>
                <div><strong>Almacenamiento:</strong> <xsl:value-of select="processing/storage_conditions"/></div>
                <hr/>
                <div><strong>Método RNA:</strong> <xsl:value-of select="processing/rna_extraction/method"/></div>
                <div><strong>RIN:</strong> <xsl:value-of select="processing/rna_extraction/rin_score"/></div>
                <div><strong>Concentración:</strong> <xsl:value-of select="processing/rna_extraction/concentration"/></div>
                <div><strong>A260/280:</strong> <xsl:value-of select="processing/rna_extraction/quality_metrics/a260_280"/></div>
                <div><strong>A260/230:</strong> <xsl:value-of select="processing/rna_extraction/quality_metrics/a260_230"/></div>
                <div><strong>Integridad:</strong> <xsl:value-of select="processing/rna_extraction/quality_metrics/integrity_assessment"/></div>
            </td>

            <!-- Experimentos -->
            <td>
                <ul>
                    <xsl:for-each select="experiment_ids/experiment_id">
                        <li><xsl:value-of select="."/></li>
                    </xsl:for-each>
                </ul>
            </td>

            <!-- Genes detectados -->
            <td>
                <ul>
                    <xsl:for-each select="genes_detected/gene_id">
                        <li><xsl:value-of select="."/></li>
                    </xsl:for-each>
                </ul>
            </td>
        </tr>
    </xsl:template>

</xsl:stylesheet>
