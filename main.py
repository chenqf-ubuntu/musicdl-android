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
import os
import sys

# Add musicdl path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from musicdl import MusicClient
    MUSICDL_AVAILABLE = True
except Exception as e:
    MUSICDL_AVAILABLE = False
    print(f"musicdl import error: {e}")

class MusicDLApp(App):
    def build(self):
        self.title = 'MusicDL 音乐下载器'
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(text='🎵 MusicDL 音乐下载器', font_size='24sp', size_hint_y=0.1)
        layout.add_widget(title)
        
        # Status
        self.status_label = Label(
            text=f'musicdl状态: {"已加载" if MUSICDL_AVAILABLE else "未加载"}\n版本: v2.11.3',
            font_size='14sp',
            size_hint_y=0.1
        )
        layout.add_widget(self.status_label)
        
        # Search input
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=5)
        self.search_input = TextInput(
            hint_text='输入歌曲名称搜索...',
            multiline=False,
            size_hint_x=0.7
        )
        search_layout.add_widget(self.search_input)
        
        search_btn = Button(text='搜索', size_hint_x=0.3)
        search_btn.bind(on_press=self.do_search)
        search_layout.add_widget(search_btn)
        layout.add_widget(search_layout)
        
        # Results area
        scroll = ScrollView(size_hint_y=0.6)
        self.results_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        scroll.add_widget(self.results_layout)
        layout.add_widget(scroll)
        
        # Info
        info = Label(
            text='支持: 网易云|酷狗|酷我|咪咕|QQ音乐|千千|B站等',
            font_size='12sp',
            size_hint_y=0.1
        )
        layout.add_widget(info)
        
        return layout
    
    def do_search(self, instance):
        query = self.search_input.text.strip()
        if not query:
            self.status_label.text = '请输入搜索内容'
            return
        
        self.status_label.text = f'正在搜索: {query}...'
        self.results_layout.clear_widgets()
        
        if not MUSICDL_AVAILABLE:
            self.status_label.text = 'musicdl模块未正确加载'
            return
        
        try:
            # Use default sources
            client = MusicClient(
                music_sources=['NeteaseMusicClient', 'QQMusicClient', 'KugouMusicClient']
            )
            
            # Search
            results = client.search(query)
            
            if results:
                for song in results[:10]:
                    song_label = Label(
                        text=f"{song.get('songname', 'Unknown')} - {song.get('singername', 'Unknown')}",
                        font_size='12sp',
                        size_hint_y=None,
                        height=40
                    )
                    self.results_layout.add_widget(song_label)
                self.status_label.text = f'找到 {len(results)} 个结果'
            else:
                self.status_label.text = '未找到结果'
                
        except Exception as e:
            self.status_label.text = f'搜索失败: {str(e)[:30]}'
            self.results_layout.add_widget(Label(text=f'错误详情: {str(e)}', font_size='10sp'))

if __name__ == '__main__':
    MusicDLApp().run()