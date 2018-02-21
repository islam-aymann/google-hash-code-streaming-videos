def main():
    a = {1: 1500, 2: 2000, 3: 5000, 4: 100}
    sorted_ends = [(k, v) for v, k in sorted(
        [(v, k) for k, v in a.items()], reverse=True
    )]
    print(sorted_ends)

if __name__ == '__main__':
    main()