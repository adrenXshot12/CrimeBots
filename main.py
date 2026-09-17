import os
import json
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup


# =========================
# مورس
# =========================

MORSE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..',
    'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..',
    '9': '----.'
}

REVERSE_MORSE = {v: k for k, v in MORSE.items()}


class CrimeBot(App):

    def build(self):
        self.title = "CRIME BOT 2.0"

        self.data_file = os.path.join(
            self.user_data_dir,
            "crime_data.json"
        )

        self.data = self.load_data()

        return self.home()

    # =========================
    # داده‌ها
    # =========================

    def default_data(self):
        return {
            "cases": [],
            "clues": [],
            "people": [],
            "witnesses": [],
            "timeline": [],
            "notes": []
        }

    def load_data(self):
        if not os.path.exists(self.data_file):
            return self.default_data()

        try:
            with open(
                self.data_file,
                "r",
                encoding="utf-8"
            ) as f:
                data = json.load(f)

            base = self.default_data()

            for key in base:
                if key not in data:
                    data[key] = []

            return data

        except Exception:
            return self.default_data()

    def save_data(self):
        os.makedirs(
            os.path.dirname(self.data_file),
            exist_ok=True
        )

        with open(
            self.data_file,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                self.data,
                f,
                ensure_ascii=False,
                indent=4
            )

    # =========================
    # ابزار رابط
    # =========================

    def clear(self):
        self.root.clear_widgets()

    def button(self, text, callback):
        b = Button(
            text=text,
            size_hint_y=None,
            height=60
        )
        b.bind(on_press=callback)
        return b

    def page(self, title):

        layout = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=8
        )

        layout.add_widget(
            Label(
                text=title,
                font_size=25,
                size_hint_y=None,
                height=65
            )
        )

        return layout

    def show_message(self, title, text):

        Popup(
            title=title,
            content=Label(text=text),
            size_hint=(0.9, 0.5)
        ).open()

    # =========================
    # صفحه اصلی
    # =========================

    def home(self, *args):

        layout = self.page(
            "🕵️ CRIME BOT 2.0\nPersonal Investigation"
        )

        scroll = ScrollView()

        box = BoxLayout(
            orientation="vertical",
            spacing=8,
            size_hint_y=None
        )

        box.bind(
            minimum_height=box.setter("height")
        )

        buttons = [
            ("📁 پرونده‌ها", self.cases_page),
            ("🔎 سرنخ‌ها", self.clues_page),
            ("👤 افراد", self.people_page),
            ("👁️ شاهدها", self.witnesses_page),
            ("⏱️ خط زمانی", self.timeline_page),
            ("📝 یادداشت تحقیق", self.notes_page),
            ("📊 خلاصه پرونده", self.summary_page),
            ("🔐 رمزگشای مورس", self.morse_page),
        ]

        for text, callback in buttons:
            box.add_widget(
                self.button(text, callback)
            )

        scroll.add_widget(box)
        layout.add_widget(scroll)

        return layout

    # =========================
    # پرونده‌ها
    # =========================

    def cases_page(self, *args):

        self.clear()

        layout = self.page("📁 پرونده‌ها")

        if not self.data["cases"]:
            layout.add_widget(
                Label(
                    text="❌ هیچ پرونده‌ای وجود ندارد."
                )
            )

        else:
            for case in self.data["cases"]:
                layout.add_widget(
                    self.button(
                        "📁 " + case,
                        lambda x, c=case:
                        self.case_info(c)
                    )
                )

        layout.add_widget(
            self.button(
                "➕ پرونده جدید",
                self.new_case
            )
        )

        layout.add_widget(
            self.button(
                "↩️ برگشت",
                self.go_home
            )
        )

        self.root.add_widget(layout)

    def new_case(self, *args):

        box = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        name = TextInput(
            hint_text="نام پرونده",
            multiline=False
        )

        box.add_widget(name)

        save = Button(
            text="ذخیره",
            size_hint_y=None,
            height=60
        )

        box.add_widget(save)

        popup = Popup(
            title="➕ پرونده جدید",
            content=box,
            size_hint=(0.9, 0.5)
        )

        def create(instance):

            value = name.text.strip()

            if not value:
                return

            if value not in self.data["cases"]:
                self.data["cases"].append(value)
                self.save_data()

            popup.dismiss()
            self.cases_page()

        save.bind(on_press=create)

        popup.open()

    def case_info(self, case):

        self.show_message(
            "📁 پرونده",
            f"پرونده انتخاب‌شده:\n\n{case}"
        )

    # =========================
    # سرنخ‌ها
    # =========================

    def clues_page(self, *args):

        self.generic_page(
            "🔎 سرنخ‌ها",
            "clues",
            "سرنخ"
        )

    # =========================
    # افراد
    # =========================

    def people_page(self, *args):

        self.generic_page(
            "👤 افراد",
            "people",
            "فرد"
        )

    # =========================
    # شاهدها
    # =========================

    def witnesses_page(self, *args):

        self.generic_page(
            "👁️ شاهدها",
            "witnesses",
            "شاهد"
        )

    # =========================
    # خط زمانی
    # =========================

    def timeline_page(self, *args):

        self.generic_page(
            "⏱️ خط زمانی",
            "timeline",
            "رویداد"
        )

    # =========================
    # یادداشت‌ها
    # =========================

    def notes_page(self, *args):

        self.generic_page(
            "📝 یادداشت‌های تحقیق",
            "notes",
            "یادداشت"
        )

    # =========================
    # صفحات داده
    # =========================

    def generic_page(self, title, key, label):

        self.clear()

        layout = self.page(title)

        scroll = ScrollView()

        box = BoxLayout(
            orientation="vertical",
            spacing=8,
            size_hint_y=None
        )

        box.bind(
            minimum_height=box.setter("height")
        )

        items = self.data[key]

        if not items:

            box.add_widget(
                Label(
                    text="هنوز موردی ثبت نشده.",
                    size_hint_y=None,
                    height=60
                )
            )

        else:

            for i, item in enumerate(items):

                text = self.item_text(key, item, i)

                row = BoxLayout(
                    size_hint_y=None,
                    height=80,
                    spacing=5
                )

                row.add_widget(
                    Label(text=text)
                )

                delete = Button(
                    text="🗑️",
                    size_hint_x=None,
                    width=70
                )

                delete.bind(
                    on_press=lambda x,
                    k=key,
                    n=i:
                    self.delete_item(k, n)
                )

                row.add_widget(delete)

                box.add_widget(row)

        scroll.add_widget(box)

        layout.add_widget(scroll)

        layout.add_widget(
            self.button(
                "➕ افزودن " + label,
                lambda x:
                self.add_item(key, label)
            )
        )

        layout.add_widget(
            self.button(
                "↩️ برگشت",
                self.go_home
            )
        )

        self.root.add_widget(layout)

    def item_text(self, key, item, index):

        if key == "people" and isinstance(item, dict):
            return (
                f"{index + 1}. 👤 {item['name']}\n"
                f"{item['info']}"
            )

        if key == "witnesses" and isinstance(item, dict):
            return (
                f"{index + 1}. 👁️ {item['name']}\n"
                f"{item['statement']}"
            )

        if key == "timeline" and isinstance(item, dict):
            return (
                f"{index + 1}. ⏱️ {item['time']}\n"
                f"{item['event']}"
            )

        if key == "notes" and isinstance(item, dict):
            return (
                f"{index + 1}. 📝 {item['time']}\n"
                f"{item['text']}"
            )

        return f"{index + 1}. {item}"

    def add_item(self, key, label):

        box = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=8
        )

        first = TextInput(
            hint_text="عنوان / نام",
            multiline=False
        )

        second = TextInput(
            hint_text="توضیحات"
        )

        box.add_widget(first)
        box.add_widget(second)

        save = Button(
            text="ذخیره",
            size_hint_y=None,
            height=60
        )

        box.add_widget(save)

        popup = Popup(
            title="➕ " + label,
            content=box,
            size_hint=(0.9, 0.7)
        )

        def save_item(instance):

            a = first.text.strip()
            b = second.text.strip()

            if not a:
                return

            if key == "clues":
                self.data[key].append(a)

            elif key == "people":
                self.data[key].append({
                    "name": a,
                    "info": b
                })

            elif key == "witnesses":
                self.data[key].append({
                    "name": a,
                    "statement": b
                })

            elif key == "timeline":
                self.data[key].append({
                    "time": a,
                    "event": b
                })

                self.data[key].sort(
                    key=lambda x: x["time"]
                )

            elif key == "notes":
                self.data[key].append({
                    "time":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "text":
                    (a + "\n" + b).strip()
                })

            self.save_data()
            popup.dismiss()

            self.generic_page(
                self.page_title(key),
                key,
                label
            )

        save.bind(on_press=save_item)

        popup.open()

    def page_title(self, key):

        titles = {
            "clues": "🔎 سرنخ‌ها",
            "people": "👤 افراد",
            "witnesses": "👁️ شاهدها",
            "timeline": "⏱️ خط زمانی",
            "notes": "📝 یادداشت‌های تحقیق"
        }

        return titles[key]

    def delete_item(self, key, index):

        if 0 <= index < len(self.data[key]):

            self.data[key].pop(index)
            self.save_data()

            self.generic_page(
                self.page_title(key),
                key,
                {
                    "clues": "سرنخ",
                    "people": "فرد",
                    "witnesses": "شاهد",
                    "timeline": "رویداد",
                    "notes": "یادداشت"
                }[key]
            )

    # =========================
    # خلاصه
    # =========================

    def summary_page(self, *args):

        self.clear()

        text = (
            "📊 خلاصه پرونده\n\n"
            f"📁 پرونده‌ها: "
            f"{len(self.data['cases'])}\n\n"
            f"🔎 سرنخ‌ها: "
            f"{len(self.data['clues'])}\n\n"
            f"👤 افراد: "
            f"{len(self.data['people'])}\n\n"
            f"👁️ شاهدها: "
            f"{len(self.data['witnesses'])}\n\n"
            f"⏱️ رویدادها: "
            f"{len(self.data['timeline'])}\n\n"
            f"📝 یادداشت‌ها: "
            f"{len(self.data['notes'])}"
        )

        layout = self.page("📊 خلاصه")

        layout.add_widget(
            Label(
                text=text,
                font_size=20
            )
        )

        layout.add_widget(
            self.button(
                "↩️ برگشت",
                self.go_home
            )
        )

        self.root.add_widget(layout)

    # =========================
    # مورس
    # =========================

    def morse_page(self, *args):

        self.clear()

        layout = self.page("🔐 رمزگشای مورس")

        input_box = TextInput(
            hint_text="متن یا کد مورس",
            size_hint_y=None,
            height=120
        )

        result = Label(
            text="نتیجه اینجا نمایش داده می‌شود."
        )

        layout.add_widget(input_box)

        layout.add_widget(
            self.button(
                "متن → مورس",
                lambda x:
                self.encode_morse(
                    input_box.text,
                    result
                )
            )
        )

        layout.add_widget(
            self.button(
                "مورس → متن",
                lambda x:
                self.decode_morse(
                    input_box.text,
                    result
                )
            )
        )

        layout.add_widget(result)

        layout.add_widget(
            self.button(
                "↩️ برگشت",
                self.go_home
            )
        )

        self.root.add_widget(layout)

    def encode_morse(self, text, result):

        output = []

        for char in text.upper():

            if char == " ":
                output.append("/")

            elif char in MORSE:
                output.append(MORSE[char])

            else:
                output.append("?")

        result.text = " ".join(output)

    def decode_morse(self, code, result):

        words = code.split(" / ")
        output = []

        for word in words:

            letters = word.split()

            output.append(
                "".join(
                    REVERSE_MORSE.get(
                        letter,
                        "?"
                    )
                    for letter in letters
                )
            )

        result.text = " ".join(output)

    # =========================
    # برگشت
    # =========================

    def go_home(self, *args):

        self.clear()
        self.root.add_widget(
            self.home()
        )


if __name__ == "__main__":
    CrimeBot().run()