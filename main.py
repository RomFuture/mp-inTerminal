import os, sys, json
import curses
from itertools import count
import time
import threading

import pygame
from mutagen.mp3 import MP3
import random
from music_mix import ML
from Color_Console import *
import locale

locale.setlocale(locale.LC_ALL, '')
pygame.init()
pygame.mixer.init()

current_track = ""

ZASTAVKA = [
r"""_______                   _             _     _           """,
r"""|__   __|                | |           | |   (_)          """,
r"""    | |_ __ __ ___      _| | ___   __ _| |__  _ _ __  ___  """,
r"""    | | '__/ _` \ \ /\ / / |/ _ \ / _` | '_ \| | '_ \/ __| """,
r"""    | | | | (_| |\ V  V /| | (_) | (_| | |_) | | | | \__ \ """,
r"""    |_|_|  \__,_| \_/\_/ |_|\___/ \__,_|_.__/|_|_| |_|___/ """,
r"""                ~ Terminal Beats ~ """]

ART = [
r"""...................--++###""",
r"""...........--++###########""",
r""".......-##################""",
r"""......-+#############+-###""",
r"""......-+######+---.....+##""",
r"""......-+##-............+##""",
r"""......-+##.............+##""",
r"""......-+##.............+##""",
r"""......-+##.............+##""",
r"""......-+##.........--+####""",
r"""......-+##......-#########""",
r"""..--######......##########""",
r"""-#########......-#######+.""",
r"""#########+..........-.....""",
r"""-######+-.................""",
]

################################################################################
# ────────────────────  БЛОК КОНФИГА  ──────────────────────────────────────────
################################################################################

CONFIG_FILE = os.path.join(os.path.dirname(sys.argv[0]), 'config.json')

def load_last_path() -> str | None:
    """Читаем сохранённый путь из config.json (если есть)."""
    try:
        with open(CONFIG_FILE, encoding='utf-8') as f:
            data = json.load(f)
            return data.get('music_folder')
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_last_path(path: str) -> None:
    """Сохраняем выбранный путь в config.json."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump({'music_folder': path}, f, ensure_ascii=False, indent=2)

def get_valid_mp3(folder: str) -> list[str]:
    """Ищет mp3-файлы в папке (без учёта регистра)."""
    return [f for f in os.listdir(folder) if f.lower().endswith('.mp3')]

def ask_music_folder() -> tuple[str, list[str]]:
    """Возвращает (music_folder, music_files), при необходимости спрашивая путь."""
    # 1️⃣  пробуем взять путь из конфига
    last_path = load_last_path()
    if last_path and os.path.isdir(last_path):
        files = get_valid_mp3(last_path)
        if files:                       # всё ок – используем «старый» путь
            print(f'🎵 Использую сохранённую папку: {last_path}')
            return last_path, files
        else:
            print('⚠ Старая папка пуста или в ней нет MP3 – нужно выбрать новую.')

    # 2️⃣  спрашиваем путь у пользователя
    while True:
        raw = input('\nВведите путь к папке с музыкой → ').strip(' "\'')
        folder = os.path.abspath(os.path.expanduser(raw))
        if not os.path.isdir(folder):
            print('⛔ Папка не найдена. Попробуйте ещё раз.')
            continue
        files = get_valid_mp3(folder)
        if not files:
            print('⛔ В указанной папке нет MP3-файлов. Попробуйте другую.')
            continue
        save_last_path(folder)          # 3️⃣  сохраняем удачный выбор
        return folder, files
################################################################################

# ─── основной код ─────────────────────────────────────────────────────────────
music_folder, music_files = ask_music_folder()


music_playing = True

valid_music_files = []
for f in music_files:
    audio = MP3(os.path.join(music_folder, f))
    if round(audio.info.length) >= 60:
        valid_music_files.append(f)

random.shuffle(valid_music_files)
music_list = ML()

def music_list_main(music_file):
    Current_index = valid_music_files.index(music_file)
    Mapa = []
    for item in range(-1,4):
        try:
            Mapa.append(valid_music_files[int(Current_index) + item])
        except:
            continue
    return Mapa


def get_russian_ending(number, forms):
    """
    Возвращает правильное окончание для слова на русском языке.
    forms: [именительная ед., родительная ед., родительная мн.]
    Пример: ["минута", "минуты", "минут"]
    """
    number = int(number)
    if 11 <= number % 100 <= 14:
        return forms[2]
    last_digit = number % 10
    if last_digit == 1:
        return forms[0]
    elif 2 <= last_digit <= 4:
        return forms[1]
    else:
        return forms[2]

def bottom_panel(music_file):
    Nau = MP3(os.path.join(music_folder, music_file)).info.length
    minutes = int(Nau // 60)
    seconds = int(round(Nau % 60))

    min_label = get_russian_ending(minutes, ["минута", "минуты", "минут"])
    sec_label = get_russian_ending(seconds, ["секунда", "секунды", "секунд"])

    return f"{minutes} {min_label} и {seconds} {sec_label}"

def play_current():
    pygame.mixer.music.stop()
    current_file = valid_music_files[music_list.index]
    pygame.mixer.music.load(os.path.join(music_folder, current_file))
    pygame.mixer.music.play()
    return current_file

def stop_current():
    pygame.mixer.music.stop()

def pause_current():
    global music_playing
    if music_playing == True:
        pygame.mixer.music.pause()
        music_playing = False
    else:
        pygame.mixer.music.unpause()
        music_playing = True


def track_watcher():
    global current_track
    while True:
        if not pygame.mixer.music.get_busy() and music_playing is True:
            time.sleep(1)  # небольшая задержка, чтобы не перегружать CPU
            if not pygame.mixer.music.get_busy():
                if music_list.index < len(valid_music_files) - 1:
                    music_list.next_track()
                    current_track = play_current()
        time.sleep(1)


def main_menu(stdscr):
    global current_track
    global music_playing
    curses.curs_set(0)
    menu = ["СЛЕД⏭", "СТОП⏹", "ПРЕД⏮", "ВЫХОД✖"]
    selected = 0
    current_track = play_current()

    threading.Thread(target=track_watcher, daemon=True).start()

    while True:
        if pygame.mixer.music.get_busy() is False and music_playing is True:
            if music_list.index < len(valid_music_files) - 1:
                music_list.next_track()
                current_track = play_current()
        stdscr.clear()
        count = -1
        for item in ZASTAVKA:
            count += 1
            stdscr.addstr(count,10,item)
        # Рисуем пунктирную рамку
        top, left, width = 9, 20, 20
        height = len(menu) + 1

        stdscr.addstr(top, left, '+')
        stdscr.addstr(top, left + width - 1, '+')
        stdscr.addstr(top + height, left, '+')
        stdscr.addstr(top + height, left + width - 1, '+')

        for x in range(left + 1, left + width - 1, 2):
            stdscr.addstr(top, x, '-')
            stdscr.addstr(top + height, x, '-')
        for y in range(top + 1, top + height):
            stdscr.addstr(y, left, '|')
            stdscr.addstr(y, left + width - 1, '|')

        # Пункты меню
        for idx, item in enumerate(menu):
            line = item.ljust(width - 4)
            x = left + 2
            y = top + 1 + idx
            if idx == selected:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, line)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, line)

        # Нижняя панель с информацией
        stdscr.addstr(top + 8, left + 4, bottom_panel(current_track))
        stdscr.addstr(top + 9, left + 9, f"— {current_track}")

        # Лист с музыкой
        list_mapa = music_list_main(current_track)
        count = -1
        for item in list_mapa:
            count += 1
            stdscr.addstr(top + count, left + 30, item)

        #АРТ
        count = -1
        for item in ART:
            count += 1
            stdscr.addstr(top + count - 5, left + 63, item)

        stdscr.nodelay(True)
        stdscr.timeout(100)
        stdscr.refresh()
        key = stdscr.getch()


        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(menu) - 1:
            selected += 1
        elif key in (10, 13):  # Enter
            if menu[selected] == "ВЫХОД✖":
                stop_current()
                break
            elif menu[selected] == "СТОП⏹":
                pause_current()
            elif menu[selected] == "СЛЕД⏭":
                if music_list.index < len(valid_music_files) - 1:
                    music_list.next_track()
                    current_track = play_current()
            elif menu[selected] == "ПРЕД⏮":
                if music_list.index > 0:
                    music_list.last_track()
                    current_track = play_current()



curses.wrapper(main_menu)