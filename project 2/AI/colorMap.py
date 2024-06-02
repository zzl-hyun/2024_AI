from simpleai.search import CspProblem, backtrack
def constraintFunc(names, values):
    return values[0] != values[1]

if __name__ == '__main__':
    names = ('서울', '인천', '경기', '충남', '강원', '충북', '세종', '대전',
             '전북', '경북', '전남', '광주', '대구', '경남', '울산', '부산')
    
    colors = dict((name, ['red', 'green', 'blue', 'gray']) for name in names)
    
    constraints = [
        (('서울', '경기'), constraintFunc),
        (('서울', '인천'), constraintFunc),
        (('경기', '충남'), constraintFunc),
        (('경기', '충북'), constraintFunc),
        (('경기', '강원'), constraintFunc),
        (('충남', '전북'), constraintFunc),
        (('충남', '대전'), constraintFunc),
        (('충남', '세종'), constraintFunc),
        (('충남', '충북'), constraintFunc),
        (('강원', '충북'), constraintFunc),
        (('강원', '경북'), constraintFunc),
        (('전북', '대전'), constraintFunc),
        (('전북', '충북'), constraintFunc),
        (('전북', '경북'), constraintFunc),
        (('전북', '전남'), constraintFunc),
        (('전북', '경남'), constraintFunc),
        (('대전', '세종'), constraintFunc),
        (('대전', '충북'), constraintFunc),
        (('세종', '충북'), constraintFunc),
        (('충북', '경북'), constraintFunc),
        (('전남', '광주'), constraintFunc),
        (('전남', '경남'), constraintFunc),
        (('경북', '경남'), constraintFunc),
        (('경북', '대구'), constraintFunc),
        (('경북', '울산'), constraintFunc),
        (('경남', '대구'), constraintFunc),
        (('경남', '울산'), constraintFunc),
        (('경남', '부산'), constraintFunc),
        (('울산', '부산'), constraintFunc),
    ]
    
    problem = CspProblem(names, colors, constraints)
    output = backtrack(problem)
    
    print("color mapping\n")
    for k, v in output.items():
        print(k, '-->', v)