from receipt import get_receipt
from flask import Flask, request

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def create_page():
    if request.method == "POST":
        plate_number = request.form["plate_number"]
        date = request.form["date"]
        last_4_digits = request.form["last_4_digits"]
        if plate_number is not None and date is not None and last_4_digits is not None:
            result = get_receipt(plate_number, date, last_4_digits)
            return '''
                <html>
                    <body>
                    <center>
                        <p style="font-size:20px;font-family:verdana">The search result is:</p>
                        <br>
                        <pre>{result}</pre>
                        <br>
                        <p><a href="/">Click here to search again</a>
                    </center>
                    </body>
                </html>
            '''.format(result=result)
    return '''
        <html>
            <body>
            <center>
                <p style="font-size:20px;font-family:verdana">Enter your data:</p>
                <form method="post" action=".">
                    <label for="plate_number">Enter the plate number:</label>
                    <p style="font-family:verdana"><input name="plate_number" /></p>
                    <label for="date">Enter the date (dd-mm-yyyy):</label>
                    <p style="font-family:verdana"><input name="date" /></p>
                    <label for="last_4_digits">Enter the last 4 digits of the credit card:</label>
                    <p style="font-family:verdana"><input name="last_4_digits" /></p>
                    <p><input type="submit" value="Get receipt" /></p>
                <form>
            </center>
            </body>
        </html>
    '''
