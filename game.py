import pandas as pd
import random


def vocabularyTest(filename):
    """
    :param filename: file including path
    """

    try:
        df = pd.read_excel(filename)

    except:
        text = "Plesa check filename, path or pip install xlrd openpyxl"
        raise ValueError(text)


    df[["T_puan", "E_puan"]] = df[["T_puan", "E_puan"]].fillna(3).astype(int)

    def saveWorkSheet(data=df):

        data.to_excel(filename, index=False)

        print(f"Worksheet is saved in {filename}\n")
        print("Scores")
        total_puan = data.shape[0] * 3
        print(f"English score: {total_puan}/{total_puan - data.E_puan.sum()}")
        print(f"Turkish score: {total_puan}/{total_puan - data.T_puan.sum()}")

    while True:

        if df.E_puan.sum() == 0 and df.T_puan.sum() == 0:
            print("All words is successfully finished")
            print("Please adds new words in Excel file")
            break

        type = input("== Which is suitable for you?\nEnglish = e\nTurkish = t\nrandom add puan = r\nquit = q\n--> ")

        if type not in ["e", "t", "r", "q"]:
            print("The choice must be one of them \ne, t, r or q\n\n")
            continue

        if type == "q":
            print("\n\n\n...GOOD BYEEEE...\n")
            break

        if type == "r":

            exists = []
            x = 0
            while x < 5:

                if len(df[df["E_puan"] == 0]) + len(df[df["T_puan"] == 0]) < 6:
                    print("breaking to fill random value because zero value reduced")
                    break

                r_index = random.randrange(0, len(df), 1)
                if r_index in exists:
                    continue

                exists.append(r_index)

                language_puan = random.choice(["E_puan", "T_puan"])
                language_p_value = df.at[r_index, language_puan]
                if language_p_value != 0:
                    continue

                df.at[r_index, language_puan] = language_p_value + 1
                print("add puan")
                x += 1

            saveWorkSheet(df)

            continue

        """Generating random range"""
        split_size = 10
        row_count = df.shape[0]
        split_list = []
        for i in range(1, row_count):
            if i % split_size == 0:
                split_list.append(i)

        final_step = random.choice(split_list)
        initial_step = final_step - split_size

        while True:

            if type in ["e", "t"]:
                print("\nChoosing method for test")
                ans = input(
                    f"\n1- Select randomly in {split_size} words\n2- Select randomly in all data\nq = Quit\n-->")

                if ans not in ["1", "2", "q"]:
                    print("The choice must be one of them \n1, 2 or q\n-->")
                    continue

                if ans == "q":
                    type = "q"
                    break

                if ans == "1":
                    initial, final = initial_step, final_step
                    break

                if ans == "2":
                    initial, final = 0, len(df)
                    break

        while True:

            r = random.randrange(initial, final, 1)

            if type == "t":
                p = df.at[r, "T_puan"]
                words = "T"
                puan = "T_puan"

            if type == "e":
                p = df.at[r, "E_puan"]
                words = "E"
                puan = "E_puan"

            english = df.at[r, "E"]

            turkish_string = df.at[r, "T"]

            turkish = df.at[r, "T"].split(",")

            turkish_and_english = turkish + [english]

            if df[puan].sum() == 0:
                saveWorkSheet(df)
                break

            if df[(df.index >= initial) & (df.index < final)][puan].sum() == 0:
                break

            if p == 0:
                continue

            answer = input(f"\n{df.at[r, words]}\n-->")

            if answer == "q":
                saveWorkSheet(df)
                break

            if answer in turkish_and_english:

                print("\nTRUE!!!")

                df.at[r, puan] = p - 1

                print(f"{english} = {turkish_string}\n--Önceki Puan: {p}\n--Yeni Puan: {df.at[r, puan]}")
                continue

            else:

                print("\nFALSE")
                print(f"English: {english}")
                print(f"Turkish: {turkish_string}")

# çalıştır
vocabularyTest(filename="word_list.xlsx")
