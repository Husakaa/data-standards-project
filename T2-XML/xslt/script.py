import lxml.etree as ET

dom = ET.parse("../xml/publications.xml")
xslt = ET.parse("publications.xsl")
transform = ET.XSLT(xslt)
newdom = transform(dom)
print(newdom)

f = open("../html/publications.html", "w",encoding='utf-8')
f.write(str(newdom))
f.close()