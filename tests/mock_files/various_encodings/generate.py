# Import necessary modules
import codecs


# Define messages tailored for each encoding
messages = {
    "utf-8": "Hello, 世界! Привет, мир! مرحبا بالعالم!",
    "utf-16": "Hello, 世界! Привет, мир! مرحبا بالعالم!",
    "iso-8859-1": "Hello, world! Bonjour, le monde! ¡Hola, mundo!",
    "ascii": "Hello, world! Greetings, Earth!",
    "shift_jis": "こんにちは、世界！これはShift JISエンコーディングのテキストサンプルです。日本語の文字が正しく表示されることを確認してください。",
    "gb2312": "你好，世界! Hello, 世界!",
    "euc_kr": "안녕하세요, 세계! Hello, world!",
    "windows-1251": "Hello, мир! Привет, world!",
    "iso-8859-5": "Привет, мир! Hello, world!",
    "big5": "你好，世界! Hello, 世界!",
}

# Dictionary to map encoding names to file suffixes
suffixes = {
    "utf-8": "utf8",
    "utf-16": "utf16",
    "iso-8859-1": "iso8859-1",
    "ascii": "ascii",
    "shift_jis": "shiftjis",
    "gb2312": "gb2312",
    "euc_kr": "euckr",
    "windows-1251": "windows1251",
    "iso-8859-5": "iso8859-5",
    "big5": "big5",
}

# Write the message to a file in each encoding
for encoding, message in messages.items():
    # Create a file name based on the encoding
    file_name = f"message_{suffixes[encoding]}.txt"

    # Open the file with the specified encoding and write the message
    with codecs.open(file_name, "w", encoding) as file:
        try:
            file.write(message)
            print(f"File created: {file_name}")
        except Exception as e:
            print(f"Failed to write to {file_name} with encoding {encoding}: {e}")

print("Files created for each encoding with the custom message.")
