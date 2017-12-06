import sys ,os
from PySide.QtCore import *
from PySide.QtGui import *

qt_app = QApplication(sys.argv)


class Window(QDialog):

    image_seq = []
    seq_dict = {}

    def __init__(self):

        QDialog.__init__(self)

        main_layout = QGridLayout()

        self.file_viewer1 = self.create_list_box(self.expand_seq)
        self.file_viewer2 = self.create_list_box(lambda *args: None)

        self.directory_viewer = self.create_directory_viewer(QDir.currentPath())

        self.browse_button = self.create_button('browse')

        self.file_viewer1.addItems(self.sequence_compressor(QDir.currentPath()))

        info_label = QLabel('Choose a Directory:')
        all_files = QLabel('All Files')
        expanded_list = QLabel('Expanded List')

        layout_1 = QHBoxLayout()
        layout_2 = QHBoxLayout()
        layout_3 = QHBoxLayout()

        layout_1.addWidget(info_label)
        layout_1.addWidget(self.directory_viewer)
        layout_1.addWidget(self.browse_button)

        layout_2.addWidget(self.file_viewer1)
        layout_2.addWidget(self.file_viewer2)

        layout_3.addWidget(all_files)
        layout_3.addWidget(expanded_list)

        main_layout.addLayout(layout_1, 1, 0)
        main_layout.addLayout(layout_2, 3, 0)
        main_layout.addLayout(layout_3, 2, 0)

        self.setWindowTitle('Image Sequence Viewer')
        self.setMinimumSize(700, 700)
        self.setLayout(main_layout)

    def create_list_box(self, member):
        table = QListWidget()
        table.itemClicked.connect(member)
        return table

    #opens a window to browse and select a folder and then runs the 'sequence_compressor' method using the current path
    def browse(self):
        directory = QFileDialog.getExistingDirectory(self, "Select a Directory", QDir.currentPath())
        self.file_viewer1.clear()
        self.file_viewer2.clear()
        self.directory_viewer.setText(directory)
        self.file_viewer1.addItems(self.sequence_compressor(directory))

    def create_directory_viewer(self, path):
        dir_viewer = QLineEdit(path)
        dir_viewer.setReadOnly(True)
        return dir_viewer

    def create_button(self, text):
        button = QPushButton(text)
        button.clicked.connect(self.browse)
        return button

    #recieves the selected folder and returns a list containing files, folders and image sequences in a condensed format
    def sequence_compressor(self, path):

        temp_seq = []
        final_seq = []
        temp_seq_1 = []
        temp_seq_2 = []
        all_dirs = []
        all_files = []


        for root, dirs, files in os.walk(path, topdown=True):
            all_files = files
            all_dirs = dirs
            break

        if all_dirs:
            for d in all_dirs:
                final_seq.append(d)

        all_files.sort()

        tempname = ''
        tempframe = ''
        count = 0
        last_frame = 0
        token = 0


        for f in all_files:
            y = f.rfind('.')
            z = f.rfind('.', 0, y)
            frame = f[z + 1:y]
            count += 1

            if tempname != f[:z] and tempframe.isdigit():
                temp_seq.append(str(int(tempframe)))

            if tempname == f[:z] and frame.isdigit():
                lfr = int(last_frame)
                fr = int(frame)
                if fr != (lfr + 1):
                    token = 1
                    temp_seq.append(str(int(last_frame)))

            if frame.isdigit() and (tempname != f[:z] or token):
                token = 0
                tempname = f[:z]
                a = f[:z]
                b = len(frame)
                c = f[y + 1:]
                last_frame = frame
                tempframe = frame
                name = '[%s][%s%sd][%s]' % (a, '%', b, c)
                temp_seq.append(name)
                temp_seq.append(str(int(frame)))

            else:
                tempframe = frame
                last_frame = frame

            if len(all_files) == count and tempframe.isdigit():
                temp_seq.append(str(int(tempframe)))

            if not frame.isdigit():
                final_seq.append(f)
            else:
                temp_seq_2.append(f)

        #all the image sequences are formatted and stored in the list final_seq
        if temp_seq:
            c = 0
            temp_seq_1 = []
            for x in temp_seq:
                c = c + 1
                if x.find('[') == 0:
                    y = x + '[' + temp_seq[c] + '-' + temp_seq[c + 1] + ']'
                    temp_seq_1.append(y)
            self.image_seq = []
            self.image_seq = self.image_seq + temp_seq_1
            final_seq += temp_seq_1

        #The Image sequences are stored in a dictionary so they can be easily recalled in the expanded view
        if temp_seq:
            seq_dict = {}
            for x in temp_seq_1:
                num1 = int(x[(x.rfind('-') + 1): x.rfind(']')])
                num2 = int(x[(x.rfind('[') + 1): x.rfind('-')])
                seq_dict.setdefault(x, [])
                for y in range(0, ((num1 + 1) - num2)):
                    seq_dict[x].append(temp_seq_2[0])
                    temp_seq_2.remove(temp_seq_2[0])
            self.seq_dict = seq_dict

        return final_seq

    #checks if the clicked item is an image sequence and expands the image sequence using the 'self.seq_dict' dictionary
    def expand_seq(self):
        self.file_viewer2.clear()
        file = self.file_viewer1.currentItem().text()

        if file in self.image_seq:
            self.file_viewer2.addItems(self.seq_dict[file])

        else:
            self.file_viewer2.addItem(file)

    def run(self):
        self.show()
        qt_app.exec_()


app = Window()

app.run()
