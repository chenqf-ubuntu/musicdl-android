'''
MusicDL Android App - Simple Music Search Demo
Uses public APIs for music search
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
import json
import urllib.request
import urllib.parse

# Simple music search using public APIs
class SimpleMusicSearch:
    def __init__(self):
        self.results = []
    
    def search_netease(self, query):
        """Search Netease Cloud Music"""
        try:
            url = f"https://music.163.com/api/search/get?s={urllib.parse.quote(query)}&type=1&offset=0&limit=10"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode('utf-8'))
            
            songs = []
            if data.get('code') == 200 and data.get('result', {}).get('songs'):
                for song in data['result']['songs'][:10]:
                    artists = ', '.join([a['name'] for a in song.get('artists', [])])
                    songs.append({
                        'name': song['name'],
                        'artist': artists,
                        'id': song['id'],
                        'source': 'Netease'
                    })
            return songs
        except Exception as e:
            print(f"Netease search error: {e}")
            return []
    
    def search_all(self, query):
        """Search all sources"""
        results = self.search_netease(query)
        return results

class MusicDLApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        self.title = 'MusicDL'
        
        self.searcher = SimpleMusicSearch()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='MusicDL Music Search',
            font_size='24sp',
            size_hint_y=0.1,
            color=(1,1,1,1)
        )
        layout.add_widget(title)
        
        # Status
        self.status_label = Label(
            text='Status: Ready\nSearch music from Netease',
            font_size='14sp',
            size_hint_y=0.1,
            color=(0.8,0.8,0.8,1)
        )
        layout.add_widget(self.status_label)
        
        # Search input
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=5)
        self.search_input = TextInput(
            hint_text='Enter song name...',
            multiline=False,
            size_hint_x=0.7,
            foreground_color=(1,1,1,1),
            background_color=(0.2,0.2,0.2,1)
        )
        search_layout.add_widget(self.search_input)
        
        search_btn = Button(
            text='Search',
            size_hint_x=0.3,
            background_color=(0.3,0.5,0.8,1)
        )
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
            text='Tap song to copy ID\nUse Netease ID to download',
            font_size='12sp',
            size_hint_y=0.1,
            color=(0.6,0.6,0.6,1)
        )
        layout.add_widget(info)
        
        return layout
    
    def do_search(self, instance):
        query = self.search_input.text.strip()
        if not query:
            self.status_label.text = 'Please enter search query'
            return
        
        self.status_label.text = f'Searching: {query}...'
        self.results_layout.clear_widgets()
        
        threading.Thread(target=self._search_thread, args=(query,), daemon=True).start()
    
    def _search_thread(self, query):
        try:
            results = self.searcher.search_all(query)
            
            if not results:
                Clock.schedule_once(lambda dt: self._update_status('No results found'), 0)
                Clock.schedule_once(lambda dt: self._add_message('Try different keywords'), 0)
                return
            
            Clock.schedule_once(lambda dt: self._display_results(results), 0)
            
        except Exception as e:
            error_msg = str(e)
            Clock.schedule_once(lambda dt: self._update_status(f'Error: {error_msg[:30]}'), 0)
            Clock.schedule_once(lambda dt: self._add_message(f'Error: {error_msg}'), 0)
    
    def _update_status(self, text):
        self.status_label.text = text
    
    def _add_message(self, text):
        item = Label(
            text=text,
            size_hint_y=None,
            height=60,
            color=(1, 0.5, 0.5, 1)
        )
        self.results_layout.add_widget(item)
    
    def _display_results(self, results):
        self.status_label.text = f'Found {len(results)} songs'
        self.results_layout.clear_widgets()
        
        for i, song in enumerate(results):
            text = f'{i+1}. {song["name"]}\nArtist: {song["artist"]}\nID: {song["id"]} | {song["source"]}'
            
            item = Button(
                text=text,
                size_hint_y=None,
                height=80,
                background_color=(0.15, 0.15, 0.2, 1),
                color=(1, 1, 1, 1)
            )
            item.bind(on_press=lambda x, s=song: self.show_song_info(s))
            self.results_layout.add_widget(item)
    
    def show_song_info(self, song):
        self.status_label.text = f'Song: {song["name"]}\nID: {song["id"]} (copied to clipboard hint)'
        # In a real app, you would copy to clipboard or start download

if __name__ == '__main__':
    MusicDLApp().run()