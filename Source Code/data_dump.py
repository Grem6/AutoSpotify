from csv import reader


def file_dump():


    with open('spotify.csv', 'r') as f_r:
        csv_reader = reader(f_r)
        for index, row in enumerate(csv_reader):
            if index ==0:
                continue
            print(f'Track {row[0]} : {row[1]}')
    print('Library updated!')
    print('Data dumped!')
    print('\n')