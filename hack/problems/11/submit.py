      
def add(a,b):
    # write your code here
    return a + b
if __name__=='__main__':
    ls = [int(x) for x in input().split()]
    j = 0
    t = ls[j]
    for i in range(t):
        a = ls[j+1]
        b = ls[j+2]
        j = j+2
        result = add(a,b)
        print(result)

    