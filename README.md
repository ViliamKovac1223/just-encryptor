# Just encryptor
Just encryptor (jenc) is cli utility that encrypts standard input and files.
All you need to encrypt and decrypt your data is password.
jenc supports pipes as any standard unix utility.

# Usage
Encrypting standard input

```bash
cat secret_file | jenc -p passwod
echo "secret" | jenc -p password
```

Decrypting standard input

```bash
cat encrypted_secret_file | jenc -dp passwod
```

Encrypting file

```bash
jenc -p password -f secret_file 
```

Decrypting file

```bash
jenc -dp password -f encrypted_secret_file 
```

# All command options
-h # print this help menu

-e # encrypt

-d # decrypt

-p <password> # password to encrypt/decrypt; you have to use this flag

-f <path_to_the_file> # file to encrypt/decrypt

-v # verbose mode

# Installation
In order to execute this file from anywhere you have to have "$HOME/.local/bin" in your "$PATH" (you probably have).
```bash
./install.sh
```

# Uninstallation
```bash
./uninstall.sh
```
