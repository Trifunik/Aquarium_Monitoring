
def web_page(HOUR_ON, MIN_ON, HOUR_OFF, MIN_OFF):
  
  
  html = """<html>
<head>
  <title>ESP Web Server</title>
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
      font-size: 3rem;
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
  <p><a href="/?hour_on_plus"><button class="button button_on">+</button></a> <a href="/?min_on_plus"><button class="button button_on">+</button></a></p>
  <p>""" + HOUR_ON +""":"""+ MIN_ON + """</p>
  <p><a href="/?hour_on_minus"><button class="button button_on">-</button></a> <a href="/?min_on_min"><button class="button button_on">-</button></a></p> 
  <p><a href="/?hour_off_plus"><button class="button button_off">+</button></a> <a href="/?min_off_plus"><button class="button button_off">+</button></a></p>
  <p>""" + HOUR_OFF +""":"""+ MIN_OFF + """</p>
  <p><a href="/?hour_off_minus"><button class="button button_off">-</button></a> <a href="/?min_off_min"><button class="button button_off">-</button></a></p>


</body>

</html>"""

  return html


#
