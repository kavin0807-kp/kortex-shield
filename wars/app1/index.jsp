<%@ page contentType="text/html;charset=UTF-8" language="java" %>
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <title>App1 - Corporate Directory</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap');

            body {
                font-family: 'Lato', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f4f6f9;
                margin: 0;
            }

            .container {
                width: 500px;
                padding: 40px;
                background: #fff;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
                border-radius: 8px;
                text-align: center;
            }

            h1 {
                color: #2c3e50;
            }

            p {
                color: #7f8c8d;
                margin-bottom: 30px;
            }

            .form-group {
                margin-bottom: 20px;
                text-align: left;
            }

            input[type="text"] {
                width: 100%;
                padding: 12px;
                border: 1px solid #dfe6e9;
                border-radius: 4px;
                font-size: 16px;
                box-sizing: border-box;
            }

            .btn {
                background-color: #3498db;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                width: 100%;
            }

            .results {
                margin-top: 20px;
                padding: 15px;
                background: #ecf0f1;
                border-radius: 4px;
                text-align: left;
                color: #34495e;
                display: none;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>Corporate Directory</h1>
            <p>Search for an employee by name or department.</p>
            <form id="searchForm" action="/" method="GET">
                <div class="form-group"><input type="text" id="employee_name" name="employee_name"
                        placeholder="Employee Name"></div>
                <div class="form-group"><input type="text" id="department" name="department" placeholder="Department">
                </div>
                <button type="submit" class="btn">Search Directory</button>
            </form>
            <div id="results" class="results"></div>
        </div>
        <script>
            document.getElementById('searchForm').addEventListener('submit', function (e) {
                e.preventDefault();
                const name = document.getElementById('employee_name').value || 'any';
                const dept = document.getElementById('department').value || 'any';
                const resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = `Searching for employee: <strong>${name}</strong> in department: <strong>${dept}</strong>...<br/>(This is a demo. No real search is performed.)`;
                resultsDiv.style.display = 'block';
            });
        </script>
    </body>

    </html>