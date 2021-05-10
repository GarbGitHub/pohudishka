import matplotlib.pyplot as plt


def create_graph(graph_img_name, date, y_list):
    date_format_date = [el.strftime("%d.%m.%Y") for el in date]
    x_list = (range(0, len(y_list)))
    plt.figure(figsize=(9, 5), dpi=100)
    plt.xticks(x_list, date_format_date, rotation=90)
    plt.ylabel('Вес, кг')
    plt.title(f'{date[0].strftime("%d.%m.%Y")} - {date[len(date) - 1].strftime("%d.%m.%Y")}')
    plt.plot(x_list, y_list, marker='.')
    fig = plt.gcf()
    fig.patch.set_facecolor('#f8f9fa')
    fig.subplots_adjust(bottom=0.23)
    plt.savefig(graph_img_name, facecolor=fig.get_facecolor(), transparent=True)
    return f'{date[0].strftime("%d.%m.%Y")} - {date[len(date) - 1].strftime("%d.%m.%Y")}'
