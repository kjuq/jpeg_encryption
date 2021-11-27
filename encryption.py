import cv2
import argparse

rotation_seed_index = 0
rotation_seed = \
    '2312003203333021'\
    '0112300130323332'\
    '0323133302130302'\
    '3032302212202201'\
    '1223021131201030'\
    '2230101132321001'\
    '0110021000220032'\
    '1223310020311232'\
    '1011212322033023'\
    '1103211311333200'\
    '0233102210312202'\
    '1020223011203311'\
    '3310330321313003'\
    '2202101231310303'\
    '2023021000133231'\
    '1033213131131312'\

invert_seed_index = 0
invert_seed = \
    '0110010120211011'\
    '0112011211120102'\
    '1211121100000202'\
    '2101210011012220'\
    '2010222121101200'\
    '0120222112000020'\
    '1000120120120120'\
    '1200212120021001'\
    '1001102102120122'\
    '2212210212212120'\
    '1122102102210000'\
    '2122122210122100'\
    '0222011201021211'\
    '0122102101110021'\
    '0110212110122110'\
    '0220010100100112'\

scramble_seed = \
    '033099223071015082059137037192139044232189014103'\
    '190227105035066185224080056095072086203236062151'\
    '067114230197209084081073175202079093115052061091'\
    '110002255094133048005125222145161000176020141097'\
    '191243109205214183239140199122200162237228083143'\
    '211053210134226194104154024136012242054129113032'\
    '152246058158179213117147064245193102169173221050'\
    '156009180057100101178092107108244034146198074040'\
    '027212049065184220026030111204047031164075155132'\
    '112043120208186215247087126089098144163229160076'\
    '039207045166070106010250078174195028234006188055'\
    '248187041127150019013042096168121181036085253018'\
    '130235217135116051167219068249231077251218142069'\
    '011148131022172153017119138170016063124128003216'\
    '254182046252038118157123159165088238201007004060'\
    '090196025021177171008149206240241233023001029225'

b_x = 16
b_y = 16
width = 256
height = 256


def rotate_img(img):
    global rotation_seed_index
    dice = int(rotation_seed[rotation_seed_index])
    print(dice)
    rotation_seed_index += 1
    if dice == 0:
        return img
    elif dice == 1:
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif dice == 2:
        return cv2.rotate(img, cv2.ROTATE_180)
    elif dice == 3:
        return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)


def invert_img(img):
    global invert_seed_index
    dice = int(invert_seed[invert_seed_index]) - 1
    invert_seed_index += 1
    return cv2.flip(img, dice)


def scramble_img(img_array, scramble_seed):
    expanded_array = []
    for img_row in img_array:
        for img in img_row:
            expanded_array.append(img)

    seed_lst = scramble_seed_to_idx_lst(scramble_seed)

    shuffled_array = []

    for idx in seed_lst:
        shuffled_array.append(expanded_array[idx])

    reconstructed_arr = []
    for x in range(0, width, b_x):
        reconstructed_arr.append(shuffled_array[x:x+b_x])
    return reconstructed_arr


def scramble_seed_to_idx_lst(scramble_seed):
    index_lst = []
    for i in range(int(width / b_x) * int(height / b_y)):
        left = i * 3
        right = (i + 1) * 3
        index = int(scramble_seed[left:right])
        index_lst.append(index)
    return index_lst


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
            '--invert',
            help='encrypt a picture by inverting',
            action='store_true'
            )
    parser.add_argument(
            '--scramble',
            help='encrypt a picture by scrambling',
            action='store_true'
            )
    parser.add_argument(
            '--rotate',
            help='encrypt a picture by rotating',
            action='store_true'
            )
    parser.add_argument(
            '-i',
            '--input',
            help='specify a file to encrypt',
            metavar='PATH_TO_INPUT'
            )
    parser.add_argument(
            '-o',
            '--output',
            help='specify a destination path to output',
            metavar='PATH_TO_OUTPUT'
            )

    args = parser.parse_args()

    img_reselt = None
    img = cv2.imread(args.input)

    # separation
    img_array = []
    for y in range(0, height, b_y):
        img_row = []
        for x in range(0, width, b_x):
            crop_img = img[y:y+b_y, x:x+b_x]
            img_row.append(crop_img)
        img_array.append(img_row)

    if args.scramble:
        img_array = scramble_img(img_array, scramble_seed)

    for y in range(0, height, b_y):
        img_reselt_row = None
        for x in range(0, width, b_x):
            img = img_array[int(y/16)][int(x/16)]

            if args.rotate:
                img = rotate_img(img)
            if args.invert:
                img = invert_img(img)

            if x == 0:
                img_reselt_row = img
            else:
                img_reselt_row = cv2.hconcat([img_reselt_row, img])
        if y == 0:
            img_reselt = img_reselt_row
        else:
            img_reselt = cv2.vconcat([img_reselt, img_reselt_row])

    cv2.imwrite(args.output, img_reselt)
















