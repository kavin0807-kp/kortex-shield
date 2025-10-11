<%@ page import="java.io.*" %>
<%
  // INTENTIONALLY INSECURE: saves uploads without sanitization
  // For demo only — do not use in production.
  if(request.getMethod().equalsIgnoreCase("POST")) {
    javax.servlet.http.Part part = request.getPart("file");
    if(part != null) {
      String fileName = part.getSubmittedFileName();
      String savePath = application.getRealPath("/") + File.separator + "uploads";
      new File(savePath).mkdirs();
      String dest = savePath + File.separator + fileName;
      part.write(dest);
      out.println("<p>Saved file to: " + dest + "</p>");
    } else {
      out.println("<p>No file uploaded.</p>");
    }
  } else {
    out.println("<p>Use POST to upload.</p>");
  }
%>
