<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head><title>Kortex Demo App1</title></head>
<body>
<h1>Welcome to Kortex Demo App1 (SQLi vulnerable)</h1>
<form action="vulnerable-sqli.jsp" method="get">
  User ID: <input type="text" name="uid" value="1"/><br/>
  <input type="submit" value="Lookup"/>
</form>
</body>
</html>
