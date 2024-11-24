def web_page():
   
  html = """<html>
        <head>
        <title>Aquarium Monitor</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="data:,">
        <style>
            html {
            font-family: Helvetica;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
            }

            h1 {
            padding: 2vh;
            }

            p {
            font-size: 1rem;
            }

            .button {
            display: inline-block;
            border: none;
            border-radius: 4px;
            padding: 8px 20px;
            text-decoration: none;
            font-size: 30px;
            margin: 2px;
            cursor: pointer;
            }

            .button_on {
            background-color: #ffffffb4;
            color: #2c3e50;
            }

            .button_off {
            background-color: #2c3e50;
            color: #ffffff;
            }
        </style>
        </head>

        <body>
            <form enctype="text/plain" action="/WIFI_INPUT">
                <label class="clabel" for="ssid">SSID:</label>
                <input type="text" id="ssidID" name="ssid" value="" placeholder="ssid"><br><br>
                <label class="clabel" for="pwd">PWD:</label>
                <input type="text" id="pwd" name="pwd" value="" placeholder="pwd"><br><br>
                <input class="clabel" type="submit" value="Submit">
            </form>
            <p>Restart after submit!</p>
        </body>

        </html>"""

  return html
