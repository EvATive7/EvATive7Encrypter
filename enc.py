import secrets
import hashlib


class EvATive7ENCv1:
    LENGTHIDENTIFIER = "="
    IDENTIFIER_COUNT_VER_HASH = 1
    CHARSET = "邶柒七0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    # CHARSET = "EvATie7邶柒七"

    BASE = len(CHARSET)
    SALT_LENGTH = 7
    CHAR_OFFSET = 7

    @classmethod
    def key(cls, length: int = 64) -> str:
        if length % 2 != 0:
            raise ValueError("Key length must be even.")
        return "".join(secrets.choice(cls.CHARSET) for _ in range(length))

    @classmethod
    def compute_hash(cls, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    @classmethod
    def encode(cls, key: str, text: str) -> tuple[str, str]:
        salt = "".join(secrets.choice(cls.CHARSET) for _ in range(cls.SALT_LENGTH))

        integrity_hash = cls.compute_hash(salt + text + key)

        encoded = []
        for index, char in enumerate(text):
            key_char = key[index % len(key)]
            salt_char = salt[index % len(salt)]
            char_code = ord(char) ^ ord(key_char) ^ ord(salt_char)
            char_code += cls.CHAR_OFFSET
            base_repr = ""
            while char_code > 0:
                remainder = char_code % cls.BASE
                base_repr = cls.CHARSET[remainder] + base_repr
                char_code //= cls.BASE
            encoded.append(base_repr)

        result = [
            cls.LENGTHIDENTIFIER * cls.IDENTIFIER_COUNT_VER_HASH + integrity_hash + salt
        ]
        last_len = None
        for encoded_word in encoded:
            cur_len = len(encoded_word)
            if cur_len != last_len:
                result.append(f"{cls.LENGTHIDENTIFIER}{cls.CHARSET[cur_len]}")
                last_len = cur_len
            result.append(encoded_word)
        result = cls.__name__ + "".join(result)

        return result

    @classmethod
    def decode(cls, key: str, text: str) -> str:
        if not text.startswith(cls.__name__):
            raise Exception("Invalid encoded text format")

        text = text.removeprefix(cls.__name__)
        text = text.removeprefix(cls.LENGTHIDENTIFIER * cls.IDENTIFIER_COUNT_VER_HASH)
        integrity_hash = text[:64]
        salt = text[64 : 64 + cls.SALT_LENGTH]
        text = text[64 + cls.SALT_LENGTH :]

        segments = []
        i = 0
        while i < len(text):
            if text[i] == cls.LENGTHIDENTIFIER:
                length_char = text[i + 1]
                char_length = cls.CHARSET.index(length_char)
                i += 2
            else:
                segments.append(text[i : i + char_length])
                i += char_length

        decoded = []
        key_length = len(key)
        salt_length = len(salt)

        for index, encoded_word in enumerate(segments):
            char_code = 0
            for char in encoded_word:
                char_code = char_code * cls.BASE + cls.CHARSET.index(char)

            key_char = key[index % key_length]
            salt_char = salt[index % salt_length]
            char_code -= cls.CHAR_OFFSET
            original_char = chr(char_code ^ ord(key_char) ^ ord(salt_char))

            decoded.append(original_char)

        result = "".join(decoded)
        expected_hash = cls.compute_hash(salt + result + key)
        if integrity_hash != expected_hash:
            raise ValueError(
                "Integrity check failed. The encoded text may have been tampered with."
            )

        return result
