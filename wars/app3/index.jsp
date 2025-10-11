<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head><title>Kortex Demo App3</title></head>
<body>
<h1>Kortex Demo App3 (Insecure file upload demo)</h1>
<form method="post" action="upload.jsp" enctype="multipart/form-data">
  Upload file: <input type="file" name="file"/><br/>
  <input type="submit" value="Upload"/>
</form>
</body>
</html>
