import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT
import random

# ------------------ MARQUEE MESSAGES ------------------
MESSAGES = [
    "You are appreciated more than you know.",
    "Kindness is contagious — spread some today!",
    "A smile from you can brighten someone’s day.",
    "Every small step forward counts — keep going!",
    "You’ve got the strength to handle today.",
    "Believe in yourself, because you can do amazing things.",
    "Why don’t skeletons fight each other? They don’t have the guts!",
    "I’m reading a book about anti-gravity — can’t put it down!",
    "Why did the scarecrow win an award? He was outstanding in his field!",
    "Dream big, start small, act now.",
    "Mistakes are proof you are trying.",
    "Push yourself, because no one else is going to do it for you."
]
random.shuffle(MESSAGES)

# ------------------ BROWSER TAB ------------------
class BrowserTab:
    def __init__(self, url="https://www.google.com"):
        self.webview = toga.WebView(url)

# ------------------ MAIN BROWSER APP ------------------
class BrowserApp(toga.App):
    def startup(self):
        self.dark_mode = False
        self.bookmarks = []

        # Main window
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=5))

        # Marquee
        self.marquee_label = toga.Label(
            text=random.choice(MESSAGES),
            style=Pack(padding=5, color='blue')
        )
        self.main_box.add(self.marquee_label)

        # URL bar and buttons
        self.url_box = toga.Box(style=Pack(direction=ROW, padding=5))
        self.url_input = toga.TextInput(style=Pack(flex=1))
        self.go_button = toga.Button('Go', on_press=self.load_url)
        self.back_button = toga.Button('◀', on_press=self.go_back)
        self.forward_button = toga.Button('▶', on_press=self.go_forward)
        self.bookmark_button = toga.Button('★', on_press=self.add_bookmark)
        self.theme_button = toga.Button('🌓', on_press=self.toggle_dark_mode)

        for w in [self.url_input, self.go_button, self.back_button,
                  self.forward_button, self.bookmark_button, self.theme_button]:
            self.url_box.add(w)

        self.main_box.add(self.url_box)

        # Bookmarks bar
        self.bookmark_box = toga.Box(style=Pack(direction=ROW, padding=5))
        self.main_box.add(self.bookmark_box)

        # Tab container
        self.tabs_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        self.main_box.add(self.tabs_box)

        # Create first tab
        self.tabs = []
        self.current_tab_index = 0
        self.add_tab("https://www.google.com")

        # Add main_box to window
        self.main_window = toga.MainWindow(title=self.name)
        self.main_window.content = self.main_box
        self.main_window.show()

        # Start marquee timer
        self.start_marquee()

    # ------------------ TABS ------------------
    def add_tab(self, url):
        tab = BrowserTab(url)
        self.tabs.append(tab)
        if len(self.tabs) == 1:
            self.tabs_box.add(tab.webview)
        self.url_input.value = url

    def current_tab(self):
        return self.tabs[self.current_tab_index]

    # ------------------ NAVIGATION ------------------
    def load_url(self, widget=None):
        url = self.url_input.value
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        self.current_tab().webview.url = url

    def go_back(self, widget=None):
        self.current_tab().webview.go_back()

    def go_forward(self, widget=None):
        self.current_tab().webview.go_forward()

    # ------------------ BOOKMARKS ------------------
    def add_bookmark(self, widget=None):
        url = self.current_tab().webview.url
        if url not in self.bookmarks:
            self.bookmarks.append(url)
            btn = toga.Button(url, on_press=lambda w, u=url: self.load_bookmark(u))
            self.bookmark_box.add(btn)

    def load_bookmark(self, url):
        self.current_tab().webview.url = url
        self.url_input.value = url

    # ------------------ DARK MODE ------------------
    def toggle_dark_mode(self, widget=None):
        self.dark_mode = not self.dark_mode
        color = 'white' if self.dark_mode else 'black'
        bg = 'black' if self.dark_mode else 'white'
        self.main_box.style.update(color=color, background_color=bg)

    # ------------------ MARQUEE ------------------
    def start_marquee(self):
        def update_label():
            self.marquee_label.text = random.choice(MESSAGES)
            self.marquee_label.refresh()
            self.marquee_label._impl.factory.after(3000, update_label)
        update_label()

# ------------------ RUN ------------------
def run_app():
    return BrowserApp('MyBrowser', 'com.example.mybrowser')