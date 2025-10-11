<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
  // INTENTIONAL REFLECTED XSS for detection demonstration only.
  String msg = request.getParameter("msg");
  if (msg == null) msg = "";
%>
<html><body>
<h2>Echo:</h2>
<!-- Intentionally unescaped user input -->
<div>Message: <%= msg %></div>
</body></html>
