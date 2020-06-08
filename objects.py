import constant


class AnnualIncome():
    """Annual taxable income
    pay_periods = Pay Peroids per year

    remuneration = Gross remuneration subject to source deductions of income tax for the pay period. Do not
     include gratuities, retroactive pay or similar lump-sum payments.
    Total of the following amounts for the pay period:
        • the contribution to an RPP;
        • the contribution to an RRSP;
        • the contribution to a VRSP or to a PRPP;
        • the contribution paid for an employee under a retirement compensation arrangement;
        • the deduction respecting the CIP, that is, 125% of the amount withheld from the employee’s
        remuneration for the purchase of preferred shares qualifying under the CIP;
        • the travel deduction for residents of designated remote areas;
        • the security option deduction;
        • the portion of the remuneration that gives entitlement to one of the following deductions:
        – the deduction for employment income situated on a reserve or premises,
        – the deduction for employment income earned on a vessel,
        – the deduction for foreign specialists,
        – the deduction for foreign researchers,
        – the deduction for foreign researchers on a post-doctoral internship,
        – the deduction for foreign experts,
        – the deduction for foreign professors,
        – the deduction for foreign producers or foreign individuals holding a key position in a foreign
        production filmed in Québec,
        – the deduction for foreign farm workers,
        – the Canadian Forces personnel and police deduction.
        
        Deduction for employment income = DeductionForEmploymentIncome()


        """
    def __init__(self, pay_periods, remuneration, contributions=0, deduction_employment_income=0, source_deduction_return=0, reduction_source_deductions=0):
        self.pay_periods = pay_periods
        self.remuneration = remuneration
        self.contributions = contributions
        self.deduction_employment_income = deduction_employment_income
        self.source_deduction_return = source_deduction_return
        self.reduction_source_deductions = reduction_source_deductions

    def calculate(self):
        result = self.pay_periods * (self.remuneration - self.contributions- self.deduction_employment_income) - self.source_deduction_return - self.reduction_source_deductions
        return result

class DeductionForEmploymentIncome():
    """docstring for DeductionForEmploymentIncome
    Gross salary or wages subject to source deductions of income tax for the pay period.
         Do not include gratuities, retroactive pay or similar lump-sum payments."""

    def __init__(self, remuneration, pay_periods):
        self.remuneration = remuneration
        self.pay_periods = pay_periods
    
    def calculate(self):
        result = (0.06* self.remuneration) 
        if result > (1190 / self.pay_periods):
            result = 1190 / self.pay_periods
        return result

class SourceDeductionReturn():
    """This is computed from the  TP-1015.3-V formule found on gov website.
    pay_periods = Pay Peroids per year
    line_19 = Deductions shown on line 19 of form TP-1015.3-V after the first pay period in the year
    remaining_periods = Number of pay periods remaining in the year (including the current pay period)
    """
    def __init__(self, pay_periods, line_19, remaining_periods):
        self.pay_periods = pay_periods
        self.line_19 = line_19
        self.remaining_periods = remaining_periods

    def calculate(self):
        result = (self.pay_periods * self.line_19) / self.remaining_periods
        return result

class ReductionSourceDeductions():
    """Annual deductions that we authorized after the individual completed form TP-1016-V, Application
     for a Reduction of Income Tax. If the value of J1
     is determined after the first pay period in the
     year, it is instead equal to the result of the following calculation:

    authorized_deduction = Deductions that we authorized after the first pay period in the year

    """
    def __init__(self, pay_periods, authorized_deduction, remaining_periods):
        self.pay_periods = pay_periods
        self.authorized_deduction = authorized_deduction
        self.remaining_periods = remaining_periods

    def calculate(self):
        result = (self.pay_periods * self.authorized_deduction) / self.remaining_periods
        return result

         

class IncomeTaxYear():
    """Income tax for the year
    Y = (T × I) – K – K1 – (0.15 × E) – (0.15 × P × Q) – (0.20 × P × Q1) I
    T = Income tax rate applicable to the bracket of annual taxable income
    I = Annual taxable income
    K = Constant applicable for the adjustment of the income tax rate on the basis of the annual taxable income
    K1 = Non-refundable tax credits that we authorized for the year after the individual completed
        form TP-1016-V (for example, the tax credit for charitable donations). If the value of K1
         is determined after the first pay period in the year, it is instead equal to the result of the following calculation:
        K1 = (P × K2) / Pr
    E = Value of personal tax credits shown on form TP-1015.3-V
        where: 
        E1 = Indexed value of personal tax credits, which corresponds to one of the following amounts:
            • the indexed value of variable E1
             for 2019 multiplied by 1.0172;
            • the amount from line 7 of form TP-1015.3-V, for an individual who completed the form
            for 2020;
            • $15,532 (the basic personal amount for 2020) for an employee who took up employment
            duties in 2020 and who did not complete form TP-1015.3-V and for a new beneficiary
            who did not complete the form.
            NOTE
            The indexed value of variable E1
             for 2019 corresponds to the value of variable E1
             for 2018,
            multiplied by the indexation factor for 2019 plus 1.
        E2 = Non-indexed value of the personal tax credits, which corresponds to the amount from
            line 9 of form TP-1015.3-V, for an individual who completed the 2020 version of the form.
            NOTE
            There may be a limit on the deductions and personal tax credits an individual can claim on
            form TP‑1015.3-V if the individual is not resident in Canada, or if he or she becomes resident in
            Canada during the year. For more information, consult guide TP-1015.G-V
    P = Number of pay periods in the year
    Q = Amount withheld for the pay period for the purchase of class A Fonds de solidarité FTQ shares
    Q1 = Amount withheld for the pay period for the purchase of class A or class B Fondaction shares
        NOTE
        The total of the amounts withheld for the year must not exceed $5,000. For the pay period in which the
        annual maximum is reached, the value of variables Q and Q1
         must be zero.


    """
    def __init__(self, I, K1=0, E=0, P=52, Q=0, Q1=0):
        self.I = I
        self.K1 = K1
        self.E = E
        self.P = P # pay periods
        self.Q = Q
        self.Q1 = Q1
        self.get_income_tax_rate()

    def get_income_tax_rate(self):
        for element in constant.INCOME_TAX_RATE_APPLICABLE:
            if element['min'] < self.I and element['max'] >= self.I:
                self.T = element['income_tax_rate']
                self.K = element['constant_k']
                print('income tax rate set to %s' %self.T)
                break

    
    def calculate(self):
        # Y = (T × I) – K – K1 – (0.15 × E) – (0.15 × P × Q) – (0.20 × P × Q1) I
        result = (self.T * self.I) - self.K - self.K1 - (0.15 * self.E) - (0.15 * self.P * self.Q) - (0.20 * self.P * self.Q1) * self.I
        return result

class IncomeTaxWithheldPerPeriod():
    """A = Income tax to be withheld for the pay period
    A = (Y / P) + L
    Y = Income tax for the year
    P = Number of pay periods in the year
    L = Additional source deduction of income tax requested by the individual on form TP-1015.3-V or
        form TP-1017-V, Request to Have Additional Income Tax Withheld at Source, or source deduction
        of income tax requested by a fisher on form TP-1015.N-V, Election by Fishers to Have Income Tax
        Deducted at Source, for the pay period
    """
    def __init__(self, income_tax_year, pay_periods, additional_source_deduction=0):
        self.income_tax_year = income_tax_year
        self.pay_periods = pay_periods
        self.additional_source_deduction = additional_source_deduction

    def calculate(self):
        # A = (Y / P) + L
        result = (self.income_tax_year / self.pay_periods) + self.additional_source_deduction
        return result

class QuebecPensionPlan():
    """Q = Employee’s QPP contribution to be withheld for the pay period
         = 0.0570 × [S3 – (V / P)], up to a maximum of M – A5
    """
    def __init__(self, S3, V, P, M, A5):
        self.S3 = S3
        self.V = V
        self.P = P
        self.M = M
        self.A5 = A5

    def calculate(self):
        result = 0.0570 * (self.S3 - (self.V / self.P))
        if result > (self.M - self.A5):
            result = (self.M - self.A5)

        return result

class QuebecParentalInsurancePlan():
    """Ap = = (0.00494 × S4), up to a maximum of N – A6

    """
    def __init__(self, S4, N, A6):
        self.S4 = S4
        self.N = N
        self.A6 = A6
    
    def calculate(self):
        result = (0.00494 * self.S4)
        if result > (self.N - self.A6):
            result = (N - A6)

        return result

