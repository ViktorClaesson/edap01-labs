def parse_data(url):
    en = []
    fr = []
    with open(url, 'r') as f:
        for line in f:
            line = line.split()
            language = int(line[0])
            to_add = [float(x.split(':')[1]) for x in line[1:]]
            if language == 0:
                en.append(to_add)
            elif language == 1:
                fr.append(to_add)
    return en, fr

if __name__ == "__main__":
    en, fr = parse_data('data/data.libsvm')
    print(en)
    print(fr)