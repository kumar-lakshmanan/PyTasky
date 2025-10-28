'''
@name: 
@author: kayma
@createdon: "2025-08-25"
@description:
'''

__created__ = "2025-08-25"
__updated__ = "2025-09-19"
__author__  = "kayma"
import sys
import keyword
import os

from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QToolBar, QAction, QWidget 
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt5.QtGui import QColor, QKeySequence
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QSize

from PyQt5.QtWidgets import QShortcut
import kTools
from ptsLib import ptsScriptEditorLexer
from kQt import kQtTools

class ScriptEditorWindow(QMainWindow):
    def __init__(self, parent=None, themeJson=None):
        self.parentObj = parent
        super().__init__(self.parentObj.ui)

        self.setGeometry(200, 100, 900, 600)

        self.ui = self.parentObj.ui
        self.tls = kTools.KTools()
        self.qttls = kQtTools.KQTTools(self.ui)        
        self.themeJson = themeJson
        self.currentScriptContent = self.parentObj.currentScriptContent
        self.currentScriptFile = self.parentObj.currentScriptFile

        # --- Toolbar with buttons ---
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.saveBtn = self.qttls.createAction("Save", self.ui, icon="file_save_as.ico", fn=self.saveScript)
        self.runBtn = self.qttls.createAction("Run", self.ui, icon="control_play_blue.ico", fn=self.runScript)
        self.closeBtn = self.qttls.createAction("Close", self.ui, icon="cross.ico", fn=self.close)
        
        toolbar.addAction(self.runBtn)
        toolbar.addAction(self.saveBtn)
        toolbar.addAction(self.closeBtn)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # QScintilla editor
        self.editor = QsciScintilla()
        layout.addWidget(self.editor)
        
        self.editor.SCN_CHARADDED.connect(self.handle_char_added) #TODO: AUTOCOMPLETE
        
        self.shortcut = QShortcut(QKeySequence("Ctrl+Space"), self.editor) #TODO: AUTOCOMPLETE
        self.shortcut.activated.connect(self.show_completions) #TODO: AUTOCOMPLETE
        
        self.editor.keyPressEvent = self._patched_keypress(self.editor.keyPressEvent) #TODO: AUTOCOMPLETE

        self.setup_editor()
    
    def runScript(self, *arg):
        newContent = self.editor.text()
        if newContent:        
            self.parentObj.console.runCode(newContent)
            
    def saveScript(self, *arg):
        newContent = self.editor.text()
        if self.currentScriptFile and self.tls.isFileExists(self.currentScriptFile):
            self.tls.writeFileContent(self.currentScriptFile, newContent)
            self.qttls.showInformation("Editor", f"Script file {self.currentScriptFile} Saved!")            
                 
    def setup_editor(self):
        """Setup editor with Python syntax highlighting, autocomplete, etc."""
        
        # encoding       
        self.editor.setUtf8(True)
        
        # font
        self.editor.setFont(self._font())  
        
        # Line numbers
        font_metrics = self.editor.fontMetrics()
        self.editor.setMarginsFont(self._font())
        self.editor.setMarginWidth(0, font_metrics.width("0000") + 6)
        self.editor.setMarginLineNumbers(0, True)

        # Indentation
        self.editor.setAutoIndent(True)
        self.editor.setTabWidth(4)
        self.editor.setIndentationGuides(True)
        self.editor.setBackspaceUnindents(True)

        # Brace matching
        self.editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line highlighting
        self.editor.setCaretLineVisible(True)        
     
        #Autocomplete
        self.editor.setAutoCompletionWordSeparators(["."])
        self.editor.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.editor.setAutoCompletionCaseSensitivity(False)
        self.editor.setAutoCompletionThreshold(1)             
        
        # EOL
        self.editor.setEolMode(QsciScintilla.EolMode.EolWindows)
        self.editor.setEolVisibility(False)
                
        # style
        self.editor.setEdgeMode(QsciScintilla.EdgeLine)
        self.editor.setContentsMargins(0, 0, 0, 0)
        
        # margin # folding
        self.editor.setMarginType(0, QsciScintilla.NumberMargin)
        self.editor.setMarginWidth(0, "0000")
        self.editor.setMarginsFont(self._font())
        self.editor.setMarginSensitivity(1, True)
        self.editor.setMarginMarkerMask(1, 0b1111)
        #self.editor.setFolding(QsciScintilla.BoxedFoldStyle, 1)
        self.editor.indicatorDefine(QsciScintilla.SquigglePixmapIndicator, 0)
        
        # caret
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretWidth(2)
                
        #Lexer
        self.lexerSetup()
        
        #Themer
        #self.applyTheme()
      
    def lexerSetup(self):        
        # Lexer for Python
        self.pylexer = ptsScriptEditorLexer.PyCustomLexer(self.editor, self.themeJson)
        #self.pylexer = QsciLexerPython()
        
        self.pylexer.setDefaultFont(self._font())
        self.editor.setLexer(self.pylexer)
        
        # API
        self.api = QsciAPIs(self.pylexer)  
        self._load_base_api()
        self.api.prepare()  

        self.editor.setCaretLineBackgroundColor(QColor("#2c313c"))
        self.editor.setCaretForegroundColor(QColor("#dedcdc"))        
                        
        
    def applyTheme(self):
        
        # bracket matching colors
        self.editor.setMatchedBraceBackgroundColor(QColor("#c678dd"))
        self.editor.setMatchedBraceForegroundColor(QColor("#F2E3E3"))

        #self.editor.setCaretLineBackgroundColor(QColor("#e6f7ff"))   
        
        #self.editor.setFoldMarginColors(QColor("#2c313c"), QColor("#2c313c"))
        #self.editor.setMarginsForegroundColor(QColor("#ff888888"))
        #self.editor.setMarginsBackgroundColor(QColor("#282c34"))
                
        # text_edit.setMarkerBackgroundColor(QColor("#FF0000"), 1)
        # text_edit.setMarkerForegroundColor(QColor("#FFFFFF"), 1)

        # self.editor.setSelectionBackgroundColor(QColor("#333a46"))
        # self.editor.setWhitespaceBackgroundColor(QColor("#2c313c"))
        # self.editor.setWhitespaceForegroundColor(QColor("#ffffff"))
        # self.editor.setIndentationGuidesBackgroundColor(QColor("#dedcdc"))
        # self.editor.setIndentationGuidesForegroundColor(QColor("#dedcdc"))
        # #self.editor.SendScintilla(self.SCI_STYLESETBACK, self.STYLE_DEFAULT, QColor("#282c34"))
        # self.editor.setEdgeColor(QColor("#2c313c"))                
                                     
    def _load_base_api(self):
        """Add Python keywords + available modules in sys.path to autocomplete."""
        # Python keywords
        for kw in keyword.kwlist:
            self.api.add(kw)

        # Builtins
        for b in dir(__builtins__):
            self.api.add(b)

        # Modules available in sys.path
        for path in sys.path:
            if os.path.isdir(path):
                for item in os.listdir(path):
                    if item.endswith(".py"):
                        mod_name = item[:-3]
                        self.api.add(mod_name)
                    elif os.path.isdir(os.path.join(path, item)):
                        self.api.add(item)

    def _font(self):
        return QFont("Consolas", 14)

    def handle_char_added(self, char_ord):
        """Check if '.' was typed, and try to offer completions."""
        if chr(char_ord) == ".":
            line, index = self.editor.getCursorPosition()
            text = self.editor.text(line)[:index]

            # e.g. "tls."
            if text.endswith("."):
                expr = text[:-1].split()[-1]  # last token before '.'
                try:
                    obj = eval(expr, sys.modules)
                    words = dir(obj)

                    # wipe and reload API
                    for w in words:
                        self.api.add(w)
                    self.api.prepare()

                    # trigger autocomplete
                    self.editor.autoCompleteFromAPIs()
                    #self.editor.autoCompletionShowSingle()
                    
                except Exception as e:
                    self.tls.error("Autocomplete failed")
                    self.tls.error(e)    
                    
            elif text and text[-1].isalpha():
                # User is typing a prefix after a dot
                parts = text.split()
                last_token = parts[-1]
                if "." in last_token:
                    try:
                        # split into object part and prefix
                        obj_expr, prefix = last_token.rsplit(".", 1)
                        obj = eval(obj_expr, sys.modules)
                        words = [w for w in dir(obj) if w.startswith(prefix)]
            
                        if words:
                            for w in words:
                                self.api.add(w)
                            self.api.prepare()
                        self.editor.autoCompleteFromAPIs()
                    except Exception as e:
                        pass                    

    def _patched_keypress(self, orig):
        def wrapper(event):
            if event.text() == ".":
                orig(event)  # insert the "."
                self.editor.autoCompleteFromAPIs()
            else:
                orig(event)
        return wrapper
    
    def show_completions(self):
        """Force show completions on Ctrl+Space"""
        self.editor.autoCompleteFromAPIs()
        
    def setText(self, content):
        self.editor.setText(content)
            
# Example usage
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     editor_win = PythonEditorWindow()
#     editor_win.show()
#     sys.exit(app.exec_())
    
# Example usage
if __name__ == "__main__":
    tls = kTools.KTools()
    textContent = tls.getFileContent('G:/pyworkspace/PyTasky/PyTasky.py')
        
    if 'PTS' not in globals():
        themeJson = 'G:/pyworkspace/PyTasky/editortheme.json'
        app = QApplication(sys.argv)
        editor_win = ScriptEditorWindow(None, themeJson)
        editor_win.setText(textContent)
        editor_win.show()
        sys.exit(app.exec_())
    else:
        themeJson = 'editortheme.json'
        PTS.editor_win = ScriptEditorWindow(PTS.ui)
        PTS.editor_win.setWindowModality(Qt.ApplicationModal)
        PTS.editor_win.setText(textContent)
        PTS.editor_win.show()
