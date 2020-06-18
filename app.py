import os
import sys
import typing

from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

from wordleech import Ui_MainWindow
from worker import LeechWorker


# noinspection PyUnresolvedReferences
class AppWindow(QMainWindow, QObject):
    def __init__(self):
        super().__init__()
        self.ui: Ui_MainWindow = Ui_MainWindow()
        self.dict_file: typing.Optional[str] = None  # The dictionary file
        self.source_files: typing.List[str] = []  # The source files to process

        # Prepare threads and workers
        self.dict_worker: typing.Optional[LeechWorker] = None  # Used to load dictionary
        self.dict_thread: typing.Optional[QtCore.QThread] = None
        self.source_worker: typing.Optional[LeechWorker] = None  # Used to load sources
        self.source_thread: typing.Optional[QtCore.QThread] = None
        self.compare_worker: typing.Optional[LeechWorker] = None  # Used to add words to dictionary
        self.compare_thread: typing.Optional[QtCore.QThread] = None
        self.download_worker: typing.Optional[LeechWorker] = None  # Used to download latest dictionary
        self.download_thread: typing.Optional[QtCore.QThread] = None

        self.lst_found: typing.List[str] = []  # List of new words found
        self.lst_add: typing.List[str] = []  # List of new words to add to dictionary

        self.init_threads()
        self.ui.setupUi(self)
        self.bind_widgets()
        self.show()

    def init_threads(self):
        """
        Initialise the various threads used by the app
        :return: None
        """

        threaded_tasks = ['dict', 'source', 'compare', 'download']

        for task in threaded_tasks:
            worker = LeechWorker()
            worker.status_signal.connect(self.update_status)
            worker.progress_signal.connect(self.update_progress)
            setattr(self, task + '_worker', worker)
            setattr(self, task + '_thread', QtCore.QThread(self))
            getattr(self, task + '_worker').moveToThread(getattr(self, task + '_thread'))

    # noinspection DuplicatedCode
    def bind_widgets(self):
        """
        Bind buttons to functions
        :return: None
        """

        self.ui.btn_load_dict.clicked.connect(self.load_dict)
        self.ui.btn_load_source.clicked.connect(self.load_sources)
        self.ui.btn_process.clicked.connect(self.process_files)
        self.ui.btn_reset.clicked.connect(self.reset)
        self.ui.btn_download_dict.clicked.connect(self.download_dict)
        self.ui.btn_remove_all.clicked.connect(self.remove_all)
        self.ui.btn_remove.clicked.connect(self.remove)
        self.ui.btn_add.clicked.connect(self.add)
        self.ui.btn_add_all.clicked.connect(self.add_all)
        self.ui.btn_generate.clicked.connect(self.write_dict)

    def load_dict(self):
        """
        Set the filename to load the dictionary from
        :return: None
        """

        options = QFileDialog.Options()
        filename = QFileDialog.getOpenFileName(self, "Choose Dictionary File", "",
                                               "Dictionary File (*.dic)", options=options)
        if filename and filename[0] != '':
            self.dict_file = str(filename[0])
            self.ui.lbl_loaded_dict.setText(os.path.basename(self.dict_file))
            self.toggle_process()
        else:
            self.ui.lbl_loaded_dict.setText('No File Loaded.')
            self.dict_file = None

    # noinspection DuplicatedCode
    def download_dict(self):
        """
        Start the thread to download the latest dictionary
        :return: None
        """

        self.ui.btn_process.setEnabled(False)
        self.ui.btn_load_dict.setEnabled(False)
        self.ui.btn_load_source.setEnabled(False)
        self.download_worker.do_run = True
        self.ui.pb_process.setValue(0)
        self.download_worker.callback = self.download_complete
        self.download_thread.started.connect(self.download_worker.download_latest)
        self.download_thread.start()

    def download_complete(self, filename: str):
        """
        Callback when file download is complete
        :param filename: str name of the downloaded file
        :return: None
        """

        self.dict_file = filename
        self.ui.lbl_loaded_dict.setText(os.path.basename(self.dict_file))
        self.ui.lbl_status.setText('Download complete.')
        self.ui.btn_load_dict.setEnabled(True)
        self.ui.btn_load_source.setEnabled(True)
        self.toggle_process()

    def load_sources(self):
        """
        Specify the source filenames to process
        :return: None
        """

        self.source_files.clear()
        options = QFileDialog.Options()
        filenames = QFileDialog.getOpenFileNames(self, "Choose Source Files", "",
                                                 "Portable Document Format (*.pdf)", options=options)

        index = 0
        if filenames:
            if len(filenames[0]) > 0:
                file_paths = filenames[0]
                self.ui.lbl_loaded_sources.setText('')
                for path in file_paths:
                    self.source_files.append(path)
                    char = '' if index == 0 else ', '
                    self.ui.lbl_loaded_sources.setText(
                        self.ui.lbl_loaded_sources.text() + char + os.path.basename(path))
                    index += 1
                self.toggle_process()
            else:
                self.source_files = []
                self.ui.lbl_loaded_sources.setText('No Sources Loaded.')

    def toggle_process(self):
        """
        Check whether or not to enable the Process button
        :return: None
        """

        if self.dict_file is not None and len(self.source_files) > 0:
            self.ui.btn_process.setEnabled(True)

    # noinspection PyUnresolvedReferences
    def process_files(self):
        """
        Start processing. Starts by calling the worker which ingests the dictionary
        :return: None
        """

        self.ui.btn_process.setEnabled(False)
        self.ui.btn_download_dict.setEnabled(False)
        self.ui.btn_load_dict.setEnabled(False)
        self.ui.btn_load_source.setEnabled(False)
        self.dict_worker.do_run = True
        self.ui.pb_process.setValue(0)
        self.dict_worker.target_file = self.dict_file
        self.dict_worker.callback = self.process_files_stage_2
        self.dict_thread.started.connect(self.dict_worker.load_dict)
        self.dict_thread.start()

    def process_files_stage_2(self):
        """
        Callback after dictionary is ingested.
        Starts thread to process source files.
        :return: None
        """

        self.source_worker.do_run = True
        self.source_worker.target_files = self.source_files
        self.source_worker.callback = self.do_compare
        self.source_thread.started.connect(self.source_worker.load_source)
        self.source_thread.start()

    def do_compare(self):
        """
        Callback after source files are processed.
        Starts thread to check for new words.
        :return: None
        """

        self.compare_worker.do_run = True
        self.compare_worker.dict = self.dict_worker.dict
        self.compare_worker.source_words = self.source_worker.source_words
        self.compare_worker.callback = self.show_results
        self.compare_thread.started.connect(self.compare_worker.compare_words)
        self.compare_thread.start()

    def show_results(self):
        """
        Callback after comparison is complete.
        Shows new words found
        :return: None
        """

        self.lst_found = self.compare_worker.new_words
        self.sync_lists()
        self.ui.grp_results.setEnabled(True)
        self.ui.lbl_new.setText('New Words Found ({})'.format(len(self.compare_worker.new_words)))
        self.update_status('Files processed.')
        self.ui.btn_load_dict.setEnabled(True)
        self.ui.btn_load_source.setEnabled(True)
        self.terminate_threads()

    def terminate_threads(self):
        """
        Safely terminates threads and workers
        :return: None
        """

        # Stop workers
        self.dict_worker.do_run = False
        self.source_worker.do_run = False
        self.compare_worker.do_run = False
        self.download_worker.do_run = False

        # Stop threads
        if self.dict_thread.started:
            self.dict_thread.quit()
            self.dict_thread.wait()

        if self.source_thread.started:
            self.source_thread.quit()
            self.source_thread.wait()

        if self.compare_thread.started:
            self.compare_thread.quit()
            self.compare_thread.wait()

        if self.download_thread.started:
            self.download_thread.quit()
            self.download_thread.wait()

    def reset(self):
        """
        Resets app to initial state
        :return: None
        """

        self.terminate_threads()

        # Re-init threads
        self.init_threads()

        self.lst_add.clear()
        self.lst_found.clear()

        # Reset UI
        self.ui.lst_found.clear()
        self.ui.lst_add.clear()
        self.ui.grp_results.setEnabled(False)
        self.ui.btn_process.setEnabled(False)
        self.ui.btn_generate.setEnabled(False)
        self.ui.btn_download_dict.setEnabled(True)
        self.ui.lbl_loaded_sources.setText('No Sources Loaded.')
        self.ui.lbl_loaded_dict.setText('No File Loaded.')
        self.ui.lbl_new.setText('New Words Found')
        self.ui.lbl_add.setText('Words To Add')
        self.dict_file = None
        self.source_files = []
        self.ui.pb_process.setValue(0)
        self.ui.lbl_status.setText('Idle')

        app.processEvents()

    def sync_lists(self):
        """
        Synchronise displayed lists with actual lists
        :return: None
        """

        self.ui.lst_found.clear()
        self.ui.lst_add.clear()
        self.lst_found.sort()
        self.lst_add.sort()
        self.ui.lst_found.addItems(self.lst_found)
        self.ui.lst_add.addItems(self.lst_add)

        total_words = len(self.lst_add) + len(self.lst_found)
        self.ui.lbl_new.setText('New Words Found ({}/{})'.format(len(self.lst_found), total_words))
        self.ui.lbl_add.setText('Words To Add ({})'.format(len(self.lst_add)))

        if len(self.lst_add) > 0:
            self.ui.btn_generate.setEnabled(True)
        else:
            self.ui.btn_generate.setEnabled(False)

    def remove_all(self):
        """
        Remove all words from the list to be added
        :return: None
        """

        self.lst_found.extend(self.lst_add)
        self.lst_add.clear()
        self.sync_lists()

    def remove(self):
        """
        Remove selected word from the list to be added
        :return: None
        """

        if self.ui.lst_add.currentItem():
            self.lst_found.append(self.ui.lst_add.currentItem().text())
            self.lst_add.remove(self.ui.lst_add.currentItem().text())
            self.sync_lists()

    def add(self):
        """
        Add the selected word to the list of words to be added
        :return: None
        """

        if self.ui.lst_found.currentItem():
            self.lst_add.append(self.ui.lst_found.currentItem().text())
            self.lst_found.remove(self.ui.lst_found.currentItem().text())
            self.sync_lists()

    def add_all(self):
        """
        Add all found words to the list of words to be added
        :return: None
        """

        self.lst_add.extend(self.lst_found)
        self.lst_found.clear()
        self.sync_lists()

    def write_dict(self):
        """
        Write a new dictionary to file
        :return: None
        """

        merged_dict = list(set().union(self.dict_worker.dict, self.lst_add))
        merged_dict.sort()

        options = QFileDialog.Options()
        filename = QFileDialog.getSaveFileName(self, "Choose Dictionary File", "",
                                               "Dictionary File (*.dic)", options=options)
        if filename and filename[0] != '':
            save_file = str(filename[0])

            self.update_status("Writing file, please wait...")

            with open(save_file, 'w') as new_dict:
                new_dict.write("%s\n" % len(merged_dict))
                for word in merged_dict:
                    new_dict.write("%s\n" % word)

            self.update_status("New dictionary written to {}".format(save_file))

    @QtCore.pyqtSlot(str)
    def update_status(self, status: str):
        """
        Called by threads to update status label
        :param status: str status to be displayed
        :return: None
        """

        self.ui.lbl_status.setText(status)

    @QtCore.pyqtSlot(int)
    def update_progress(self, progress: int):
        """
        Called by threads to update progress bar
        :param progress: int percentage progress to be displayed
        :return: None
        """

        self.ui.pb_process.setValue(progress)


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
