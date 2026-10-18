from httptools import PATHS, report, check_login


def main():
    rezultate = []

    # Testam toate adresele
    for path in PATHS:
        rezultat = report(path)
        rezultat["path"] = path
        rezultate.append(rezultat)

    # Selectam paginile cu statusul 200
    reusite = [
        r for r in rezultate
        if r["status"] == 200
    ]

    # Sortam descrescator dupa timpul de raspuns
    reusite.sort(
        key=lambda r: r["seconds"],
        reverse=True
    )

    # Afisam paginile reusite
    print("Pagini reusite, ordonate dupa timpul de raspuns:")

    for r in reusite:
        print(
            r["path"],
            "-",
            round(r["seconds"], 3),
            "secunde -",
            r["final_url"]
        )

    # Numararea rezultatelor
    nr_reusite = sum(
        1 for r in rezultate
        if r["status"] == 200
    )

    nr_esecuri = len(rezultate) - nr_reusite

    print("\nPagini reusite:", nr_reusite)
    print("Pagini esuate:", nr_esecuri)


if __name__ == "__main__":
    main()
