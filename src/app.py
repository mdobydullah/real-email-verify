import json

from flask import Flask, jsonify, request, render_template
from flask_caching import Cache  # Import Cache from flask_caching module
import re
import smtplib
import dns.resolver

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
# Set the configuration variables to the flask application
app.config.from_object('config.Config')
cache = Cache(app)  # Initialize Cache

# index route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        toEmail = request.form['email']

        response = verifyEmail('', toEmail)
        return render_template('index.html', data=response, email=toEmail)
    else:
        return render_template('index.html', email='')

# api route
@app.route('/api/verify')
def api_verify():
    fromEmail = request.args.get('from')
    toEmail = request.args.get('email')

    response = verifyEmail(fromEmail, toEmail)
    return json.dumps(response)

# email verify function
def verifyEmail(fromEmail, toEmail):
    try:
        # Address used for SMTP MAIL FROM command
        if fromEmail:
            fromAddress = fromEmail
        else:
            fromAddress = 'noreply@shouts.dev'

        # Email address to verify
        addressToVerify = toEmail
        if addressToVerify == None:
            return {
                "success": False,
                "message": str('Please enter an email to verify!')
            }

        # Simple Regex for syntax checking
        regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

        # Syntax check
        match = re.match(regex, addressToVerify)
        if match == None:
            return {
                "success": False,
                "message": str('Email syntax is bad!!')
            }

        # Get domain for DNS lookup
        splitAddress = addressToVerify.split('@')
        domain = str(splitAddress[1])

        # MX record lookup
        mxRecord = cache.get(domain)
        if mxRecord is None:
            records = dns.resolver.resolve(domain, 'MX')
            mxRecord = records[0].exchange
            mxRecord = str(mxRecord)

            mxCached = False
            cache.set(domain, mxRecord, timeout=1440 * 60)
        else:
            mxCached = True

        # SMTP lib setup (use debug level for full output)
        server = smtplib.SMTP()
        server.set_debuglevel(0)

        # SMTP Conversation
        server.connect(mxRecord)
        server.helo(server.local_hostname)  ### server.local_hostname(Get local server hostname)
        server.mail(fromAddress)
        code, message = server.rcpt(str(addressToVerify))
        server.quit()

        # Assume SMTP response 250 is success
        if code == 250:
            emailAddressIsValid = True
        else:
            emailAddressIsValid = False

        # Return response
        return {
            "success": emailAddressIsValid,
            "send_from": fromAddress,
            "send_to": addressToVerify,
            "domain": domain,
            "mx_cached": mxCached,
            "mx_record": mxRecord,
            "response_code": code,
            "message": str(message),
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
