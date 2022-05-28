import copy
import sys

matrix = []
mainTargetFunction = []
targetFunction = []

width = 0
height = 0
prevWidth = 0
basis = []
tmpC = -1
tmpL = -1


def getSizeInfo():
    global width
    global height
    print('Введите размеры матрицы')
    print('Кол-во переменных:')
    width = 2  # int(input())
    print('Кол-во уравнений:')
    height = 2  # int(input())
    return


def getFillMatrix():
    global matrix
    for j in range(height):
        row = []
        print('Введите коэффициенты ' + str(j + 1) + '-го уравнения')
        for i in range(width):
            print('Коэффициент при x' + str(i + 1))
            row.append(2)  # int(input())
        print('Знак уравнения (<=, =, >=)')
        row.append('=')  # input()
        print('Коэффициент при B')
        row.append(2)  # int(input())
        matrix.append(row)


def getTargetFunction():
    global targetFunction
    print('Введите коэффициенты целевой функции:')
    for i in range(width):
        print('Коэффициент при x' + str(i + 1))
        targetFunction.append(-3)  # -1 * int(input())
    print('Значение C')
    targetFunction.append(-3)  # -1 * int(input())
    print('Стремление целевой функции (min, max)')
    targetFunction.append('max')  # input()


def canonForm():
    global matrix
    global width
    global prevWidth
    prevWidth = width
    for i in range(height):
        if matrix[i][prevWidth] == '<=' or matrix[i][prevWidth] == '>=':
            width += 1
    cnt = 0
    for i in range(height):
        newRow = []
        if matrix[i][prevWidth] == '<=':
            for j in range(width):
                if j >= prevWidth:
                    if j == prevWidth + cnt:
                        newRow.append(1)
                    else:
                        newRow.append(0)
                else:
                    newRow.append(matrix[i][j])
            newRow.append(matrix[i][prevWidth + 1])
            matrix[i] = newRow
            cnt += 1
        elif matrix[i][prevWidth] == '>=':
            for j in range(width):
                if j >= prevWidth:
                    if j == prevWidth + cnt:
                        newRow.append(1)
                    else:
                        newRow.append(0)
                else:
                    newRow.append(matrix[i][j] * (-1))
            newRow.append(matrix[i][prevWidth + 1] * (-1))
            matrix[i] = newRow
            cnt += 1
        elif matrix[i][prevWidth] == '=':
            for j in range(width):
                if j >= prevWidth:
                    newRow.append(0)
                else:
                    newRow.append(matrix[i][j])
            newRow.append(matrix[i][prevWidth + 1])
            matrix[i] = newRow
    return


def getBasis():
    global matrix
    basisCount = 0
    global basis
    basis = []
    for i in range(width):
        basis.append(0)
    basised = []
    for i in range(height):
        basised.append(0)

    for i in range(height):
        for j in range(prevWidth, width):
            if matrix[i][j] == 1:
                basisCount += 1
                basised[i] = 1
                basis[j] = 1
                print('x' + str(j + 1) + ' был выбран как базис')
    if not basisCount == height:
        for i in range(height):
            if basised[i] == 0:
                if (prevWidth == width):
                    for j in range(prevWidth-1, 0, -1):
                        if matrix[i][j] != 0:
                            znam = matrix[i][j]
                            for k in range(height):
                                if k != i:
                                    koef = matrix[k][j] / matrix[i][j]
                                    for l in range(width + 1):
                                        matrix[k][l] -= matrix[i][l] * koef
                                else:
                                    for l in range(width + 1):
                                        matrix[k][l] = matrix[k][l] / znam
                            basisCount += 1
                            basised[i] = 1
                            basis[j] = 1
                            print('x' + str(j + 1) + ' был выбран как базис')
                else:
                    for j in range(prevWidth, 0, -1):
                        if matrix[i][j] != 0:
                            znam = matrix[i][j]
                            for k in range(height):
                                if k != i:
                                    koef = matrix[k][j] / matrix[i][j]
                                    for l in range(width + 1):
                                        matrix[k][l] -= matrix[i][l] * koef
                                else:
                                    for l in range(width + 1):
                                        matrix[k][l] = matrix[k][l] / znam
                            basisCount += 1
                            basised[i] = 1
                            basis[j] = 1
                            print('x' + str(j + 1) + ' был выбран как базис')


def addNewVariablesIntoTargetFunction():
    global mainTargetFunction
    newTargetFunction = []
    for i in range(width):
        if i >= prevWidth:
            newTargetFunction.append(0)
        else:
            newTargetFunction.append(mainTargetFunction[i])
    newTargetFunction.append(mainTargetFunction[prevWidth])
    newTargetFunction.append(mainTargetFunction[prevWidth + 1])
    mainTargetFunction = newTargetFunction


def expressBasis():
    global targetFunction
    tfcp = copy.deepcopy(targetFunction)
    for i in range(width):
        if not tfcp[i] == 0:
            temp = tfcp[i]
            if basis[i] == 1:
                for j in range(width):
                    targetFunction[j] += temp * -matrix[i][j]
                targetFunction[width] += temp * matrix[i][width]


def checkNegativeElementsB(m):
    for i in range(height):
        if m[i][width] < 0:
            return True
    return False


def checkNegativeElementsIndex(targetFunction):
    for i in range(width):
        if targetFunction[i] < 0:
            return True
    return False


def methodJordanGauss():
    # Какой базис на какой заменить? подобрать под ЛЮБОЙ ИЗ ОТРИЦАТЕЛЬНЫХ КЛЮЧЕВЫХ
    max = 0
    global matrix
    global targetFunction
    global tmpL
    global tmpC
    for i in range(height):
        if matrix[i][width] < 0 and abs(matrix[i][width]) > max:
            max = abs(matrix[i][width])
            tmpL = i
    for j in range(width-1,-1,-1):
        if matrix[tmpL][j] < 0:
            tmpC = j
            break
    for j in range(width):
        if matrix[tmpL][j] == 1 and basis[j] == 1:
            basisFrom = j+1
            basisTo = tmpC+1
    print('Заменяем базис x'+str(basisFrom)+' на x'+str(basisTo))
    basis[basisFrom - 1] = 0
    basis[basisTo - 1] = 1
    mcp = copy.deepcopy(matrix)
    resElem = mcp[tmpL][tmpC]
    for i in range(height):
        if not i == tmpL:
            for j in range(width + 1):
                if not j == tmpC:
                    mcp[i][j] = matrix[i][j] - (matrix[tmpL][j] * matrix[i][tmpC]) / resElem
    for i in range(height):
        if not i == tmpL:
            mcp[i][tmpC] = 0
    tfcp = copy.deepcopy(targetFunction)
    for j in range(width + 1):
        mcp[tmpL][j] = mcp[tmpL][j] / resElem
        tfcp[j] = targetFunction[j] - (matrix[tmpL][j] * targetFunction[tmpC]) / resElem
    targetFunction = tfcp
    matrix = mcp


def getResolvingElement():
    global tmpC
    global tmpL
    tmpC = -1
    tmpL = -1
    max = 0
    for i in range(width):
        if abs(targetFunction[i]) > max and targetFunction[i] < 0:
            max = abs(targetFunction[i])
            tmpC = i
    min = sys.float_info.max
    for j in range(height):
        if matrix[j][tmpC] > 0 and matrix[j][width] / matrix[j][tmpC] < min:
            min = matrix[j][width] / matrix[j][tmpC]
            tmpL = j
    print('X' + str(tmpL + 1) + str(tmpC + 1) + ' был выбран разрешающим = ' + str(matrix[tmpL][tmpC]))
    for i in range(width):
        if matrix[tmpL][i] == 1 and basis[i] == 1:
            basis[i] = 0
            basis[tmpC] = 1
            print('Заменяем базисный элемент x' + str(i + 1) + ' на x' + str(tmpC + 1))


def simplexMethod():
    global matrix
    global targetFunction
    mcp = copy.deepcopy(matrix)
    resElem = mcp[tmpL][tmpC]
    for i in range(height):
        if not i == tmpL:
            for j in range(width + 1):
                if not j == tmpC:
                    mcp[i][j] = matrix[i][j] - (matrix[tmpL][j] * matrix[i][tmpC]) / resElem
    for i in range(height):
        if not i == tmpL:
            mcp[i][tmpC] = 0
    tfcp = copy.deepcopy(targetFunction)
    for j in range(width + 1):
        mcp[tmpL][j] = mcp[tmpL][j] / resElem
        tfcp[j] = targetFunction[j] - (matrix[tmpL][j] * targetFunction[tmpC]) / resElem
    targetFunction = tfcp
    matrix = mcp


getSizeInfo()
getFillMatrix()
getTargetFunction()
# matrix = [[16, 18, 9, '<=', 520], [7, 7, 2, '<=', 140], [9, 2, 1, '<=', 810]]
# mainTargetFunction = [1, 2, 0, 0, 'max']
# matrix = [[1, 1, '>=', 4], [-1, 1,  '>=', 2], [1, -1, '<=', 2], [0, 1, '<=', 6]]
# mainTargetFunction = [1, 2, 0, 'max']
# matrix = [[2, 11, '<=', 33], [1, 1,  '=', 7], [4, -5, '>=', 5]]
# mainTargetFunction = [10, 1, 0, 'max']
# matrix = [[2, 1, -3, 0, '<=', 9], [0, 1, 2, -1, '<=', 7], [3, 0, -2, -2, '<=', 4], [1, 1, 1, 1, '<=', 17]]
# mainTargetFunction = [1, -2, 1, 2, 0, 'max']
matrix = [[2, 3, 1, 0, 0, 0, '=', 19], [2, 1, 0, 1, 0, 0, '=', 13], [0, 3, 0, 0, 1, 0, '=', 15], [3, 0, 0, 0, 0, 1, '=', 18]]
mainTargetFunction = [-7, -5, 0, 0, 0, 0, 0, 'min']

#КОЛ-ВО ПЕРЕМЕННЫХ
width = 6
#КОЛ_ВО УРАВНЕНИЙ
height = 4
if mainTargetFunction[width+1] == 'max':
    for i in range(width):
        mainTargetFunction[i] = -mainTargetFunction[i]
canonForm()
getBasis()
addNewVariablesIntoTargetFunction()
targetFunction = copy.deepcopy(mainTargetFunction)
if checkNegativeElementsB(matrix):
    while (checkNegativeElementsB(matrix)):
        methodJordanGauss()
    expressBasis()
else:
    targetFunction = copy.deepcopy(mainTargetFunction)
targetFunction[width] = 0
# Получен опорный базисный план
# Проверяем критерий оптимальности
while checkNegativeElementsIndex(targetFunction):
    getResolvingElement()
    simplexMethod()
for i in range(len(matrix)):
    for j in range(width+1):
        matrix[i][j] = round(float(matrix[i][j]), 2)

for i in range(width+1):
    targetFunction[i] = round(float(targetFunction[i]), 2)

for i in range(len(matrix)):
    print(matrix[i])

print(targetFunction)
sum = 0
for i in range(prevWidth):
    if basis[i] == 1:
        for j in range(height):
            if (matrix[j][i] == 1):
                sum += -mainTargetFunction[i]*matrix[j][width]
                print('x'+str(i+1)+' = '+str(matrix[j][width]))
    else:
        print('x' + str(i + 1) + ' = 0')
if (mainTargetFunction[width+1] == 'max'):
    print('F(x) = ' + str(sum))
else:
    print('F(x) = ' + str(-sum))
