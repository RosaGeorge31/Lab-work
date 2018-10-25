<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h2>All Concert Ad Information</h2>
  <table border="1">
    <tr>
      <th>Name</th>
      <th>Genre</th>
      <th>Place</th>	
    </tr>

    <xsl:for-each select="concert_tickets/ad">
    <tr>
      <td><xsl:value-of select="Band_name"/></td>
      <xsl:if test= "Genre='Pop'" >
      <td style= "color:red;" ><xsl:value-of select="Genre"/></td>
      </xsl:if>
      <xsl:if test= "Genre='Classical'" >
      <td style="color:blue;"><xsl:value-of select="Genre"/></td>
      </xsl:if> 
      <xsl:if test= "Genre='Instrumental'" >
      <td style="color:green;"><xsl:value-of select="Genre"/></td>
      </xsl:if>
      <td><xsl:value-of select="Address/Venue_info"/></td>
    </tr>
    </xsl:for-each>
  </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet> 
