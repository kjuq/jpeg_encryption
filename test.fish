#python encryptor.py --type=encrypt --scramble -i lena_orig.jpg -o lena_tmp.jpg
#python encryptor.py --type=encrypt --rotate -i lena_tmp.jpg -o lena_encrypted.jpg

python encryptor.py --type=encrypt --rotate --invert -i lena_orig.jpg -o lena_encrypted.jpg

#python encryptor.py --type=decrypt --rotate -i lena_encrypted.jpg -o lena_tmp.jpg
#python encryptor.py --type=decrypt --scramble -i lena_tmp.jpg -o lena_decrypted.jpg

python encryptor.py --type=decrypt --rotate --invert -i lena_encrypted.jpg -o lena_decrypted.jpg

#dl lena_tmp.jpg
