from django import template


register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def currency(value):
    bank = [
        'Еба', 'еба',
        'Бля', 'бля',
        'Пизд', 'пизд',
        'Хуй', 'хуй',
        'Хуё', 'хуё',
    ]

    new_title = []
    x = value.split()
    for title_words in x:
        cnt = 0
        for bad_words in bank:
            if bad_words in title_words:
                leng = len(title_words) - 1
                new_title.append(title_words[:1] + '*' * leng)
                cnt += 1
        if cnt == 0:
            new_title.append(title_words)

    return ' '.join(new_title)

