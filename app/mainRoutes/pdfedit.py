from app import app
import re
import sys,os

from flask import render_template, request, Response
from os import listdir
from os.path import isfile, join


'''
pdf append
'''
from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


@app.route('/pdflist', methods=['GET'])
def pdflist():

	mypath = "app/static/pdfpng/"

	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) and f.endswith('png')]

	pageInfo = {
				'layout':	'layout_default.html',
				'template': 'page_listpdfs.html',
				'replaces': '#theMainContent',
				'data' : {
					'title':		'List Pdf Templates',
					'pdf_img_files': onlyfiles,
					'mypath': mypath
				}
			}

	if request.is_xhr:
		return Response( json.dumps(pageInfo), mimetype='text/json')

	else:
		return render_template( pageInfo['template'], 
								layout		= pageInfo['layout'],
								title		= pageInfo['data']['title'],
								pdf_img_files = pageInfo['data']['pdf_img_files'],
								mypath = pageInfo['data']['mypath'])

@app.route('/pdfedit/<id>', methods=['GET'])
def pdfedit(id):

	pageInfo = {
				'layout':	'layout_default.html',
				'template': 'page_editpdf.html',
				'replaces': '#theMainContent',
				'data' : {
					'title': 'Edit Pdf Templates',
					'pdfTemplate': id
				}
			}

	if request.is_xhr:
		return Response( json.dumps(pageInfo), mimetype='text/json')

	else:
		return render_template( pageInfo['template'], 
								layout		= pageInfo['layout'],
								title		= pageInfo['data']['title'],
								pdfTemplate = pageInfo['data']['pdfTemplate'])

	return ''

@app.route('/pdfedit2/<id>', methods=['GET'])
def pdfedit2(id):

	pageInfo = {
				'layout':	'layout_default.html',
				'template': 'page_edit2pdf.html',
				'replaces': '#theMainContent',
				'data' : {
					'title':		'Scrape Pdf Templates',
					'pdfTemplate': id
				}
			}

	if request.is_xhr:
		return Response( json.dumps(pageInfo), mimetype='text/json')

	else:
		return render_template( pageInfo['template'], 
								layout		= pageInfo['layout'],
								title		= pageInfo['data']['title'],
								pdfTemplate = pageInfo['data']['pdfTemplate'])

	return ''




import pdfquery

@app.route('/pdfscrape', methods=['POST'])
def pdfscrape():

	try:
		page = int(request.form["theImage"].split("-")[1].split(".")[0])
		
	except:
		page = 0

	path = os.path.abspath( os.path.dirname( sys.argv[0] ) )


	foundit = re.search(r"-\d+.png",request.form["theImage"])

	if foundit:
		thePNG = path+"/app/static/pdfpng/"+request.form["theImage"].split("-")[0]
	else:
		thePNG = path+"/app/static/pdfpng/"+request.form["theImage"].split(".png")[0]

	thePDF = thePNG+".pdf"

	print "page : %s"%page
	print "thePNG : %s"%thePNG
	print "thePDF : %s"%thePDF

	pdf = pdfquery.PDFQuery(thePDF)

	existing_pdf = PdfFileReader(file(thePDF, "rb"))

	pdf.load(page)

	# read your existing PDF
	
	page = existing_pdf.getPage(page)

	inX = int(request.form["x"].split(".")[0])
	inY = int(request.form["y"].split(".")[0])
	print " inX : %s inY: %s" % (inX,inY)
	pageX = int(page.mediaBox.getUpperRight_x())
	pageY = int(page.mediaBox.getUpperRight_y())

	print " x : %s y: %s" % (pageX,pageY)

	posX = inX*0.24
	posY = pageY-(inY*0.24)


	print " posX : %s posY : %s" % (posX,posY)

	extracted = pdf.extract([('with_formatter', 'text'),('found', 'LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")'%(posX,posY,posX,posY))])
	print "ExTrAcTeD :: %s"%extracted['found']
	return extracted['found']

	return ''

@app.route('/pdfappend', methods=['POST'])
def pdfappend():

	packet = StringIO.StringIO()

	page = int(request.form["theImage"].split("-")[1].split(".")[0])

	inX = int(request.form["x"])
	inY = int(request.form["y"])

	print "page : %s : X : %s : Y : %s" % (page,inX,inY)

	# read your existing PDF
	existing_pdf = PdfFileReader(file("/home/damian/PDFEdit/GrampianSetup.orig.pdf", "rb"))
	page = existing_pdf.getPage(page)

	pageX = page.mediaBox.getUpperRight_x()
	pageY = page.mediaBox.getUpperRight_y()

	posX = inX*0.24
	posY = pageY-(inY*0.24)

	print " x : %s y: %s" % (pageX,pageY)
	print " posX : %s posY : %s" % (posX,posY)

	# create a new PDF with Reportlab
	can = canvas.Canvas(packet, pagesize=letter)

	can.drawString(posX, posY, "Here I am")
	can.save()

	#move to the beginning of the StringIO buffer
	packet.seek(0)
	new_pdf = PdfFileReader(packet)

	output = PdfFileWriter()
	# add the "watermark" (which is the new pdf) on the existing page

	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)
	# finally, write "output" to a real file
	outputStream = file("/home/damian/PDFEdit/pyJucks/app/static/pdfpng/destination_" + str( datetime.datetime.now() ) + ".pdf" , "wb")
	output.write(outputStream)
	outputStream.close()

	return ''
