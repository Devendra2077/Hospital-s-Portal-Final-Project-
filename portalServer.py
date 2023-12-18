from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
from portalDatabase import Database
import cgi

class HospitalPortalHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args):
        self.database = Database()
        BaseHTTPRequestHandler.__init__(self, *args)
    
    def do_POST(self):
        try:
            if self.path == '/addPatient':
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                patient_name = form.getvalue("patient_name")
                age = int(form.getvalue("patient_age"))
                admission_date = form.getvalue("admission_date")
                discharge_date = form.getvalue("discharge_date")
                
                '''
                    Example call: self.database.addPatient(patient_name, age, admission_date,discharge_date)
                '''
                #Calls Database Method for new patients 
                self.database.addPatient(patient_name, age, admission_date, discharge_date)
                print("Patient added:",patient_name, age, admission_date)
                
                self.wfile.write(b"<html><head><title> Hospital Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addPatient'>Add Patient</a>|\
                                  <a href='/scheduleAppointment'>Schedule Appointment</a>|\
                                  <a href='/viewPatients'>View Patients</a>|\
                                  <a href='/dischargePatient'>Discharge Patient</a></div>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Patient has been added</h3>")
                self.wfile.write(b"<div><a href='/addPatient'>Add Another Patient</a></div>")
                self.wfile.write(b"</center></body></html>")
                
            if self.path == '/scheduleAppointment':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                patient_id = int(form.getvalue("patient_id"))
                doctor_id = int(form.getvalue("doctor_id"))
                appointment_date = form.getvalue("appointment_date")
                appointment_time = float(form.getvalue("appointment_time"))

                #Calls Database Method for new appointments
                self.database.scheduleAppointment(patient_id, doctor_id, appointment_date, appointment_time)
                print("Appointment scheduled:", patient_id, doctor_id, appointment_date, appointment_time)

                self.wfile.write(b"<html><head><title> Hospital Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addPatient'>Add Patient</a>|\
                                  <a href='/scheduleAppointment'>Schedule Appointment</a>|\
                                  <a href='/viewPatients'>View Patients</a>|\
                                  <a href='/dischargePatient'>Discharge Patient</a></div>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Appointment Scheduled</h3>")
                self.wfile.write(b"<div><a href='/scheduleAppointment'>Schedule Another Appointment</a></div>")
                self.wfile.write(b"</center></body></html>")

            if self.path == '/dischargePatient':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                patient_id = int(form.getvalue("patient_id"))
                discharge_date = form.getvalue("discharge_date")

                #Calls Database Method to discharge patient
                self.database.dischargePatient(patient_id, discharge_date)
                print("Patient discharged:", patient_id, discharge_date)

                self.wfile.write(b"<html><head><title> Hospital Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addPatient'>Add Patient</a>|\
                                  <a href='/scheduleAppointment'>Schedule Appointment</a>|\
                                  <a href='/viewPatients'>View Patients</a>|\
                                  <a href='/dischargePatient'>Discharge Patient</a></div>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Patient Discharged</h3>")
                self.wfile.write(b"<div><a href='/dischargePatient'>Discharge Another Patient</a></div>")
                self.wfile.write(b"</center></body></html>")
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

        return
    
    def do_GET(self):
        
        try:
            # I have implemented for you the getAllPatients
            if self.path == '/':
                data=[]
                records = self.database.getAllPatients()
                print(records)
                data=records
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Hospital's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addPatient'>Add Patient</a>|\
                                  <a href='/scheduleAppointment'>Schedule Appointment</a>|\
                                  <a href='/viewAppointments'>View Appointments</a>|\
                                  <a href='/dischargePatient'>Discharge Patient</a></div>")
                self.wfile.write(b"<hr><h2>All Patients</h2>")
                self.wfile.write(b"<table border=2> \
                                    <tr><th> Patient ID </th>\
                                        <th> Patient Name</th>\
                                        <th> Age </th>\
                                        <th> Admission Date </th>\
                                        <th> Discharge Date </th></tr>")
                for row in data:
                    self.wfile.write(b' <tr> <td>')
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[1]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[2]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[3]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[4]).encode())
                    self.wfile.write(b'</td></tr>')
                
                self.wfile.write(b"</table></center>")
                self.wfile.write(b"</body></html>")
                return
            ##addPatient Implemented : complete Code in do_Post /addPatient, Read comment in do_Post
            if self.path == '/addPatient':
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Hospital's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addPatient'>Add Patient</a>|\
                                  <a href='/scheduleAppointment'>Schedule Appointment</a>|\
                                  <a href='/viewAppointments'>View Appointments</a>|\
                                  <a href='/dischargePatient'>Discharge Patient</a></div>")
                self.wfile.write(b"<hr><h2>Add New Patient</h2>")

                self.wfile.write(b"<form action='/addPatient' method='post'>")
                self.wfile.write(b'<label for="patient_name">Patient Name:</label>\
                      <input type="text" id="patient_name" name="patient_name"/><br><br>\
                      <label for="patient_age">Age:</label>\
                      <input type="number" id="patient_age" name="patient_age"><br><br>\
                      <label for="admission_date">Admission Date:</label>\
                      <input type="date"id="admission_date" name="admission_date"><br><br>\
                      <label for="discharge_date">Discharge Date:</label>\
                      <input type="date"id="discharge_date" name="discharge_date"><br><br>\
                      <input type="submit" value="Submit">\
                      </form>')
                
                self.wfile.write(b"</center></body></html>")
                return
            
            if self.path == '/scheduleAppointment':
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Hospital's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addPatient'>Add Patient</a>|\
                                  <a href='/scheduleAppointment'>Schedule Appointment</a>|\
                                  <a href='/viewAppointments'>View Appointments</a>|\
                                  <a href='/dischargePatient'>Discharge Patient</a></div>")
                self.wfile.write(b"<hr><h2>Schedule Appointiment</h2>")

                #Code added for form to scheduling appointment
                self.wfile.write(b"<form action='/scheduleAppointment' method='post'>")
                self.wfile.write(b'<label for="patient_id">Patient ID:</label>\
                      <input type="number" id="patient_id" name="patient_id"/><br><br>\
                      <label for="doctor_id">Doctor ID:</label>\
                      <input type="number" id="doctor_id" name="doctor_id"><br><br>\
                      <label for="appointment_date">Appointment Date:</label>\
                      <input type="date"id="appointment_date" name="appointment_date"><br><br>\
                      <label for="appointment_time">Appointment Time:</label>\
                      <input type="number"id="appointment_time" name="appointment_time"><br><br>\
                      <input type="submit" value="Submit">\
                      </form>')
                self.wfile.write(b"</center></body></html>")
                return
                self.database.scheduleAppointment(patient_id, doctor_id, appointment_date, appointment_time)
                print("Appointment scheduled:", patient_id, doctor_id, appointment_date, appointment_time)
                
            if self.path == '/viewAppointment':
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Hospital's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addPatient'>Add Patient</a>|\
                                  <a href='/scheduleAppointment'>Schedule Appointment</a>|\
                                  <a href='/viewAppointments'>View Appointments</a>|\
                                  <a href='/dischargePatient'>Discharge Patient</a></div>")
                self.wfile.write(b"<hr><h2>View Appointiment</h2>")

                #Code added for form to Viewing Appointment
                self.wfile.write(b"</center></body></html>")
                return

            if self.path == '/viewAppointments':
                data = []
                records = self.database.viewAppointments()
                print(records)
                data = records
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Hospital's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addPatient'>Add Patient</a>|\
                                  <a href='/scheduleAppointment'>Schedule Appointment</a>|\
                                  <a href='/viewAppointments'>View Appointments</a>|\
                                  <a href='/dischargePatient'>Discharge Patient</a></div>")
                self.wfile.write(b"<hr><h2>View Appointiments</h2>")

                # Table for View Appointment
                self.wfile.write(b"<table border=2> \
                                    <tr><th> Appointment ID </th>\
                                        <th> Patient ID</th>\
                                        <th> Doctor ID </th>\
                                        <th> Appointment Date </th>\
                                        <th>Appointment Time </th></tr>")
                for row in data:
                        self.wfile.write(b' <tr> <td>')
                        self.wfile.write(str(row[0]).encode())
                        self.wfile.write(b'</td><td>')
                        self.wfile.write(str(row[1]).encode())
                        self.wfile.write(b'</td><td>')
                        self.wfile.write(str(row[2]).encode())
                        self.wfile.write(b'</td><td>')
                        self.wfile.write(str(row[3]).encode())
                        self.wfile.write(b'</td><td>')
                        self.wfile.write(str(row[4]).encode())
                        
                       
                
                self.wfile.write(b"</table></center>")
                self.wfile.write(b"</body></html>")
                return
            if self.path == '/dischargePatient':
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Hospital's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addPatient'>Add Patient</a>|\
                                  <a href='/scheduleAppointment'>Schedule Appointment</a>|\
                                  <a href='/viewAppointments'>View Appointments</a>|\
                                  <a href='/dischargePatient'>Discharge Patient</a></div>")
                self.wfile.write(b"<hr><h2>Discharge Patient</h2>")

                #Form for discharge patient
                self.wfile.write(b"<form action='/dischargePatient' method='post'>")
                self.wfile.write(b'<label for="patient_id">Patient ID:</label>\
                    <input type="number" id="patient_id" name="patient_id"/><br><br>\
                    <label for="discharge_date">Discharge Date:</label>\
                    <input type="date" id="discharge_date" name="discharge_date"><br><br>\
                    <input type="submit" value="Discharge">\
                    </form>')

                self.wfile.write(b"</center></body></html>")
                return
            ##view patients tab 
            if self.path == '/viewPatients':
                data = []
                records = self.database.viewPatients()
                print(records)
                data = records
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Hospital's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addPatient'>Add Patient</a>|\
                                  <a href='/scheduleAppointment'>Schedule Appointment</a>|\
                                  <a href='/viewAppointments'>View Appointments</a>|\
                                  <a href='/dischargePatient'>Discharge Patient</a></div>")
                self.wfile.write(b"<hr><h2>View Appointiments</h2>")

                #view patients table
                self.wfile.write(b"<table border=2> \
                                    <tr><th> Patient ID </th>\
                                        <th> Patient Name</th>\
                                        <th> Age </th>\
                                        <th> Appointment Date </th>\
                                        <th>Discharge Time </th></tr>")
                for row in data:
                        self.wfile.write(b'<tr> <td>')
                        self.wfile.write(str(row[0]).encode())
                        self.wfile.write(b'</td><td>')
                        self.wfile.write(str(row[1]).encode())
                        self.wfile.write(b'</td><td>')
                        self.wfile.write(str(row[2]).encode())
                        self.wfile.write(b'</td><td>')
                        self.wfile.write(str(row[3]).encode())
                        self.wfile.write(b'</td><td>')
                        self.wfile.write(str(row[4]).encode())
                        
               
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
            

def run(server_class=HTTPServer, handler_class=HospitalPortalHandler, port=8000):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()

run()
