        i = collections.OrderedDict()
        if len(rows) > 0:
            iou_cache = {}
            iou_prev = 1
            for row in rows:
                # if 'IOU' not in io:
                io = collections.OrderedDict()
                io['id'] = row.ID
                io['iou_id'] = row.IOU_ID
                io['del_bat_id'] = row.DEL_BAT_ID
                io['fill_id'] = row.FIL_ID
                io['fill_date'] = str(row.FIL_DATE).replace(" 00:00:00", "")
                io['kop'] = row.FIL_KOP
                io['facility'] = row.FACILITY
                io['pat_id'] = row.PAT_ID
                io['name'] = row.NAME
                io['drg_dname'] = row.DRG_DNAME
                io['drg_strength'] = row.DRG_STRENGTH
                io['fill_qty'] = round(row.FILL_QTY,2)
                io['iou_date'] = row.IOU_DATE
                io['color'] = row.COLOR
                io['pharm_tech'] = row.PHARM_TECH
                io['initials'] = row.INTIALS
                io['iou_qty'] = round(row.IOU_QTY,2)
                io['iou_comp'] = round(row.IOU_COMP,2)
                io['status'] = row.STATUS
                io['stat_desc'] = row.STAT_DESC
                io['trans_row'] = row.TRANS_ROW
                # else:
                #     if not 'details' in io: 
                #         io['details'] = collections.OrderedDict()                       
                #         io['details'][row.TRANS_ID] = ({'trans_type': row.TRANS_TYPE})
                iou_items.append(io)

        else:
            iou_items = []
 
                # ean = EAN(u'5901234123457', writer=ImageWriter())
                # text = 
                # ean = barcode.get(u'code39', unicode(i), writer=ImageWriter())
                # filename = ean.save('temp/images/iou_' + i)
    
    
    #     if request.form['exception'] == 'Y':
    #         # sql = "{CALL dbo.put_completed_batch (?, ?, ?, ?, ?, ?)}"
    #         # params = (request.form['batch_id'], request.form['facility'].split(
    #         #     "-")[0].strip(), request.form['ship'], request.form['tech'], request.form['batch_complete_code'], session['initials'])
    #         # cur.execute(sql, params)
    #         # conn.commit()

    #         print(request.form.getlist("cbfil"))
    #         # for key, value in request.form.iteritems():
    #         #     print(key + ":  + ")
    #             # if len(key.split('_')) == 2:
    #             #     id, field = key.split('_')

    #             #     if field == "name":
    #             #         cur.execute("{CALL dbo.resolve_override (?, ?)}",
    #             #                     (request.form['batch_id'], id))
    #             #         conn.commit()
    #     else:
    #         # sql = "{CALL dbo.put_completed_batch (?, ?, ?, ?, ?, ?)}"
    #         # params = (request.form['batch_id'], request.form['facility'].split(
    #         #     "-")[0].strip(), request.form['ship'], request.form['tech'], request.form['batch_complete_code'], session['initials'])
    #         # cur.execute(sql, params)
    #         # conn.commit()

    #         objects_list = []
    #         print(request.form.getlist("cbfil"))
    #         # for key, value in request.form.iteritems():
    #         #     print(key + ": " + value)
    #             # if len(key.split('_')) == 2:
    #             #     id, field = key.split('_')

    #             #     if field == 'exception':
    #             #         complete = 1

    #             #         if request.form[key] != '':
    #             #             complete = 0
    #             #             params = (int(id), (request.form['batch_id']), int(
    #             #                 request.form[key]))
    #             #             cur.execute(
    #             #                 "{CALL dbo.generate_exception (?,?,?)}", params)

    #             #         cur.execute("{CALL dbo.update_shipping_notes (?, ?, ?)}", (int(
    #             #             id), request.form['batch_id'], complete))
    #             #         conn.commit()

    #     return redirect(url_for("iou"))
    # else:
    #     objects_list = None
    #     batch_id = None