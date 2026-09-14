# Talk-to-Print — local voice CAD loop

Voice → parameter patch → CadQuery rebuild → orbiting STL.

This is the path that stays **parametric** (editable numbers, not a mesh blob).
It is not a movie-style morph. CadQuery rebuilds in a few seconds; the viewer
swaps the solid when the new STL is ready.

## Run (once)

```bash
cd talk_to_print
python3 -m pip install flask cadquery
python3 server.py
```

Open http://127.0.0.1:8787

Chrome or Edge (Web Speech API). Allow the microphone.

## Voice examples

- "show the outer"
- "show the inner"
- "air gap 1.2 millimeters"
- "make the spokes thinner"
- "sixteen poles"
- "export stl"

Locked magnet pockets (Ø20.60 / Ø5.60) will not change unless you say
"unlock pockets".

## Two layers — do not mix them up

| Layer | What it is | When to use |
|---|---|---|
| This app | Your RF16S family, locked physics, local | Generators you will print |
| Grok voice in this chat | I rebuild and hand you an STL | No install, slower loop |
| Zoo Design Studio / Zookeeper | Cloud B-rep + talk-to-edit | Brand-new parts, not our family |
| Meshy / Tripo / Luma | Pretty mesh | Never for printable generators |

Optional: set `XAI_API_KEY` if you want free-form speech mapped by Grok
instead of the built-in command parser. The kernel still owns dimensions.
