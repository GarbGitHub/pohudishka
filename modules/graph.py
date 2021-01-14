import matplotlib.pyplot as plt


def create_graph(list, graph_img_name):
    y_list = []
    date = []

    for el in reversed(list):
        date.append(el.created_at.strftime("%d.%m.%Y"))
        y_list.append(el.real_weight)

    x_list = (range(0, len(y_list)))

    plt.figure(figsize=(9, 5), dpi=100)
    plt.xticks(x_list, date, rotation=90)
    plt.ylabel('Вес, кг')
    plt.plot(x_list, y_list, marker='.')
    fig = plt.gcf()
    fig.patch.set_facecolor('#f8f9fa')
    fig.subplots_adjust(bottom=0.23)
    print(graph_img_name)

    plt.savefig(graph_img_name, facecolor=fig.get_facecolor(), transparent=True)
    # plt.show()
