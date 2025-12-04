<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" indent="yes" encoding="UTF-8"/>

    <!-- Raíz -->
    <xsl:template match="/">
        <html>
            <head>
                <title>Genes</title>
                <meta charset="UTF-8"/>
                <style>
                    table { border-collapse: collapse; width: 100%; margin-bottom: 1.5em; }
                    th, td { border: 1px solid #ccc; padding: 4px 6px; vertical-align: top; }
                    th { background-color: #f0f0f0; }
                    h1 { font-family: sans-serif; }
                    h2 { font-family: sans-serif; margin-top: 1.5em; }
                    .subtable { width: 100%; font-size: 0.9em; }
                </style>
            </head>
            <body>
                <h1>Listado de genes</h1>
                <table>
                    <tr>
                        <th>Gene ID</th>
                        <th>Símbolo</th>
                        <th>Nombre</th>
                        <th>Avg TPM</th>
                        <th>Tejidos</th>
                        <th>GO Terms</th>
                        <th>Pathways</th>
                        <th>Interacciones</th>
                        <th>Samples</th>
                        <th>Publicaciones</th>
                    </tr>
                    <xsl:apply-templates select="genes/gene"/>
                </table>
            </body>
        </html>
    </xsl:template>

    <!-- Cada gen -->
    <xsl:template match="gene">
        <tr>
            <td><xsl:value-of select="gene_id"/></td>
            <td><xsl:value-of select="symbol"/></td>
            <td><xsl:value-of select="name"/></td>
            <td><xsl:value-of select="expression_data/avg_tpm"/></td>

            <!-- Tejidos -->
            <td>
                <table class="subtable">
                    <tr>
                        <th>Tejido</th>
                        <th>TPM</th>
                        <th>Normal</th>
                        <th>Tumor</th>
                        <th>Fold change</th>
                        <th>p-value</th>
                        <th>adj p-value</th>
                    </tr>
                    <xsl:for-each select="expression_data/tissues/tissue">
                        <tr>
                            <td><xsl:value-of select="tissue_type"/></td>
                            <td><xsl:value-of select="tpm"/></td>
                            <td><xsl:value-of select="conditions/normal"/></td>
                            <td><xsl:value-of select="conditions/tumor"/></td>
                            <td><xsl:value-of select="conditions/statistics/fold_change"/></td>
                            <td><xsl:value-of select="conditions/statistics/p_value"/></td>
                            <td><xsl:value-of select="conditions/statistics/adjusted_p_value"/></td>
                        </tr>
                    </xsl:for-each>
                </table>
            </td>

            <!-- GO terms -->
            <td>
                <ul>
                    <xsl:for-each select="functional_annotation/go_terms/term">
                        <li><xsl:value-of select="."/></li>
                    </xsl:for-each>
                </ul>
            </td>

            <!-- Pathways -->
            <td>
                <ul>
                    <xsl:for-each select="functional_annotation/pathways/pathway">
                        <li><xsl:value-of select="."/></li>
                    </xsl:for-each>
                </ul>
            </td>

            <!-- Interacciones -->
            <td>
                <strong>Proteínas:</strong>
                <ul>
                    <xsl:for-each select="functional_annotation/interactions/protein_interactions/protein">
                        <li><xsl:value-of select="."/></li>
                    </xsl:for-each>
                </ul>
                <strong>Red:</strong>
                <ul>
                    <li>Degree: <xsl:value-of select="functional_annotation/interactions/network_properties/degree"/></li>
                    <li>Betweenness: <xsl:value-of select="functional_annotation/interactions/network_properties/betweenness"/></li>
                    <li>Clustering: <xsl:value-of select="functional_annotation/interactions/network_properties/clustering_coefficient"/></li>
                </ul>
            </td>

            <!-- Samples -->
            <td>
                <ul>
                    <xsl:for-each select="sample_ids/sample_id">
                        <li><xsl:value-of select="."/></li>
                    </xsl:for-each>
                </ul>
            </td>

            <!-- Publicaciones -->
            <td>
                <ul>
                    <xsl:for-each select="publication_ids/publication_id">
                        <li><xsl:value-of select="."/></li>
                    </xsl:for-each>
                </ul>
            </td>
        </tr>
    </xsl:template>

</xsl:stylesheet>
