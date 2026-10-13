import sys, json, os
sys.path.insert(0, 'tools')
import pixel_common as pc
from PIL import Image
H = dict(rat=28, **{'dust-moth':26,'cellar-spider':24,'cave-cricket':28,'rustle':36,'cobweb-wraith':40,'barrel-mimic':38,
     'crock-mimic':34,'toad':30,'shade':40,'wick-sprite':32,'root-tangle':40,'keybearer-moth':64,'keybearer-beetle':68,
     'keybearer-mushroom':68,'cellar-king':80})
pal = pc.load_palette('palette.json')
for n, h in H.items():
    sheet = Image.open(f'mclean/{n}.png').convert('RGB')
    back = (0, 255, 0)
    cw = sheet.width // 6
    subs = []
    for i in range(6):
        c = pc.hard_alpha(pc.key_out(sheet.crop((i*cw, 0, (i+1)*cw, sheet.height)), back))
        bb = pc.opaque_bbox(c); subs.append(c.crop(bb))
    k = h / subs[0].height
    smalls = []
    for s in subs:
        w2, h2 = max(1, round(s.width*k)), max(1, round(s.height*k))
        smalls.append(pc.lock_palette(pc.despeckle(pc.shrink(s, w2, h2)), pal))
    fw = max(s.width for s in smalls) + 2; fh = max(s.height for s in smalls) + 1
    out = Image.new('RGBA', (fw*6, fh), (0,0,0,0))
    for i, s in enumerate(smalls):
        out.alpha_composite(s, (i*fw + (fw - s.width)//2, fh - s.height))
    os.makedirs('creatures', exist_ok=True)
    out.save(f'creatures/{n}-sheet.png'); smalls[0].save(f'creatures/{n}.png')
    json.dump({"image": f"{n}-sheet.webp", "frame": [fw, fh], "fps": 8,
               "directions": {"down": {"idle": [0,0,0,0,1,1,1,1], "walk": [2,3], "attack": [4,4,4], "hurt": [5,5,5]}}},
              open(f'creatures/{n}.sheet.json','w'), indent=1)
    print(n, (fw, fh), [s.size for s in smalls][:2])
