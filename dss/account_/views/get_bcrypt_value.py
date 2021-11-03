import bcrypt
from dss.settings import SECRET_KEY

def get_bcrypt_value(value):
    new_salt =  bcrypt.gensalt() # salt 값 생성
    new_value = str(value).encode('utf-8') # 들어온 값을 str로 형 변환해주고 utf-8 유니코드로 인코딩
    hashed_value = bcrypt.hashpw(new_value, new_salt) # 해쉬값 생성
    decode_hash_value = hashed_value.decode('utf-8') # 바이트형의 해쉬값을 utf-9로 디코딩하여 해쉬값을 문자열로 바꿈.
    return decode_hash_value