<%@ page contentType="text/html;charset=UTF-8" language="java" %>
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <title>App3 - System Diagnostics</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');

            body {
                font-family: 'Roboto Mono', monospace;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #1a1a1a;
                color: #00ff7f;
                margin: 0;
            }

            .terminal {
                width: 700px;
                height: 400px;
                background: #0d0d0d;
                border: 1px solid #00ff7f;
                border-radius: 5px;
                padding: 20px;
                box-shadow: 0 0 15px rgba(0, 255, 127, 0.2);
                display: flex;
                flex-direction: column;
            }

            .header {
                margin-bottom: 20px;
            }

            .header h1 {
                font-size: 24px;
                text-shadow: 0 0 5px #00ff7f;
            }

            .output {
                flex-grow: 1;
                overflow-y: auto;
                margin-bottom: 20px;
            }

            .output p {
                margin: 0 0 5px 0;
            }

            .prompt {
                display: flex;
                align-items: center;
            }

            .prompt label {
                margin-right: 10px;
            }

            .prompt-input {
                flex-grow: 1;
                background: transparent;
                border: none;
                color: #00ff7f;
                font-size: 16px;
                outline: none;
            }

            .run-btn {
                background: #00ff7f;
                color: #0d0d0d;
                border: none;
                padding: 10px 15px;
                font-family: inherit;
                cursor: pointer;
                margin-left: 15px;
            }
        </style>
    </head>

    <body>
        <div class="terminal">
            <div class="header">
                <h1>KORTEX DIAGNOSTICS v1.0</h1>
            </div>
            <div class="output" id="output">
                <p>> Ready for input...</p>
            </div>
            <form id="commandForm" action="/?app=app3" method="POST">
                <div class="prompt">
                    <label for="command">CMD:</label>
                    <input type="text" id="command" name="command" class="prompt-input" autocomplete="off" autofocus>
                    <button type="submit" class="run-btn">EXECUTE</button>
                </div>
            </form>
        </div>
        <script>
            const form = document.getElementById('commandForm'), input = document.getElementById('command'), output = document.getElementById('output');
            form.addEventListener('submit', function (e) {
                e.preventDefault(); const cmd = input.value; if (!cmd) return;
                const p = document.createElement('p'); p.innerHTML = `> Executing: <strong>${cmd}</strong>`;
                output.appendChild(p); input.value = '';
                const responses = ["Checking network...", "Pinging target...", "Packet sent.", "Packet received.", "Status: OK.", "Done."];
                let i = 0; const interval = setInterval(() => {
                    if (i < responses.length) {
                        const resp = document.createElement('p'); resp.textContent = `  ${responses[i]}`;
                        output.appendChild(resp); output.scrollTop = output.scrollHeight; i++;
                    } else { clearInterval(interval); }
                }, 300);
            });
        </script>
    </body>

    </html>