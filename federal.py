import constant

class AnnualTaxableIncome(): # A
    """Annual income formula
    A = Annual taxable income
    A = [P × (I – F – F2 – U1 )] – HD – F1
    If the result is negative, T = L.
    P   The number of pay periods in the year
    I   Gross remuneration for the pay period. This includes overtime earned and paid in the same pay period, pension income, qualified pension income, and taxable benefits, but does not include bonuses, retroactive pay increases, or other non-periodic payments
    F   Payroll deductions for the pay period for employee contributions to a registered pension plan (RPP) for current and past services, a registered retirement savings plan (RRSP), to a pooled registered pension plan (PRPP), or a retirement compensation arrangement (RCA). For tax deduction purposes, employers can deduct amounts contributed to an RPP, RRSP, PRPP, or RCA by or on behalf of an employee to determine the employee's taxable income
    F2  Alimony or maintenance payments required by a legal document dated before May 1, 1997, to be payroll-deducted authorized by a tax services office or tax centre
    U1  Union dues for the pay period paid to a trade union, an association of public servants, or dues required under the law of a province to a parity or advisory committee or similar body
    HD  Annual deduction for living in a prescribed zone, as shown on Form TD1
    F1  Annual deductions such as child care expenses and support payments, requested by an employee or pensioner and authorized by a tax services office or tax centre

    """
    def __init__(self, P, I, F=0, F2=0, U1=0, HD=0, F1=0, L=0):
        
        self.P = P # periode de paye dans l'annee
        self.I = I # salary per pay period
        self.F = F # cotisation a un reer, etc.
        self.F2 = F2 # retenue pour pension
        self.U1 = U1 # paiement syndicat
        self.HD = HD # Deduction pour region, voir formulaire TD1
        self.F1 = F1 # pensions et autres
        
    def calculate(self):
        # [P x (I - F - F2 - U1)] - HD - F1
        result = (self.P * (self.I - self.F - self.F2 - self.U1)) - self.HD - self.F1
        if result <= 0:
            result = self.L
        return result

    def calculate_comission(self):
        pass

class BasicFederalTax(): # T3
    """Formula to calculate the basic federal tax
    T3 = Annual basic federal tax
    T3 = (R × A) – K – K1 – K2 – K3 – K4
    If the result is negative, T3 = $0.
    A = Annual taxable income(see previous formula result)
    R and K are based on 2020 index values
    A see the Rates (R, V), income thresholds (A), and constants (K, KP) for 2020 Table 9.1 in Chapter 9.
    K   Federal constant. The constant is the tax overcharged when applying the 20.5%, 26%, 29%, and 33% rates to the annual taxable income A
    K1 = 0.15 × TC
    K2 = [(0.15 × (P x C, maximum $2,898.00)) + (0.15 x (P × EI, maximum $856.36))]
    K2Q = Quebec Pension Plan contributions, employment insurance premiums, and Quebec Parental Insurance Plan premiums federal tax credits for the year
    = [(0.15 × (P × C, maximum $3,146.40)) + (0.15 × (P × EI, maximum $650.40)) + (0.15 × (P × IE × 0.00494, maximum $387.79))]*
    K1  Federal non-refundable personal tax credit (the lowest federal tax rate is used to calculate this credit)
    K2Q Quebec Pension Plan contributions, employment insurance premiums, and Quebec Parental Insurance Plan premiums federal tax credits for the year (the lowest federal tax rate is used to calculate this credit)
    K3  Other federal non-refundable tax credits (such as medical expenses and charitable donations) authorized by a tax services office or tax centre
    K4  Factor calculated using the Canada employment amount credit (the lowest federal tax rate is used to calculate this credit)
    TC  "Total claim amount" reported on federal Form TD1. If Form TD1 is not filed by the employee or pensioner, TC is the basic personal amount, and for non-resident individuals, TC is $0. If the claim code is E, T = $0. If the province is Ontario, even if the claim code is E, the Ontario Health Premium is payable on annual income over $20,000
    P   The number of pay periods in the year
    C   Canada (or Quebec) Pension Plan contributions for the pay period
    AE  Assurance emploi?
    


    """

    def __init__(self, R, A, K, K1, K2Q, K3, K4, TC, P, C, AE, IE, CEA):
        self.R = R
        self.A = A
        self.K = K
        self.K3 = K3
        self.K4 = K4
        self.TC = TC
        self.P = P 
        self.C = C
        self.AE = AE
        self.IE = IE
        self.CEA = CEA

        self.K1 = 0.15 * self.TC  
        if self.P * self.C > 3146.4:
            self.P_C = 3146.4
        else:
            self.P_C = self.P * self.C

        if self.P * self.AE > 650.4:
            self.P_AE = 650.4
        else:
            self.P_AE = self.P * self.AE

        self.P_IE = self.P * self.IE
        if self.P_IE * 0.00494 > 387.79:
            self.P_IE = 387.79

        self.K4 = min(0.15 * self.A, 0.15 * self.CEA)


        self.K2Q = ((0.15 * self.P_C) + (0.15 * self.P_AE) + (0.15 * self.P_IE))


    def calculate(self):
        # print(self.R, self.A, self.K, self.K1, 'K2Q', self.K2Q, 'K3', self.K3, self.K4)

        result = (self.R * self.A) - self.K - self.K1 - self.K2Q - self.K3 - self.K4
        if result < 0:
            result = 0
        return result

class AnnualPayableTaxFederal(): # T1
    """docstring for AnnualPayableTaxFederal"""
    def __init__(self, T3, LCF):
        self.T3 = T3
        self.LCF = LCF
    
    def calculate(self):
        self.T3_LCF = self.T3 - self.LCF
        if self.T3_LCF < 0:
            self.T3_LCF = 0

        result = (self.T3_LCF) - 0.165 * self.T3
        if result < 0:
            result = 0
        return result


class FederalTaxRate():
    """Federal tax rate T"""
    def __init__(self, T1, P, L):
        self.T1 = T1
        self.P = P
        self.L = L

    def calculate(self):
        result = (self.T1 / self.P) + self.L
        return result

class EmployementInsurance():
    """Employement insurance premium"""
    def __init__(self, insurable_earning, premium_rate, year_max, paid_this_year):
        self.insurable_earning = insurable_earning
        self.premium_rate = premium_rate
        self.year_max = year_max
        self.paid_this_year = paid_this_year

    def calculate(self):
        result = self.insurable_earning * self.premium_rate
        if self.year_max <= self.paid_this_year:
            self.year_max = self.paid_this_year
        if result > (self.year_max - self.paid_this_year):
            result = self.year_max - self.paid_this_year

        return result
        
        