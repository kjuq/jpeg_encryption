import cv2

orig_filename = 'lena_orig.jpg'

base = 'lena_orig'
print(base)

filename_70 = base + '_70.jpg'
filename_20 = base + '_20.jpg'

orig_img = cv2.imread('./' + orig_filename)

img_70 = cv2.imread('./' + filename_70)
img_20 = cv2.imread('./' + filename_20)

print('70:', cv2.PSNR(orig_img, img_70))
print('20:', cv2.PSNR(orig_img, img_20))
