<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" encoding="UTF-8"/>

<xsl:template match="/">
<html>
<head>
<meta charset="utf-8"/>
<title>Scientific Publications</title>
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
  .publication {
    background: white;
    max-width: 1100px;
    margin: 40px auto;
    padding: 40px;
    border-radius: 16px;
    border: 1px solid #e1e5eb;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  }
  h2 {
    color: #2c6db2;
    border-left: 6px solid #2c6db2;
    padding-left: 12px;
    margin: 35px 0 15px 0;
    font-size: 1.4em;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0 25px 0;
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
  .tag {
    display: inline-block;
    background: #e6f0fa;
    color: #1e5a96;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.9em;
    margin: 4px 6px 4px 0;
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
    padding-bottom: 15px;
    border-bottom: 2px solid #f0f4fa;
  }
  .doi-link {
    font-family: monospace;
    background: #f0f4fa;
    padding: 4px 10px;
    border-radius: 6px;
  }
  .geo-link {
    font-family: monospace;
    background: #e8f5e8;
    padding: 6px 12px;
    border-radius: 8px;
  }
  .abstract {
    background: #fafafa;
    padding: 18px;
    border-left: 4px solid #2c6db2;
    border-radius: 8px;
    margin: 20px 0;
    line-height: 1.7;
  }
</style>
</head>
<body>
<h1>Scientific Publications</h1>

<xsl:for-each select="//publication">
<div class="publication" id="{_id}">

  <div class="header-block">
    <strong style="font-size:1.5em;"><xsl:value-of select="title"/></strong>
    <p style="margin-top:8px; color:#555;">
      Journal: <xsl:value-of select="publication_details/journal"/> | 
      Year: <xsl:value-of select="publication_details/year"/> 
      <xsl:if test="pmid"> | PMID: <xsl:value-of select="pmid"/></xsl:if>
      <xsl:if test="doi"> | DOI: <xsl:value-of select="doi"/>
      </xsl:if>
    </p>
  </div>

  <h2>Impact &amp; Reach</h2>
  <table>
    <tr><th>Impact Factor</th><td><xsl:value-of select="publication_details/metrics/impact_factor"/></td></tr>
    <tr><th>Citations</th><td><xsl:value-of select="publication_details/metrics/citations"/></td></tr>
    <tr><th>Attention Score</th><td><xsl:value-of select="publication_details/metrics/altmetrics/attention_score"/></td></tr>
    <tr><th>News mentions</th><td><xsl:value-of select="publication_details/metrics/altmetrics/news_mentions"/></td></tr>
    <tr><th>Twitter mentions</th><td><xsl:value-of select="publication_details/metrics/altmetrics/twitter_mentions"/></td></tr>
  </table>

  <h2>Abstract</h2>
  <div class="abstract">
    <xsl:value-of select="content/abstract"/>
  </div>

  <h2>Keywords</h2>
  <div>
    <xsl:for-each select="content/keywords/keyword">
      <span class="tag"><xsl:value-of select="."/></span>
    </xsl:for-each>
  </div>

  <h2>Data Availability</h2>
  <p>
    <strong>Repositories: </strong> 
    <xsl:for-each select="content/datasets/repositories/repository">
      <xsl:value-of select="."/>
      <xsl:if test="position() != last()">, </xsl:if>
    </xsl:for-each>
  </p>
  <xsl:if test="content/datasets/accessions/geo_series">
    <p>
      <strong>GEO Series: </strong><span class="tag"> <xsl:value-of select="content/datasets/accessions/geo_series"/></span>
    </p>
  </xsl:if>

  <h2>Researchers</h2>
  <p>
    <xsl:for-each select="researcher_ids/researcher_id">
      <xsl:variable name="rid" select="."/>
      <xsl:variable name="author" select="document('../xml/researchers.xml')//researcher[_id = $rid]"/>
      <xsl:if test="$author">
        <strong><xsl:value-of select="$author/name"/></strong>
        <xsl:if test="position() != last()">, </xsl:if>
      </xsl:if>
    </xsl:for-each>
  </p>

  <h2>Related Experiments</h2>
  <xsl:choose>
    <xsl:when test="experiment_ids/experiment_id">
      <ul>
        <xsl:for-each select="experiment_ids/experiment_id">
          <xsl:variable name="eid" select="."/>
          <xsl:variable name="exp" select="document('../xml/experiments.xml')//experiment[_id = $eid]"/>
          <li>
            <a href="experiments.html#{$eid}">
              <xsl:value-of select="$exp/experiment_id"/> — <xsl:value-of select="$exp/title"/>
            </a>
          </li>
        </xsl:for-each>
      </ul>
    </xsl:when>
    <xsl:otherwise><em>No experiments linked.</em></xsl:otherwise>
  </xsl:choose>

  <h2>Associated Genes</h2>
  <xsl:choose>
    <xsl:when test="gene_ids/gene_id">
      <div style="display: flex; flex-wrap: wrap; gap: 12px;">
        <xsl:for-each select="gene_ids/gene_id">
          <xsl:variable name="gid" select="."/>
          <xsl:variable name="gene" select="document('../xml/genes.xml')//gene[_id = $gid]"/>
          <xsl:if test="$gene">
            <div class="tag" style="background:#e8f4ff; font-weight:600; padding:8px 14px; border-radius:12px;">
              <strong><xsl:value-of select="$gene/symbol"/></strong>
              <span style="margin-left:6px; color:#555; font-weight:normal;">
                (<xsl:value-of select="$gene/name"/>)
              </span>
            </div>
          </xsl:if>
        </xsl:for-each>
      </div>
    </xsl:when>
    <xsl:otherwise>
      <em>No genes associated with this publication.</em>
    </xsl:otherwise>
  </xsl:choose>

</div>
</xsl:for-each>

</body>
</html>
</xsl:template>
</xsl:stylesheet>