import os
from fpdf import FPDF, HTMLMixin

# msg = "This is a test print"
# print(msg)

# f=open("test.txt", "w+")
# for i in range(10):
#     f.write(msg + " %d\r\n" % (i+1))
    
# f.close()

filename = "simple_demo.pdf"

# pdf = FPDF()
# pdf.add_page()
# pdf.set_font("Arial", size=12)
# pdf.cell(200, 10, txt="Welcome to Python!", ln=1, align="C")
# pdf.output(filename)

# os.startfile(filename, "print")
# os.remove(filename)

def simple_table(spacing=1):
    data = [['LAST NAME,FIRST NAME', 'MEDICATION', 'ORIG QTY', 'OWED QTY', 'TECH'],
            ['Driscoll,Mike', 'LISINOPRIL-HCTZ - 20-25MG', '14', '14', 'BT']
            # ['John', 'Doe', 'jdoe@doe.com', '12345'],
            # ['Nina', 'Ma', 'inane@where.com', '54321']
            ]

    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()

    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height*spacing,txt=item, border=1)
        pdf.ln(row_height*spacing)

    pdf.output('simple_table.pdf')
    

    
# simple_table(2)

class HTML2PDF(FPDF, HTMLMixin):
    pass

def simple_table_html():
    pdf = HTML2PDF()
    table = """<table align="center" width="100%" style="font-size:8px">
            <tr><td width="33%">IHS PHARMACY</td><td width="34%">&nbsp;</td><td width="33%">BATCH NUMBER</td></tr>
            <tr><td width="33%">504 MCCURD AVE S, STE 7</td><td width="34%" text-align="center">IOU SHEET</td><td width="33%">9999999</td></tr>
            <tr><td width="33%">RAINSVILLE, AL 35986</td><td width="34%">&nbsp;</td><td width="33%">&nbsp;</td></tr>
            </table><br />"""
    

    table += """<table border="1" align="center" width="100%">
    <thead>
    <tr><th width="30%">LAST NAME,FIRST NAME</th><th width="30%">MEDICATION</th><th width="14%">ORIG QTY</th><th width="14%">OWED QTY</th><th width="12%">TECH</th></tr></thead>
    <tbody>
    <tr><td>Driscoll,Mike</td><td style="font-size:8px">LISINOPRIL-HCTZ - 20-25MG</td><td>14</td><td>14</td><td>HDA</td></tr>
    </tbody>
    </table>"""

    pdf.add_page()
    pdf.write_html(table)
    pdf.output('simple_table_html.pdf')

# def simple_table_html():
#     pdf = HTML2PDF()
 
#     table = """<table border="0" align="center" width="50%">
#     <thead><tr><th width="30%">Header 1</th><th width="70%">header 2</th></tr></thead>
#     <tbody>
#     <tr><td>cell 1</td><td>cell 2</td></tr>
#     <tr><td>cell 2</td><td>cell 3</td></tr>
#     </tbody>
#     </table>"""
 
#     pdf.add_page()
#     pdf.write_html(table)
#     pdf.output('simple_table_html.pdf')
 
# if __name__ == '__main__':
#     simple_table_html()
    
simple_table_html()