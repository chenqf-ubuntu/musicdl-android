'''
MusicDL Android App - Music Downloader
'''
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
import os
import sys
import threading

# Add musicdl path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Debug log
def log(msg):
    print(f"[MusicDL] {msg}")

log("Starting app...")

try:
    from musicdl import MusicClient
    MUSICDL_AVAILABLE = True
    log("musicdl loaded successfully")
except Exception as e:
    MUSICDL_AVAILABLE = False
    log(f"musicdl import error: {e}")

class MusicDLApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        self.title = 'MusicDL'
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(text='MusicDL Music Downloader', font_size='24sp', size_hint_y=0.1, color=(1,1,1,1))
        layout.add_widget(title)
        
        # Status
        self.status_label = Label(
            text=f'Status: {"Ready" if MUSICDL_AVAILABLE else "Module not loaded"}\nVersion: v2.11.3',
            font_size='14sp',
            size_hint_y=0.1,
            color=(0.8,0.8,0.8,1)
        )
        layout.add_widget(self.status_label)
        
        # Search input
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=5)
        self.search_input = TextInput(
            hint_text='Enter song name to search...',
            multiline=False,
            size_hint_x=0.7,
            foreground_color=(1,1,1,1),
            background_color=(0.2,0.2,0.2,1)
        )
        search_layout.add_widget(self.search_input)
        
        search_btn = Button(text='Search', size_hint_x=0.3, background_color=(0.3,0.5,0.8,1))
        search_btn.bind(on_press=self.do_search)
        search_layout.add_widget(search_btn)
        layout.add_widget(search_layout)
        
        # Results area
        scroll = ScrollView(size_hint_y=0.6)
        self.results_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        scroll.add_widget(self.results_layout)
        layout.add_widget(scroll)
        
        # Sources selector
        sources_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=5)
        
        self.btn_netease = Button(text='Netease', background_color=(0.4,0.2,0.6,1))
        self.btn_netease.bind(on_press=lambda x: self.set_source('NeteaseMusicClient'))
        sources_layout.add_widget(self.btn_netease)
        
        self.btn_qq = Button(text='QQ Music', background_color=(0.2,0.4,0.6,1))
        self.btn_qq.bind(on_press=lambda x: self.set_source('QQMusicClient'))
        sources_layout.add_widget(self.btn_qq)
        
        self.btn_kugou = Button(text='Kugou', background_color=(0.6,0.3,0.2,1))
        self.btn_kugou.bind(on_press=lambda x: self.set_source('KugouMusicClient'))
        sources_layout.add_widget(self.btn_kugou)
        
        layout.add_widget(sources_layout)
        
        # Current source
        self.current_source = 'NeteaseMusicClient'
        self.source_label = Label(
            text='Current Source: Netease',
            font_size='12sp',
            size_hint_y=0.05,
            color=(0.6,0.6,0.6,1)
        )
        layout.add_widget(self.source_label)
        
        return layout
    
    def set_source(self, source):
        self.current_source = source
        self.source_label.text = f'Current Source: {source.replace("MusicClient", "")}'
        log(f"Source changed to: {source}")
    
    def do_search(self, instance):
        query = self.search_input.text.strip()
        if not query:
            self.status_label.text = 'Please enter search query'
            log("Empty search query")
            return
        
        self.status_label.text = f'Searching: {query}...'
        self.results_layout.clear_widgets()
        log(f"Searching for: {query}")
        
        if not MUSICDL_AVAILABLE:
            self.status_label.text = 'ERROR: musicdl module not loaded'
            log("musicdl not available")
            self.add_result_item('ERROR: Module not loaded. Check dependencies.')
            return
        
        # Run search in thread to avoid blocking UI
        threading.Thread(target=self._search_thread, args=(query,), daemon=True).start()
    
    def _search_thread(self, query):
        try:
            log(f"Creating client with source: {self.current_source}")
            client = MusicClient(music_sources=[self.current_source])
            
            log("Calling search...")
            results = client.search(query)
            log(f"Search returned: {len(results) if results else 0} results")
            
            if not results:
                Clock.schedule_once(lambda dt: self._update_status('No results found'), 0)
                return
            
            # Display results
            Clock.schedule_once(lambda dt: self._display_results(results), 0)
            
        except Exception as e:
            log(f"Search error: {e}")
            error_msg = str(e)
            Clock.schedule_once(lambda dt: self._update_status(f'Error: {error_msg[:50]}'), 0)
            Clock.schedule_once(lambda dt: self.add_result_item(f'Error: {error_msg}'), 0)
    
    def _update_status(self, text):
        self.status_label.text = text
    
    def _display_results(self, results):
        self.status_label.text = f'Found {len(results)} results'
        self.results_layout.clear_widgets()
        
        for i, song in enumerate(results[:20]):  # Limit to 20 results
            song_name = song.get('song_name', 'Unknown')
            singer = song.get('singer', 'Unknown')
            source = song.get('source', 'Unknown')
            
            text = f'{i+1}. {song_name}\n   Artist: {singer}\n   Source: {source}'
            
            item = Button(
                text=text,
                size_hint_y=None,
                height=80,
                background_color=(0.15, 0.15, 0.2, 1),
                color=(1, 1, 1, 1)
            )
            item.bind(on_press=lambda x, s=song: self.download_song(s))
            self.results_layout.add_widget(item)
    
    def add_result_item(self, text):
        item = Label(
            text=text,
            size_hint_y=None,
            height=60,
            color=(1, 0.5, 0.5, 1)
        )
        self.results_layout.add_widget(item)
    
    def download_song(self, song):
        song_name = song.get('song_name', 'Unknown')
        self.status_label.text = f'Downloading: {song_name}...'
        log(f"Download request: {song_name}")
        
        threading.Thread(target=self._download_thread, args=(song,), daemon=True).start()
    
    def _download_thread(self, song):
        try:
            song_name = song.get('song_name', 'Unknown')
            log(f"Starting download: {song_name}")
            
            client = MusicClient(music_sources=[self.current_source])
            
            # Download to Android external storage
            download_dir = '/storage/emulated/0/MusicDL'
            os.makedirs(download_dir, exist_ok=True)
            log(f"Download directory: {download_dir}")
            
            client.download(song, target_dir=download_dir)
            
            log(f"Download completed: {song_name}")
            Clock.schedule_once(lambda dt: self.status_label.text = f'Downloaded: {song_name}'), 0)
            
        except Exception as e:
            log(f"Download error: {e}")
            error_msg = str(e)
            Clock.schedule_once(lambda dt: self.status_label.text = f'Download Error: {error_msg[:40]}'), 0)

if __name__ == '__main__':
    MusicDLApp().run()