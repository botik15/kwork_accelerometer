import math

# '''
#     Для ввода пользователя данных используйте эту функцию. Она без проверки вхходных данных(с плавающей точкой или нет, символы есть или нет, натуральное или нет...)
# '''
# def input_data():
#     data = []
#     print('Введите количество входных данных')
#     num = input()
#     for i in range(int(num)):
#         data_1 = []
#         print(f'{i} - {num}')
#         print(f'Введите время:')
#         data_1.append(float(input()))
#         print(f'Введите X:')
#         data_1.append(float(input()))
#         print(f'Введите Y:')
#         data_1.append(float(input()))
#         print(f'Введите Z:')
#         data_1.append(float(input()))
#         data.append(data_1)
#     return data
# data = input_data()

# данные с акселерометра: время в мс, ускорение по оси x, по оси y, по оси z
data = [[0, 0.785, 0.932, 1.101],
        [10, 0.794, 0.909, 1.097],
        [20, 0.789, 0.921, 1.094],
        [30, 0.783, 0.935, 1.091],
        [40, 0.777, 0.943, 1.086],
        [50, 0.774, 0.937, 1.081],
        [60, 0.768, 0.943, 1.078],
        [70, 0.764, 0.936, 1.076],
        [80, 0.758, 0.941, 1.074],
        [90, 0.752, 0.935, 1.071]]

# коэффициент пересчета для ускорения в системе СИ
g = 9.81

# переводим ускорение из g в м/с^2, попутно вычисляя среднее ускорение по трём осям
n = len(data)
ax_sum = 0
ay_sum = 0
az_sum = 0
for i in range(n):
    t, ax, ay, az = data[i]
    ax = ax * g
    ay = ay * g
    az = az * g
    data[i][1] = ax
    data[i][2] = ay
    data[i][3] = az
    ax_sum += ax
    ay_sum += ay
    az_sum += az
ax_avg = ax_sum / n
ay_avg = ay_sum / n
az_avg = az_sum / n

# вычисляем длину вектора ускорения и углы наклона по трем осям
f_avg = math.sqrt(ax_avg ** 2 + ay_avg ** 2 + az_avg ** 2)
teta_x = math.atan2(ax_avg, math.sqrt(ay_avg ** 2 + az_avg ** 2))
teta_y = math.atan2(ay_avg, math.sqrt(ax_avg ** 2 + az_avg ** 2))
teta_z = math.atan2(math.sqrt(ax_avg ** 2 + ay_avg ** 2), az_avg)

# выводим результаты
print("Среднее ускорение по осям (в м/с^2):")
print("ax =", round(ax_avg, 2))
print("ay =", round(ay_avg, 2))
print("az =", round(az_avg, 2))
print("Длина вектора ускорения (в м/с^2):")
print("f =", round(f_avg, 2))
print("Углы наклона по осям (в радианах):")
print("teta_x =", round(teta_x, 2))
print("teta_y =", round(teta_y, 2))
print("teta_z =", round(teta_z, 2))


# интерполируем полиномом Лагранжа экспериментальные точки координаты x и y от времени
def lagrange_interpolation(x, y, t):
    n = len(x)
    p = 0
    for i in range(n):
        a = 1
        b = 1
        for j in range(n):
            if i != j:
                a *= (t - x[j])
                b *= (x[i] - x[j])
        p += y[i] * a / b
    return p


# строим графики изменения координаты x и y от времени
import matplotlib.pyplot as plt
t = [row[0] for row in data]
x = [row[1] for row in data]
y = [row[2] for row in data]



# вычисляем двойной интеграл от полинома Лагранжа
def double_integral(x, y, t):
    n = len(t) - 1
    dt = t[1] - t[0]
    s = 0
    for i in range(n):
        for j in range(n):
            s += lagrange_interpolation(x, y, t[i]) * lagrange_interpolation(x, y, t[j]) * dt ** 2
    return s


# вычисляем пройденное расстояние
s = double_integral(t, x, t) + double_integral(t, y, t)
print("Пройденное расстояние (в м):")
print(round(s, 2))


# Выводим график изменения координаты x и y от времени
plt.plot(t, x, 'ro-', label='x(t)')
plt.plot(t, y, 'bo-', label='y(t)')
plt.xlabel('Время, мс')
plt.ylabel('Ускорение, м/с^2')
plt.legend()
plt.show()
