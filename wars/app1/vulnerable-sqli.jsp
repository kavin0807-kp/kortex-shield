<%@ page import="java.sql.*" %>
<%
  // INTENTIONALLY VULNERABLE: vulnerable to SQL injection for demonstration only.
  // DO NOT deploy to production.
  String uid = request.getParameter("uid");
  if(uid == null) uid = "1";

  // An embedded H2 memory DB could be used; for demo we show the vulnerable pattern.
  // In a real demo deployment, configure a local DB and teach detection rather than exploitation.
  out.println("<h2>Lookup result for: " + uid + "</h2>");
  // Demonstrative pseudo-code (no active DB connection):
  out.println("<pre>SELECT * FROM users WHERE id = '" + uid + "';</pre>");
%>
