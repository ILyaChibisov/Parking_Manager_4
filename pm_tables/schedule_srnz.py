import matplotlib.pyplot as plt


def schedule_srnz(device, srnz_list):
    data = [str(i) for i in srnz_list[0]]
    my_srnz_nolpn = srnz_list[1]
    my_srnz_good = srnz_list[2]
    proc_nolpn = []
    for i in range(len(my_srnz_nolpn)):
        if my_srnz_good[i] == '0':
            my_srnz_good[i] = '1'  # избегаем деления на ноль
        proc_nolpn.append(round(float(my_srnz_nolpn[i]) / (float(my_srnz_good[i]) / 100), 2))

    plt.plot(data, proc_nolpn)
    ax = plt.gca()
    ax.set_xlabel("День")
    ax.set_ylabel("Не распознано %")

    plt.title(f"График СРНЗ устройства: {device}")
    plt.show()


if __name__ == '__menu__':
    menu()


