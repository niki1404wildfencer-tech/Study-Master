import json
from managers.app_paths import data_file
from datetime import datetime


class NoteManager:

    def __init__(self):
        self.file_path = data_file("notes.json")
        self.folders_path = data_file("folders.json")
        self._ensure_file(self.file_path, [])
        self._ensure_file(self.folders_path, [])

    # =====================================================
    # Storage
    # =====================================================

    def _ensure_file(self, path, default):
        if not path.exists():
            self._save_raw(path, default)

    def _load_raw(self, path):
        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, list):
                return data
            return []
        except (json.JSONDecodeError, OSError):
            return []

    def _save_raw(self, path, data):
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def _load(self):
        return self._load_raw(self.file_path)

    def _save(self, notes):
        self._save_raw(self.file_path, notes)

    def _load_folders(self):
        return self._load_raw(self.folders_path)

    def _save_folders(self, folders):
        self._save_raw(self.folders_path, folders)

    # =====================================================
    # Helpers
    # =====================================================

    def _next_id(self, items):
        if not items:
            return 1
        return max(int(x.get("id", 0)) for x in items) + 1

    def _now(self):
        return datetime.now().isoformat(timespec="seconds")

    # =====================================================
    # FOLDERS
    # =====================================================

    def add_folder(self, name, color="#4F7CFF"):
        name = name.strip()
        if not name:
            return None
        folders = self._load_folders()
        folder = {
            "id": self._next_id(folders),
            "name": name,
            "color": color,
            "created_at": self._now(),
        }
        folders.append(folder)
        self._save_folders(folders)
        return folder

    def get_folders(self):
        return self._load_folders()

    def get_folder(self, folder_id):
        for folder in self._load_folders():
            if folder.get("id") == folder_id:
                return folder
        return None

    def update_folder(self, folder_id, name, color):
        name = name.strip()
        if not name:
            return None
        folders = self._load_folders()
        for folder in folders:
            if folder.get("id") != folder_id:
                continue
            folder["name"] = name
            folder["color"] = color
            self._save_folders(folders)
            return folder
        return None

    def delete_folder(self, folder_id):
        folders = self._load_folders()
        original = len(folders)
        folders = [f for f in folders if f.get("id") != folder_id]
        if len(folders) == original:
            return False
        self._save_folders(folders)

        notes = self._load()
        changed = False
        for note in notes:
            if note.get("folder_id") == folder_id:
                note["folder_id"] = None
                changed = True
        if changed:
            self._save(notes)
        return True

    # =====================================================
    # NOTES — Create
    # =====================================================

    def add_note(self, title, content, subject_id=None, task_id=None, folder_id=None):
        notes = self._load()
        now = self._now()
        note = {
            "id": self._next_id(notes),
            "title": title.strip(),
            "content": content.strip(),
            "subject_id": subject_id,
            "task_id": task_id,
            "folder_id": folder_id,
            "created_at": now,
            "updated_at": now,
        }
        notes.append(note)
        self._save(notes)
        return note

    # =====================================================
    # NOTES — Read
    # =====================================================

    def get_notes(self):
        return self._load()

    def get_notes_by_folder(self, folder_id):
        notes = self._load()
        if folder_id == "all":
            return notes
        return [n for n in notes if n.get("folder_id") == folder_id]

    def count_notes_by_folder(self, folder_id):
        return len(self.get_notes_by_folder(folder_id))

    def get_note(self, note_id):
        for note in self._load():
            if note.get("id") == note_id:
                return note
        return None

    # =====================================================
    # NOTES — Update
    # =====================================================

    def update_note(self, note_id, title, content, subject_id=None, task_id=None, folder_id=None):
        notes = self._load()
        for note in notes:
            if note.get("id") != note_id:
                continue
            note["title"] = title.strip()
            note["content"] = content.strip()
            note["subject_id"] = subject_id
            note["task_id"] = task_id
            note["folder_id"] = folder_id
            note["updated_at"] = self._now()
            self._save(notes)
            return note
        return None

    # =====================================================
    # NOTES — Delete
    # =====================================================

    def delete_note(self, note_id):
        notes = self._load()
        for note in notes:
            if note.get("id") == note_id:
                notes.remove(note)
                self._save(notes)
                return True
        return False

    # =====================================================
    # NOTES — Search
    # =====================================================

    def search_notes(self, query, folder_id="all"):
        query = query.strip().lower()
        notes = self.get_notes_by_folder(folder_id)
        if not query:
            return notes
        results = []
        for note in notes:
            title = str(note.get("title", "")).lower()
            content = str(note.get("content", "")).lower()
            if query in title or query in content:
                results.append(note)
        return results