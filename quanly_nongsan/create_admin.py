import bcrypt

password = b"51241994" 
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

print("Mật khẩu đã được băm (sao chép giá trị này vào database):")
print(hashed.decode())