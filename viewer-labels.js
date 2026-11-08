// Shared part labels for the separated views (2026-11-08).
// Labels sit in two straight columns, right of the parts and left of the parts (bolts, screws and other
// side items go left), each with a thin leader line to its part. Every frame the labels on a side are sorted
// by height and pushed apart so no two ever overlap, whatever the zoom.
import * as THREE from 'three';

export function makeLabeler(scene, items, { rx, RADIAL, makeLabel, size = 1.7, left = it => !!(it.p.radial || it.p.side) }) {
  const grp = new THREE.Group(); scene.add(grp);
  const R0 = rx + RADIAL + 40;
  const lineMat = new THREE.LineBasicMaterial({ color: 0x555a63, depthTest: false, transparent: true, opacity: 0.85 });
  const rows = items.map(it => {
    const spr = makeLabel(it.p.label); const w = spr.scale.x, h = spr.scale.y;
    const L0 = left(it); grp.add(spr);
    const geo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3(), new THREE.Vector3()]);
    const ln = new THREE.Line(geo, lineMat); ln.renderOrder = 9; grp.add(ln);
    const s = it.bbL || it.bb; const rPart = Math.max(Math.abs(s.min.x), Math.abs(s.max.x), Math.abs(s.min.y), Math.abs(s.max.y));
    const it2 = { it, spr, w, h, L0, L: L0, ln, rPart }; it.lbl = spr; return it2; });
  let vis = true;
  function setVisible(v) { vis = v; grp.visible = v; }
  function update(ls, f = 1) {
    if (!vis) return;
    const S = 48 * 0.25 * ls * size * 1.15;                      // label height in world units + a gap
    const anchors = rows.map(r => { const c = (r.it.cL || r.it.c).clone(); r.it.g.localToWorld(c); return c; });
    // assign sides greedily from the bottom up: each label goes to the column where it moves the least
    // (bolts and side parts prefer the left), so both columns stay short and nothing is pushed off screen
    const all = rows.map((r, i) => ({ r, a: anchors[i] })).sort((p, q) => p.a.z - q.a.z);
    const last = { true: -Infinity, false: -Infinity };
    for (const o of all) {
      const zl = Math.max(o.a.z, last[true] + S), zr = Math.max(o.a.z, last[false] + S);
      const pref = o.r.L0 ? (zl - o.a.z) <= (zr - o.a.z) + S : (zl - o.a.z) + S < (zr - o.a.z);
      o.r.L = pref; o.z = pref ? zl : zr; last[pref] = o.z; }
    let zTop = -Infinity, zBot = Infinity;
    for (const side of [true, false]) {
      const rs = all.filter(o => o.r.L === side);
      rs.forEach(o => { zTop = Math.max(zTop, o.z + S / 2); zBot = Math.min(zBot, o.z - S / 2); });
      for (const o of rs) {
        const sg = side ? -1 : 1, r = o.r;
        r.spr.scale.set(r.w * ls * size, r.h * ls * size, 1);
        r.spr.center.set(side ? 1 : 0, 0.5); r.spr.position.set(sg * R0, 0, o.z);
        const reach = r.rPart + (r.it.p.radial ? RADIAL * f : 0);
        const p = r.ln.geometry.attributes.position;
        p.setXYZ(0, sg * (R0 - 3 * ls), 0, o.z); p.setXYZ(1, sg * (R0 - 22 * ls), 0, o.z); p.setXYZ(2, sg * reach, 0, o.a.z);
        p.needsUpdate = true; r.ln.geometry.computeBoundingSphere();
      }
    }
    api.zTop = zTop; api.zBot = zBot; api.wMax = Math.max(...rows.map(r => r.spr.scale.x));
  }
  const maxW = Math.max(...rows.map(r => r.w)) * size;
  const api = { update, setVisible, R0, maxW, group: grp, zTop: null, zBot: null };
  return api;
}
