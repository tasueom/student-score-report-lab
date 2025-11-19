def calculate(kor, eng, math):
    total = kor + eng + math
    average = total / 3
    grade = 'A' if average >= 90 else 'B' if average >= 80 else 'C' if average >= 70 else 'D' if average >= 60 else 'F'
    return total, average, grade