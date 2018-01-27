# A functional keg tracker with real-world usefulness for a brewery.
# TODO: For V_1_1, add analyses. How long has beer X been in keg Y, then save and compile that data over time.
# TODO: Track and analyze total production volume by site and beer style.
# TODO: Report number of kegs full of each given style.

import pickle
from datetime import datetime

try:
    keg_tracker_file = open('Local storage file path here/keg_tracker_ids.p', 'rb')
    keg_ids = pickle.load(keg_tracker_file)
    keg_tracker_file.close()
except:
    n = int(input('Number of kegs to initialize inventory: '))
    keg_ids = {}

    for k in range(1, n + 1):
        keg_ids[k] = {
            'location': 'brewery',
            'contents': 'empty',
            'keg_date': None,
            'last_change': None,
            'last_change_ord': None
        }


def change_location(keg_id):
    new_location = input('New location for keg #{}: '.format(keg_id))
    keg_ids[keg_id]['location'] = new_location
    now = datetime.now().replace(second=0, microsecond=0)
    keg_ids[keg_id]['last_change'] = 'changed location to {} at {}'.format(new_location, now)
    keg_ids[keg_id]['last_change_ord'] = datetime.toordinal(now)
    print('Location changed to {}.'.format(new_location))
    print()


def change_contents(keg_id):
    old_contents = keg_ids[keg_id]['contents']
    new_contents = input('New contents for keg #{}: '.format(keg_id))
    keg_ids[keg_id]['contents'] = new_contents
    now = datetime.now().replace(second=0, microsecond=0)
    keg_ids[keg_id]['last_change'] = 'changed contents to {} at {}'.format(new_contents, now)
    keg_ids[keg_id]['last_change_ord'] = datetime.toordinal(now)
    if old_contents == 'empty' and new_contents != 'empty':
        keg_ids[keg_id]['keg_date'] = datetime.today().replace(second=0, microsecond=0)
    print('Contents changed to: {}'.format(new_contents))
    print()


def new_keg(num):
    total_new = list(range(0, num))
    for k in total_new:
        new_keg_num = len(keg_ids) + 1
        keg_ids[new_keg_num] = {
                'location': 'brewery',
                'contents': 'empty',
                'keg_date': None,
                'last_change': None,
                'last_change_ord': None
            }
        now = datetime.now().replace(second=0, microsecond=0)
        keg_ids[new_keg_num]['last_change'] = 'keg initialized at {}'.format(now)
    print('{} new kegs created. {} kegs in database.'.format(num, len(keg_ids)))
    print()


def get_one_report(keg_id):
    print('Keg ID no.: {}'.format(keg_id))
    print('Location: {}'.format(keg_ids[keg_id]['location']))
    print('Contents: {}'.format(keg_ids[keg_id]['contents']))
    print('Keg date: {}'.format(keg_ids[keg_id]['keg_date']))
    print('Last change: {}'.format(keg_ids[keg_id]['last_change']))
    print()


def get_all_missing():
    for keg in keg_ids:
        if keg_ids[keg]['location'] != 'brewery' and keg_ids[keg]['location'] != None:
            print('Keg {} is out. Location: {}'.format(keg, keg_ids[keg]['location']))
            days_since_keg = datetime.toordinal(datetime.today()) - datetime.toordinal(keg_ids[keg]['keg_date'])
            print('Kegged {} days ago.'.format(days_since_keg))
            print()


def days_since_change(keg_id):
    today = datetime.today()
    elapsed = datetime.toordinal(today) - keg_ids[keg_id]['last_change_ord']
    return elapsed

loop = True

while loop:
    actions = ['update', 'new keg', 'report', 'exit']
    update_actions = ['location', 'contents', 'exit']
    report_actions = ['all kegs', 'one keg', 'off site kegs', 'exit']
    action = input('Input action (type "update", "new keg", "report", or "exit"): ')
    if action == 'update':
        inner_loop = True
        while inner_loop:
            try:
                keg_id = int(input('Which keg would you like to update? (type ID number 1-{}): '.format(len(keg_ids))))
                update_action = input('What would you like to update? (type "location", "contents", or "exit"): ')
                if update_action == 'location':
                    print('Current location for keg #{}: {}'.format(keg_id, keg_ids[keg_id]['location']))
                    change_location(keg_id)
                    inner_loop = False
                if update_action == 'contents':
                    print('Current contents for keg #{}: {}'.format(keg_id, keg_ids[keg_id]['contents']))
                    change_contents(keg_id)
                    inner_loop = False
                if update_action == 'exit':
                    inner_loop = False
                elif update_action not in update_actions:
                    print('Please provide valid input.')
                    print()
            except:
                print('Please provide valid input.')
                print()
    if action == 'new keg':
        inner_loop = True
        while inner_loop == True:
            num = input('Number of new kegs to initialize (type a number, or "exit": ')
            if num == 'exit':
                inner_loop = False
            else:
                try:
                    num = int(num)
                    new_keg(num)
                    inner_loop = False
                except:
                    print('Please provide valid input.')
                    print()
    if action == 'report':
        inner_loop = True
        while inner_loop:
            report_type = input('Get what report? (type "all kegs," "one keg", "off site kegs", or "exit"): ')
            if report_type == 'all kegs':
                print()
                for keg in keg_ids:
                    get_one_report(keg)
                inner_loop = False
            if report_type == 'one keg':
                try:
                    keg_id = int(input('Keg ID # to report: '))
                    print()
                    get_one_report(keg_id)
                    inner_loop = False
                except:
                    print('Not a valid keg ID #.')
                    print()
            if report_type == 'off site kegs':
                print()
                get_all_missing()
                inner_loop = False
            elif report_type not in report_actions:
                print('Please provide valid input.')
                print()
    if action == 'exit':
        loop = False
    elif action not in actions:
        print('Please provide valid input.')
        print()

# for keg in keg_ids:
#     get_one_report(keg)  # human-friendly reports

keg_tracker_file = open('Local storage file path here/keg_tracker_ids.p', 'wb')
pickle.dump(keg_ids, keg_tracker_file)
keg_tracker_file.close()
