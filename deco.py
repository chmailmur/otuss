# from dis import dis 

# registry = [] 
# def register(func): 
#     print(f'running register({func})') 
#     registry.append(func) 
#     return func 

# @register 
# def f1():
#     print('running f1()')

# @register
# def f2():
#     print('running f2()')

# def f3():
#     print('running f3()')

# def main():
#     print('running main()')
#     print('registry ->', registry)

#     f1()
#     f2()
#     f3()

# dis(f1)

# if __name__ == '__main__':
#     main() 

def t():
    
    s = []

    def add(new_val):
        s.append(new_val)
        return sum(s)


    return add

f = t()

print(f(10))
print(f.__code__.co_varnames)
print(f.__code__.co_freevars)
print(f.__closure__)
print(f(30))
print(f.__code__.co_varnames)
print(f.__code__.co_freevars)
print(f.__closure__)
print(f(10))
print(f.__code__.co_varnames)
print(f.__code__.co_freevars)
print(f.__closure__)
print(f.__closure__[0].cell_contents)
