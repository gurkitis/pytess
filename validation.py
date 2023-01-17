import re


def validate(name, target_suffix='Output.txt'):
    img_rgx = '<img.*'
    img_content_rgx = '(?<=<img).*(?=/>)'
    errors = 0
    total = 0
    extra_work = 0

    base_rows, out_rows = [], []
    with open('./' + name + '/' + name + 'Base.txt', 'r') as f:
        base_rows = f.readlines()

    with open('./' + name + '/' + name + target_suffix, 'r') as f:
        out_rows = f.readlines()

    for x, base_row in enumerate(base_rows):
        base_words = base_row.split(' ')
        out_words = out_rows[x].split(' ')

        if len(base_words) == len(out_words):
            for y, base_word in enumerate(base_words):
                out_word = out_words[y]
                total += 1
                if re.search(img_rgx, out_word) is not None:
                    content = re.findall(img_content_rgx, out_word)[0]
                    if base_word == content:
                        extra_work += 1
                    continue
                elif not base_word == out_word:
                    errors += 1

    if total > 0:
        errors /= total
        extra_work /= total

    return errors, extra_work
