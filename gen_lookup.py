#!/usr/bin/env python3
"""Generate `.lookup` (codebase map) in the repo root. No git required.

Usage (from repo root):  python3 gen_lookup.py [path]
Output file: [path] if given, else the first that exists of lookup.md / .lookup,
else .lookup. (So renaming .lookup to lookup.md just works.)
Auto-filled: package map, mixin table, hotspots, per-file table.
Hand-edit: Verdict / Notes columns, the PLAN section, any extra sections.

Safe to re-run: an existing .lookup is read first and these survive
  - any line containing "AI GENERATED" (the marker; moved to the top)
  - Verdict/Notes cells (package map, mixin table, per-file table), matched by name
  - sections 2, 4, 10 and 11 exactly as you edited them (they are static text)
  - Target path cells you edited in section 12 (clear a cell to get a fresh suggestion)
  - extra "- key: value" lines you add to section 1 (e.g. "- Fork rename: ...")
  - any section you added whose number is above 12 or has no number
  - free-text lines you put above the first "## " heading
Rows for files that no longer exist are dropped; new files appear with "?".
"""
import datetime, json, os, re, sys

ROOT = os.getcwd()
SRC = os.path.join(ROOT, "src/main/java")
RES = os.path.join(ROOT, "src/main/resources")


def read(p):
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def props():
    d = {}
    for line in read(os.path.join(ROOT, "gradle.properties")).splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip()
    return d


java = []
for dp, _, fs in os.walk(SRC):
    for fn in fs:
        if fn.endswith(".java"):
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, ROOT)
            java.append((rel, read(p).count("\n") + 1, read(p)))
java.sort()

base = None
for rel, _, _ in java:
    parts = rel.split("/")
    if "java" in parts:
        i = parts.index("java")
        base = "/".join(parts[: i + 1])
        break


def pkg(rel):
    d = os.path.dirname(rel)
    tail = d[len(base):].lstrip("/") if base else d
    # drop the root mod package (first 3 path segments, e.g. net/parkabird/changedsynergy)
    segs = tail.split("/")
    return "/".join(segs[3:]) or "(root)"


def role(rel, src):
    n = os.path.basename(rel)[:-5]
    p = pkg(rel)
    if p.startswith("mixin"):
        return "mixin"
    if p.startswith("client"):
        return "client"
    if p.startswith("network"):
        return "packet" if "Packet" in n else "network"
    if p.startswith("event"):
        return "events"
    if p.startswith("compat"):
        return "compat"
    if p.startswith("world/inventory"):
        return "menu"
    if p.startswith("init"):
        return "registry"
    if p.startswith("command"):
        return "command"
    if p.startswith("dialogue"):
        return "dialogue"
    if "extends SavedData" in src:
        return "saved-data"
    if n.endswith("Goal"):
        return "ai-goal"
    if n.endswith("Service"):
        return "service"
    if n.endswith(("Data", "Memory", "State", "Profile", "Settings")):
        return "state"
    return "model/util"


def paren_body(src, start):
    depth, i = 0, start
    while i < len(src):
        if src[i] == "(":
            depth += 1
        elif src[i] == ")":
            depth -= 1
            if depth == 0:
                return src[start + 1 : i]
        i += 1
    return ""


# ---- mixins
mj_path = None
for f in os.listdir(RES) if os.path.isdir(RES) else []:
    if f.endswith(".mixins.json"):
        mj_path = os.path.join(RES, f)
mixin_side, mixin_cfg = {}, {}
if mj_path:
    try:
        mixin_cfg = json.loads(read(mj_path))
        for k in ("mixins", "client", "server"):
            for m in mixin_cfg.get(k, []):
                mixin_side[m] = "common" if k == "mixins" else k
    except json.JSONDecodeError:
        pass

mixin_rows = []
for rel, n, src in java:
    if "/mixin/" in rel:
        name = os.path.basename(rel)[:-5]
        m = re.search(r"@Mixin\s*\(", src)
        tgt = re.sub(r"\s+", " ", paren_body(src, m.end() - 1)) if m else "?"
        tgt = tgt.replace(".class", "").strip()
        tgt = re.sub(r"^(value|targets)\s*=\s*", "", tgt).replace(", remap = false", "").strip()
        mixin_rows.append((name, mixin_side.get(name, "UNLISTED"), tgt, n))

# ---- package map
pk = {}
for rel, n, _ in java:
    f, l = pk.get(pkg(rel), (0, 0))
    pk[pkg(rel)] = (f + 1, l + n)

PURPOSE = {
    "(root)": "Mod entry point + common/client config",
    "ai": "Core gameplay: relationships, bonds, factions, settlements, grabs, hypnosis, takeover, hunting",
    "api": "Stable integration surface for other mods",
    "advancement": "Advancement triggers",
    "client": "Screens, radial menus, renderers, client state",
    "command": "Server commands (bond, config, spawn)",
    "compat": "Optional-mod bridges (Addon Plus, Extras, Vanilla, Domestication, firearms)",
    "compat/addon": "Classes whose signatures use Changed Addon Plus types (load only if present)",
    "compat/curios": "Curios integration",
    "dialogue": "Contextual NPC lines, emotes, translation selection",
    "effect": "Mob effects",
    "entity": "Entity classes",
    "event": "Forge event handlers (social, hunt AI, reputation, territory, disguises)",
    "init": "DeferredRegister registries + gamerules",
    "item": "Items",
    "mixin": "Patches to Changed / Addon Plus / vanilla / other mods",
    "network": "SimpleChannel packets and sync",
    "performance": "Performance snapshot/measurement",
    "recipe": "Recipe serializers",
    "util": "Misc helpers",
    "world": "World-level helpers, biome/territory",
    "world/inventory": "Menus / containers (social, bonded inventory, relationship)",
}


def table_row(*cells):
    return "| " + " | ".join(str(c) for c in cells) + " |"


def target(rel, src):
    """Suggest where a file goes in the planned layout. '(review)' = judgement call."""
    p, n = pkg(rel), os.path.basename(rel)[:-5]
    top = p.split("/")[0]
    if p == "(root)":
        return {"ChangedSynergyClientConfig": "operbehavior/client/config",
                "ChangedSynergyConfig": "operbehavior/common/config"}.get(n, "(root)")
    if top == "ai":
        if "extends SavedData" in src or re.search(r"(Data|Memory|State|Profile|Settings|Session|SessionNbt)$", n):
            return "ai/states"
        if n.endswith("Goal"):
            return "ai/goals"
        if n.endswith("Service"):
            return "ai/services"
        return "ai/rules"
    if top == "client":
        return "operbehavior/client"
    if top == "event":
        return "operbehavior/server/events"
    if top == "command":
        return "operbehavior/server/commands"
    if top == "network":
        if n.endswith("Packet") or n == "ChangedSynergyNetwork":
            return "operbehavior/network"
        return "operbehavior/common/states (review)"
    if p.startswith("world/inventory"):
        return "operbehavior/common/menus"
    if top == "init":
        return "operbehavior/common/registry"
    if top == "mixin":
        return "mixin/client" if mixin_side.get(n) == "client" else "mixin/common"
    if top == "api":
        return "api"
    if top == "compat":
        return p
    if top == "dialogue":
        return "operbehavior/server/dialogue (review)"
    if top == "world":
        return ("operbehavior/server/world" if "extends SavedData" in src
                else "operbehavior/common/world (review)")
    if top in ("advancement", "effect", "entity", "item", "recipe", "util"):
        return "operbehavior/common/" + top
    if top == "performance":
        return "operbehavior/common/performance (review)"
    return p + " (review)"


MARKER_DEFAULT = "AI GENERATED, CLAUDE SONNET 5.5 @ MEDIUM EFFORT"


def parse_old(text):
    markers = list(dict.fromkeys(re.findall(r"(?m)^.*AI GENERATED.*$", text)))
    cells, sections, preamble, headers = {}, {}, [], {}
    sec, cur, prev = None, None, None
    for line in text.splitlines():
        if line.startswith("## "):
            h = re.match(r"## (\d+)\.", line)
            cur, sec = line, (int(h.group(1)) if h else None)
            sections[cur] = []
            continue
        if cur is None:
            if (line.strip() and "AI GENERATED" not in line
                    and not line.startswith(("# .lookup", "# Generated"))):
                preamble.append(line)
            continue
        sections[cur].append(line)
        if sec in (3, 7, 12) and line.startswith("|"):
            if line.startswith("| ---"):
                if prev is not None:
                    headers[sec] = prev  # the row above a separator is a header; last table wins
                continue
            c = [x.strip() for x in line.strip()[1:-1].split("|")]
            prev = [x.lower() for x in c]
            cells[(sec, c[0])] = c
    return markers, cells, sections, preamble, headers


def pick_target():
    if len(sys.argv) > 1:
        return sys.argv[1]
    for name in ("lookup.md", ".lookup"):
        if os.path.exists(os.path.join(ROOT, name)):
            return name
    return ".lookup"


TARGET = pick_target()
OLD = read(os.path.join(ROOT, TARGET))
OLD_MARKERS, OLD_CELLS, OLD_SECTIONS, OLD_PREAMBLE, OLD_HEADERS = parse_old(OLD)


def carry(sec, key, names, defaults):
    """Return old cell values (found by column-header name) if you filled them in."""
    old, hdr, out = OLD_CELLS.get((sec, key)), OLD_HEADERS.get(sec), list(defaults)
    if old and hdr:
        for j, nm in enumerate(names):
            i = next((x for x, h in enumerate(hdr) if nm in h), None)
            if i is not None and i < len(old) and old[i] not in ("", "?"):
                out[j] = old[i]
    return out


P = props()
today = datetime.date.today().isoformat()
out = []
a = out.append

for _m in (OLD_MARKERS or [MARKER_DEFAULT]):
    a(_m)
a("# .lookup - codebase map")
a(f"# Generated {today} by gen_lookup.py. Auto sections regenerate; Verdict/Notes/PLAN are for hand edits.")
for _l in OLD_PREAMBLE:
    a(_l)
a("")
a("## 1. Identity")
a(f"- Mod: `{P.get('mod_name','?')}` (mod_id `{P.get('mod_id','?')}`, group `{P.get('mod_group_id','?')}`)")
a(f"- Upstream author: {P.get('mod_authors','?')}   License: {P.get('mod_license','?')}")
a(f"- Version at fork point: {P.get('mod_version','?')}")
a(f"- Target: Minecraft {P.get('minecraft_version','?')}, Forge {P.get('forge_version','?')}, mappings {P.get('mapping_channel','?')}")
a(f"- Source size: {len(java)} Java files, {sum(n for _,n,_ in java)} lines; {len(mixin_rows)} mixin classes")
a("- Fork goal: LTS rewrite - deeper behaviors, new features, wider compat")
a("- Fork repo: goldfinder/changed-charged-synergy")
a("")
a("## 2. Dependency direction (from docs/ARCHITECTURE.md)")
a("- Hard dep: Changed. Optional: Addon Plus, Additions, Extras, Vanilla, Domestication Innovation, Curios, FurMutage, Survive Protocol, firearms mods.")
a("- Optional-mod types must stay under `compat/` (`compat/addon` for signatures using Addon types). They must NOT leak into the main class, api, menus, packets, or client state.")
a("- Layers: init/registries -> ai (state + services + goals) -> event (Forge hooks) -> dialogue -> world.inventory (menus) -> network -> client.")
a("")
a("## 3. Package map")
a(table_row("Package", "Files", "Lines", "Purpose", "First-pass verdict", "Notes"))
a(table_row("---", "---", "---", "---", "---", "---"))
for k in sorted(pk, key=lambda x: -pk[x][1]):
    f, l = pk[k]
    v, nt = carry(3, k, ("verdict", "notes"), ("?", ""))
    a(table_row(k, f, l, PURPOSE.get(k, ""), v, nt))
a("")
a("## 4. Entry points and registration")
a("- Main class: `ChangedSynergyMod` (`@Mod`). Registers COMMON + CLIENT configs, network channel, optional compat events, then DeferredRegisters.")
a("- Registries (init/): Entities, Items, Menus, MobEffects, RecipeSerializers, SoundEvents, GameRules.")
a("- Access transformer: `META-INF/accesstransformer.cfg` (GameRules create, Mob goalSelector/persistenceRequired, goal speed modifiers, Entity shared flag).")
a("- Mixin config: `changed_synergy.mixins.json` (required=true, defaultRequire=1 -> any failed injection crashes load).")
a("")
a("## 5. Persistence (breaking these breaks existing worlds)")
a("- Creature NBT compound `ChangedSynergySocial`; player compounds prefixed `ChangedSynergy`.")
a("- SavedData classes:")
for rel, n, src in java:
    if "extends SavedData" in src:
        a(f"  - `{rel}` ({n} lines)")
a("- DECISION NEEDED: keep mod_id / NBT keys / gamerule names / channel name for save-compat with upstream, or break compat and migrate.")
a("")
a("## 6. Network packets")
net = [os.path.basename(r)[:-5] for r, _, _ in java if "/network/" in r]
a("- " + ", ".join(sorted(net)))
a("")
a("## 7. Mixins")
a(table_row("Mixin", "Side", "Target", "Lines", "Verdict", "Notes"))
a(table_row("---", "---", "---", "---", "---", "---"))
for name, side, tgt, n in sorted(mixin_rows, key=lambda r: (r[1], r[0])):
    v, nt = carry(7, name, ("verdict", "notes"), ("?", ""))
    a(table_row(name, side, tgt.replace("|", "/"), n, v, nt))
a("- Mixins listed in json but missing a source file, or source files not listed (UNLISTED), are bugs worth checking.")
listed = set(mixin_side)
have = {r[0] for r in mixin_rows}
miss = sorted(listed - have)
if miss:
    a("- In json but no source file: " + ", ".join(miss))
a("")
a("## 8. Hotspots (largest files, refactor candidates)")
a(table_row("File", "Lines", "Role"))
a(table_row("---", "---", "---"))
for rel, n, src in sorted(java, key=lambda r: -r[1])[:25]:
    a(table_row(rel.split("changedsynergy/", 1)[-1], n, role(rel, src)))
a("")
a("## 9. Resources")
if os.path.isdir(RES):
    counts = {}
    for dp, _, fs in os.walk(RES):
        r = os.path.relpath(dp, RES)
        depth = r.split(os.sep)
        key = os.sep.join(depth[:3]) if r != "." else "."
        counts[key] = counts.get(key, 0) + len(fs)
    a(table_row("Directory", "Files"))
    a(table_row("---", "---"))
    for k in sorted(counts):
        a(table_row(k, counts[k]))
a("")
a("## 10. Known risks (from KNOWN_ISSUES.md + survey)")
a("- Tightly pinned to Changed 0.15.7 ([0.15.7,0.15.8)); a small upstream update can break a mixin.")
a("- Large mixin surface with defaultRequire=1; one stale target crashes startup.")
a("- God classes in `ai/` and `event/` (see Hotspots); splitting them is the main maintainability win.")
a("- No automated in-game test suite; only tools/tests/FactionDiplomacyTest.java exists.")
a("- Behavior is spread across ai/, event/, mixin/ and compat/; one feature (e.g. takeover, hypnosis) touches all four.")
a("")
a("## 11. PLAN (edit me)")
a("1. Snapshot: branch `upstream-snapshot` untouched; work on `lts/main`.")
a("2. Decide identity: new mod_id/name vs keep (see section 5) and publish naming so it cannot clash with upstream.")
a("3. Decide target: stay Forge 1.20.1 for the LTS, or port (NeoForge/newer MC) first.")
a("4. Get a clean build + run configuration working before changing behavior.")
a("5. Triage per-file table: mark each keep / rewrite / drop; start with the Hotspots.")
a("6. Add tests around persistence, packets, and relationship transitions before rewriting them.")
a("7. Rewrite by feature slice (takeover, hypnosis, settlements, ...), each slice owning its ai/event/mixin/client files.")
a("")
a("## 12. Per-file table")
a("Planned layout (the Target column is a suggestion: edit it, or clear a cell for a fresh one):")
a("```")
a("operbehavior/{common,network,client,server}   ai/{goals,services,states,rules}")
a("mixin/{client,common}   api/   compat/")
a("```")
a("Dependency rule: common -> nothing side-specific; network -> common; client and server -> common + network, never each other.")
a("")
tally = {}
for rel, n, src in java:
    t = target(rel, src).replace(" (review)", "")
    f, l = tally.get(t, (0, 0))
    tally[t] = (f + 1, l + n)
a(table_row("Target folder", "Files", "Lines"))
a(table_row("---", "---", "---"))
for t in sorted(tally):
    a(table_row(t, tally[t][0], tally[t][1]))
a("")
a(table_row("Path", "Lines", "Role", "Target path (proposed)", "Verdict (keep/rewrite/drop)", "Notes"))
a(table_row("---", "---", "---", "---", "---", "---"))
for rel, n, src in java:
    path = rel.split("changedsynergy/", 1)[-1]
    tg, v, nt = carry(12, path, ("target", "verdict", "notes"), (target(rel, src), "?", ""))
    a(table_row(path, n, role(rel, src), tg, v, nt))

def splice_old_section(num):
    for head, body in OLD_SECTIONS.items():
        if head.startswith(f"## {num}."):
            i = next((j for j, l in enumerate(out) if l.startswith(f"## {num}.")), None)
            if i is None:
                return
            k = next((j for j in range(i + 1, len(out)) if out[j].startswith("## ")), len(out))
            out[i:k] = [head] + body
            return


for _n in (2, 4, 10, 11):
    splice_old_section(_n)


def key_of(line):
    return re.sub(r"[`*\s]+", " ", line.lstrip("- ").split(":", 1)[0]).strip().lower()


def carry_section1_extras():
    old = next((b for h, b in OLD_SECTIONS.items() if h.startswith("## 1.")), [])
    i = next((j for j, l in enumerate(out) if l.startswith("## 1.")), None)
    if i is None:
        return
    k = next((j for j in range(i + 1, len(out)) if out[j].startswith("## ")), len(out))
    have = {key_of(l) for l in out[i + 1:k] if l.startswith("- ")}
    extras = [l for l in old if l.startswith("- ") and ":" in l and key_of(l) not in have]
    j = k
    while j > i + 1 and not out[j - 1].strip():
        j -= 1
    out[j:j] = extras


carry_section1_extras()
for head, body in OLD_SECTIONS.items():
    m = re.match(r"## (\d+)\.", head)
    if not m or int(m.group(1)) > 12:
        out.append("")
        out.append(head)
        out.extend(body)

with open(os.path.join(ROOT, TARGET), "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print(f"Wrote {TARGET} ({len(out)} lines)")
