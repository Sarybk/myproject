import xmlrpc.client

#Connnection odoo db
url = 'http://localhost:8069'
db = 'db_api_smile'
username = 'admin'
password = '1'

# Authentcation login
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
if uid:
	print('Authentication Successful')
	#Search Method
	models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
	# partner = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]], {'limit':5})
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
	# partner = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['email', '=', 'odoomateexternal@gmail.com']]])
	# #Write method
	models.execute_kw(db, uid, password, 'res.partner', 'write', [partner, {'phone':'25082407', 'mobile': '885577'}])
	# #Unlink method
	# models.execute_kw(db, uid, password, 'res.partner', 'unlink', [partner])


else:
	print('Authentication Failed')