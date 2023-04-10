import xmlrpc.client

#Connnection odoo db
url = 'http://localhost:8069'
db = 'db_indeal_api_main'
username = 'admin'
password = '123'

# Authentcation login
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
if uid:
	print('Authentication Successful')
	#Search Method
	models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
	# partner = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]], {'limit':5})
	temp_id = 410
	wz_temp_run = models.execute_kw(db, uid, password, 'account.move.template.run', 'search_read', [[['template_id', '=', temp_id]]])
	# wz = models.execute_kw(db, uid, password, 'account.move.template.run', 'generate_move', [[temp[0], {'line_ids':{'amount':'1000'}}]])
	# print('ssssssssssssssssss', wz)
	# wrt = models.execute_kw(db, uid, password, 'account.move.template.line.run', 'write', [temp[0], {'name':'soooooo'}])

	wz_temp_id = wz_temp_run[0]['id']
	vals = {'amount':1000}
	line_id = models.execute_kw(db, uid, password, 'account.move.template.line.run', 'search_read', [[['wizard_id','=', wz_temp_id]]], {'fields':['id']})
	wz_temp_run_line = models.execute_kw(db, uid, password, 'account.move.template.line.run', 'write', [line_id[0]['id'], vals])
	
	models.execute_kw(db, uid, password, 'account.move.template.run', 'write', [wz_temp_run[0]['id'], {'partner_id':13}])
	entey = models.execute_kw(db, uid, password, 'account.move.template.run', 'generate_move', [wz_temp_run[0]['id']])

	# man = models.execute_kw(db, uid, password, 'account.move.template.run', 'write', [29, {'partner_id':13}])
	# wz = models.execute_kw(db, uid, password, 'account.move.template.run', 'generate_move', [[29]])

	# sch = models.execute_kw(db, uid, password, 'account.move.template.line.run', 'search_read', [[['wizard_id','=', 29]]], {'fields':['id']})
	print('lllllllllllll', entey)

	# #search count
	# partner_count = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[['is_company', '=', True]]])
	# print('>>>>>>>', partner_count)

	# #Read Method
	# partner_rec = models.execute_kw(db, uid, password, 'res.partner', 'read', [partner], {'fields':['id', 'name']})

	# #Search_read in one method
	# partner_rec2 = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['is_company','=', True]]], {'fields':['id', 'name']})
	# # print('>>>>>>>>>', partner_rec2)

	# #Create record in odoo DB
	# vals = {
	# 	'name': 'Odoo Mate External API',
	# 	'email': 'odoomateexternal@gmail.com'
	# }
	# create_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [vals])
	# print('4444444444', create_id)
	# partner = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['email', '=', 'odoomateexternal@gmail.com']]])
	# #Write method
	# models.execute_kw(db, uid, password, 'res.partner', 'write', [partner, {'phone':'25082407', 'mobile': '885577'}])
	# #Unlink method
	# models.execute_kw(db, uid, password, 'res.partner', 'unlink', [partner])


else:
	print('Authentication Failed')