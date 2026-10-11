"""Cut the CoreFall promo trailer from a raw gameplay recording with ffmpeg.

Usage:  python tools/make_trailer.py <hub_story_recording.mkv> <endless_recording.mkv> [--ffmpeg path/to/ffmpeg.exe]
Outputs media/trailer.mp4, media/preview.gif and screenshots/*.png

Only clean in-game segments are used; editor/debug stretches of the raw
recording are skipped (see CLIPS). Captions are burned in with drawtext.
"""
import argparse, os, subprocess, sys, tempfile

FONT = r"C\:/Windows/Fonts/msyh.ttc"   # any CJK-capable font
# (source, start_s, duration_s, speed, zh caption, en caption)   source: "A" = hub/story take, "B" = endless take
CLIPS = [
    ("A", 49,  8, 1.0, "临危受命 · 据点 Hub",        "A living base you walk around — mentor & survivors tell the story"),
    ("A", 99, 14, 1.0, "敌人 / 蓝图档案馆",            "Archive: study every enemy before it kills you"),
    ("A", 139, 16, 1.0, "行动中心 · 主动能力",          "Ability Center: shields, gates, tractor pulls — loadout of 3"),
    ("A", 169, 18, 1.0, "蓝图工坊 · 研究塔形",          "Blueprint Workshop: research new tower shapes (T, +, L, S …)"),
    ("A", 199, 10, 1.0, "补给站 · 永久升级",            "Supply Station: starting modules, core HP, wave module cap"),
    ("A", 229, 18, 1.0, "塔连接中枢 · 俄罗斯方块式拼装", "Tower Connection Hub: fit linker modules on a 10x10 grid"),
    ("A", 586, 14, 1.0, "剧情战斗 · 第 10 天",          "Story battle: a fixed day, two waves, a limited module budget"),
    ("B", 207, 6,  1.0, "通关后解锁 · 无尽模式",        "Finish the story and the Core Gate opens Endless Mode"),
    ("B", 84, 20,  1.0, "无尽模式 · 越建越大",          "Endless: levels tick up every 30 s, 6 tower types, entropy map"),
    ("B", 156, 44, 1.0, "同屏 200+ 敌人，依然流畅",      "Endless late game: 250+ enemies on screen after the performance pass"),
]
SHOTS = {  # name: (source, timestamp s)
    "01-hub-mentor": ("A", 52), "02-hub-explore": ("A", 87), "03-enemy-archive": ("A", 106),
    "04-archive-lore": ("A", 112), "05-ability-center": ("A", 150), "06-blueprint-workshop": ("A", 181),
    "07-supply-station": ("A", 207), "08-linker-tutorial": ("A", 233), "09-tower-connection-hub": ("A", 256),
    "10-story-build-phase": ("A", 516), "11-story-wave-incoming": ("A", 536), "12-story-shield-towers": ("A", 596),
    "13-endless-gate": ("B", 209), "14-endless-opening": ("B", 96), "15-endless-growing": ("B", 140),
    "16-endless-swarm": ("B", 178), "17-endless-250-enemies": ("B", 196),
}

def run(ff, *a):
    r = subprocess.run([ff, "-v", "error", "-y", *a])
    if r.returncode: sys.exit("ffmpeg failed: " + " ".join(a)[:200])

def txt(d, name, s):
    p = os.path.join(d, name); open(p, "w", encoding="utf-8").write(s); return p.replace("\\", "/").replace(":", r"\:")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("endless"); ap.add_argument("--ffmpeg", default="ffmpeg")
    a = ap.parse_args(); ff = a.ffmpeg
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(f"{root}/media", exist_ok=True); os.makedirs(f"{root}/screenshots", exist_ok=True)
    srcs = {"A": a.src, "B": a.endless}
    for n, (k, t) in SHOTS.items():
        run(ff, "-ss", str(t), "-i", srcs[k], "-frames:v", "1", "-vf", "scale=1920:-1", f"{root}/screenshots/{n}.png")
    tmp = tempfile.mkdtemp(); parts = []
    enc = ["-c:v", "libx264", "-crf", "26", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "160k"]
    def card(i, big, small, dur):
        f1, f2 = txt(tmp, f"c{i}a.txt", big), txt(tmp, f"c{i}b.txt", small)
        out = f"{tmp}/p{i:02d}.mp4"
        vf = (f"drawtext=fontfile='{FONT}':textfile='{f1}':fontcolor=white:fontsize=110:x=(w-tw)/2:y=h/2-120,"
              f"drawtext=fontfile='{FONT}':textfile='{f2}':fontcolor=0x7fe8ff:fontsize=38:x=(w-tw)/2:y=h/2+40,"
              f"fade=t=in:d=0.8,fade=t=out:st={dur-0.8}:d=0.8")
        run(ff, "-f", "lavfi", "-i", f"color=c=0x0b141c:s=1920x1080:d={dur}:r=30", "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo",
            "-t", str(dur), "-vf", vf, *enc, out); parts.append(out)
    card(0, "CoreFall · 临危受命", "Modular tower defense — build, link, survive the swarm", 4)
    for i, (k, ss, d, sp, zh, en) in enumerate(CLIPS, 1):
        f1, f2 = txt(tmp, f"k{i}a.txt", zh), txt(tmp, f"k{i}b.txt", en); out = f"{tmp}/p{i:02d}.mp4"; od = d / sp
        vf = (f"setpts=PTS/{sp},scale=1920:1080,fps=30,"
              f"drawbox=x=0:y=ih-190:w=iw:h=190:color=black@0.55:t=fill:enable='between(t,0.5,{od-0.5})',"
              f"drawtext=fontfile='{FONT}':textfile='{f1}':fontcolor=white:fontsize=64:x=70:y=h-165:enable='between(t,0.5,{od-0.5})',"
              f"drawtext=fontfile='{FONT}':textfile='{f2}':fontcolor=0x7fe8ff:fontsize=34:x=72:y=h-70:enable='between(t,0.5,{od-0.5})',"
              f"fade=t=in:d=0.4,fade=t=out:st={od-0.4}:d=0.4")
        af = f"atempo={sp},afade=t=in:d=0.4,afade=t=out:st={od-0.4}:d=0.4"
        run(ff, "-ss", str(ss), "-t", str(d), "-i", srcs[k], "-vf", vf, "-af", af, *enc, out); parts.append(out)
    card(99, "CoreFall", "Showcase repository · Godot 4  ·  github.com/lasersoldier", 5)
    lst = f"{tmp}/list.txt"; open(lst, "w").write("".join(f"file '{p.replace(chr(92), '/')}'\n" for p in parts))
    trailer = f"{root}/media/trailer.mp4"
    run(ff, "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", trailer)
    run(ff, "-ss", "170", "-t", "8", "-i", a.endless, "-vf",
        "fps=8,scale=560:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=bayer:bayer_scale=4", f"{root}/media/preview.gif")
    print("done:", trailer)
if __name__ == "__main__": main()
