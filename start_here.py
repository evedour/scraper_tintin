print(f'\n########Σύστημα συγκομιδής και δεικτοδότησης σελίδων########\n')
print(f'####Project Γλωσσικής Τεχνολογίας - Σεπτέμβρης 2021####\n')
print('##########################################################')
flag= True
while flag:
    print('Πληκτρολογήστε \"EXIT\" για να κλείσετε το πρόγραμμα')
    user_in = input('Πληκτρολογήστε \"S\" για να τρέξετε τον scraper ή \"V\" για να τρέξετε τη σύγκριση διανυσμάτων: ')
    if user_in.upper() == 'S':
        from Scraper.NewsScrape import main
    elif user_in.upper() == 'V':
        from VectorCompare import vector_compare_main
    if user_in.upper == 'EXIT':
        flag = False
        break
