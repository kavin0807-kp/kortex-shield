<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head><title>Kortex Demo App2</title></head>
<body>
<h1>Kortex Demo App2 (Reflected XSS demo)</h1>
<form action="reflected-xss.jsp" method="get">
  Message: <input type="text" name="msg" value="hello"/><br/>
  <input type="submit" value="Echo"/>
</form>
</body>
</html>
