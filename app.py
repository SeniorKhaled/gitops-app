from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

notes = [
    {"id": 1, "title": "Welcome to Noted", "content": "Start writing your thoughts here.", "updated": datetime.utcnow().isoformat()}
]

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Noted</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #f9f9f8; --surface: #ffffff; --border: rgba(0,0,0,0.08);
    --text: #1a1a1a; --muted: #6b6b6b; --hint: #aaa;
    --accent: #2563eb; --accent-light: #eff6ff;
    --danger: #dc2626; --warning: #d97706;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #141414; --surface: #1e1e1e; --border: rgba(255,255,255,0.08);
      --text: #f0f0f0; --muted: #999; --hint: #555;
      --accent: #3b82f6; --accent-light: #1e3a5f;
    }
  }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--bg); color: var(--text); height: 100dvh; display: flex; flex-direction: column; overflow: hidden; }
  /* topbar */
  .topbar { height: 52px; background: var(--surface); border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 12px; padding: 0 1.25rem; flex-shrink: 0; }
  .topbar h1 { font-size: 15px; font-weight: 600; flex: 1; }
  .topbar-btn { background: transparent; border: 1px solid var(--border); border-radius: 8px; padding: 6px 14px; font-size: 13px; cursor: pointer; color: var(--text); display: flex; align-items: center; gap: 6px; }
  .topbar-btn:hover { background: var(--accent-light); border-color: var(--accent); color: var(--accent); }
  .char-count { font-size: 11px; color: var(--hint); }
  /* layout */
  .layout { display: flex; flex: 1; overflow: hidden; }
  /* sidebar */
  .sidebar { width: 260px; background: var(--surface); border-right: 1px solid var(--border); display: flex; flex-direction: column; flex-shrink: 0; }
  .sidebar-header { padding: 12px 14px; border-bottom: 1px solid var(--border); }
  .search-wrap { position: relative; }
  .search-wrap svg { position: absolute; left: 9px; top: 50%; transform: translateY(-50%); pointer-events: none; color: var(--hint); }
  .search-input { width: 100%; padding: 7px 10px 7px 32px; border-radius: 8px; border: 1px solid var(--border); background: var(--bg); color: var(--text); font-size: 13px; outline: none; }
  .search-input:focus { border-color: var(--accent); }
  .notes-list { flex: 1; overflow-y: auto; padding: 6px; }
  .note-item { padding: 10px 12px; border-radius: 8px; cursor: pointer; margin-bottom: 2px; border: 1px solid transparent; }
  .note-item:hover { background: var(--bg); }
  .note-item.active { background: var(--accent-light); border-color: var(--accent); }
  .note-item-top { display: flex; align-items: center; }
  .note-item-title { font-size: 13px; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; }
  .note-item-meta { font-size: 11px; color: var(--hint); margin-top: 2px; }
  .note-item-preview { font-size: 12px; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 3px; }
  .del-btn { background: none; border: none; cursor: pointer; color: var(--hint); padding: 3px 5px; border-radius: 5px; }
  .del-btn:hover { color: var(--danger); background: #fee2e2; }
  /* editor */
  .editor-pane { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
  .editor-toolbar { background: var(--surface); border-bottom: 1px solid var(--border); padding: 8px 1.25rem; display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
  .tb-btn { background: transparent; border: none; padding: 5px 9px; border-radius: 6px; cursor: pointer; font-size: 13px; color: var(--muted); font-weight: 500; }
  .tb-btn:hover { background: var(--bg); color: var(--text); }
  .tb-sep { width: 1px; height: 18px; background: var(--border); margin: 0 2px; }
  .save-status { margin-left: auto; font-size: 12px; color: var(--hint); }
  .editor-body { flex: 1; overflow-y: auto; padding: 2rem 2.5rem; background: var(--bg); }
  .note-title-input { width: 100%; border: none; outline: none; font-size: 22px; font-weight: 600; color: var(--text); background: transparent; margin-bottom: 1rem; }
  .note-content-input { width: 100%; border: none; outline: none; font-size: 15px; color: var(--text); background: transparent; resize: none; line-height: 1.75; min-height: 60vh; }
  .empty-state { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; color: var(--hint); gap: 10px; background: var(--bg); }
  /* mobile */
  @media (max-width: 640px) {
    .sidebar { position: absolute; inset: 52px 0 0 0; width: 100%; z-index: 20; transform: translateX(-100%); transition: transform 0.2s; }
    .sidebar.open { transform: none; }
    .mob-toggle { display: flex !important; }
  }
  .mob-toggle { display: none; background: none; border: none; cursor: pointer; padding: 4px; color: var(--text); }
</style>
</head>
<body>
<div class="topbar">
  <button class="mob-toggle" id="mob-toggle" aria-label="Toggle sidebar">&#9776;</button>
  <h1>&#128221; Noted</h1>
  <span class="char-count" id="char-count"></span>
  <button class="topbar-btn" id="new-btn">+ New note</button>
</div>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <div class="search-wrap">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input class="search-input" id="search" type="search" placeholder="Search notes&hellip;" autocomplete="off">
      </div>
    </div>
    <div class="notes-list" id="notes-list"></div>
  </aside>
  <main class="editor-pane">
    <div class="editor-toolbar">
      <button class="tb-btn" onclick="fmt('bold')"><b>B</b></button>
      <button class="tb-btn" onclick="fmt('italic')"><i>I</i></button>
      <button class="tb-btn" onclick="fmt('underline')"><u>U</u></button>
      <div class="tb-sep"></div>
      <button class="tb-btn" onclick="insertPrefix('&#x2022; ')">&#x2022; List</button>
      <button class="tb-btn" onclick="insertPrefix('1. ')">1. List</button>
      <span class="save-status" id="save-status">Saved</span>
    </div>
    <div class="editor-body">
      <div class="empty-state" id="empty-state">
        <div style="font-size:40px">&#128221;</div>
        <p>Select a note or create a new one</p>
      </div>
      <div id="editor-content" style="display:none">
        <input class="note-title-input" id="note-title" placeholder="Note title&hellip;" autocomplete="off">
        <textarea class="note-content-input" id="note-content" placeholder="Start writing&hellip;"></textarea>
      </div>
    </div>
  </main>
</div>
<script>
  let notes = [], activeId = null, saveTimer = null;

  function timeAgo(iso) {
    const s = (Date.now() - new Date(iso)) / 1000;
    if (s < 60) return 'just now';
    if (s < 3600) return Math.floor(s/60) + 'm ago';
    if (s < 86400) return Math.floor(s/3600) + 'h ago';
    return Math.floor(s/86400) + 'd ago';
  }

  function renderList(q='') {
    const list = document.getElementById('notes-list');
    const filtered = notes.filter(n =>
      n.title.toLowerCase().includes(q) || n.content.toLowerCase().includes(q)
    ).sort((a,b) => new Date(b.updated) - new Date(a.updated));
    if (!filtered.length) { list.innerHTML = '<p style="padding:1rem;font-size:13px;color:var(--hint)">No notes found</p>'; return; }
    list.innerHTML = filtered.map(n => `
      <div class="note-item${n.id===activeId?' active':''}" onclick="openNote(${n.id},event)" data-id="${n.id}">
        <div class="note-item-top">
          <span class="note-item-title">${n.title||'Untitled'}</span>
          <button class="del-btn" onclick="deleteNote(${n.id},event)" title="Delete">&#x2715;</button>
        </div>
        <div class="note-item-meta">${timeAgo(n.updated)}</div>
        <div class="note-item-preview">${n.content.split('\\n')[0]||'&mdash;'}</div>
      </div>`).join('');
  }

  function openNote(id, e) {
    if (e && e.target.closest('.del-btn')) return;
    activeId = id;
    const n = notes.find(x => x.id===id);
    document.getElementById('empty-state').style.display = 'none';
    document.getElementById('editor-content').style.display = 'block';
    document.getElementById('note-title').value = n.title;
    document.getElementById('note-content').value = n.content;
    updateCharCount();
    renderList(document.getElementById('search').value);
    document.getElementById('sidebar').classList.remove('open');
  }

  function deleteNote(id, e) {
    e.stopPropagation();
    fetch('/api/notes/' + id, {method:'DELETE'}).then(() => {
      notes = notes.filter(n => n.id !== id);
      if (activeId === id) {
        activeId = null;
        document.getElementById('empty-state').style.display = 'flex';
        document.getElementById('editor-content').style.display = 'none';
      }
      renderList(document.getElementById('search').value);
    });
  }

  function onContentChange() {
    if (!activeId) return;
    const n = notes.find(x => x.id===activeId);
    n.title = document.getElementById('note-title').value;
    n.content = document.getElementById('note-content').value;
    n.updated = new Date().toISOString();
    updateCharCount();
    const st = document.getElementById('save-status');
    st.textContent = 'Saving\u2026'; st.style.color = 'var(--warning)';
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      fetch('/api/notes/' + activeId, {
        method:'PUT', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({title: n.title, content: n.content})
      }).then(() => { st.textContent = 'Saved'; st.style.color = 'var(--hint)'; renderList(document.getElementById('search').value); });
    }, 800);
  }

  function updateCharCount() {
    const len = (document.getElementById('note-content').value||'').length;
    document.getElementById('char-count').textContent = len.toLocaleString() + ' chars';
  }

  function fmt(cmd) { document.getElementById('note-content').focus(); document.execCommand(cmd, false, null); }
  function insertPrefix(p) {
    const ta = document.getElementById('note-content');
    const s = ta.selectionStart, v = ta.value;
    const ls = v.lastIndexOf('\\n', s-1)+1;
    ta.value = v.slice(0,ls)+p+v.slice(ls);
    ta.selectionStart = ta.selectionEnd = ls+p.length+(s-ls);
    ta.focus(); onContentChange();
  }

  document.getElementById('note-title').addEventListener('input', onContentChange);
  document.getElementById('note-content').addEventListener('input', onContentChange);
  document.getElementById('search').addEventListener('input', e => renderList(e.target.value));
  document.getElementById('new-btn').addEventListener('click', () => {
    fetch('/api/notes', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({title:'', content:''})})
    .then(r => r.json()).then(n => { notes.unshift(n); openNote(n.id); });
  });
  document.getElementById('mob-toggle').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('open');
  });

  fetch('/api/notes').then(r => r.json()).then(data => {
    notes = data;
    renderList();
    if (notes.length) openNote(notes[0].id);
  });
</script>
</body>
</html>'''

# --- API routes ---

@app.route('/api/notes', methods=['GET'])
def get_notes():
    return jsonify(sorted(notes, key=lambda n: n['updated'], reverse=True))

@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.json
    note = {
        "id": int(datetime.utcnow().timestamp() * 1000),
        "title": data.get('title', ''),
        "content": data.get('content', ''),
        "updated": datetime.utcnow().isoformat()
    }
    notes.append(note)
    return jsonify(note), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = next((n for n in notes if n['id'] == note_id), None)
    if not note:
        return jsonify({"error": "Not found"}), 404
    data = request.json
    note['title'] = data.get('title', note['title'])
    note['content'] = data.get('content', note['content'])
    note['updated'] = datetime.utcnow().isoformat()
    return jsonify(note)

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    global notes
    notes = [n for n in notes if n['id'] != note_id]
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    # test jenkins