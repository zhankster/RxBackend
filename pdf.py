from flask import Flask, render_template, url_for, request, redirect, jsonify, session, make_response
import webbrowser as wb
import barcode
from barcode.writer import ImageWriter
import pdfkit
path_wkhtmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
# pdfkit.from_url("http://google.com", "out.pdf", configuration=config)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Creating a PDF <a href="iou_delivery" target="blank">IOU</a>'

@app.route('/iou_delivery')
def iou_delivery():
    batch = 9999999
    medication = 'LISINOPRIL-HCTZ 20-25M'
    name = 'Driscoll,Mike'
    org_qty = 14
    iou_qty = 7
    pharm_tech = 'HDA'
    
    ean = barcode.get('code39', '123456789102', writer=ImageWriter())
    filename = ean.save('temp/images/code39_barcode')
    # filename
    
    rendered = render_template('iou_delivery.html', batch=batch, medication = medication, name = name, org_qty = org_qty, iou_qty = iou_qty, pharm_tech = pharm_tech)
    
    with open("temp/iou_123.html","wb") as fo:
        fo.write(rendered)
        
    batch = 1111111
    medication = 'TYLENOL-500M'
    name = 'Parker,Joe'
    org_qty = 100
    iou_qty = 50
    pharm_tech = 'RDA'
        
    rendered = render_template('iou_delivery.html', batch=batch, medication = medication, name = name, org_qty = org_qty, iou_qty = iou_qty, pharm_tech = pharm_tech)
    with open("temp/iou_456.html","wb") as fo:
        fo.write(rendered)
        
    
    # pdf = pdfkit.from_string([rendered,rendered] , False, configuration=config)
    pdf = pdfkit.from_file(['temp/iou_123.html','temp/iou_456.html'] , False, configuration=config)
    # pdf.
    # pdf.on('pageAdded', () => pdf.text(rendered))
    
    
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    
    return response
    

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(host= '0.0.0.0')