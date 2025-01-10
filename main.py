from enc import *
import time

if __name__ == "__main__":
    model = EvATive7ENCv1
    #model = EvATive7ENCv1Short
    for i in range(1):
        origin = open("text.txt", "r", encoding="utf-8").read()
        #origin = "你好，我是邶柒EvATive7。"
        key = model.key()

        begin = time.time()
        encoded = model.encode(key, origin)
        end = time.time()
        cost = end - begin

        print(
            f"Cost {cost}, Encoded,\nOrigin length: {len(origin)}, encoded length: {len(encoded)}, Efficiency: {len(origin)/len(encoded)}",
        )
        open("encoded.txt", "w", encoding="utf-8").write(
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
        open("decoded.txt", "w", encoding="utf-8").write(decoded)

        assert origin == decoded
