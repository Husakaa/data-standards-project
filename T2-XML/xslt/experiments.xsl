<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" indent="yes" encoding="UTF-8"/>

  <xsl:template match="/">
    <html>
      <head>
        <meta charset="utf-8"/>
        <title>RNA-Seq Experiments</title>

        <style>
          body {
            font-family: "Inter", Arial, sans-serif;
            margin: 40px;
            background: #f4f6f8;
            color: #222;
          }

          h1 {
            text-align: center;
            font-size: 2.4em;
            color: #1e2a38;
            margin-bottom: 40px;
            letter-spacing: 0.5px;
          }

          .experiment {
            background: white;
            max-width: 1100px;
            margin: 30px auto;
            padding: 35px;
            border-radius: 16px;
            border: 1px solid #e1e5eb;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
          }

          h2 {
            color: #2c6db2;
            border-left: 6px solid #2c6db2;
            padding-left: 12px;
            margin-top: 35px;
            margin-bottom: 15px;
            font-size: 1.4em;
          }

          table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0 20px 0;
          }

          th {
            width: 260px;
            text-align: left;
            padding: 12px;
            background: #f0f4fa;
            font-weight: 600;
          }

          td {
            padding: 12px;
            border-bottom: 1px solid #eee;
          }

          ul {
            margin: 0;
            padding-left: 20px;
          }

          a {
            color: #2a6bb8;
            text-decoration: none;
          }

          a:hover {
            text-decoration: underline;
          }

          .header-block {
            margin-bottom: 25px;
          }

          .header-id {
            font-size: 1.3em;
            font-weight: bold;
            color: #1e2a38;
          }
        </style>
      </head>

      <body>
        <h1>Experiments </h1>

        <xsl:for-each select="//experiment">

          <div class="experiment">

            <div class="header-block">
              <span class="header-id">
                <xsl:value-of select="experiment_id"/>
              </span>
              — <strong><xsl:value-of select="title"/></strong>

              <p style="margin-top:6px;">
                <strong>Type: </strong> <xsl:value-of select="type"/> |
                <strong>Date: </strong> <xsl:value-of select="date"/> |
                <strong>Status </strong> <xsl:value-of select="status"/>
              </p>
            </div>

            <h2>Researcher</h2>

            <xsl:variable name="res_id" select="researcher_id"/>
            <xsl:variable name="res" select="document('../xml/researchers.xml')//researcher[_id = $res_id]"/>

            <p>
              <strong><xsl:value-of select="$res/name"/></strong><br/>
              <a href="mailto:{$res/email}">
                <xsl:value-of select="$res/email"/>
              </a><br/>
              <xsl:value-of select="$res/affiliation/institution"/> —
              <xsl:value-of select="$res/affiliation/department"/>
            </p>

            <h2>Sequencing Methodology</h2>
            <table>
              <tr><th>Platform</th><td><xsl:value-of select="methodology/platform"/></td></tr>
              <tr><th>Library Preparation</th><td><xsl:value-of select="methodology/library_prep"/></td></tr>
              <tr><th>Read Length</th><td><xsl:value-of select="methodology/sequencing_params/read_length"/> bp</td></tr>
              <tr><th>Target Coverage</th><td><xsl:value-of select="methodology/sequencing_params/coverage"/></td></tr>
            </table>

            <h2>Quality Control Metrics</h2>
            <table>
              <tr><th>Q30 Bases</th><td><xsl:value-of select="methodology/sequencing_params/quality_control/q30_percentage"/>%</td></tr>
              <tr><th>Adapter Contamination</th><td><xsl:value-of select="methodology/sequencing_params/quality_control/adapter_contamination"/>%</td></tr>
              <tr><th>Duplication Rate</th><td><xsl:value-of select="methodology/sequencing_params/quality_control/duplication_rate"/>%</td></tr>
            </table>

            <h2>Samples </h2>

            <ul>
              <xsl:for-each select="sample_ids/sample_id">
                <xsl:variable name="sid" select="."/>
                <xsl:variable name="sample" select="document('../xml/samples.xml')//sample[_id = $sid]"/>

                <li>
                  <strong><xsl:value-of select="$sample/sample_id"/></strong>:
                  <xsl:value-of select="$sample/source"/> 
                  <xsl:value-of select="$sample/tissue"/>
                  <xsl:if test="$sample/treatment"> (<xsl:value-of select="$sample/treatment"/>)</xsl:if>
                  <xsl:if test="$sample/condition"> | Condition: <xsl:value-of select="$sample/condition"/></xsl:if>
                </li>
              </xsl:for-each>
            </ul>

            <h2>Linked Publications</h2>

            <xsl:choose>
              <xsl:when test="publication_ids/publication_id">
                <ul>
                  <xsl:for-each select="publication_ids/publication_id">
                    <xsl:variable name="pid" select="."/>
                    <xsl:variable name="pub" select="document('../xml/publications.xml')//publication[_id = $pid]"/>

                    <li>
                      <a href="publications.html#{$pid}">
                        <xsl:value-of select="$pub/title"/>
                      </a>
                      <xsl:if test="$pub/publication_details/year">
                        (<xsl:value-of select="$pub/publication_details/year"/>)
                      </xsl:if>
                    </li>
                  </xsl:for-each>
                </ul>
              </xsl:when>

              <xsl:otherwise>
                <em>No publications available.</em>
              </xsl:otherwise>
            </xsl:choose>

          </div>

        </xsl:for-each>

      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
