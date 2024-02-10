from werkzeug.security import generate_password_hash, check_password_hash

hashed_password = generate_password_hash('password456')
print(hashed_password)


# # Substitute the following values with actual data for testing
# stored_hash = 'scrypt:32768:8:1$kLi5SvtVdyoifzlw$926e4e714452a5576d29000891dbd5d2345dbeb55f4fd31a798d54ea0f94e55058f66a38d18022b49c1a6faccc81747c8339c6036c6dad5e4a67e9e3ab084c9c'
# password_to_check = 'password789'

# # Verify if the password matches the stored hash
# is_valid = check_password_hash(stored_hash, password_to_check)
# print(is_valid)  # Should print True for a match
