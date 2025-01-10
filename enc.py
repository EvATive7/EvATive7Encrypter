import secrets
import hashlib
from pypinyin import pinyin, Style


def get_chinese_characters_with_pinyin_qi():
    start, end = 0x4E00, 0x9FFF
    result = []

    for char_code in range(start, end + 1):
        char = chr(char_code)
        py = pinyin(char, style=Style.NORMAL, heteronym=False)
        if py and py[0][0] == "qi":
            result.append(char)

    return "".join(result)


class EvATive7ENCv1:
    NAME = __name__
    IDENTIFIER = "="
    VERHASH_IDENTIFIER_LENGTH = 0
    CHARSET = "邶柒七0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    # CHARSET = get_chinese_characters_with_pinyin_qi()
    # CHARSET = "!@#$%^&*()_-+/\\邶柒七0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    # CHARSET = "7EATIVeativ邶柒七"

    BASE = len(CHARSET)

    SALT_LENGTH = 7
    HASH_LENGTH = 77
    CHAR_OFFSET = 7
    KEY_LENGTH = 77

    @classmethod
    def key(cls, length: int = None) -> str:
        if not length:
            length = cls.KEY_LENGTH
        return "".join(secrets.choice(cls.CHARSET) for _ in range(length))

    @classmethod
    def _compute_hash(cls, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()[: cls.HASH_LENGTH]

    @classmethod
    def _base_encode(cls, char_code: int) -> str:
        base_repr = ""
        while char_code > 0:
            remainder = char_code % cls.BASE
            base_repr = cls.CHARSET[remainder] + base_repr
            char_code //= cls.BASE
        return base_repr

    @classmethod
    def _base_decode(cls, chars: str) -> int:
        char_code = 0
        for char in chars:
            char_code = char_code * cls.BASE + cls.CHARSET.index(char)
        return char_code

    @classmethod
    def _paragraph_combination(cls, chars: list[str]) -> str:
        result = []
        last_len = None
        for encoded_word in chars:
            cur_len = len(encoded_word)
            if cur_len != last_len:
                result.append(f"{cls.IDENTIFIER}{cls.CHARSET[cur_len]}")
                last_len = cur_len
            result.append(encoded_word)
        return "".join(result)

    @classmethod
    def _paragraph_split(cls, text: str, limit: int = None) -> tuple[list[str], int]:
        segments = []
        i = 0
        while i < len(text):
            if limit:
                if len(segments) == limit:
                    break
            if text[i] == cls.IDENTIFIER:
                length_char = text[i + 1]
                char_length = cls.CHARSET.index(length_char)
                i += 2
            else:
                segments.append(text[i : i + char_length])
                i += char_length
        return segments, i

    @classmethod
    def encode(cls, key: str, text: str) -> str:
        salt = "".join(secrets.choice(cls.CHARSET) for _ in range(cls.SALT_LENGTH))

        integrity_hash = cls._compute_hash(salt + text + key)

        encoded = []
        for index, char in enumerate(text):
            key_char = key[index % len(key)]
            salt_char = salt[index % len(salt)]
            char_code = ord(char) ^ ord(key_char) ^ ord(salt_char)
            char_code += cls.CHAR_OFFSET

            encoded.append(cls._base_encode(char_code))

        result = (
            cls.NAME
            + cls.IDENTIFIER * cls.VERHASH_IDENTIFIER_LENGTH
            + cls._paragraph_combination(
                [cls._base_encode(ord(char)) for char in integrity_hash]
            )
            + salt
            + cls._paragraph_combination(encoded)
        )

        return result

    @classmethod
    def decode(cls, key: str, text: str) -> str:
        if not text.startswith(cls.NAME):
            raise Exception("Invalid encoded text format")

        text = text.removeprefix(cls.NAME)
        text = text.removeprefix(cls.IDENTIFIER * cls.VERHASH_IDENTIFIER_LENGTH)
        integrity_hash_segments, salt_start_index = cls._paragraph_split(
            text, cls.HASH_LENGTH
        )
        integrity_hash = "".join(
            [chr(cls._base_decode(_segment)) for _segment in integrity_hash_segments]
        )
        salt = text[salt_start_index : salt_start_index + cls.SALT_LENGTH]
        text = text[salt_start_index + cls.SALT_LENGTH :]

        segments, _ = cls._paragraph_split(text)
        decoded = []
        key_length = len(key)
        salt_length = len(salt)

        for index, encoded_word in enumerate(segments):
            char_code = cls._base_decode(encoded_word)
            key_char = key[index % key_length]
            salt_char = salt[index % salt_length]
            char_code -= cls.CHAR_OFFSET
            original_char = chr(char_code ^ ord(key_char) ^ ord(salt_char))

            decoded.append(original_char)

        result = "".join(decoded)
        expected_hash = cls._compute_hash(salt + result + key)
        if integrity_hash != expected_hash:
            raise ValueError(
                "Integrity check failed. The encoded text may have been tampered with."
            )

        return result


class EvATive7ENCv1Short(EvATive7ENCv1):
    NAME = '7E1S'

    SALT_LENGTH = 1
    HASH_LENGTH = 1
    KEY_LENGTH = 1
