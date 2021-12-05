import cv2
import argparse
import random

# {{{ SEEDS
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

scramble_pre_seed = '1234'

# }}}

rotation_seed_index = 0
invert_seed_index = 0

b_x = 120
b_y = 120
width = 1920
height = 1080

assert width % b_x == 0
assert height % b_y == 0

h_block_num = int(width / b_x)
v_block_num = int(height / b_y)

block_num = h_block_num * v_block_num
digit = len(str(block_num))


def generate_scramble_seed(pre_seed):
    random.seed(pre_seed)

    perm = [str(i).zfill(digit) for i in range(block_num)]
    random.shuffle(perm)

    scramble_seed = ''.join(perm)

    return scramble_seed


def rotate_img(img):
    global rotation_seed_index
    dice = int(rotation_seed[rotation_seed_index])
    rotation_seed_index += 1
    if dice == 0:
        return img
    elif dice == 1:
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif dice == 2:
        return cv2.rotate(img, cv2.ROTATE_180)
    elif dice == 3:
        return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)


def unrotate_img(img):
    global rotation_seed_index
    dice = int(rotation_seed[rotation_seed_index])
    rotation_seed_index += 1
    if dice == 0:
        return img
    elif dice == 1:
        return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif dice == 2:
        return cv2.rotate(img, cv2.ROTATE_180)
    elif dice == 3:
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)


def invert_img(img):
    global invert_seed_index
    dice = int(invert_seed[invert_seed_index]) - 1
    invert_seed_index += 1
    return cv2.flip(img, dice)


def uninvert_img(img):
    global invert_seed_index
    dice = int(invert_seed[invert_seed_index]) - 1
    invert_seed_index += 1
    return cv2.flip(img, dice)


def scramble_img(img_array):
    expanded_array = []
    for img_row in img_array:
        for img in img_row:
            expanded_array.append(img)

    seed_lst = scramble_seed_to_idx_lst(scramble_seed)

    shuffled_array = []

    for idx in seed_lst:
        shuffled_array.append(expanded_array[idx])

    reconstructed_arr = []
    for x in range(0, block_num, h_block_num):
        reconstructed_arr.append(shuffled_array[x:x + h_block_num])
    return reconstructed_arr


def unscramble_img(img_array):
    expanded_array = []
    for img_row in img_array:
        for img in img_row:
            expanded_array.append(img)
    unshuffled_arr = unshuffle_array(expanded_array, scramble_seed)
    reconstructed_arr = []
    for x in range(0, block_num, h_block_num):
        reconstructed_arr.append(unshuffled_arr[x:x + h_block_num])
    return reconstructed_arr


def scramble_seed_to_idx_lst(scramble_seed):
    index_lst = []
    for i in range(int(width / b_x) * int(height / b_y)):
        left = i * digit
        right = (i + 1) * digit
        index = int(scramble_seed[left:right])
        index_lst.append(index)
    return index_lst


def seed_to_index_lst(scramble_seed):
    index_lst = []
    for i in range(int(width / b_x) * int(height / b_y)):
        left = i * digit
        right = (i + 1) * digit
        index = int(scramble_seed[left:right])
        index_lst.append(index)
    return index_lst


def unshuffle_array(array, seed):
    # https://crypto.stackexchange.com/questions/78309#answers-header
    index_lst = seed_to_index_lst(seed)
    zipped_lst = list(zip(array, index_lst))
    zipped_lst.sort(key=lambda x: x[1])
    return [a for (a, b) in zipped_lst]


if __name__ == '__main__':  # noqa: W391
    # parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--type',
        choices=['encrypt', 'decrypt'],
        help='specify what you\'d like to do',
        required=True
    )
    parser.add_argument(
        '--invert',
        help='encrypt/decrypt a picture by inverting',
        action='store_true'
    )
    parser.add_argument(
        '--scramble',
        help='encrypt/decrypt a picture by scrambling',
        action='store_true'
    )
    parser.add_argument(
        '--rotate',
        help='encrypt/decrypt a picture by rotating',
        action='store_true'
    )
    parser.add_argument(
        '-i',
        '--input',
        help='specify a file to encrypt/decrypt',
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

    assert img is not None, 'Failed to load the image'

    # separation
    img_array = []
    for y in range(0, height, b_y):
        img_row = []
        for x in range(0, width, b_x):
            crop_img = img[y:y + b_y, x:x + b_x]
            img_row.append(crop_img)
        img_array.append(img_row)

    # scramble
    scramble_seed = generate_scramble_seed(scramble_pre_seed)

    if args.scramble and args.type == 'encrypt':
        img_array = scramble_img(img_array)

    # (un)rotate and (un)invert
    for y, img_row in enumerate(img_array):
        for x, img in enumerate(img_row):
            if args.type == 'encrypt':
                if args.rotate:
                    img_array[y][x] = rotate_img(img)
                if args.invert:
                    img_array[y][x] = invert_img(img)
            elif args.type == 'decrypt':
                if args.rotate:
                    img_array[y][x] = unrotate_img(img)
                if args.invert:
                    img_array[y][x] = uninvert_img(img)

    # unscramble
    if args.scramble and args.type == 'decrypt':
        img_array = unscramble_img(img_array)

    # reconstructe image
    for y, img_row in enumerate(img_array):
        img_reselt_row = None
        for x, img in enumerate(img_row):
            if x == 0:
                img_reselt_row = img
            else:
                img_reselt_row = cv2.hconcat([img_reselt_row, img])
        if y == 0:
            img_reselt = img_reselt_row
        else:
            img_reselt = cv2.vconcat([img_reselt, img_reselt_row])

    cv2.imwrite(args.output, img_reselt)









