"""
Contains worker which ingests files and performs comparisons
"""

import codecs
import typing
from typing import Callable
from urllib.request import urlopen
from io import StringIO
from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtCore import QObject

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


class LeechWorker(QObject):
    """
    Contains methods for loading a dictionary, loading source files, downloading the latest
    dictionary and comparing words from sources with current dictionary.
    Various methods called in separate threads to prevent UI blockage.

    """

    status_signal = QtCore.pyqtSignal(str)
    progress_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.target_file: typing.Optional[str] = None  # Used for the source file
        self.target_files: typing.List[str] = []  # Used for the source files
        self.dict: typing.List[str] = []  # List of words in the dictionary
        self.source_words: typing.List[str] = []  # List of words from the source files
        self.new_words: typing.List[str] = []  # List of new words found
        self.callback: typing.Optional[Callable] = None  # Stores callback lambda when called as thread
        self.do_run: bool = True  # Worker stops if set to False
        self.lang: str = "English"  # Language for status messages

    @QtCore.pyqtSlot()
    def load_dict(self):
        """
        Loads dictionary from file
        :return: None
        """

        base_status = 'Ingesting Dictionary: ' if self.lang == "English" else "Jinqara d-Dizzjunarju: "
        self.status_signal.emit(base_status)

        dict_length = LeechWorker.file_len(self.target_file)
        count = 1

        with codecs.open(self.target_file, 'r', encoding='utf-8') as dict_file:
            for line in (line for line in dict_file if self.do_run):

                # Skip first line of dict, which contains word count
                if count == 1:
                    count += 1
                    continue

                if self.lang == "English":
                    status = base_status + 'Word {} of {}'.format(count, dict_length)
                else:
                    status = base_status + 'Kelma {} minn {}'.format(count, dict_length)
                self.status_signal.emit(status)
                self.dict.append(line.strip())

                progress = int(round((count / dict_length * 100)))
                self.progress_signal.emit(progress)

                count += 1

        if self.do_run:
            self.callback()
        else:
            self.status_signal.emit("Idle.")
            self.progress_signal.emit(0)

    @QtCore.pyqtSlot()
    def load_source(self):
        """
        Loads source(s) from file(s)
        :return: None
        """

        output_string = StringIO()

        file_count = 1
        for target in (target for target in self.target_files if self.do_run):
            with open(target, 'rb') as in_file:
                if self.lang == "English":
                    base_status = 'Processing source {} of {}'.format(file_count, len(self.target_files))
                else:
                    base_status = 'Ipproċessar tas-sors {} minn {}'.format(file_count, len(self.target_files))
                self.status_signal.emit(base_status)

                parser = PDFParser(in_file)
                doc = PDFDocument(parser)
                res_man = PDFResourceManager()
                device = TextConverter(res_man, output_string, laparams=LAParams())
                interpreter = PDFPageInterpreter(res_man, device)
                pages = PDFPage.create_pages(doc)

                page_list = []
                for page in (page for page in pages if self.do_run):
                    page_list.append(page)

                page_count = 1
                for page in (page for page in page_list if self.do_run):
                    if self.lang == "English":
                        status = base_status + ': Paġna {} minn {}'.format(page_count, len(page_list))
                    else:
                        status = base_status + ': Page {} of {}'.format(page_count, len(page_list))
                    self.status_signal.emit(status)
                    interpreter.process_page(page)

                    progress = int(round((page_count / len(page_list) * 100)))
                    self.progress_signal.emit(progress)

                    page_count += 1

                file_count += 1

        self.source_words = output_string.getvalue().split()

        if self.do_run:
            self.callback()
        else:
            self.status_signal.emit("Idle.")
            self.progress_signal.emit(0)

    @QtCore.pyqtSlot()
    def compare_words(self):
        """
        Compares words in the source file with those in the dictionary, and saves words
        which were not found in the dictionary.
        :return: None
        """

        word_count = 1
        for word in (word for word in self.source_words if self.do_run):
            if self.lang == "English":
                self.status_signal.emit('Checking word {} of {}'.format(word_count, len(self.source_words)))
            else:
                self.status_signal.emit('Titqabbel kelma {} minn {}'.format(word_count, len(self.source_words)))
            self.append_word(word)

            progress = int(round((word_count / len(self.source_words) * 100)))
            self.progress_signal.emit(progress)

            word_count += 1

        self.new_words = list(set(self.new_words))  # Remove duplicates
        self.new_words.sort()

        if self.do_run:
            self.callback()
        else:
            self.status_signal.emit("Idle.")
            self.progress_signal.emit(0)

    @QtCore.pyqtSlot()
    def download_latest(self):
        """
        Downloads the latest version of the dictionary
        :return: None
        """

        url = 'https://github.com/keithvassallomt/maltese_spelling_dict/releases/download/latest/mt_MT.dic'
        stat = 'Downloading latest dictionary' if self.lang == "English" else "Qed jitniżżel dizzjunarju aġġornat"
        self.status_signal.emit(stat)
        save_path = Path.home() / 'mt_MT.dic'
        length = self.urlretrieve(url, str(save_path), self.download_status)

        if length > 0:
            self.callback(save_path)

    def download_status(self, blocks: int, chunk_size: int, total_length: int):
        """
        Updates progress bar as latest dictionary is downloading
        :param blocks: int number of blocks downloaded
        :param chunk_size: int size of this chunk in bytes
        :param total_length: int size of download in bytes
        :return: None
        """
        total_blocks = total_length / chunk_size
        progress = int(round((blocks / total_blocks) * 100))
        self.progress_signal.emit(progress)

        total_size = total_length / 1024 / 1024
        downloaded = (blocks * chunk_size) / 1024 / 1024
        downloaded = total_size if downloaded > total_size else downloaded
        if self.lang == "English":
            download_status = 'Downloaded {0:.2f}MiB of {1:.2f}MiB'.format(downloaded, total_size)
        else:
            download_status = 'Niżlu {0:.2f}MiB minn {1:.2f}MiB'.format(downloaded, total_size)
        self.status_signal.emit(download_status)

    def append_word(self, word: str):
        """
        Adds a word to the list of words from the source file which were not found in the
        dictionary. Removes numbers, symbols not in the Maltese alphabet (or articles/quotes),
        Uppercase words.
        :param word: str word to add to the dictionary
        :return: None
        """

        # Numbers should be ignored
        if word.replace('.', '', 1).isdigit():
            return

        # Only these symbols are accepted
        allowed_symbols = ['a', 'b', 'ċ', 'd', 'e', 'f', 'g', 'ġ', 'h', 'ħ', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                           'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ż', '-', '\'', '`']
        for c in word.lower():
            if c not in allowed_symbols:
                return

        # Ignore words that are entirely uppercase
        if word.upper() == word:
            return

        # Append the word if it is not currently in the dictionary
        if word not in self.dict:
            self.new_words.append(word)

    @staticmethod
    def file_len(filename: str):
        """
        Gets length in bytes of given file
        :param filename: str the file to get the length for
        :return: int length of file in bytes
        """

        with codecs.open(filename, 'r', encoding='utf-8') as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def urlretrieve(self, urllib2_request: str, filepath: str, reporthook: Callable = None, chunk_size: int = 4096):
        """
        Retrieves the file at the given URL
        :param urllib2_request: str URL of the file to retrieve
        :param filepath: str name of the local file to create
        :param reporthook: Callable callback function to call with download progress updates
        :param chunk_size: int how many bytes to download at a time
        :return: int the number of blocks downloaded
        """
        req = urlopen(urllib2_request)

        total_size = 0
        if reporthook:
            try:
                # get response length
                total_size = int(req.getheader('Content-Length'))
            except KeyError:
                reporthook = None

        num_blocks = 0

        with open(filepath, 'wb') as f:
            while True:
                if not self.do_run:
                    return
                data = req.read(chunk_size)
                num_blocks += 1
                if reporthook:
                    # report progress
                    reporthook(num_blocks, chunk_size, total_size)
                if not data:
                    break
                f.write(data)

        # return downloaded block count
        return num_blocks
