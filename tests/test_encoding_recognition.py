import pytest
import deepqt.utils as ut
from tests.helpers import mock_file_path
from tests.mock_files import various_encodings

# Define expected messages tailored for each encoding
expected_messages = {
    "message_utf8.txt": "Hello, 世界! Привет, мир! مرحبا بالعالم!",
    "message_utf16.txt": "Hello, 世界! Привет, мир! مرحبا بالعالم!",
    "message_iso8859-1.txt": "Hello, world! Bonjour, le monde! ¡Hola, mundo!",
    "message_ascii.txt": "Hello, world! Greetings, Earth!",
    "message_shiftjis.txt": "こんにちは、世界！これはShift JISエンコーディングのテキストサンプルです。日本語の文字が正しく表示されることを確認してください。",
    "message_gb2312.txt": "你好，世界! Hello, 世界!",
    "message_euckr.txt": "안녕하세요, 세계! Hello, world!",
    "message_windows1251.txt": "Hello, мир! Привет, world!",
    "message_iso8859-5.txt": "Привет, мир! Hello, world!",
    "message_big5.txt": "你好，世界! Hello, 世界!",
}


@pytest.mark.parametrize("file_name, expected_message", expected_messages.items())
def test_read_text_encoding(file_name, expected_message):
    # Get the file path using mock_file_path
    path = mock_file_path(file_name, module=various_encodings)

    # Guess the encoding using the read_text_encoding function
    guessed_encoding = ut.detect_encoding(path)

    # Read the file with the guessed encoding
    with path.open(encoding=guessed_encoding) as f:
        recovered_message = f.read()

    # Assert that the recovered message matches the expected message
    actual_encoding = file_name.split("_")[1].split(".")[0]

    def simplify(encoding):
        return encoding.lower().replace("-", "").replace("_", "")

    assert simplify(actual_encoding) == simplify(
        guessed_encoding
    ), f"Failed for encoding in {file_name}: Guessed {guessed_encoding}, got {actual_encoding}"
    assert (
        recovered_message == expected_message
    ), f"Failed for encoding in {file_name}: Guessed {guessed_encoding}, got {recovered_message}"

    # Running the wrapper version that combines both tests.
    with ut.read_autodetect_encoding(path) as f:
        recovered_message = f.read()

    assert (
        recovered_message == expected_message
    ), f"Failed for encoding in {file_name}: Got {recovered_message}"
