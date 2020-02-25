from PyQt5 import QtCore, QtGui, QtWidgets
import wikipedia, sys, nltk, heapq, re, gtts, os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.searchBar = QtWidgets.QLineEdit(self.centralwidget)
        self.searchBar.setGeometry(QtCore.QRect(10, 10, 261, 22))
        self.searchBar.setObjectName("searchBar")
        
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 50, 331, 451))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea1 = QtWidgets.QWidget()
        self.scrollArea1.setGeometry(QtCore.QRect(0, 0, 329, 449))
        self.scrollArea1.setObjectName("scrollArea1")
        
        self.text1 = QtWidgets.QTextEdit(self.scrollArea1)
        self.text1.setGeometry(QtCore.QRect(0, 0, 331, 451))
        self.text1.setObjectName("text1")
        self.scrollArea.setWidget(self.scrollArea1)

        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setGeometry(QtCore.QRect(450, 50, 341, 451))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollArea2 = QtWidgets.QWidget()
        self.scrollArea2.setGeometry(QtCore.QRect(0, 0, 339, 449))
        self.scrollArea2.setObjectName("scrollArea2")
        
        self.text2 = QtWidgets.QTextEdit(self.scrollArea2)
        self.text2.setGeometry(QtCore.QRect(0, 0, 341, 451))
        self.text2.setObjectName("text2")
        self.scrollArea_2.setWidget(self.scrollArea2)

        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(280, 10, 93, 28))
        self.searchButton.setObjectName("searchButton")
        
        self.speak1 = QtWidgets.QPushButton(self.centralwidget)
        self.speak1.setGeometry(QtCore.QRect(250, 510, 93, 28))
        
        self.speak1.setObjectName("speak1")
        self.speak2 = QtWidgets.QPushButton(self.centralwidget)
        self.speak2.setGeometry(QtCore.QRect(700, 510, 93, 28))
        self.speak2.setObjectName("speak2")
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.searchButton.clicked.connect(lambda: self.search(self.searchBar.text()))
        self.speak1.clicked.connect(lambda: self.speak(self.text1.toPlainText()))
        self.speak2.clicked.connect(lambda: self.speak(self.text2.toPlainText()))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.searchBar.setPlaceholderText(_translate("MainWindow", "Type article search here..."))
        self.searchButton.setText(_translate("MainWindow", "Search"))
        self.speak1.setText(_translate("MainWindow", "Speak"))
        self.speak2.setText(_translate("MainWindow", "Speak"))

    def search(self, text):
        self.text1.clear()
        self.text2.clear()
        wiki = wikipedia.WikipediaPage(title=text, redirect=True)
        article = wiki.content
        self.text1.setText(wiki.summary)
        self.text2.setText(summary(article))
        self.searchBar.clear()

    def speak(self, text):
        tts = gtts.gTTS(text=text, lang='en', slow=False)
        # Save an .mp3 of the summary as the current time
        tts.save("summary.mp3")
        # Play previously saved .mp3
        os.system("start summary.mp3")

def summary(str):
    #Get article content from method
    article_text = str
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    # Tokenizes sentences from text
    sentence_list = nltk.sent_tokenize(article_text)
    # Stopwords variable to store all englsih stop words from nltk library
    stopwords = nltk.corpus.stopwords.words('english')
    # Sort through formatted text (with no punctuation) and
    # stores the frequency of each word in word_frequencies dictionary
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    # Gets the maximum frequency value
    maximum_frequncy = max(word_frequencies.values())
    # Divides number of each words frequencies by the most occuring words frequency
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    # Sort through sentence_list to get each individual sentence's
    # score using  word_frequencies_dict
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                # Adjust the number at the end since it
                # makes the algorithm only allow sentences with less than X words
                # X being 30 in this case
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    # Get user input for how long summary should be
    # x = int(input('How long do you want your summary to be?\nNumber of sentences: '))
    # Get the top x sentences from sentence_scores
    summary_sentences = heapq.nlargest(15, sentence_scores, key=sentence_scores.get)
    # Make and print the summary
    summary = ' '.join(summary_sentences)
    # Return summarized text
    return summary

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())