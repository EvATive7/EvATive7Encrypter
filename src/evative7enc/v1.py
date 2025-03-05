import hashlib
import logging
import secrets
import time


class EvATive7ENCv1:
    _NAME = "EvATive7ENCv1"
    _IDENTIFIER = "="
    _VERHASH_IDENTIFIER_LENGTH = 0
    _CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    _SALT_LENGTH = 7
    _HASH_LENGTH = 64
    _CHAR_OFFSET = 7
    _KEY_LENGTH = 64

    _KEY_BEGIN_MARKER = "=== KEY BEGIN ==="
    _KEY_END_MARKER = "=== KEY END ==="
    _ENCRYPTED_BEGIN_MARKER = "=== ENCRYPTED BEGIN ==="
    _ENCRYPTED_END_MARKER = "=== ENCRYPTED END ==="

    _logger = logging.getLogger(_NAME)

    @classmethod
    def _base(cls):
        return len(cls._CHARSET)

    @classmethod
    def _compute_hash(cls, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()[: cls._HASH_LENGTH]

    @classmethod
    def _base_encode(cls, char_code: int) -> str:
        base_repr = ""
        while char_code > 0:
            remainder = char_code % cls._base()
            base_repr = cls._CHARSET[remainder] + base_repr
            char_code //= cls._base()
        return base_repr

    @classmethod
    def _base_decode(cls, chars: str) -> int:
        char_code = 0
        for char in chars:
            char_code = char_code * cls._base() + cls._CHARSET.index(char)
        return char_code

    @classmethod
    def _paragraph_combination(cls, chars: list[str]) -> str:
        result = []
        last_len = None
        for encrypted_word in chars:
            cur_len = len(encrypted_word)
            if cur_len != last_len:
                result.append(f"{cls._IDENTIFIER}{cls._CHARSET[cur_len]}")
                last_len = cur_len
            result.append(encrypted_word)
        return "".join(result)

    @classmethod
    def _paragraph_split(cls, text: str, limit: int = None) -> tuple[list[str], int]:
        segments = []
        i = 0
        while i < len(text):
            if limit:
                if len(segments) == limit:
                    break
            if text[i] == cls._IDENTIFIER:
                length_char = text[i + 1]
                char_length = cls._CHARSET.index(length_char)
                i += 2
            else:
                segments.append(text[i : i + char_length])
                i += char_length
        return segments, i

    @classmethod
    def _extract(cls, text, start_marker, end_marker) -> str | None:
        start_index = text.find(start_marker) + len(start_marker)
        end_index = text.find(end_marker)
        if start_index != -1 and end_index != -1:
            return text[start_index:end_index].strip()
        else:
            return None

    @classmethod
    def key(cls, length: int = None) -> str:
        if not length:
            length = cls._KEY_LENGTH
        return "".join(secrets.choice(cls._CHARSET) for _ in range(length))

    @classmethod
    def encrypt_to_evative7encformatv1(cls, key: str, text: str) -> str:
        encrypted = cls.encrypt(key, text)
        result = f"""EvATive7ENCv1

{cls._KEY_BEGIN_MARKER}
{key}
{cls._KEY_END_MARKER}


{cls._ENCRYPTED_BEGIN_MARKER}
{encrypted}
{cls._ENCRYPTED_END_MARKER}
"""
        return result

    @classmethod
    def decrypt_from_evative7encformatv1(cls, text: str) -> str:
        if not text.startswith("EvATive7ENCv1"):
            raise Exception("Invalid EvATive7ENCFormatv1")
        key = cls._extract(text, cls._KEY_BEGIN_MARKER, cls._KEY_END_MARKER)
        encrypted = cls._extract(
            text, cls._ENCRYPTED_BEGIN_MARKER, cls._ENCRYPTED_END_MARKER
        )

        return cls.decrypt(key, encrypted)

    @classmethod
    def encrypt(cls, key: str, text: str) -> str:
        begin = time.time()

        salt = "".join(secrets.choice(cls._CHARSET) for _ in range(cls._SALT_LENGTH))
        integrity_hash = cls._compute_hash(salt + text + key)

        encrypted = []
        for index, char in enumerate(text):
            key_char = key[index % len(key)]
            salt_char = salt[index % len(salt)]
            char_code = ord(char) ^ ord(key_char) ^ ord(salt_char)
            char_code += cls._CHAR_OFFSET

            encrypted.append(cls._base_encode(char_code))

        result = (
            cls._NAME
            + cls._IDENTIFIER * cls._VERHASH_IDENTIFIER_LENGTH
            + cls._paragraph_combination(
                [cls._base_encode(ord(char)) for char in integrity_hash]
            )
            + salt
            + cls._paragraph_combination(encrypted)
        )

        end = time.time()
        cls._logger.debug(
            f"Encrypted after {(end-begin)*1000}ms. "
            + f"Origin length: {len(text)}, "
            + f"Encrypted length: {len(result)}, "
            + f"Efficiency: {len(text)/len(result)}"
        )

        return result

    @classmethod
    def decrypt(cls, key: str, text: str) -> str:
        text = text.strip()
        begin = time.time()

        if not text.startswith(cls._NAME):
            raise Exception("Invalid encrypted text format")

        text = text.removeprefix(cls._NAME)
        text = text.removeprefix(cls._IDENTIFIER * cls._VERHASH_IDENTIFIER_LENGTH)
        integrity_hash_segments, salt_start_index = cls._paragraph_split(
            text, cls._HASH_LENGTH
        )
        integrity_hash = "".join(
            [chr(cls._base_decode(_segment)) for _segment in integrity_hash_segments]
        )
        salt = text[salt_start_index : salt_start_index + cls._SALT_LENGTH]
        text = text[salt_start_index + cls._SALT_LENGTH :]

        segments, _ = cls._paragraph_split(text)
        decrypted = []
        key_length = len(key)
        salt_length = len(salt)

        for index, encrypted_word in enumerate(segments):
            char_code = cls._base_decode(encrypted_word)
            key_char = key[index % key_length]
            salt_char = salt[index % salt_length]
            char_code -= cls._CHAR_OFFSET
            original_char = chr(char_code ^ ord(key_char) ^ ord(salt_char))

            decrypted.append(original_char)

        result = "".join(decrypted)
        expected_hash = cls._compute_hash(salt + result + key)
        if integrity_hash != expected_hash:
            raise ValueError(
                "Integrity check failed. The encrypted text may have been tampered with."
            )

        end = time.time()
        cls._logger.debug(f"Decrypted after {(end-begin)*1000}ms")

        return result


class EvATive7ENCv1Short(EvATive7ENCv1):
    _NAME = "7E1S"

    _SALT_LENGTH = 1
    _HASH_LENGTH = 1
    _KEY_LENGTH = 1


class EvATive7ENCv1Chinese(EvATive7ENCv1):
    _NAME = "柒密一"
    _KEY_BEGIN_MARKER = "密钥始"
    _KEY_END_MARKER = "密钥末"
    _ENCRYPTED_BEGIN_MARKER = "密文始"
    _ENCRYPTED_END_MARKER = "密文末"
    _IDENTIFIER = "邶"
    _CHARSET = "七柒丌乞亓亝亟企伎俟倛偈傶僛其凄切刺剘勤吃启吱呇呮咠唘唭啓啔啟喰嘁噐器圻埼夡奇契妻娸婍宿屺岂岐岓崎嵜己帺幾弃忔忮忯忾恓恝悽愒愭愾慼慽憇憩懠戚扢扱扺技抵挈捿掑揭摖支攲敧斉斊旂旗晵暣朞期杞枝栔栖桤桼梩棄棊棋棨棲榿槭檱櫀欫欹欺歧气気氣汔汽沏泣洓淇淒湆湇溪滊漆漬濝濟炁焏猉玂玘琦琪璂甈甭畦畸疧盀盵矵砌碁碕碛碶磎磜磧磩礘示祁祇祈祺禥禨稘稽竒簯簱籏粸紪絜綥綦綨綮綺緀緕緝纃绮缉缼罊耆肐肵脐臍舙艩芑芞芪荠萁萋萕葺蕲薺藄蘄蚑蚔蚚蛣蛴蜝蜞螇螧蟣蟿蠐衹袳裿褀褄觭訖諆諬諿讫豈起趞趿跂踑踖踦蹊躩軙軝迄迉逗邔郪鄿釮錡鏚鐖锜闙隑霋頎颀饑騎騏騹骐骑鬐鬾鬿魌鮨鯕鰭鲯鳍鵸鶀鶈鸂麒麡鼜齊齐齮"
