// allWords: array of {word, tag} where tag is "n" (NWL only), "s" (SOWPODS only), "b" (both)
let allWords = null;

const DICT_TAGS = {
  all:          null,              // no tag filter
  nwl:          new Set(["n", "b"]),
  sowpods:      new Set(["s", "b"]),
  common:       new Set(["b"]),
  "nwl-only":   new Set(["n"]),
  "sowpods-only": new Set(["s"]),
};

async function loadWords() {
  const res = await fetch("words.txt");
  if (!res.ok) throw new Error("Failed to load word list");
  const text = await res.text();
  allWords = text.split("\n").filter(Boolean).map(line => {
    const tab = line.indexOf("\t");
    return tab === -1
      ? { word: line, tag: "b" }
      : { word: line.slice(0, tab), tag: line.slice(tab + 1) };
  });
}

function parseLetters(s) {
  return new Set(s.replace(/[,\s]/g, "").toLowerCase());
}

function matches(word, allowed, required) {
  for (const c of word) {
    if (!allowed.has(c)) return false;
  }
  if (required.size > 0) {
    let hasRequired = false;
    for (const c of word) {
      if (required.has(c)) { hasRequired = true; break; }
    }
    if (!hasRequired) return false;
  }
  return true;
}

function render(found) {
  const results = document.getElementById("results");
  const status = document.getElementById("status");

  if (found.length === 0) {
    status.textContent = "No words found.";
    results.innerHTML = "";
    return;
  }

  status.textContent = `Found ${found.length} word${found.length === 1 ? "" : "s"}`;

  // Group by length, longest first
  const groups = new Map();
  for (const w of found) {
    const len = w.length;
    if (!groups.has(len)) groups.set(len, []);
    groups.get(len).push(w);
  }
  const lengths = [...groups.keys()].sort((a, b) => b - a);

  results.innerHTML = lengths.map(len => {
    const group = groups.get(len);
    const wordEls = group.map(w => `<span class="word">${w}</span>`).join("");
    return `
      <div class="group">
        <div class="group-header">${len} letters &mdash; ${group.length}</div>
        <div class="word-grid">${wordEls}</div>
      </div>
    `;
  }).join("");
}

document.getElementById("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const btn = document.getElementById("btn");
  const status = document.getElementById("status");

  const optionalStr = document.getElementById("optional").value.trim();
  if (!optionalStr) {
    status.textContent = "Enter at least one available letter.";
    return;
  }

  if (!allWords) {
    btn.disabled = true;
    status.textContent = "Loading word list\u2026";
    try {
      await loadWords();
    } catch {
      status.textContent = "Error loading word list.";
      btn.disabled = false;
      return;
    }
    btn.disabled = false;
  }

  const optional = parseLetters(optionalStr);
  const required = parseLetters(document.getElementById("required").value);
  const allowed = new Set([...optional, ...required]);

  const dictVal = document.getElementById("dict").value;
  const tagFilter = DICT_TAGS[dictVal];

  const found = allWords
    .filter(({ tag }) => !tagFilter || tagFilter.has(tag))
    .map(({ word }) => word)
    .filter(w => matches(w, allowed, required));

  // Sort: longest first, then alphabetical
  found.sort((a, b) => b.length - a.length || a.localeCompare(b));

  render(found);
});
