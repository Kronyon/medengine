import sys, json, glob, importlib
sys.path.insert(0, '/home/claude/study/snap')
import snapdsl
for f in sorted(glob.glob('/home/claude/study/snap/s*_*.py')):
    importlib.import_module(f.split('/')[-1][:-3])
json.dump({str(k): v for k, v in snapdsl.SNAP.items()}, open(sys.argv[1], 'w'), ensure_ascii=False)
print(len(snapdsl.SNAP))
if snapdsl.ERR: print('\n'.join(snapdsl.ERR)); raise SystemExit(1)
