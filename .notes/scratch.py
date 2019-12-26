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