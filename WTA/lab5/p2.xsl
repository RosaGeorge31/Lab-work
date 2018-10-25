<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h2>All Concert Ad Information</h2>
 
   
  <table border="0" cellspacing="5" cellpadding="5">
     <tr>
      <th>Band Name</th>
      <th>Venue Name</th>
      <th>Venue Address</th>
      <th>Venue Contact</th>
      <th>Dates</th>
      <th>Genre</th>
      <th>Ticket price</th>
      <th>Ticket type</th>
      <th>Discount</th> 
    </tr>

    <xsl:for-each select="concert_tickets/ad">
       <xsl:sort select="Band_name"/>
      <xsl:if test="Ticket_price &lt; 100">
        <xsl:if test="Venue_info/Address='Mangalore'">
          <xsl:if test="month='April'">
        <tr>
          <td><xsl:value-of select="Band_name"/></td>
          <td><xsl:value-of select="Venue_info/Name"/></td>
          <td><xsl:value-of select="Venue_info/Address"/></td>
          <td><xsl:value-of select="Venue_info/Contact_no"/></td>
          <td><xsl:value-of select="date_time"/></td>
          <td><xsl:value-of select="Genre"/></td>
          <td><xsl:value-of select="Ticket_price"/></td>
          <td><xsl:value-of select="Ticket_type"/></td>
          <td><xsl:value-of select="Discounts"/></td>
        </tr>
      </xsl:if>
      </xsl:if>
      </xsl:if>
    
       <xsl:if test="Discounts!='NA'">
        <tr>
          <td bgcolor="green;"><xsl:value-of select="Band_name"/></td>
          <td bgcolor="green;"><xsl:value-of select="Venue_info/Name"/></td>
          <td bgcolor="green;"><xsl:value-of select="Venue_info/Address"/></td>
          <td bgcolor="green;"><xsl:value-of select="Venue_info/Contact_no"/></td>
          <td bgcolor="green;"><xsl:value-of select="date_time"/></td>
          <td bgcolor="green;"><xsl:value-of select="Genre"/></td>
         <td bgcolor="green;"><xsl:value-of select="Ticket_price"/></td>
          <td bgcolor="green;"><xsl:value-of select="Ticket_type"/></td>
          <td bgcolor="green;"><xsl:value-of select="Discounts"/></td>
        </tr>
      </xsl:if>
      </xsl:for-each>
  </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet> 
