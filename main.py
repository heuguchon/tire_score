import requests


def find_holders():
    products = ['8ce886bf-1d81-4927-bdf2-9281c8264012', 'b6792826-f314-4f50-9efb-35dac2726949', 'f4d80662-a0d4-4848-84ec-978a1eb9b27f', '291b1513-a7a6-4525-8793-c32a74e13493']
    holders = {}

    for product in products:
        page = 1
        while True:
            r = requests.get(f'https://ccx.upbit.com/nx/v1/products/{product}/editions?isOnlyForSale=false&page={page}&size=100&sort=SELL_PRICE_ASC')
            p = r.json()

            for item in p['items']:
                owner_uuid = item['ownerUuid']
                if owner_uuid not in holders:
                    holders[owner_uuid] = {p: 0 for p in products}
                holders[owner_uuid][product] += 1

            if p['isLast']:
                break
            else:
                page += 1

    return holders


def calc_score(holders):
    score = {'8ce886bf-1d81-4927-bdf2-9281c8264012': 10,
             'b6792826-f314-4f50-9efb-35dac2726949': 5,
             'f4d80662-a0d4-4848-84ec-978a1eb9b27f': 2,
             '291b1513-a7a6-4525-8793-c32a74e13493': 1}
    scores = {}
    for holder in holders:
        scores[holder] = sum(score[k] * holders[holder][k] for k in score.keys())

    print(sorted(scores.items(), key = lambda item: item[1], reverse = True))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    holders = find_holders()
    calc_score(holders)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
