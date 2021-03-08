import docplex
from docplex.mp.model import Model
m = Model(name='LnPr')
x1 = m.integer_var(name='x1')
x2 = m.integer_var(name='x2')
func = m.integer_var(name='func')

m.add_constraint(x1 + 2*x2 <= 6)
m.add_constraint(3*x1 + x2 <= 9)

func = 4*x1 + 2*x2

m.maximize(func)
m.print_information()
m.solve()
m.print_solution()
