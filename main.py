from pathlib import Path

from parser.leitor import read_csv


def main():
    csv_file_path = Path("data.csv")
    try:
        data = read_csv(csv_file_path)
        for row in data:
            print(row)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        print("CSV file read successfully.")


if __name__ == "__main__":
    main()
