<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" indent="yes" encoding="UTF-8"/>

  <xsl:template match="/">
    <html>
      <head>
        <meta charset="utf-8"/>
        <title>Researchers Overview</title>

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

          .researcher {
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

        <h1>Researcher Profile</h1>

        <xsl:for-each select="//researcher">

          <div class="researcher">

            <div class="header-block">
              <span class="header-id">
                <xsl:value-of select="researcher_id"/>
              </span>
              — <strong><xsl:value-of select="name"/></strong>

              <p style="margin-top:6px;">
                <a href="mailto:{email}"><xsl:value-of select="email"/></a>
              </p>
            </div>

            <h2>Affiliation</h2>
            <table>
              <tr>
                <th>Institution</th>
                <td><xsl:value-of select="affiliation/institution"/></td>
              </tr>
              <tr>
                <th>Department</th>
                <td><xsl:value-of select="affiliation/department"/></td>
              </tr>
              <tr>
                <th>Research Group</th>
                <td><xsl:value-of select="affiliation/research_group/name"/></td>
              </tr>
              <tr>
                <th>Principal Investigator</th>
                <td><xsl:value-of select="affiliation/research_group/pi"/></td>
              </tr>
            </table>

            <h2>Funding</h2>

            <table>
              <tr><th>Total Budget</th><td><xsl:value-of select="affiliation/research_group/funding/total_budget"/> €</td></tr>
            </table>

            <h3 style="margin-top:10px;">Grants</h3>
            <ul>
              <xsl:for-each select="affiliation/research_group/funding/grants/grant">
                <li>
                  <strong><xsl:value-of select="agency"/></strong> — 
                  Project <xsl:value-of select="project_id"/>  
                  (Amount: <xsl:value-of select="amount"/> €, Period: <xsl:value-of select="period"/>)
                </li>
              </xsl:for-each>
            </ul>

            <h2>Expertise</h2>

            <h3>Research Areas</h3>
            <ul>
              <xsl:for-each select="expertise/areas/area">
                <li><xsl:value-of select="."/></li>
              </xsl:for-each>
            </ul>

            <h3>Computational Skills</h3>
            <ul>
              <xsl:for-each select="expertise/skills/computational/language">
                <li><xsl:value-of select="."/></li>
              </xsl:for-each>
            </ul>

            <h3>Metrics</h3>
            <table>
              <tr><th>H-index</th><td><xsl:value-of select="expertise/skills/metrics/h_index"/></td></tr>
              <tr><th>Total Citations</th><td><xsl:value-of select="expertise/skills/metrics/total_citations"/></td></tr>
              <tr><th>Publications Count</th><td><xsl:value-of select="expertise/skills/metrics/publications_count"/></td></tr>
            </table>

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
