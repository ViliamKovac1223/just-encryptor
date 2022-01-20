# Just encryptor
Just encryptor (jenc) is cli utility that encrypts standard input.
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

# All command options
-h # print this help menu

-e # encrypt text form standard input

-d # decrypt text from standard input

-p <password> # password to encrypt/decrypt; you have to use this flag

-v # verbose mode

# Installation
In order to execute this program from anywhere you have to have "$HOME/.local/bin" in your "$PATH" (you probably have).
```bash
./install.sh
```

# Uninstallation
```bash
./uninstall.sh
```
