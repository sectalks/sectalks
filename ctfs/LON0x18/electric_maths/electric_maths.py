# socat -T30 -d -d TCP-LISTEN:6000,fork,reuseaddr EXEC:"python3 -u electric_maths.py",pty,echo=0
import sys
import secrets
import uuid

loop_count = 100
tag = uuid.uuid4()

flag = 'STL{experience_voracious_stitch}'

def make_problem():
    op = secrets.randbelow(4)
    a = secrets.randbelow(1000)
    b = secrets.randbelow(1000)

    problem = ""
    answer = 0
    
    if op == 0:
        problem = "multiply {} and {}".format(a, b)
        answer = a * b
    elif op == 1:
        problem = "divide {} by {}".format(a, b)
        answer = round(a / b, 8)
    elif op == 2:
        problem = "add {} and {}".format(a, b)
        answer = a + b
    elif op == 3:
        problem = "subtract {} from {}".format(a, b)
        answer = b - a
    
    return problem, answer

def main():
    print('Hello there')
    print('Are you ready for some maths?')

    for i in range(loop_count):
        problem, answer = make_problem()
        sys.stderr.write('{} sending {} ({}) ({}/{})\n'.format(tag, problem, answer, i+1, loop_count))
        print(problem)

        s = sys.stdin.readline().rstrip()
        sys.stderr.write('{} received {} ({}/{})\n'.format(tag, s, i+1, loop_count))

        if float(s) == answer:
            print('Nice!')
        else:
            print('Wrong! {}'.format(answer))
            break
    else:
        sys.stderr.write('{} sending flag!\n'.format(tag))
        print(flag)
    
if __name__ == "__main__":
    main()