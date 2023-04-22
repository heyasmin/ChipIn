class Debt:
    def __init__(self, debt_total_figure, debt_source, debt_interest, debt_term, repayment):
        self._debt_total_figure = debt_total_figure
        self._debt_source = debt_source
        self._debt_interest = debt_interest
        self._debt_term = debt_term
        self._repayment = repayment

        if self._debt_total_figure:
            self._debt_total_figure = int(self._debt_total_figure)
        else:
            self._debt_total_figure = 0

        if self._debt_interest:
            self._debt_interest = int(self._debt_interest)
        else:
            self._debt_interest = 0

        if self._debt_term:
            self._debt_term = int(self._debt_term)
        else:
            self._debt_term = 0
        
        if self._repayment:
            self._repayment = int(self._repayment)
        else:
            self._repayment = 0
        
    
    def get_debt_total_figure(self):
        return self._debt_total_figure
    
    def get_debt_source(self):
        return self._debt_source
    
    def get_debt_interest(self):
        return self._debt_interest
    
    def get_debt_term(self):
        return self._debt_term
    
    def get_repayment(self):
        return self._repayment
    
    def get_debt_list(self):
        return [self._debt_total_figure, self._debt_source, self._debt_interest, self._debt_term, self._repayment]

    def get_debt_dict(self):
        return {
        'debt_total_figure': self._debt_total_figure,
        'debt_source': self._debt_source, 
        'debt_interest': self._debt_interest,
        'debt_term': self._debt_term,
        'debt_repayment': self._repayment
        }
