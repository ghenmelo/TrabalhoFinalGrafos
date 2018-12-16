def intersecao(y1_r1, y2_r1, y1_r2, y2_r2):
    return ((y1_r1 >= y1_r2) == (y2_r1 <= y2_r2)) and ((y1_r1 <= y1_r2) == (y2_r1 >= y2_r2))


print(intersecao(3, 1, 2, -1))