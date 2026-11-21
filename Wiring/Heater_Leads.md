# Heater Leads: Kanthal to Terminal Block

How the two kanthal coil leads join the power wire, and how to keep the joint from burning up.

## What went wrong (2026-11-20 prototype)

![Burnt terminal block, screw side](burnt_block_2026-11-20_a.jpg)
![Burnt terminal block in the oven](burnt_block_2026-11-20_b.jpg)

The 1-way porcelain terminal block went black, the screw oxidized, the porcelain cracked, and the
bare kanthal lead melted into a ball at its tip.

Why: the lead was a single strand of the same thin kanthal as the coil, so it got as hot as the coil
all the way to the block. The heat oxidized the screw and the wire under it, the oxide raised the
contact resistance, and the joint began heating itself. Every heat cycle loosened the screw a little
more. The block also sat right against the hot core.

## The fix: a doubled "cold lead"

![How to double the kanthal lead](kanthal_cold_lead_2026-11-20.png)

The coil stays the same. Only the lead, from where the coil stops to the block, gets doubled. Do it
on both leads.

1. **Cut back to clean wire.** Snip off any melted ball and any dark, dull or crusty wire until the
   kanthal is bright. Oxidized kanthal does not carry current well under a screw.
2. **Make room.** Leave the lead about 2x the distance from the coil to the block. If it's short,
   unwind one wrap at each end of the coil: one wrap around the core is about 29 cm (11 in). Losing
   one wrap per end makes the coil slightly stronger; the REX-C100 still holds the set temperature.
   Keep the last remaining wrap snug and not touching its neighbor.
3. **Fold it in half.** Bend the end back so it meets the spot where the coil stops.
4. **Twist the two strands tight** (drill or pliers), all the way from the coil to the fold.
5. **The folded loop goes under the terminal screw.** Clean, shiny wire only. Tighten it hard, and
   snug it again after the first 2 heat-ups (kanthal loosens as it cycles).

Two strands share the current, so each runs far cooler. The lead stops glowing and stops cooking
the screw.

## Block and insulation

- Replace any block that is cracked or blackened.
- Keep the block out of the hot zone when possible: the leads drop through the support ring holes
  into the 25 mm open space under the base, so the block can sit there instead of against the core.
- The doubled leads are insulated with ceramic fiber sleeve where they pass through the insulation.

## Better build (researched 2026-11-20)

**3D view:** [viewer-heater-leads.html](https://nicedreamzapp.github.io/Heat-N-Clean-Glass-Oven/viewer-heater-leads.html)
shows this build on the real oven parts (C1 core with its grooves and temp hole, 03, 04, 01), with a
close-up of each connection part. Rebuild it with `python3 Scripts/build_viewer_heater_leads.py`.

Every kiln maker (Skutt, Paragon, Olympic, Evenheat, L&L) gets the hot kanthal out of the hot zone
first, then makes the joint. None of them clamp kanthal under a brass screw against the core.

| Part | Rated to |
|---|---|
| Brass-screw porcelain block (what burned) | ~200-240 C at the screw |
| Steatite block with stainless hardware | ~450 C |
| MG (mica/fiberglass) high-temp wire | 450 C |
| Nickel-plated crimp splice | ~650 C |
| Steatite / porcelain beads | ~1200 C |

**Recommended build, per lead:**

1. **Lead:** fold back and twist the last ~70 mm (the steps above), so the twist starts inside the hot
   zone and runs through the insulation plus the 25 mm space. Slide 12-15 steatite beads (2.3 mm bore)
   over the twist. Beads keep the wire spaced and don't fray or hold moisture like fiber sleeve.
2. **Through the stainless plate:** a porcelain tube insulator pressed into a 3/8" hole. Never a bare
   hole.
3. **The joint:** trim the pigtail ~8 mm past the insulator, crimp a nickel-plated kiln element
   connector (or a 12-10 AWG high-temp butt splice) onto it, and 12 AWG MG wire into the other end.
   No screw. Use an uninsulated-terminal crimper.
4. **Where it lives:** in the 25 mm space under the base, outside the insulation, with a few vent
   holes so air moves. Keep the joint under ~200 C.
5. **To the controller:** MG wire to a steatite terminal block with stainless hardware on the bottom
   cap, then regular wire to the SSR.
6. **Strain relief:** a stainless P-clip on the MG wire past the joint, so the crimp never carries load.

Avoid: brass or zinc-plated screws on kanthal, porcelain wire nuts (they loosen on kanthal), solder
(won't take on kanthal A1).

**Parts (about $110 for both leads, with spares):**

| Part | Example | Approx |
|---|---|---|
| Steatite beads, 2.3 mm bore | Tempco CER-103-105, or 400-pc packs on Amazon/Newegg | ~$10 |
| Porcelain tube insulator | Skutt porcelain insulator (Krueger Pottery) | ~$2.50 ea |
| Element crimp connectors | Skutt element connectors (6 pack), or Crimp Supply 12-10 high-temp butt splices | $8-22 |
| 12 AWG MG wire, 450 C | Supco 25 ft, or Nassau by the foot | ~$2.70/ft |
| Steatite terminal block, stainless hardware | Tempco EHD-108-101 (Zoro) | $10-15 |
| Stainless P-clips | any hardware supplier | a few $ |

Sources: Skutt element replacement guide (cdn.shopify.com/s/files/1/0272/1968/9606/files/elements.pdf),
L&L terminal hardware (theceramicshop.com/product/24201), Skutt element connectors
(theceramicshop.com/product/2497), Tempco ceramic accessories catalog (tempco.com), Bev Howard kiln
rewiring (bevhoward.com/kiln/KilnWire.htm), Nassau MG wire (nassaunationalcable.com), Crimp Supply
high-temp butt splices (crimpsupply.com). Prices are from the research date and may change.
