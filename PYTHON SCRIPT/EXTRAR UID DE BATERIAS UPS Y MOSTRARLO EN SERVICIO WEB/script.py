from flask import Flask, render_template
from pysnmp.hlapi import *
import time

app = Flask(__name__)

@app.route('/')
def battery_state():
    state = ''
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('apc', mpModel=0),
               UdpTransportTarget(('192.168.1.10', 161), timeout=5, retries=2),
               ContextData(),
               ObjectType(ObjectIdentity('.1.3.6.1.4.1.318.1.1.1.2.2.1.0'))) ##debe cambiar el uid por la de su bateria
    )
    if errorIndication:
        state = 'Error: ' + errorIndication
    elif errorStatus:
        state = 'Error: ' + str(errorStatus)
    else:
        state = varBinds[0][1]

    return render_template('index.html', state=state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
