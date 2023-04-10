def _prvs_mnth_dates(self):
         today = fields.date.today()
         current_month = date_utils.subtract(today)
         start_month = date_utils.start_of(current_month, "month")
         end_month = date_utils.end_of(current_month, "month")
         print('previous_month:::', current_month)
         print('starting_prevs_month:::', start_month)
         print('ending_prevs_month:::', end_month)

         #  Get Current month
        today = fields.date.today()
        current_month = date_utils.subtract(today)
        start_month = date_utils.start_of(current_month, "month")
        end_month = date_utils.end_of(current_month, "month")
        domain+= [('date', '>=', start_month),('date', '<=', end_month)]

