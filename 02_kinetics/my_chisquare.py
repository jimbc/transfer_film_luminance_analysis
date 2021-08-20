def my_chisquare(computed, observed):
    chi2 = 0.0

    for i in range(len(computed)):
        chi2 += (observed[i] - computed[i]) ** 2
    ndf = len(computed) - 2

    residual = 0.0
    for i in range(len(computed)):
        residual += (observed[i] - (computed[i])) ** 2
    observed_mean = sum(observed) / len(observed)
    observed_sq_devs_from_mean = 0.0
    for i in range(len(observed)):
        observed_sq_devs_from_mean += (observed[i] - observed_mean) ** 2
    try:
        r2 = 1.0 - (float(residual) / float(observed_sq_devs_from_mean))
        return chi2, r2
    except ZeroDivisionError:
        return None, None

if __name__ == '__main__':
    _, r2 = my_chisquare([1, 2, 3, 4, 5], [13, 2, 73, 4, 9])
    print(r2) # -0.4218
    _, r2 = my_chisquare([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    print(r2) # 1.0
    _, r2 = my_chisquare([1, 2, 3, 4, 5], [1, 2, 3, 7, 9])
    print(r2) # 0.4703