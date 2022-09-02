import sys
import time
import traceback
from enum import IntEnum, auto
from math import ceil

import deepl
from PySide6.QtCore import QRunnable, Slot, Signal, QObject
from logzero import logger

import deepqt.config as cfg
import deepqt.helpers as hp
import deepqt.quote_protection as qp
import deepqt.structures as st
import deepqt.worker_thread as wt


class Abort(Exception):
    """
    Exception to abort the worker.
    """

    pass


class State(IntEnum):
    """
    The state of the worker.
    """

    WORKING = auto()
    DONE = auto()
    ABORTED = auto()
    QUOTA_EXCEEDED = auto()
    ERROR = auto()


class DeeplSignals(QObject):
    """
    Defines the signals available from a running deepl worker thread.

    Supported signals are:

    error
        An instance of WorkerError.

    result
        Exit code.

    progress
        The file_id, progress message, processed chars, and total chars.

    """

    result = Signal(State)
    error = Signal(wt.WorkerError)
    progress = Signal(str, str, int, int)


# noinspection PyUnresolvedReferences
class DeeplWorker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    DO NO. I REPEAT. DO NOT PUT @Slot() DECORATORS ON THE FUNCTIONS THAT YOU
    CONNECT TO THE SIGNALS. YOU WILL ONLY BE REWARDED WITH SEGFAULTS.

    Signals need to be connected manually.

    Slot:
        abort
    """

    state: State
    current_file_id: str | None
    translator: deepl.Translator
    input_files: dict[str, st.InputFile]
    config: cfg.Config
    total_chars: int
    processed_chars: int

    def __init__(self, translator: deepl.Translator, input_files: dict[str, st.InputFile], config: cfg.Config):
        """
        Initialise the worker thread.

        :param translator: Pre-configured deepl translator.
        :param input_files: The input files to translate.
        :param config: The config to use.
        """

        QRunnable.__init__(self)

        self.state = State.WORKING
        self.current_file_id = None
        self.translator = translator
        self.input_files = input_files
        self.config = config
        self.signals = DeeplSignals()  # Create new signals instance.
        self.processed_chars = 0

    @Slot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """

        # Retrieve args/kwargs here; and fire processing using them.
        try:
            self.total_chars = sum(file.char_count for file in self.input_files.values())
            logger.info(f"Total chars to translate: {self.total_chars}.")
            # Do all the things.
            self.main()
            self.check_aborted()

        except Abort:
            logger.warning("Deepl Aborted.")
            if self.state == State.ABORTED and self.current_file_id is not None:
                self.signals.progress.emit(self.current_file_id, "Translation manually aborted.", None, None)
            self.signals.result.emit(State.ABORTED)

        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit(wt.WorkerError(exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(State.DONE)  # Return the result of the processing

    def main(self):
        """
        The main function of the worker thread.
        """

        self.clean_up_previous_translations()
        self.check_aborted()

        self.partition_input_files()
        self.check_aborted()

        self.translate_input_files()
        self.check_aborted()

    def clean_up_previous_translations(self):
        """
        Clean up any previous translations.
        """
        logger.info("Clearing previous translations.")
        for input_file in self.input_files.values():
            input_file.translation = ""
            input_file.translation_chunks = []

    def partition_input_files(self):
        """
        Partition the input files into text_chunks.
        """

        logger.info("Partitioning input files.")
        for key, input_file in self.input_files.items():
            self.check_aborted()
            self.current_file_id = key
            self.signals.progress.emit(key, "Partitioning file...", None, None)

            if isinstance(input_file, st.TextFile):
                input_file.text_chunks = partition_text(
                    input_file.current_text(), self.config.tl_max_chunks, self.config.tl_min_chunk_size
                )
                # Share chunk statistics.
                chunk_count = len(input_file.text_chunks)
                logger.info(f"Split {input_file.path.name} into {chunk_count} chunks.")
                self.signals.progress.emit(
                    key, f"Split into {chunk_count} {hp.f_plural(chunk_count, 'chunk', 'chunks')}", None, None
                )
            else:
                raise NotImplementedError("Epub support not implemented yet.")

    def translate_input_files(self):
        logger.info("Translating text_chunks.")
        for key, input_file in self.input_files.items():
            self.check_aborted()
            self.current_file_id = key

            if isinstance(input_file, st.TextFile):
                for i, chunk in enumerate(input_file.text_chunks):
                    self.check_aborted()
                    if not chunk:
                        logger.warning(f"Empty chunk {i} in {input_file.path.name}.")
                        continue
                    self.signals.progress.emit(
                        key,
                        f"Translating chunk {i + 1} / {len(input_file.text_chunks)}",
                        self.processed_chars,
                        self.total_chars,
                    )
                    if self.config.tl_mock:
                        logger.info("Mocking translation.")
                        translation = self.translator.translate_text("Proton Beam", source_lang="EN", target_lang="DE")
                        # Pretend that we make progress.
                        self.processed_chars += len(chunk)
                        time.sleep(1)
                    else:
                        translation = self.try_translate(chunk, key)

                    input_file.translation_chunks.append(translation.text)
                    # logger.debug(f"Translation: {translation.text}")
                # Smelt the translation chunks into a single translation.
                input_file.translation = "".join(input_file.translation_chunks)
                # If quote protection was used, remove it.
                if input_file.process_level & st.ProcessLevel.PROTECTED:
                    logger.debug("Restoring quote protection.")
                    input_file.translation = qp.restore(input_file.translation)

                self.signals.progress.emit(
                    key,
                    f"Translated {len(input_file.text_chunks)} / {len(input_file.text_chunks)} "
                    f"{hp.f_plural(len(input_file.text_chunks), 'chunk', 'chunks')}",
                    self.processed_chars,
                    self.total_chars,
                )

    def try_translate(self, chunk: str, key: str) -> deepl.TextResult:
        """
        Try to translate the text.

        :param chunk: The text to translate.
        :param key: The key of the input file. Used for error reporting.
        """
        tries = 1
        while True:
            try:
                t_start = time.time()
                translation = self.translator.translate_text(
                    chunk,
                    source_lang=self.config.lang_from,
                    target_lang=self.config.lang_to,
                    preserve_formatting=self.config.tl_preserve_formatting,
                )
                if translation is None:
                    raise deepl.DeepLException()
                # Claim the chunk as translated.
                self.processed_chars += len(chunk)
                d_time = time.time() - t_start
                # Calculate how long it took per 1000 chars. Update the average.
                time_per_mille = d_time / (len(chunk) / 1000)
                self.config.avg_time_per_mille = hp.weighted_average(self.config.avg_time_per_mille, time_per_mille)
                logger.info(f"Translation took {d_time:.2f} seconds, {time_per_mille:.3f} seconds per 1000 chars.")
                return translation

            except deepl.TooManyRequestsException:
                if tries >= 5:
                    logger.error(f"Too many requests. Aborting.")
                    self.signals.progress.emit(key, "Too many requests. Aborting!", None, None)
                    self.state = State.ERROR
                    raise Abort

                logger.warning(f"Too many requests. Sleeping for 5 seconds.")
                self.signals.progress.emit(key, "Too many requests. Waiting...", None, None)
                time.sleep(5)
                tries += 1
                continue
            except deepl.QuotaExceededException:
                logger.error("Quota exceeded. Aborting.")
                # Don't immediately abort, at least finish the current chunk for a cleaner dump.
                # Merely setting the flag will raise the Abort signal when the next chunk starts.
                self.state = State.QUOTA_EXCEEDED
                self.signals.progress.emit(key, "API Quota Exceeded!", None, None)
                return quota_exceeded_banner()
            except deepl.DeepLException:
                logger.error("Translation failed. Aborting.")
                self.signals.progress.emit(key, "Translation Failed!", None, None)
                self.state = State.ERROR
                raise Abort

    @Slot()
    def abort(self):
        """
        Abort the worker thread.
        """
        self.state = State.ABORTED

    def check_aborted(self):
        """
        Check if the worker thread has been aborted.
        """
        if self.state >= State.ABORTED:
            raise Abort


def partition_text(text: str, max_chunks: int, min_chunk_size: int) -> list[str]:
    """
    Partition the input files into text_chunks.
    The config contains a maximum number of batches and a minimum size of each chunk.
    """
    # Figure out how many buckets we can even fill, since it doesn't make sense to
    # have a lot of buckets if they are all basically empty.
    lines = text.splitlines(keepends=True)
    max_possible_chunks = (len(text) // min_chunk_size) + 1
    bucket_count = min(max_chunks, max_possible_chunks)
    approx_chunk_size = ceil(len(text) / bucket_count)
    # logger.debug(f"Approximate chunk size: {approx_chunk_size}")
    # logger.debug(f"Bucket count: {bucket_count}")

    # Place lines into the buckets so that we have approximately the same number of characters in each chunk.
    chunks = []
    for i in range(bucket_count):
        temp_chunk = []
        current_len = 0
        # Fill text_chunks evenly, and dump the remainder into the last bucket.
        while lines and (current_len < approx_chunk_size or i == bucket_count - 1):
            temp_chunk.append(lines.pop(0))
            current_len += len(temp_chunk[-1])
        # Smelt the temp chunk into a real chunk.
        chunks.append("".join(temp_chunk))

    # Sanity check.
    if text_length(chunks) != len(text):
        logger.error(f"Text length mismatch. Expected {len(text)}, got {text_length(chunks)}.")
        raise ValueError("Text length mismatch.")

    return chunks


def text_length(lines: list[str]) -> int:
    """
    Calculate the length of a list of lines.
    """
    return sum([len(line) for line in lines])


def quota_exceeded_banner() -> deepl.TextResult:
    return deepl.TextResult(
        """
#================================#
          
          QUOTA EXCEEDED   :‘(
          
#================================#

""",
        detected_source_lang="FUBAR",
    )
