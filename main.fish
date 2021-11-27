python main.py --type=encrypt --scramble -i lena_orig.jpg -o lena_tmp.jpg
python main.py --type=encrypt --rotate -i lena_tmp.jpg -o lena_encrypted.jpg

#python combined.py --type=encrypt --invert -i lena_orig.jpg -o lena_encrypted.jpg

python main.py --type=decrypt --rotate -i lena_encrypted.jpg -o lena_tmp.jpg
python main.py --type=decrypt --scramble -i lena_tmp.jpg -o lena_decrypted.jpg

#python combined.py --type=decrypt --invert -i lena_encrypted.jpg -o lena_decrypted.jpg

dl lena_tmp.jpg
