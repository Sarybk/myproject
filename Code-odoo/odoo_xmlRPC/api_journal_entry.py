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
	#@Parameter
	mada = 'Mada'
	master_card = 'Master Card'
	transaction_id = '12345'
	journal_id = 347
	date = '2023-03-14'
	total_transaction_amount = 3000
	#@dict list 
	vals = {
		'date' : date, 
		'journal_id': journal_id, 
		'x_studio_transaction_id':transaction_id, 
		'x_studio_payment_method': mada, 
		'x_studio_total_transaction_amount': total_transaction_amount
	}
	je_id = models.execute_kw(db, uid, password, 'account.move', 'create', [vals])
	#@Parameter
	vendor_id = 18
	customer_id = 49
	account_debit = 5055
	account_credit = 5056
	deb_vals = {
      'move_id': je_id, 
      'account_id': account_debit,
      'partner_id': customer_id,
      'debit' : total_transaction_amount
    }
	cred_vals = {
      'move_id': je_id, 
      'account_id': account_credit,
      'partner_id': vendor_id,
      'credit': total_transaction_amount
    }
	debit = models.execute_kw(db, uid, password, 'account.move.line', 'create',[deb_vals],{'context' :{'check_move_validity': False}})
	credit = models.execute_kw(db, uid, password, 'account.move.line', 'create',[cred_vals],{'context' :{'check_move_validity': False}})

else:
	print('Authentication Failed')