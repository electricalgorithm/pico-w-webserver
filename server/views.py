def home_page(temperature, led_state, rtc_time):
    return str(f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title> Pico W Demo Server!</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
  </head>
  <body>
    <section class="section">
      <div class="container">
        <h1 class="title">Pico W Server Demo</h1>
        <p class="subtitle">This server lives on an <strong>RP2040</strong> microcontroller!</p>
    
    <div class="columns">
        <div class="column is-two-fifths">
          <div class="card">
            <header class="card-header">
              <p class="card-header-title">Onboard LED State</p>
            </header>
            <footer class="card-footer">
              <a href="/enable" class="card-footer-item">Activate</a>
              <a href="/disable" class="card-footer-item">Deactivate</a>
            </footer>
          </div>
        </div>
      
        <div class="column is-two-fifths">
          <article class="message is-info">
            <div class="message-header">
              <p>Dashboard</p>
            </div>
            <div class="message-body">
              - Temperature is {temperature} Celcius degree.
              <br>- Onboard led is {led_state}
              <br>- Current time on RTC is {rtc_time}
            </div>
          </article>
        </div>
      </div>
        
        </div>
    </section>
    <footer class="footer">
  <div class="content has-text-centered">
    <p>
      <strong>Pico W Server Demo</strong> by <a href="https://github.com/electricalgorithm">@electricalgorithm</a>. The source code is licensed <a href="http://opensource.org/licenses/mit-license.php">MIT</a>.
    </p>
  </div>
</footer>
  </body>
</html>
""")
