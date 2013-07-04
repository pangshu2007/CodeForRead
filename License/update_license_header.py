import fnmatch
import os
import re

license_txt = """\
(*)~----------------------------------------------------------------------------------
 Pupil - eye tracking platform
 Copyright (C) 2012-2013  Moritz Kassner & William Patera

 Distributed under the terms of the CC BY-NC-SA License. 
 License details are in the file license.txt, distributed as part of this software.
----------------------------------------------------------------------------------~(*)\
"""

# find out the cwd and change to the top level Pupil folder
cwd = os.getcwd()
pupil_dir = os.path.join(*os.path.split(cwd)[:-1])

pattern = re.compile('(\'{3}|[/][*])\n\([*]\)~(.+?)~\([*]\)\n(\'{3}|[*][/])', re.DOTALL|re.MULTILINE)

# choose files types to include
# choose directories to exclude from search
includes = ['*.py', '*.c'] 
excludes = ['.git', 'atb', 'glfw', 'src_video', 'v4l2_ctl', 'data', 'License'] 

# transform glob patterns to regular expressions
includes = r'|'.join([fnmatch.translate(x) for x in includes])
excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

def get_files(start_dir, includes, excludes):
	# use os.walk to recursively dig down into the Pupil directory
	match_files = []
	for root, dirs, files in os.walk(start_dir):
		if not re.search(excludes, root):
			files = [f for f in files if re.search(includes, f) and not re.search(excludes, f)]
			files = [os.path.join(root, f) for f in files]
			match_files += files
	return match_files

def write_header(file_name, pattern, license_txt):
	# find and replace license header
	# or add new header if not existing
	c_comment = ['/*\n', '\n*/\n']
	py_comment = ["'''\n","\n'''\n"]
	file_type = os.path.splitext(file_name)[-1]

	if file_type == '.py':
		license_txt = py_comment[0] + license_txt + py_comment[1]
	if file_type == '.c':
		license_txt = c_comment[0] + license_txt + c_comment[1]

	with file(file_name, 'r') as original: 
		data = original.read()

	with file(file_name, 'w') as modified:
		if re.findall(pattern, data):
			# if header already exists, then update
			modified.write(re.sub(pattern, license_txt, data))
			modified.close()
		else:
			# else write the license header
			modified.write(license_txt + data)
			modified.close()

def update_header():
	# Add a license/docstring header to selected files
	match_files = get_files(pupil_dir, includes, excludes)
	print match_files 

	for f in match_files:
		write_header(f, pattern, license_txt)

if __name__ == '__main__':
	# run update_header() to add headers to found files
	update_header()