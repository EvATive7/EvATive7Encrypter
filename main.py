from enc import EvATive7ENCv1
import time

if __name__ == "__main__":
    origin = open("text.txt", "r", encoding="utf-8").read()
    key = EvATive7ENCv1.key(64)

    begin = time.time()
    encoded = EvATive7ENCv1.encode(key, origin)
    end = time.time()
    cost = end - begin

    print(
        f"Cost {cost}, Encoded,\nOrigin length: {len(origin)}, encoded length: {len(encoded)}, Efficiency: {len(origin)/len(encoded)}",
    )
    open("encoded.txt", "w", encoding="utf-8").write(
        f"""=== KEY BEGIN ===
{key}
=== KEY END ===


=== ENCODED BEGIN ===
{encoded}
=== ENCODED END ==="""
    )

    begin = time.time()
    decoded = EvATive7ENCv1.decode(key, encoded)
    end = time.time()
    cost = end - begin

    print(f"Cost {cost}, Decoded")
    open("decoded.txt", "w", encoding="utf-8").write(decoded)

    assert origin == decoded
