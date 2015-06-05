import sys, os, subprocess

def pdf_to_thumbs ( file ):

	file_no_ext = os.path.split(os.path.splitext( file )[0])[1]

	path = os.path.abspath( os.path.dirname( sys.argv[0] ) )
	in_file = path+file
	out_file = in_file[0:-4]

	cmd = "convert -density 300 %s %s.png" % ( in_file, out_file )

	print "CMD : %s"%cmd

	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)