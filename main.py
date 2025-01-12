from enc import *
import time

if __name__ == "__main__":
    model = EvATive7ENCv1
    origin = open("txt/text.txt", "r", encoding="utf-8").read()
    # model = EvATive7ENCv1Short
    # origin = "你好，我是邶柒EvATive7。"
    for i in range(1):
        key = model.key()

        begin = time.time()
        encoded = model.encode(key, origin)
        end = time.time()
        cost = end - begin

        print(
            f"Cost {cost}, Encoded,\nOrigin length: {len(origin)}, encoded length: {len(encoded)}, Efficiency: {len(origin)/len(encoded)}",
        )
        open("txt/encoded.txt", "w", encoding="utf-8").write(
            f"""EvATive7ENCv1

=== KEY BEGIN ===
{key}
=== KEY END ===


=== ENCODED BEGIN ===
{encoded}
=== ENCODED END ===
"""
        )

        begin = time.time()
        decoded = model.decode(key, encoded)
        end = time.time()
        cost = end - begin

        print(f"Cost {cost}, Decoded")
        open("txt/decoded.txt", "w", encoding="utf-8").write(decoded)

        assert origin == decoded
