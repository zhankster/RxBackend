@app.route("/ptest", methods=["GET", "POST"])
@login_required
def ptest():
	batch_id = request.args.get("batch-id")
	batch_codes = None
	exception_codes = None
	conn = pyodbc.connect(RX_CONNECTION_STRING)
	cur = conn.cursor()
	error=None
	
	objects_list = {}
	if request.method == "GET" and batch_id != None:
		if batch_id == "":
			return redirect(url_for("ptest"))
			
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
			
        #Get Facility data HDA-2019-09-24
        facility_items = {}
        
        cur.execute("""EXEC dbo.todays_all_rx_by_facility""", fac_dcode.replace(' ', ''))
		rows_facility = cur.fetchall()
        
        if len(rows) > 0:
            for row in rows_facility:
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
                d['tech'] = row.TECH                
                d['rx'] = row.RX_INITIALS
                d['new'] = row.NEW
                d['exception'] = row.EXCEPTION
                d['fac_dcode'] = row.FAC_DCODE
                d['status'] = row.STATUS
		
                facility_items.append(d)
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
			
		return redirect(url_for("ptest"))
	else:
		objects_list = None
		batch_id = None
	
	return render_template('ptest.html', errors=error, batch_id=batch_id, batch=objects_list, batch_codes=batch_codes, exception_codes=exception_codes)
#end Ptest