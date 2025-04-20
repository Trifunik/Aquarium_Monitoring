
def web_page(global_dict):
	if global_dict["next_state"] == "ON":
		button_state = "<p><a href=\"/?light=on\"><button class=\"button button_on\">ON</button></a></p>"
	else:
		button_state = "<p><a href=\"/?light=off\"><button class=\"button button_off\">OFF</button></a></p>"
		
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
      background-color: #eeeeee;
      color: #2c3e50;
    }

    .button_off {
      background-color: #2c3e50;
      color: #ffffff;
    }
  </style>
</head>

<body>
    <p>Temp: <strong>""" + global_dict["temp"] + """</strong></p>
    <form enctype="text/plain" action="/TIME_INPUT">
        <p><label class="clabel" for="on-time">ON-Time:</label>
        <input type="time" id="onTime" name="onTime" value="""+global_dict["HOUR_ON"]+":"+global_dict["MIN_ON"]+""" /></p>
        <p><label class="clabel" for="off-time">  OFF-Time:</label>
        <input type="time" id="offTime" name="offTime" value="""+global_dict["HOUR_OFF"]+":"+global_dict["MIN_OFF"]+""" /></p>
        <p><input class="clabel" type="submit" value="Submit"></p>
    </form>

    """ + button_state + """
    
</body>

</html>"""

	return html