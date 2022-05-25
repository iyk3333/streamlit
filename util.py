import json
import random



def BST(lat: list, loc: float, index: str) -> int:
    left = 0
    right = 16330

    ans = 1500
    while left < right:
        mid = (left + right) // 2

        if lat[mid][index] < loc:
            left = mid+1
        else:
            right = mid-1

    return left


def findLocation(latitude: float, longitude: float) -> list:
    json_file_path = 'data/placeInfo.json'
    with open(json_file_path, 'r', encoding='utf-8') as j:
        contents = json.loads(j.read())  # open : r - 읽기모드, w-쓰기모드, a-추가모드

    # print(contents)
    # place = pd.DataFrame(contents)

    for i, j in enumerate(contents):
        j['index'] = i

    place = list(contents)

    lat = list(contents)
    long = list(contents)

    lat.sort(key=lambda x: x['latitude'])
    long.sort(key=lambda x: x['longitude'])

    latLeft = BST(lat, latitude-0.001, 'latitude')
    latRight = BST(lat, latitude+0.001, 'latitude')


    longLeft = BST(long, longitude - 0.001, 'longitude')
    longRight = BST(long, longitude + 0.001, 'longitude')


    latitudeSet = set()
    longitudeSet = set()

    for i in lat[latLeft:latRight+1]:
        latitudeSet.add(i['index'])

    for i in long[longLeft:longRight+1]:
        longitudeSet.add(i['index'])


    result = latitudeSet.intersection(longitudeSet)

    results = []
    if len(result) != 0:
        for i in range(10):
            results.append(place[random.randint(1, len(result))])

    return results
