def links_pagination_generation(total_lines: int, lines_page: int, page: int) -> list:
    """Генерация списка постраничной навигации, присвоение классов"""

    pagination = []
    max_lines = total_lines // lines_page + 1 if total_lines % lines_page == 0 else total_lines // lines_page + 2

    for number in range(1, max_lines):
        link_class = 'page-item'  # class link
        if page == number:
            link_class = 'page-item active'
        pagination.append({'page_id': number, 'link_class': link_class})

    return pagination  # [{'page_id': 1, 'link_class': page-item}, {'page_id': 2, 'link_class': 'page-item active'}]
