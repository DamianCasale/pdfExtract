import json
import os

from flask import render_template, request, Response
from app.lib.pdf2Thumbs import pdf_to_thumbs
from werkzeug import secure_filename
from app import app

@app.route('/upload', methods=['GET'])
def uploadGET():
	pageInfo = {
				'layout':	'layout_default.html',
				'template': 'page_upload.html',
				'replaces': '#theMainContent',
				'data' : {
					'title':		'Upload Pdf Templates'
				}
			}

	if request.is_xhr:
		return Response( json.dumps(pageInfo), mimetype='text/json')

	else:
		return render_template( pageInfo['template'], 
								layout		= pageInfo['layout'],
								title		= pageInfo['data']['title'])

@app.route('/upload', methods=['POST'])
def uploadPOST():

	file = request.files['file']
	filename = secure_filename(file.filename)
	file.save(os.path.join('app/static/pdfpng/', filename))

	pdf_to_thumbs( '/app/static/pdfpng/'+filename )

	return 'ok',200