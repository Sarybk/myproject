
	#quarter Year 3 months
        far_future = start_of_quarter + timedelta(days=120)
	# Half Year 6 months
        far_future = start_of_quarter + timedelta(days=182)
	# Every Year
        far_future = start_of_quarter + timedelta(days=368)
	#Every Month
        far_future = start_of_quarter + timedelta(days=40)





def action_invoices_contract(self):
        period = 3
        if period == 1:
            lst = self.quarter_year(self.date_order)
            for i in range(0, 12):
                lst_next = [rec for rec in lst[0]][i]
                due_date = [x for x in lst[1]][i]
                print('rrrrrrrrrrrrrr', lst_next)
                vals = self._prepare_invoice_vals()
                vals.update({'invoice_date_due': due_date, 'periods': lst_next})
                # print("Create record1", vals)
            self.env['account.move'].create(vals)
        if period == 3:
            lst = self.half_of_year(self.date_order)
            for i in range(0, 12):
                lst_next = [rec for rec in lst[0]][i]
                due_date = [x for x in lst[1]][i]
                print('rrrrrrrrrrrrrr', lst_next)
                print('rrrrrrrrrrrrrr', due_date)
                vals = self._prepare_invoice_vals()
                vals.update({'invoice_date_due': due_date, 'periods': lst_next})
                # print("Create record1", vals)
            # self.env['account.move'].create(vals)
        if period == 2:
            lst = self.monthly_of_year(self.date_order)
            for i in lst:
                due_date = i
                print('rrrrrrrrrrrrrr', due_date)
                vals = self._prepare_invoice_vals()
                vals.update({'invoice_date_due': due_date, 'periods': due_date})
                # print("Create record1", vals)
                # self.env['account.move'].create(vals)
        # print('llllllllllllll', lst[1][2])




















def quarter_year(date):
	date_now = date
	years_to_add = date_now.year + 1

	start_date_str = date_now.strftime('%d/%m/%Y')
	end_date_str = date_now.replace(year=years_to_add).strftime('%d/%m/%Y')

	check = 2
	start_date = datetime.strptime(start_date_str, "%d/%m/%Y").date()
	end_date = datetime.strptime(end_date_str, "%d/%m/%Y").date()

	print(f"Quarters within {start_date_str} and {end_date_str}:")
	start_of_quarter = start_date
	while True:
		if check == 1:
			far_future = start_of_quarter + timedelta(days=180)
		elif check == 2:
			far_future = start_of_quarter + timedelta(days=100)
	    # print('far_future', far_future)
		start_of_next_quarter = far_future.replace(day=date_now.day)
	    # print('start_of_next_quarter', start_of_next_quarter)
		end_of_quarter = start_of_next_quarter - timedelta(days=date_now.day)

	    # middl = start_of_quarter.month + 1

	    # middl_of_date = start_of_quarter.replace(month=middl)
	    # print('middle_of_quarter', middl_of_date)
		if end_of_quarter > end_date:
			break
		print(f"\t{start_of_quarter:%d/%m/%Y} - {end_of_quarter:%d/%m/%Y}")
		start_of_quarter = start_of_next_quarter


today = datetime.strptime('18/3/2023', "%d/%m/%Y").date()
quarter_year(today)





def action_invoices_contract(self):


        # dat = date_utils.get_quarter(self.date_order)
        # print(dat, '77777777777777777777777777777')
        # lst = {'name': self.name}
        # print('===========SUCCESS CONTRACT==============', self._prepare_invoice_vals())
        # self.env['account.move'].create(self._prepare_invoice_vals())
        lst = self.quarter_year(self.date_order)
        for i in range(0, 4):
            lst_next = [rec for rec in lst[0]][i]
            due_date = [x for x in lst[1]][i]
            print('rrrrrrrrrrrrrr', lst_next)
            vals = self._prepare_invoice_vals()
            vals.update({'invoice_date_due': due_date, 'periods': lst_next})
            # print("Create record1", vals)
            self.env['account.move'].create(vals)
        # print('llllllllllllll', lst[1][2])


                    
    def quarter_year(self, date):
        date_now = date
        years_to_add = date_now.year + 1
        lst = []
        lst_start_date = []

        start_date_str = date_now.strftime('%d/%m/%Y')
        end_date_str = date_now.replace(year=years_to_add).strftime('%d/%m/%Y')


        start_date = datetime.strptime(start_date_str, "%d/%m/%Y").date()
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y").date()

        print(f"Quarters within {start_date_str} and {end_date_str}:")
        start_of_quarter = start_date
        while True:
            far_future = start_of_quarter + timedelta(days=90)
            start_of_next_quarter = far_future.replace(day=date_now.day)
            end_of_quarter = start_of_next_quarter - timedelta(days=date_now.day)

            middl = start_of_quarter.month + 1
            if middl > 12:
                middl = middl - 12
            else:
                pass

            middl_of_date = start_of_quarter.replace(month=middl)
            # print('middle_of_quarter', middl_of_date)
            if end_of_quarter > end_date:
                break
            # print(f"\t{start_of_quarter:%d/%m/%Y} - {middl_of_date:%d/%m/%Y} - {end_of_quarter:%d/%m/%Y}")



#######################################################################################################################################


from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import pandas as pd

# start_date_str = "01/03/2020"
# end_date_str = "01/03/2021"


def quarter_year(date):
	date_now = date
	years_to_add = date_now.year + 1
	start_date_str = date_now.strftime('%d/%m/%Y')
	end_date_str = date_now.replace(year=years_to_add).strftime('%d/%m/%Y')
	start_date = datetime.strptime(start_date_str, "%d/%m/%Y").date()
	end_date = datetime.strptime(end_date_str, "%d/%m/%Y").date()
	lst_quarter_year = []
	lst_due_date = []
	
	print(f"Quarters within {start_date_str} and {end_date_str}:")
	start_of_quarter = start_date
	while True:
		
		# far_future = start_of_quarter + timedelta(days=25)
		# far_future = start_of_quarter + timedelta(days=180) 
		far_future = start_of_quarter + timedelta(days=100)
		start_of_next_quarter = far_future.replace(day=date_now.day)
		end_of_quarter = start_of_next_quarter - timedelta(days=date_now.day)
		month = start_of_quarter.month + 1
		if month > 12:
			month = month - 12
		middle_of_quarter = start_of_quarter.replace(month=month)
		if end_of_quarter > end_date:
			break
		# print(f"\t{start_of_quarter:%d/%m/%Y} - {middle_of_quarter:%d/%m/%Y} - {end_of_quarter:%d/%m/%Y}")
		lst_quarter_year.append(f"\t{start_of_quarter:%m} - {middle_of_quarter:%m} - {end_of_quarter:%m}")
		lst_due_date.append(start_of_quarter)
		print(lst_quarter_year)
		start_of_quarter = start_of_next_quarter
	return lst_quarter_year, lst_due_date



def half_of_year(date):
	years_to_add = date.year + 1
	start_date_str = date.strftime('%d/%m/%Y')
	end_date_str = date.replace(year=years_to_add).strftime('%d/%m/%Y')
	start_date = datetime.strptime(start_date_str, "%d/%m/%Y").date()
	end_date = datetime.strptime(end_date_str, "%d/%m/%Y").date()
	lst_half_year = []
	lst_due_date = []
	
	print(f"Quarters within {start_date_str} and {end_date_str}:")
	start_of_quarter = start_date
	while True:
		
		# far_future = start_of_quarter + timedelta(days=25)
		# far_future = start_of_quarter + timedelta(days=100)

		far_future = start_of_quarter + timedelta(days=180) 
		start_of_next_quarter = far_future.replace(day=date.day)
		end_of_quarter = start_of_next_quarter - timedelta(days=date.day)
		if end_of_quarter > end_date:
			break
		# print(f"\t{start_of_quarter:%d/%m/%Y}  - {end_of_quarter:%d/%m/%Y}")
		lst_half_year.append(f"\t{start_of_quarter:%d/%m/%Y}  'to' {end_of_quarter:%d/%m/%Y}")
		lst_due_date.append('lst_due_date:::::::::', end_of_quarter)
		print(lst_half_year)
		start_of_quarter = start_of_next_quarter
	return lst_half_year, lst_due_date

def all_of_year(date):
	years_to_add = date.year + 1
	start_date_str = date.strftime('%d/%m/%Y')
	end_date_str = date.replace(year=years_to_add).strftime('%d/%m/%Y')
	start_date = datetime.strptime(start_date_str, "%d/%m/%Y").date()
	end_date = datetime.strptime(end_date_str, "%d/%m/%Y").date()
	lst_half_year = []
	lst_due_date = []
	
	print(f"Quarters within {start_date_str} and {end_date_str}:")
	start_of_quarter = start_date
	while True:
		
		# far_future = start_of_quarter + timedelta(days=25)
		# far_future = start_of_quarter + timedelta(days=100)

		far_future = start_of_quarter + timedelta(days=360) 
		start_of_next_quarter = far_future.replace(day=date.day)
		end_of_quarter = start_of_next_quarter - timedelta(days=date.day)
		if end_of_quarter > end_date:
			break
		print(f"\t{start_of_quarter:%d/%m/%Y}  - {end_of_quarter:%d/%m/%Y}")
		# lst_half_year.append(f"\t{start_of_quarter:%d/%m/%Y}  'to' {end_of_quarter:%d/%m/%Y}")
		# lst_due_date.append(start_of_quarter)
		# print(lst_half_year)
		start_of_quarter = start_of_next_quarter
	return lst_half_year, lst_due_date





def all_of_month(date):
	years_to_add = date.year + 1
	start_date_str = date.strftime('%d/%m/%Y')
	end_date_str = date.replace(year=years_to_add).strftime('%d/%m/%Y')
	start_date = datetime.strptime(start_date_str, "%d/%m/%Y").date()
	end_date = datetime.strptime(end_date_str, "%d/%m/%Y").date()
	lst_month = []
	
	print(f"Quarters within {start_date_str} and {end_date_str}:")
	start_of_quarter = start_date
	while True:
		
		far_future = start_of_quarter + timedelta(days=25)
		# far_future = start_of_quarter + timedelta(days=100)
		start_of_next_quarter = far_future.replace(day=date.day)
		end_of_quarter = start_of_next_quarter - timedelta(days=date.day)
		if end_of_quarter > end_date:
			break
		# print(f"\t{start_of_quarter:%d/%m/%Y}  - {end_of_quarter:%d/%m/%Y}")
		# lst_month.append(f"\t{start_of_quarter:%m}")
		# print(lst_month)
		start_of_quarter = start_of_next_quarter
	return lst_month




# today = datetime.strptime('18/3/2023', "%d/%m/%Y").date()
today = datetime.now()
# quarter_year(today)
# half_of_year(today)
all_of_year(today)

	    

# today = datetime.now()

# date_now = datetime.now()
# years_to_add = date_now.year + 1

# date_1 = date_now.strftime('%Y-%m-%d')
# date_2 = date_now.replace(year=years_to_add).strftime('%Y-%m-%d')

# print(date_1)
# print(date_2)



# No_of_quarters=4

# today = "04/04/2021"
# month = pd.Period(today, freq='M')
# quarter = month.asfreq('Q-DEC')

# print("Quarters:")
# for x in range (1,No_of_quarters):
#     print(quarter+x)

# print("Months:")
# for x in range (1,(No_of_quarters*3)+1):
#     print(month-1+x)
#     # print(x)



# No_of_quarters=4

# today = "05/01/2023"
# month = pd.Period(today, freq='M')
# quarter = month.asfreq('Q-Jan')

# print("Quarters:")
# for x in range (1,No_of_quarters):
#     print(quarter+x)

# print("Months:")
# for x in range (1,(No_of_quarters*3)+1):
#     print(month+x)
#     print(x)


# datelist = pd.bdate_range(start=pd.datetime.now(), periods = 12).tolist
# print(datelist)
            lst.append(f"\t{start_of_quarter:%m} - {middl_of_date:%m} - {end_of_quarter:%m}")
            lst_start_date.append(start_of_quarter)
            start_of_quarter = start_of_next_quarter
        return lst, lst_start_date
