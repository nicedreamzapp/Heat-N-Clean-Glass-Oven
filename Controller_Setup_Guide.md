# REX-C100 Controller Setup Guide — Heat-N-Clean Glass Oven

## Overview

Each unit ships with a REX-C100 PID controller locked to 100–870°F.
Customer can ONLY change the target temperature. All other settings are locked.

---

## Parts List (Controller Box)

| Part | Purpose | Cost |
|------|---------|------|
| REX-C100 (K-type, SSR output) | Temperature control | ~$10 |
| DH48S-2Z timer relay | 6-hour auto-shutoff | ~$10 |
| SSR (40A solid state relay) | Switches Kanthal coil | ~$5 |
| On/Off switch | Master power | ~$2 |
| Inline fuse | Surge protection | ~$0.50 |
| Thermal fuse (~900°F) | Failsafe on oven body | ~$1 |

**Total controller cost: ~$28-30 per unit**

---

## Wiring Order

```
Wall Power (120V AC) → On/Off Switch → DH48S Timer → REX-C100 Power
                                                        ↓
                                              REX-C100 SSR Output → SSR → Kanthal Coil
                                                        ↓
                                              K-Type Thermocouple ← Oven Chamber
```

---

## Programming Each Unit (5 minutes)

### Step 1 — Initial Settings

Hold **SET + DOWN arrow together for 3 seconds** to enter Initial Settings menu.

| Parameter | Set to | Purpose |
|-----------|--------|---------|
| SL1 | `K` | K-type thermocouple input |
| SL2 | `0001` | Fahrenheit, heating only |
| SL4 | `0011` | Process high alarm (overheat safety) |
| SL5 | `0000` | Alarm 2 disabled |
| SLH | `870` | Max temperature customer can set |
| SLL | `100` | Min temperature customer can set |
| oH | `2` | 2°F hysteresis for ON/OFF |
| AH1 | `2` | Alarm hysteresis |

Press SET to confirm each, then hold SET to exit back to normal display.

### Step 2 — PID and Alarm Settings

Hold **SET alone for 3 seconds** to enter Parameter menu.

| Parameter | Set to | Purpose |
|-----------|--------|---------|
| AL1 | `900` | Overheat alarm — kills output at 900°F |
| ATU | `1` | Start auto-tune (run at typical operating temp ~500°F) |

Wait 10-20 minutes for auto-tune to complete (display flashes "AT" then stops).
Auto-tune sets P, I, D values automatically. Do NOT change them after.

| Parameter | Set to | Purpose |
|-----------|--------|---------|
| Ar | `50` | Anti-reset windup |
| T | `2` | Output cycle time (2 sec for SSR) |

### Step 3 — Engineering Menu

Hold SET, scroll to **COD**, enter `0001`.

| Parameter | Set to | Purpose |
|-----------|--------|---------|
| dF | `0` | Disable digital filter (causes false readings if enabled) |

### Step 4 — Lock It Down

Hold SET for 3 seconds, scroll to **LCK**, set to `0110`.

**Customer can now ONLY change target temperature between 100–870°F.**
All menus, PID settings, alarms, and limits are invisible and locked.

### Step 5 — Set DH48S Timer

Set DH48S-2Z timer to 6 hours. When customer turns unit on, timer counts down
and cuts power at 6 hours automatically.

---

## What The Customer Experiences

- Plug in, flip On/Off switch
- Display shows current temperature (top, red) and target temperature (bottom, green)
- Press SET briefly to change target temp (100–870°F only)
- Use arrow buttons to adjust
- Oven heats to target and holds it
- Auto-shutoff at 6 hours
- Turn off when done

That's it. No menus. No confusion. No manual needed.

---

## Security — What Customers CANNOT Do

| Action | Result |
|--------|--------|
| Set temp above 870°F | Blocked by SLH |
| Set temp below 100°F | Blocked by SLL |
| Access PID settings | Blocked by LCK |
| Access initial settings menu | Blocked by LCK |
| Factory reset | No such feature exists |
| Accidentally change settings | Impossible |

Settings survive power outages (stored in EEPROM / non-volatile memory).
No reset button. No backdoor. Locked is locked.

---

## Three-Layer Safety System

1. **REX-C100** — Max setpoint locked at 870°F (software limit)
2. **AL1 alarm at 900°F** — Controller kills output if temp exceeds 900°F
3. **Thermal fuse on oven body (~930°F)** — Permanently cuts power if controller fails

---

## Reliability

- REX-C100: solid state, no moving parts, 10+ year lifespan
- Settings: EEPROM, survives unlimited power cycles
- SSR: most likely part to wear out first (replace every few years if needed)

### Protect Against

| Risk | Solution |
|------|----------|
| Power surge | Inline fuse ($0.50) |
| Thermocouple breaks | AL1 alarm triggers on open circuit |
| SSR fails stuck-on | Thermal fuse melts and cuts power |
| Liquid ingress | Seal controller box enclosure |

---

## REX-C100 Menu Reference

**Two different menus accessed by different button combos:**

| How to enter | Menu | Contains |
|-------------|------|----------|
| Hold SET (3 sec) | Parameter menu | P, I, D, AT, AL1, AL2, Ar, T, LCK |
| Hold SET + DOWN (3 sec) | Initial Settings | SL1, SL2, SL4, SL5, SLH, SLL, oH, AH1, AH2, Pb |

**LCK (Lock) codes:**

| Code | Effect |
|------|--------|
| 0100 | Everything unlocked (for your setup) |
| 0110 | Only target temp changeable (for customers) |
| 0101 | Everything locked |
| 0111 | Total lockout |

**SL2 (Temperature unit) codes:**

| Code | Effect |
|------|--------|
| 0000 | Celsius, heating only |
| 0001 | Fahrenheit, heating only |
| 0010 | Celsius, heating + cooling |
| 0011 | Fahrenheit, heating + cooling |

---

## Future Scaling

At 100+ units, consider sourcing a custom OEM controller from Alibaba:
- Single knob for temp, built-in timer, no menus
- Search: "oven temperature controller with timer OEM"
- Send spec: K-type input, SSR output, 100–870°F, 6hr timer, custom logo
- Expected cost: $12-22/unit at 100 pcs, $6-12/unit at 1000 pcs
- Ask for UL/ETL certification if selling retail in US
