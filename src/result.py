import re
import os

def concat(sources, dest):
    emails = []

    for src in sources:
        with open(src, 'r') as f:
            emls = f.readlines()
            emls = [eml.strip('\n') for eml in emls]
            emails.extend(emls)

    with open(dest, 'w') as f:
        f.write('\n'.join(sorted(set(emails))))

def concat_all(directory, dest):
    path = os.path.abspath(directory)
    files = [os.path.join(path, f) for f in os.listdir(directory) if f != dest]
    files = [f for f in files if os.path.isfile(f)]
    print(files)

    emails = []
    for src in files:
        with open(src, 'r') as f:
            emls = f.readlines()
            emls = [eml.strip('\n') for eml in emls]
            emails.extend(emls)

    with open(dest, 'w') as f:
        f.write('\n'.join(sorted(set(emails))))

def main():
    #sources = ['result/sciencedirect.txt',
    #    'result/springer.txt']
    #concat(sources, 'result/total.txt')
    concat_all('result', 'total.txt')
    print('Done')

if __name__ == '__main__':
    main()
