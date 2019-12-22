import os
import collections
import json
import pyodbc
import time

from flask import Flask, render_template, url_for, request, redirect, jsonify, session
# Flask-LoginManager
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import urllib

## GLOBALS
UPS_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=UPS_Shipping;Trusted_Connection=yes'
RX_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=RXBackend;Trusted_Connection=yes'
CIPS_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=CIPS;Trusted_Connection=yes'
RXBACKEND_VERSION='0.1'

## Init APP
app = Flask(__name__)
app.secret_key = 'super secret string'
login_manager = LoginManager()
login_manager.session_protection='basic'
login_manager.init_app(app)

general_users = ('Administrator','User')
pharm_redirect = 'iou'

def check_role(roles):
        if session['role'] not in roles:
            print(roles)
            return True
    
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("""EXEC get_user_by_username ?""", username)
	u = {}
	rows = cur.fetchall()
	if len(rows) <= 0:
		return
		
	for row in rows:
		u['username'] = row.username		
		
	user = User()
	user.id = username
	
	return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))
	
@login_manager.request_loader
def request_loader(request):
	username = request.form.get('username')
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("""EXEC get_user_by_username ?""", username)
	
	u = {}
	rows = cur.fetchall()
	if len(rows) <= 0:
		return
	
	for row in rows:
		u['username'] = row.username
		u['password'] = row.password
	
	user = User()
	user.id = username
		
	if check_password_hash(u['password'], request.form['password']):
		user.is_authenticated = True
	else:
		return
	return user

# BEGIN ROUTES
@app.route("/", methods=["GET"])
def index():
	return redirect(url_for('pending'))

@app.route("/version", methods=["GET"])
@login_required
def version():
	return "RXBackend Version: %s" % RXBACKEND_VERSION

@app.route("/ups_shipping_db_test", methods=["GET"])
def ups_shipping_db_test():
	conn = pyodbc.connect(UPS_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("SELECT count(*) FROM TO_UPS WHERE FIL_DATE='%s'" % "2018-05-07")
	data = cur.fetchall()
	
	return "Row Count: %s" % data
	
@app.route("/rxbackend_db_test", methods=["GET"])
def rxbackend_db_test():
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("SELECT count(*) FROM role")
	data = cur.fetchall()
	
	return "Row Count: %s" % data

@app.route("/cips_db_test", methods=["GET"])
def cips_backend_db_test():
	conn = pyodbc.connect(CIPS_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("SELECT count(*) FROM FAC")
	data = cur.fetchall()
	
	return "Row Count: %s" % data
	
@app.route("/across_db_test")
def all_db_test():
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("SELECT count(*) FROM CIPS..FAC")
	data = cur.fetchall()

	return "Row Count: %s" % data
	
@app.route("/ping", methods=["GET"])
def ping():
	return "pong"

@app.route("/pending", methods=["GET"])
def pending():
	filterArg = request.args.get("filter")
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()

    
	if filterArg == None:
		cur.execute("""EXEC todays_batches""")
	else:
		cur.execute("""EXEC todays_batches_by_shipping ?""",filterArg+'%')
	
	rows = cur.fetchall()
	
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['del_bat_id'] = row.DEL_BAT_ID
		d['facility'] = row.FACILITY
		d['color'] = row.COLOR
		d['total'] = row.P + row.M + row.S + row.U + row.O
		d['p'] = row.P
		d['m'] = row.M
		d['s'] = row.S
		d['u'] = row.U
		d['o'] = row.O
		d['tech'] = row.TECH
		d['ship'] = row.SHIP
		d['new'] = row.NEW
		d['exception'] = row.EXCEPTION
		
		objects_list.append(d)
	
	return render_template('pending.html', batches=objects_list, filter=filterArg)


def get_batch_complete_codes():
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("""EXEC dbo.get_batch_complete_codes""")
	rows = cur.fetchall()
	
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id'] = row.ID
		d['desc'] = row.DESC
		objects_list.append(d)
		
	return objects_list
	
def get_exception_codes():
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("""EXEC dbo.get_exception_codes""")
	rows = cur.fetchall()
	
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id'] = row.ID
		d['desc'] = row.DESC
		d['virt_fil_date_offset'] = row.VIRT_FIL_DATE_OFFSET
		objects_list.append(d)
		
	return objects_list


@app.route("/batch/<int:batch_id>", methods=["GET"])
@login_required
def get_batch_detail(batch_id):
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("""EXEC batch_detail_for_processing ?""", batch_id)
	
	rows = cur.fetchall()
	objects_list = []	
	for row in rows:
		temp = {}
		temp['facility'] = row.FACILITY
		temp['kop'] = row.FIL_KOP
		temp['name'] = row.NAME
		temp['drg_name'] = row.DRG_DNAME
		temp['drg_strength'] = row.DRG_STRENGTH
		#
		objects_list.append(temp)

	return jsonify(objects_list)

@app.route("/batch/summary/<int:batch_id>", methods=["GET"])
@login_required
def get_batch_summary(batch_id):
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	
	objects_list = {}
	pat_cache = {}
	# batch_codes = get_batch_complete_codes()
	# exception_codes = get_exception_codes()
	
	cur.execute("""EXEC dbo.batch_detail_for_processing ?""", batch_id)
	rows = cur.fetchall()
	
	for row in rows: 
		if not objects_list.has_key('batch_id'):
			objects_list['batch_id'] = row.DEL_BAT_ID
			objects_list['color'] = row.COLOR
			objects_list['facility'] = row.FACILITY
			objects_list['tech'] = row.TECH
			objects_list['ship'] = row.SHIP
		if not objects_list.has_key('KOP'):
			objects_list['KOP'] = collections.OrderedDict()
		if not objects_list['KOP'].has_key(row.FIL_KOP):
			objects_list['KOP'][row.FIL_KOP] = collections.OrderedDict()
			pat_cache[row.FIL_KOP] = []
			objects_list['KOP'][row.FIL_KOP]['rxTotal'] = 0
			objects_list['KOP'][row.FIL_KOP]['patTotal'] = 0
		if row.PAT_ID not in pat_cache[row.FIL_KOP]:
			pat_cache[row.FIL_KOP].append(row.PAT_ID)
			objects_list['KOP'][row.FIL_KOP]['patTotal'] = objects_list['KOP'][row.FIL_KOP]['patTotal'] + 1
		objects_list['KOP'][row.FIL_KOP]['rxTotal'] = objects_list['KOP'][row.FIL_KOP]['rxTotal'] + 1
		objects_list['KOP'][row.FIL_KOP][row.ID] = {'name': row.NAME, 'id': row.ID, 'fil_id': row.FIL_ID, 'pat_id': row.PAT_ID, 'qty': int(row.QTY), 'drg_strength': row.DRG_STRENGTH, 'drg_name': row.DRG_DNAME}	
	
	return jsonify(objects_list), 200	
		
@app.route("/pro_org", methods=["GET", "POST"])
@login_required
def pro_org():
	batch_id = request.args.get("batch-id")
	batch_codes = None
	exception_codes = None
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	error=None
	
	objects_list = {}
	if request.method == "GET" and batch_id != None:
		if batch_id == "":
			return redirect(url_for("processing"))
			
		batch_codes = get_batch_complete_codes()
		exception_codes = get_exception_codes()
			
		cur.execute("""EXEC dbo.batch_detail_for_processing ?""", batch_id.replace(' ', ''))
		rows = cur.fetchall()
		
		if len(rows) > 0:
			pat_cache = {}
			for row in rows: 
				if not objects_list.has_key('batch_id'):
					objects_list['batch_id'] = row.DEL_BAT_ID
					objects_list['color'] = row.COLOR
					objects_list['facility'] = row.FACILITY
					objects_list['tech'] = row.TECH
					objects_list['ship'] = row.SHIP
				if not objects_list.has_key('KOP'):
					objects_list['KOP'] = collections.OrderedDict()
				if not objects_list['KOP'].has_key(row.FIL_KOP):
					objects_list['KOP'][row.FIL_KOP] = collections.OrderedDict()
					pat_cache[row.FIL_KOP] = []
					objects_list['KOP'][row.FIL_KOP]['rxTotal'] = 0
					objects_list['KOP'][row.FIL_KOP]['patTotal'] = 0
				if row.PAT_ID not in pat_cache[row.FIL_KOP]:
					pat_cache[row.FIL_KOP].append(row.PAT_ID)
					objects_list['KOP'][row.FIL_KOP]['patTotal'] = objects_list['KOP'][row.FIL_KOP]['patTotal'] + 1
				objects_list['KOP'][row.FIL_KOP]['rxTotal'] = objects_list['KOP'][row.FIL_KOP]['rxTotal'] + 1
				objects_list['KOP'][row.FIL_KOP][row.ID] = { 'exception': row.EXCEPTION, 'name': row.NAME, 'id': row.ID, 'fil_id': row.FIL_ID, 'pat_id': row.PAT_ID, 'qty': int(row.QTY), 'drg_strength': row.DRG_STRENGTH, 'drg_name': row.DRG_DNAME}	
		else:
			error = 404
	elif request.method == "POST":
		
		if request.form['exception'] == 'Y':
			sql = "{CALL dbo.put_completed_batch (?, ?, ?, ?, ?, ?)}"
			params = (request.form['batch_id'], request.form['facility'].split("-")[0].strip(), request.form['ship'], request.form['tech'], request.form['batch_complete_code'], session['initials'])		
			cur.execute(sql, params)
			conn.commit()
			
			for key, value in request.form.iteritems():
				if len(key.split('_')) == 2:
					id, field = key.split('_')
					
					if field == "name":
						cur.execute("{CALL dbo.resolve_override (?, ?)}", (request.form['batch_id'], id))
						conn.commit()
		else: 
			sql = "{CALL dbo.put_completed_batch (?, ?, ?, ?, ?, ?)}"
			params = (request.form['batch_id'], request.form['facility'].split("-")[0].strip(), request.form['ship'], request.form['tech'], request.form['batch_complete_code'], session['initials'])		
			cur.execute(sql, params)
			conn.commit()
		
			objects_list = []		
			for key, value in request.form.iteritems():
				if len(key.split('_')) == 2:
					id, field = key.split('_')
				
					if field == 'exception':
						complete = 1
					
						if request.form[key] != '':
							complete = 0
							params = (int(id), (request.form['batch_id']), int(request.form[key]))
							cur.execute("{CALL dbo.generate_exception (?,?,?)}", params)
					
						cur.execute("{CALL dbo.update_shipping_notes (?, ?, ?)}", (int(id), request.form['batch_id'], complete))
						conn.commit()
			
		return redirect(url_for("processing"))
	else:
		objects_list = None
		batch_id = None
	
	return render_template('processing.html', errors=error, batch_id=batch_id, batch=objects_list, batch_codes=batch_codes, exception_codes=exception_codes)
	

#end Processing


@app.route("/processing", methods=["GET", "POST"])
@login_required
def processing():
    # return render_template('test1.html')
    batch_id = request.args.get("batch-id")
    batch_codes = None
    exception_codes = None
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    error = None
    objects_list = {}
    facility_items = []
    fac_dcode = '0'
    bg = '#FFFFFF'
    bat_total = 0

    if request.method == "GET" and batch_id != None:
        if batch_id == "":
            return redirect(url_for("processing"))

        batch_codes = get_batch_complete_codes()
        exception_codes = get_exception_codes()
        cur.execute("""EXEC dbo.batch_detail_for_processing_facility ?""",
                    batch_id.replace(' ', ''))
        rows = cur.fetchall()

        if len(rows) > 0:
            pat_cache = {}
            for row in rows:
                if not objects_list.has_key('batch_id'):
                    objects_list['batch_id'] = row.DEL_BAT_ID
                    objects_list['color'] = row.COLOR
                    objects_list['facility'] = row.FACILITY
                    objects_list['tech'] = row.TECH
                    objects_list['ship'] = row.SHIP
                    # Added Facility code HDA-2019-09-24
                    fac_dcode = row.FAC_DCODE
                if not objects_list.has_key('KOP'):
                    objects_list['KOP'] = collections.OrderedDict()
                if not objects_list['KOP'].has_key(row.FIL_KOP):
                    objects_list['KOP'][row.FIL_KOP] = collections.OrderedDict()
                    pat_cache[row.FIL_KOP] = []
                    objects_list['KOP'][row.FIL_KOP]['rxTotal'] = 0
                    objects_list['KOP'][row.FIL_KOP]['patTotal'] = 0
                if row.PAT_ID not in pat_cache[row.FIL_KOP]:
                    pat_cache[row.FIL_KOP].append(row.PAT_ID)
                    objects_list['KOP'][row.FIL_KOP]['patTotal'] = objects_list['KOP'][row.FIL_KOP]['patTotal'] + 1
                objects_list['KOP'][row.FIL_KOP]['rxTotal'] = objects_list['KOP'][row.FIL_KOP]['rxTotal'] + 1
                objects_list['KOP'][row.FIL_KOP][row.ID] = {'exception': row.EXCEPTION, 'name': row.NAME, 'id': row.ID, 'fil_id': row.FIL_ID, 'pat_id': row.PAT_ID, 'qty': int(
                    row.QTY), 'drg_strength': row.DRG_STRENGTH, 'drg_name': row.DRG_DNAME}
        else:
            error = 404

        # Get Facility data HDA-2019-09-24
        conn1 = pyodbc.connect(RX_CONNECTION_STRING)
        cur1 = conn1.cursor()
        cur1.execute("""EXEC dbo.todays_all_rx_by_facility ?""",fac_dcode.replace(' ', ''))
        #cur1.execute("""EXEC dbo.todays_all_rx_by_facility ?""",'GL')
        rows_facility = cur1.fetchall()

        if len(rows_facility) > 0:
            for row in rows_facility:
                d = collections.OrderedDict()
                d['del_bat_id'] = row.DEL_BAT_ID
                d['fil_date'] = str(row.FIL_DATE).replace(" 00:00:00", "")
                d['facility'] = row.FACILITY
                d['color'] = row.COLOR
                d['total'] = row.P + row.M + row.S + row.U + row.O
                d['p'] = row.P
                d['m'] = row.M
                d['s'] = row.S
                d['u'] = row.U
                d['o'] = row.O
                d['ship'] = row.SHIP
                d['tech'] = row.TECH
                d['rx'] = row.RX_INITIALS
                d['new'] = row.NEW
                d['exception'] = row.EXCEPTION
                ## d['fac_dcode'] = row.FAC_DCODE
                d['status'] = row.STATUS
                if d['status'] == "P":
                    d['bg'] = "#FA6A6A"
                elif d['status'] == "X":
                    d['bg'] = "#DEDEE0"
                elif d['status'] == "C":
                    d['bg'] = "#FBFBBB"
                elif d['status'] == "R":
                    d['bg'] = "#7FBF3F"
                else:
                    d['bg'] = "#FFFFFF"

                facility_items.append(d)
				#End Get Facilities HDA
		cur1.execute("""EXEC [dbo].get_batch_total_cost ?""", batch_id.replace(' ', ''))
		row_batch = cur1.fetchall()

		if len(row_batch) > 0:
    			for row in row_batch:
					bat_total = row.TOTAL_COST


		

        else:
            error = 404
    #@@@@@@### END Facility data HDA-2019-09-24

    elif request.method == "POST":

        if request.form['exception'] == 'Y':
            sql = "{CALL dbo.put_completed_batch (?, ?, ?, ?, ?, ?)}"
            params = (request.form['batch_id'], request.form['facility'].split(
                "-")[0].strip(), request.form['ship'], request.form['tech'], request.form['batch_complete_code'], session['initials'])
            cur.execute(sql, params)
            conn.commit()

            for key, value in request.form.iteritems():
                if len(key.split('_')) == 2:
                    id, field = key.split('_')

                    if field == "name":
                        cur.execute("{CALL dbo.resolve_override (?, ?)}",
                                    (request.form['batch_id'], id))
                        conn.commit()
        else:
            sql = "{CALL dbo.put_completed_batch (?, ?, ?, ?, ?, ?)}"
            params = (request.form['batch_id'], request.form['facility'].split(
                "-")[0].strip(), request.form['ship'], request.form['tech'], request.form['batch_complete_code'], session['initials'])
            cur.execute(sql, params)
            conn.commit()

            objects_list = []
            for key, value in request.form.iteritems():
                if len(key.split('_')) == 2:
                    id, field = key.split('_')

                    if field == 'exception':
                        complete = 1

                        if request.form[key] != '':
                            complete = 0
                            params = (int(id), (request.form['batch_id']), int(
                                request.form[key]))
                            cur.execute(
                                "{CALL dbo.generate_exception (?,?,?)}", params)

                        cur.execute("{CALL dbo.update_shipping_notes (?, ?, ?)}", (int(
                            id), request.form['batch_id'], complete))
                        conn.commit()

        return redirect(url_for("processing"))
    else:
        objects_list = None
        batch_id = None

    #return render_template('processing.html', errors=error, batch_id=batch_id, batch=objects_list, batch_codes=batch_codes, exception_codes=exception_codes)
    return render_template('processing.html', errors=error, batch_id=batch_id, batch=objects_list, batch_codes=batch_codes, exception_codes=exception_codes, facility_items=facility_items, bg=bg, bat_total = bat_total)
	#return render_template('processing.html')
#end Processing

@app.route("/iou", methods=["GET", "POST"])
@login_required
def iou():
    # return render_template('test1.html')
    batch_id = request.args.get("batch-id")
    batch_codes = None
    exception_codes = None
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    error = None
    objects_list = {}
    fac_dcode = '0'
    bg = '#FFFFFF'

    if request.method == "GET" and batch_id != None:
        if batch_id == "":
            return redirect(url_for("iou"))

        batch_codes = get_batch_complete_codes()
        exception_codes = get_exception_codes()
        cur.execute("""EXEC dbo.batch_detail_for_processing_iou ?""",
                    batch_id.replace(' ', ''))
        rows = cur.fetchall()

        if len(rows) > 0:
            pat_cache = {}
            for row in rows:
                if not objects_list.has_key('batch_id'):
                    objects_list['batch_id'] = row.DEL_BAT_ID
                    objects_list['color'] = row.COLOR
                    objects_list['facility'] = row.FACILITY
                    objects_list['tech'] = row.TECH
                    objects_list['ship'] = row.SHIP
                    # Added Facility code HDA-2019-09-24
                    fac_dcode = row.FAC_DCODE
                if not objects_list.has_key('KOP'):
                    objects_list['KOP'] = collections.OrderedDict()
                if not objects_list['KOP'].has_key(row.FIL_KOP):
                    objects_list['KOP'][row.FIL_KOP] = collections.OrderedDict()
                    pat_cache[row.FIL_KOP] = []
                    objects_list['KOP'][row.FIL_KOP]['rxTotal'] = 0
                    objects_list['KOP'][row.FIL_KOP]['patTotal'] = 0
                if row.PAT_ID not in pat_cache[row.FIL_KOP]:
                    pat_cache[row.FIL_KOP].append(row.PAT_ID)
                    objects_list['KOP'][row.FIL_KOP]['patTotal'] = objects_list['KOP'][row.FIL_KOP]['patTotal'] + 1
                objects_list['KOP'][row.FIL_KOP]['rxTotal'] = objects_list['KOP'][row.FIL_KOP]['rxTotal'] + 1
                objects_list['KOP'][row.FIL_KOP][row.ID] = {'exception': row.EXCEPTION, 'name': row.NAME, 'id': row.ID, 'fil_id': row.FIL_ID, 'pat_id': row.PAT_ID, 'qty': round(
                    row.QTY,2), 'drg_strength': row.DRG_STRENGTH, 'drg_name': row.DRG_DNAME, 'status': row.STATUS, 'iou_qty':round(row.IOU_QTY,2)}
        else:
            error = 404
    elif request.method == "POST":
        sql = "{CALL dbo.put_batch_fill_for_iou (?, ?, ?)}"
        if True:
			fills = request.form.getlist("cbfil")
        fills = [x.encode('UTF8') for x in fills]
        user = session['initials']
        # print(fills)
        for i in fills:
            key = i + "_iouqty"
            if request.form[ key ] != '':
                print(request.form[key] + ' : ' + i  + ' : ' + user)
                params = (int(i), float(request.form[key]), user)
                cur.execute(sql, params)
                conn.commit()
                
        return redirect(url_for("iou"))
        
    else:
        objects_list = None
        batch_id = None

    return render_template('iou.html', errors=error, batch_id=batch_id, batch=objects_list, batch_codes=batch_codes, exception_codes=exception_codes, bg=bg)

@app.route("/iou_processing", methods=["GET", "POST"])
@login_required
def iou_processing():
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    iou_items = []
    bg = '#FFFFFF'

    if request.method == "GET":
        cur.execute("""EXEC dbo.batch_detail_for_completing_iou """)
        rows = cur.fetchall()

        if len(rows) > 0:
            for row in rows:
                i = collections.OrderedDict()
                i['id'] = row.ID
                i['del_bat_id'] = row.DEL_BAT_ID
                i['fill_id'] = row.FIL_ID
                i['fill_date'] = str(row.FIL_DATE).replace(" 00:00:00", "")
                i['kop'] = row.FIL_KOP
                i['facility'] = row.FACILITY
                i['pat_id'] = row.PAT_ID
                i['name'] = row.NAME
                i['drg_dname'] = row.DRG_DNAME
                i['drg_strength'] = row.DRG_STRENGTH
                i['fill_qty'] = round(row.FILL_QTY,2)
                i['iou_date'] = row.IOU_DATE
                i['color'] = row.COLOR
                i['pharm_tech'] = row.PHARM_TECH
                i['iou_qty'] = round(row.IOU_QTY,2)
                i['status'] = row.STATUS
                
                iou_items.append(i)

        else:
            iou_items = []
            
    elif request.method == "POST":
        sql = "{CALL dbo.close_iou_request (?, ?, ?)}"
        id = request.form['valSubmit']
        user = session['initials']
        status = "IC"
        params = (int(id), user, status)
        print("Post")
        cur.execute(sql, params)
        conn.commit()
        return redirect(url_for("iou_processing"))
    else:
        iou_items = []
        

    return render_template('iou_processing.html', iou_items=iou_items)





@app.route("/rx/batch/<int:batch_id>", methods=["GET"])
@login_required
def get_preprocess_batch_detail(batch_id):
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("""EXEC batch_detail_for_pre_processing ?""", batch_id)
	
	rows = cur.fetchall()
	objects_list = []	
	for row in rows:
		temp = {}
		temp['facility'] = row.FACILITY
		temp['kop'] = row.FIL_KOP
		temp['name'] = row.NAME
		temp['drg_name'] = row.DRG_DNAME
		temp['drg_strength'] = row.DRG_STRENGTH
		
		objects_list.append(temp)

	return jsonify(objects_list)	
	
@app.route("/pre_processing", methods=["GET", "POST"])
@login_required
def pre_processing():
	batch_id = request.args.get("batch-id")
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	error=None
	
	objects_list = {}
	if request.method == "GET" and batch_id != None:
		if batch_id == "":
			return redirect(url_for("pre_processing"))
			
		try:
			cur.execute("""EXEC dbo.batch_detail_for_pre_processing ?""", batch_id.strip())
			rows = cur.fetchall()
			
			if len(rows) > 0:
				pat_cache = {}
				for row in rows: 
					if not objects_list.has_key('batch_id'):
						objects_list['batch_id'] = row.DEL_BAT_ID
						objects_list['color'] = row.COLOR
						objects_list['facility'] = row.FACILITY
						objects_list['tech'] = row.TECH
						objects_list['ship'] = row.SHIP
						objects_list['fil_date'] = row.FIL_DATE
					
					if not objects_list.has_key('KOP'):
						objects_list['KOP'] = collections.OrderedDict()
					if not objects_list['KOP'].has_key(row.FIL_KOP):
						objects_list['KOP'][row.FIL_KOP] = collections.OrderedDict()
						pat_cache[row.FIL_KOP] = []
						objects_list['KOP'][row.FIL_KOP]['rxTotal'] = 0
						objects_list['KOP'][row.FIL_KOP]['patTotal'] = 0
					if row.PAT_ID not in pat_cache[row.FIL_KOP]:
						pat_cache[row.FIL_KOP].append(row.PAT_ID)
						objects_list['KOP'][row.FIL_KOP]['patTotal'] = objects_list['KOP'][row.FIL_KOP]['patTotal'] + 1
					objects_list['KOP'][row.FIL_KOP]['rxTotal'] = objects_list['KOP'][row.FIL_KOP]['rxTotal'] + 1
					objects_list['KOP'][row.FIL_KOP][row.ID] = { 'exception': row.EXCEPTION, 'name': row.NAME, 'id': row.ID, 'fil_id': row.FIL_ID, 'pat_id': row.PAT_ID, 'qty': int(row.QTY), 'drg_strength': row.DRG_STRENGTH, 'drg_name': row.DRG_DNAME}	
			else:
				error = 404
		except pyodbc.Error as e:
			error=404
	elif request.method == "POST":	
		sql = "{CALL dbo.put_pre_processed_batch (?, ?, ?)}"
		params = (request.form['batch_id'], session['initials'], request.form['fil_date'])		
		cur.execute(sql, params)
		conn.commit()
		
		if request.form['exception'] == 'Y':
			for key, value in request.form.iteritems():
				if len(key.split('_')) == 2:
					id, field = key.split('_')
					if field == "name":
						cur.execute("{CALL dbo.put_virt_fil_date (?, ?)}", (request.form['batch_id'], id))
						conn.commit()
						
		return redirect(url_for("pre_processing"))
	else:
		objects_list = None
		batch_id = None		
	
	return render_template('pre_processing.html', errors=error, batch_id=batch_id, batch=objects_list)

@app.route("/rx_complete", methods=["GET"])
@login_required    
def rx_complete():
    if check_role(general_users):
        return redirect(url_for(pharm_redirect))
    
    filterArg = request.args.get("filter")
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    
    if filterArg == None:
        cur.execute("""EXEC todays_rx_complete_batches""")
    else:
        cur.execute("""EXEC todays_complete_rx_batches_by_shipping ?""",filterArg+'%')
        
    rows = cur.fetchall()

    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['del_bat_id'] = row.DEL_BAT_ID
        d['facility'] = row.FACILITY
        d['color'] = row.COLOR
        d['total'] = row.P + row.M + row.S + row.U + row.O
        d['p'] = row.P
        d['m'] = row.M
        d['s'] = row.S
        d['u'] = row.U
        d['o'] = row.O
        d['ship'] = row.SHIP        
        d['rx'] = row.RX_INITIALS
        d['new'] = row.NEW
        d['exception'] = row.EXCEPTION
        
        objects_list.append(d)
        
    return render_template('rx_complete.html', batches=objects_list, filter=filterArg)
	
@app.route("/complete")
@login_required
def complete():
	filterArg = request.args.get("filter")
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	
	if filterArg == None:
		cur.execute("""EXEC todays_complete_batches""")
	else:
		cur.execute("""EXEC todays_complete_batches_by_shipping ?""", filterArg+'%')
		
	rows = cur.fetchall()
	
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['del_bat_id'] = row.DEL_BAT_ID
		d['facility'] = row.FACILITY
		d['color'] = row.COLOR
		d['total'] = row.P + row.M + row.S + row.U + row.O
		d['p'] = row.P
		d['m'] = row.M
		d['s'] = row.S
		d['u'] = row.U
		d['o'] = row.O
		d['tech'] = row.TECH
		d['ship'] = row.SHIP
		d['new'] = row.NEW
		d['exception'] = row.EXCEPTION
		objects_list.append(d)
		
	return render_template('complete.html', batches=objects_list, filter=filterArg)


@app.route("/reconcile/batches", methods=["GET"])
@login_required
def facility_batches_to_reconcile():
	batch_id = request.args.get("batch_id").strip()
	
	if batch_id != None:
		try:
			conn = pyodbc.connect(RX_CONNECTION_STRING)
			cur = conn.cursor()
			cur.execute("""EXEC facility_batches_for_reconcile ?""", int(batch_id))
			rows = cur.fetchall()
		except ValueError:
			return "Not Found", 404
		
		data = {}
		
		for row in rows:
			if not data.has_key(row.FAC_DCODE):
				data[row.FAC_DCODE] = {}
			if not data[row.FAC_DCODE].has_key(row.DEL_BAT_ID):
				
				data[row.FAC_DCODE][row.DEL_BAT_ID] = {'completed': row.COMPLETED, 'reconciled': row.RECONCILED, 'overrides': [], 'resolved': row.RESOLVED}
		
			# ADD OVERRIDES OBJECTS 
			if row.FIL_ID != None and row.FILLED==0 and row.VIRT_FIL_DATE != date:				
				data[row.FAC_DCODE][row.DEL_BAT_ID]['overrides'].append({'id': row.FIL_ID, 'desc': row.DESC, 'filled': row.FILLED})			
		
		return jsonify(data), 200
	else: 
		return 500
	
@app.route("/reconcile", methods=["GET", "POST"])
@login_required
def reconcile():
	filterArg = request.args.get("filter")
	batch = None
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	
	if request.method == "POST":		
		if request.form['batches']:
			data = json.loads(request.form['batches'])
			
			try:
				for batch_id in data:					
					cur.execute("{CALL put_reconciled_batch (?, ?)}", (batch_id, session['initials']))
					# RESOLVE OVERRIDES #
					#if len(data[batch_id]['overrides']) > 0:
					#	for o in data[batch_id]['overrides']:						
					#		cur.execute("{CALL dbo.resolve_override (?, ?)}", (batch_id, o['id']))
			except pyodbc.IntegrityError:
				return "Conflict", 409
			
			conn.commit()
			#
			return "success", 200
		return "error", 500
				
	if filterArg == None:
		cur.execute("""EXEC todays_batches_to_reconcile""")
	else:
		cur.execute("""EXEC todays_batches_to_reconcile_by_shipping ?""", filterArg+'%')
		
	rows = cur.fetchall()

	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['facility'] = row.FACILITY
		d['total'] = row.P + row.M + row.S + row.U + row.O
		d['p'] = row.P
		d['m'] = row.M
		d['s'] = row.S
		d['u'] = row.U
		d['o'] = row.O
		d['tech'] = row.TECH
		d['ship'] = row.SHIP
		d['new'] = row.NEW		
		objects_list.append(d)

	return render_template('reconcile.html', batches=objects_list, filter=filterArg, batch=batch)


@app.route("/admin/user_manager", methods=["GET", "POST"])
@login_required
def admin_user_manager():
	if session['role'] != 'Administrator':
		return redirect(url_for('pending'))
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	
	if request.method == "POST":
		if request.form['op-code'] == 'update':
			enabled=0
			password=""
			
			if request.form.has_key('enabled'):
				enabled=1
			if len(request.form['inputPassword']) > 0:
				password=generate_password_hash(request.form['inputPassword'])
			sql = "{CALL dbo.update_user (?, ?, ?, ?, ?, ?)}"
			params=((request.form['user-id'], request.form['inputUsername'], password, request.form['selRole'], enabled, request.form['inputInitals']))
			cur.execute(sql, params)
			conn.commit()
		elif request.form['op-code'] == 'delete':			
			cur.execute("DELETE FROM users WHERE ID=?", request.form['del_user_id'])
			conn.commit()
		else:
			enabled=0
			if request.form.has_key('enabled'):
				enabled=1
			sql = "{CALL put_user (?, ?, ?, ?, ?)}" 
			params = ((request.form['inputUsername'], generate_password_hash(request.form['inputPassword']), request.form['selRole'], enabled, request.form['inputInitals']))			
			cur.execute(sql, params)
			conn.commit()			
	
	cur.execute("""EXEC get_users""")
	rows = cur.fetchall()
	
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id'] = row.id
		d['username'] = row.username
		d['enabled'] = row.enabled
		d['role'] = row.role_id
		objects_list.append(d)

	return render_template('admin/user_manager.html', users=objects_list)

@app.route("/admin/user_manager/user/<int:userid>")
@login_required
def admin_user_manager_user(userid):
	if session['role'] != 'Administrator':
		return redirect(url_for('pending'))
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("""EXEC dbo.get_user_by_id ?""", userid)
	rows = cur.fetchall()
	
	objects_list = {}
	for row in rows:
		objects_list['id'] = row.id
		objects_list['username'] = row.username
		objects_list['enabled'] = row.enabled
		objects_list['role'] = row.role_id
		objects_list['initials'] = row.initials

	return jsonify(objects_list)

@app.route("/admin/facility_config/facility/<facility>")
@login_required
def get_facility_config(facility):
	if session['role'] != 'Administrator':
		return redirect(url_for('pending'))
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("{CALL get_fac_color (?)}", facility)
	rows = cur.fetchall()
	
	objects_list = {}
	
	for row in rows:
		objects_list['row_count'] = len(rows)
		objects_list['fac_dcode'] = row.FAC_DCODE.strip()
		objects_list['2'] = row.MON
		objects_list['3'] = row.TUES
		objects_list['4'] = row.WED
		objects_list['5'] = row.THURS
		objects_list['6'] = row.FRI
	
	return jsonify(objects_list)
	
def get_facility_color_codes():
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("""EXEC get_facility_color_codes""")
	rows = cur.fetchall()
	
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id'] = row.ID
		d['color'] = row.Color
		d['description'] = row.Description
		objects_list.append(d)
		
	return objects_list

@app.route('/admin/facility_config', methods=["GET", "POST"])
@login_required
def admin_facility_config():
	if session['role'] != 'Administrator':
		return redirect(url_for('pending'))
	color_codes=get_facility_color_codes()
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	
	if request.method == "POST":
		
		if request.form['op-code'] == 'update':	
			sql = "{CALL update_facility_color_code (?, ?, ?, ?, ?, ?)}"
			params = (request.form ['txtFacility'], request.form['selMon'], request.form['selTues'], request.form['selWed'], request.form['selThurs'], request.form['selFri'])
			cur.execute(sql, params)
			conn.commit()
		elif request.form['op-code'] == 'delete':
			cur.execute("DELETE FROM FAC_CONFIG WHERE FAC_DCODE=?", request.form['facility_dcode'])
			conn.commit()
		else:
			sql = "{CALL put_facility_color_code (?, ?, ?, ?, ?, ?)}"
			params = (request.form ['txtFacility'], request.form['selMon'], request.form['selTues'], request.form['selWed'], request.form['selThurs'], request.form['selFri'])
			cur.execute(sql, params)
			conn.commit()
			
		return redirect(url_for('admin_facility_config'))
			
	cur.execute("""EXEC get_facility_configs""")
	rows = cur.fetchall()
	
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['facility_code'] = row.FAC_DCODE
		d['2'] = row.MON
		d['3'] = row.TUES
		d['4'] = row.WED
		d['5'] = row.THURS
		d['6'] = row.FRI
		objects_list.append(d)
	
	return render_template('admin/facility_config.html', color_codes=color_codes, config=objects_list)


@app.route('/admin/exceptions', methods=["GET"])
@login_required
def admin_all_exceptions():
	if session['role'] != "Administrator":
		return redirect(url_for('pending'))
		
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("""EXEC get_all_exceptions""")
	rows = cur.fetchall()
	
	objects_list = []
	for row in rows:
		temp = collections.OrderedDict()
		temp['fac_dcode'] = row.FAC_DCODE
		temp['del_bat_id'] = row.DEL_BAT_ID
		temp['exception_count'] = row.EXCEPTION_COUNT
		objects_list.append(temp)
	
	return jsonify(objects_list)
	
@app.route('/admin/exception_manager', methods=["GET", "POST"])
@login_required
def admin_exception_manager():
	if session['role'] != 'Administrator':
		return redirect(url_for('pending'))
	batch_id = request.args.get("batch-id")
	batch_codes = None
	exception_codes = None
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
		
	objects_list = {}
	if request.method == "GET" and batch_id != None:	
		batch_codes = get_batch_complete_codes()
		exception_codes = get_exception_codes()
		
		cur.execute("""EXEC dbo.batch_detail_exceptions ?""", batch_id.strip())
		rows = cur.fetchall()
	
		pat_cache = {}
		for row in rows: 
			if not objects_list.has_key('batch_id'):
				objects_list['batch_id'] = row.DEL_BAT_ID
				objects_list['facility'] = row.FACILITY
				objects_list['tech'] = row.TECH
				objects_list['ship'] = row.SHIP
			if not objects_list.has_key('KOP'):
				objects_list['KOP'] = collections.OrderedDict()
			if not objects_list['KOP'].has_key(row.FIL_KOP):
				objects_list['KOP'][row.FIL_KOP] = collections.OrderedDict()
				pat_cache[row.FIL_KOP] = []
				objects_list['KOP'][row.FIL_KOP]['rxTotal'] = 0
				objects_list['KOP'][row.FIL_KOP]['patTotal'] = 0
			if row.PAT_ID not in pat_cache[row.FIL_KOP]:
				pat_cache[row.FIL_KOP].append(row.PAT_ID)
				objects_list['KOP'][row.FIL_KOP]['patTotal'] = objects_list['KOP'][row.FIL_KOP]['patTotal'] + 1
			objects_list['KOP'][row.FIL_KOP]['rxTotal'] = objects_list['KOP'][row.FIL_KOP]['rxTotal'] + 1
			objects_list['KOP'][row.FIL_KOP][row.ID] = {'exception_desc': row.DESC, 'name': row.NAME, 'id': row.ID, 'fil_id': row.FIL_ID, 'pat_id': row.PAT_ID, 'qty': int(row.QTY), 'drg_strength': row.DRG_STRENGTH, 'drg_name': row.DRG_DNAME}
				
	elif request.method == "POST":				
		objects_list = []		
		
		for key, value in request.form.iteritems():	
			if len(key.split('_')) == 2:
				id, field = key.split('_')				
				if (field == 'drgname') and (request.form[key] != ''):
					#params = (id, request.form['batch_id'], request.form[key])
					#objects_list.append(params) 
					
					cur.execute("{CALL dbo.resolve_override (?, ?)}", (request.form['batch_id'], id))
				
		conn.commit()		
		return redirect(url_for('admin_exception_manager'))
	else:
		objects_list = None
		
	return render_template('admin/exception.html', batch_id=batch_id, batch=objects_list, batch_codes=batch_codes, exception_codes=exception_codes)

@app.route('/admin/exception_codes')
@login_required
def admin_exception_codes():	
	return jsonify(get_exception_codes())

	
@app.route('/admin/exception_code_manager', methods=["GET", "POST"])
@login_required
def admin_exception_code_manager():
	errorText = ""
	
	if session['role'] != 'Administrator':
		return redirect(url_for('pending'))
	
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	
	if request.method == "POST" and request.form["op-code"] == "delete":
		conn.execute("DELETE FROM BAT_EXCEPTION_CODE WHERE [ID]=?", request.form['del_code_id'])
		conn.commit()		
	elif request.method == "POST" and request.form["op-code"] == "update":
		cur.execute("UPDATE BAT_EXCEPTION_CODE SET [DESC]=? WHERE [ID]=?", request.form["inputDescription"], int(request.form["inputCode"]))
		conn.commit()
	elif request.method == "POST" and request.form["op-code"] == "create":				
		cur.execute("INSERT INTO BAT_EXCEPTION_CODE([ID], [DESC]) VALUES(?,?)", int(request.form["inputCode"]), request.form["inputDescription"])
		conn.commit()		
	elif request.method == "POST":
		errorText = "An unrecoginzed operation was performed."
		
	return render_template('admin/exception_code_mgr.html', errors=errorText)
	
@app.route('/admin/kickback', methods=["GET", "POST"])
@login_required
def admin_kickback():
	if session['role'] != 'Administrator':
		return redirect(url_for('pending'))
			
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	
	if request.method == "POST":				
		cur.execute("""EXEC kickback_facility ?""", request.form['facility-id'])
		conn.commit() 
		
		return redirect(url_for("complete"))
			
	return render_template('admin/kickback.html')

@app.route('/admin/batches/<path:batch_date>', methods=["GET"])
@login_required
def admin_batches_by_date(batch_date):
	if session['role'] != 'Administrator':
		return redirect(url_for('pending'))
	
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	
	rows = cur.execute("""EXEC dbo.todays_batches_by_date ?""", batch_date)
	
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['del_bat_id'] = row.DEL_BAT_ID
		d['facility'] = row.FACILITY
		d['color'] = row.COLOR
		d['total'] = row.P + row.M + row.S + row.U + row.O
		d['p'] = row.P
		d['m'] = row.M
		d['s'] = row.S
		d['u'] = row.U
		d['o'] = row.O
		d['tech'] = row.TECH
		d['ship'] = row.SHIP
		d['new'] = row.NEW
		
		objects_list.append(d)
	
	return jsonify(objects_list)
	
@app.route('/admin/batch_viewer', methods=["GET", "POST"])
@login_required
def admin_batch_viewer():
	if session['role'] != 'Administrator':
		return redirect(url_for('pending'))
	
	return render_template('admin/batch_viewer.html')

@app.route('/login', methods=["GET", "POST"])
def login():
	errors=None
	if request.method == 'GET':
		return render_template('login.html', errors=errors)
	
	username = request.form['username']
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	cur.execute("""EXEC get_user_by_username ?""", username)
	
	rows = cur.fetchall()
	if len(rows) <= 0:
		errors = "Invalid Username or Password"
		return render_template('login.html', errors=errors)
	u = {}
	for row in rows:
		u['password'] = row.password
		u['username'] = row.username
		u['role'] = row.role
		u['initials'] = row.initials
	
	if check_password_hash(u['password'], request.form['password']):		
		user = User()
		user.id = username
		session['role'] = u['role']
		session['initials'] = u['initials']
		login_user(user)

		return redirect(url_for('pending'))
	else:
		errors = "Invalid Username or Password"
		return render_template('login.html', errors=errors)


@app.route('/logout')
def logout():	
	logout_user()
	return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
    
# if __name__ == "__main__":
#     app.run(host= '0.0.0.0')