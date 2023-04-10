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
	payment_method = 'mada'
	if payment_method == 'mada':
		temp_mada = models.execute_kw(db, uid, password, 'res.config.settings', 'search_read', [], {'fields':['template_mada_id']})
		# temp_mada_id = temp_mada[-1]['template_mada_id'][0]
		# print('MADA:::::::', temp_mada[-1]['template_mada_id'][0])
		wz_temp_run = models.execute_kw(db, uid, password, 'account.move.template.run', 'search_read', [[['template_id', '=', 427]]])
		wz_temp_id = wz_temp_run[0]['id']
		print('7777777', wz_temp_id)
		partner_id = 13
		amount = 1000
		ref = '8796'
		vals = {'partner_id': partner_id,'ref': ref}
		line_vals = {'amount':amount}

		wz_line_id = models.execute_kw(db, uid, password, 'account.move.template.line.run', 'search_read', [[['wizard_id','=', wz_temp_id]]])
		print('5555555555555', wz_line_id)
		# wz_temp_run_line = models.execute_kw(db, uid, password, 'account.move.template.line.run', 'write', [wz_line_id[0]['id'], line_vals])
		
		# wz_temp_run_update = models.execute_kw(db, uid, password, 'account.move.template.run', 'write', [wz_temp_run[0]['id'], vals])
		# move_temp_wizard = models.execute_kw(db, uid, password, 'account.move.template.run', 'generate_move', [wz_temp_run[0]['id']])
		# print('wwwwwww', move_temp_wizard)

	# elif payment_method == 'master_card':

	# 	temp_master = models.execute_kw(db, uid, password, 'res.config.settings', 'search_read', [], {'fields':['template_master_id']})
	# 	temp_master_id = temp_master[-1]['template_master_id'][0]
	# 	wz_temp_run = models.execute_kw(db, uid, password, 'account.move.template.run', 'search_read', [[['template_id', '=', temp_master_id]]])
	# 	wz_temp_id = wz_temp_run[0]['id']
	# 	partner_id = 8
	# 	amount = 1750
	# 	ref = '6666'
	# 	vals = {'partner_id': partner_id,'ref': ref}
	# 	line_vals = {'amount':amount}

	# 	wz_line_id = models.execute_kw(db, uid, password, 'account.move.template.line.run', 'search_read', [[['wizard_id','=', wz_temp_id]]], {'fields':['id']})
	# 	wz_temp_run_line = models.execute_kw(db, uid, password, 'account.move.template.line.run', 'write', [wz_line_id[0]['id'], line_vals])
		
	# 	wz_temp_run_update = models.execute_kw(db, uid, password, 'account.move.template.run', 'write', [wz_temp_run[0]['id'], vals])
	# 	move_temp_wizard = models.execute_kw(db, uid, password, 'account.move.template.run', 'generate_move', [wz_temp_run[0]['id']])
	# 	print('wwwwwww', move_temp_wizard)

else:
	print('Authentication Failed')