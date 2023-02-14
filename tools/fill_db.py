#!/bin/env python3

from pymongo import MongoClient

data = '''Alterra Technology
-1625 -350 100	Entrance to second wreck in the Dunes
-1445 -330 720	Entrance to Wreck 6 (1) in the Dunes
-1405 -330 720	Entrance to Wreck 6 (1) in the Dunes
-1395 -320 710	Entrance to Wreck 6 (1) in the Dunes
-1215 -350 -380	Entrance to Wreck 8 in the Blood Kelp Zone
-1210 -217 7	Entrance to third wreck in the Dunes
-1205 -330 -390	Entrance to Wreck 8 in the Blood Kelp Zone
-1160 -185 -740	Entrance to Wreck 7 (1) in the Sea Treader's Path
-1155 -160 -740	Entrance to Wreck 7 (1) in the Sea Treader's Path
-1120 -185 -735	Entrance to Wreck 7 in the Sea Treader's Path
-919 -177 508	Destroyed Lifepod 13
-900 -420 -1430	Entrance to Wreck 11 in the Grand Reef
-885 -440 -1415	Entrance to Wreck 11 in the Grand Reef
-808 -298 -873	Destroyed Lifepod 19
-795 -220 -715	Entrance to Wreck 20 in the Sparse Reef
-795 -200 -780	Entrance to Wreck 20 in the Sparse Reef
-665 -120 781	Entrance to Wreck 9 (1) in the Northwestern Mushroom Forest
-660 -123 760	Entrance to Wreck 9 (1) in the Northwestern Mushroom Forest
-660 -100 775	Entrance to Wreck 9 (1) in the Northwestern Mushroom Forest
-645 -110 775	Entrance to Wreck 9 in the Northwestern Mushroom Forest
-665 -80 -15	Entrance to Wreck 2 in the Grassy Plateaus
-625 -70 -15	Entrance to Wreck 2 in the Grassy Plateaus
-520 -90 -215	Small Wreck 3 in the Grassy Plateaus
-510 -91 -45	Destroyed Lifepod 17
-490 -500 1330	Destroyed Lifepod 2
-425 -105 -275	Entrance to Wreck 14 (1) in the Grassy Plateaus
-425 -105 -260	Entrance to Wreck 14 (1) in the Grassy Plateaus
-400 -130 650	Entrance to Wreck 12 (1) in the Grassy Plateaus
-390 -125 635	Entrance to Wreck 12 (1) in the Grassy Plateaus
-370 -100 475	Small Wreck 1 in the Grassy Plateaus
-320 -75 255	Entrance to Wreck 18 in the Kelp Forest
-284 -93 606	Small Wreck in the Grassy Plateaus
-280 -265 -795	Entrance to Wreck 10 (1) in the Grand Reef
-280 -250 -775	Entrance to Wreck 10 (1) in the Grand Reef
-275 -230 -780	Entrance to Wreck 10 (1) in the Grand Reef
-160 -20 -225	Small Wreck 10 in the Safe Shallows
-140 -190 850	Entrance to Wreck 4 (1) on Underwater Islands
-125 -185 895	Entrance to Wreck 4 (1) on Underwater Islands
-90 -190 860	Entrance to Wreck 4 (1) on Underwater Islands
-55 -180 -1040	Destroyed Lifepod 7
-35 -25 -400	Entrance to Wreck 15 in the Safe Shallows
-33 -20 410	Destroyed Lifepod 3
-30 -95 -610	Entrance to Wreck 13 in the Grassy Plateaus
20 -10 300	Small Wreck 6 in the Safe Shallows
65 -35 390	Entrance to Wreck 17 (1) in the Kelp Forest
65 -30 385	Entrance to Wreck 17 (1) in the Kelp Forest
65 -10 -85	Small Wreck 8 in the Safe Shallows
90 -20 120	Small Wreck 9 in the Safe Shallows
165 -86 -520	Small Wreck 2 in the Grassy Plateaus
175 -23 -253	Small Wreck 11 in the Safe Shallows
270 -85 70	Small Wreck 5 in the Grassy Plateaus
305 -100 450	Entrance to Wreck 1 (1) in the Grassy Plateaus
310 -23 -119	Small Wreck 7 in the Safe Shallows
320 -90 450	Entrance to Wreck 1 (1) in the Grassy Plateaus
322 -90 222	Small Wreck 4 in the Grassy Plateaus
335 -90 435	Entrance to Wreck 1 (1) in the Grassy Plateaus
364 -110 310	Destroyed Lifepod 6
390 -15 -190	Entrance to Wreck 16 in the Safe Shallows
685 -335 1195	Entrance to Wreck 5 in the Mountains
715 -370 1190	Entrance to Wreck 5 in the Mountains
640 -130 -580	Aurora debris in the Crash Zone Trenches
717 -7 161	Destroyed Lifepod 4
840 -55 -10	Post-explosion tunnel entrance leading the Aurora's power generator room (in latest versions this entrance has been blocked off)
925 -195 605	Entrance to Wreck 3 in the Bulb Zone
1000 40 110	Post-explosion doorway leading to the Aurora's power generator room
1070 -275 1345	Entrance to Wreck 19 in the Mountains
1115 -265 565	Destroyed Lifepod 12
1295 -215 577	Entrance to second wreck in the Bulb Zone
1300 -215 580	Entrance to second wreck (1) in the Bulb Zone
1315 -225 577	Entrance to second wreck (1) in the Bulb Zone

Biomes
-725 -105 0	Jellyshroom Cave entrance (1)
-495 -90 15	Jellyshroom Cave entrance (1)
-360 -110 -225	Jellyshroom Cave entrance (1)
130 -95 -390	Jellyshroom Cave entrance (1)
-840 -450 -1335	Opening to the Deep Grand Reef (1)
-710 -375 -1190	Opening to the Deep Grand Reef (1)
-670 -400 -1280	Opening to the Deep Grand Reef (1)
-650 -390 -1100	Opening to the Deep Grand Reef (1)
-640 -390 -1205	Opening to the Deep Grand Reef (1)
-510 -420 -1220	Opening to the Deep Grand Reef (1)
-460 -440 -1020	Opening to the Deep Grand Reef (1)
-1220 -610 -325	Opening to the Lost River Corridor (1) from the Blood Kelp Trench
-1137 -613 -446	Opening to the Lost River Ghost Canyon (1) from the Blood Kelp Trench
-705 -565 1090	Opening to the Lost River Ghost Forest (1) from the Northern Blood Kelp Zone
1166 -410 889	Opening to the Lost River Mountains Corridor (1) between the Bulb Zone and Mountains
-1280 -970 400	Opening to the Inactive Lava Zone Corridor (1) from the Lost River Tree Cove
270 -909 688	Opening to the Inactive Lava Zone (1) from the Lost River Mountains Corridor
-79 -1180 0	Entrance to the Lava Castle (1)
-20 -1180 210	Entrance to the Lava Castle (1)
-250 -1340 -80	Opening to the Lava Lakes (1) from the Lava Pit
75 -1260 340	Opening to the Lava Lakes (1) from the Inactive Lava Zone

Caves
-1640 -255 700	Dunes Caves entrance (1)
-1620 -270 775	Dunes Caves entrance (1)
-1500 -400 530	Sea Crown Caves entrance
-1490 -340 580	Dunes Caves entrance
-1475 -415 515	Dunes Caves entrance
-1470 -400 465	Dunes Caves entrance
-1320 -435 -260	Entrance to the Blood Kelp Trench Caves
-1260 -320 -680	Entrance to the Sea Treader's Tunnel Caves (1)
-1200 -210 -830	Entrance to the Sea Treader's Tunnel Caves (1)
-1150 -395 -510	Entrance to the Blood Kelp Trench Caves (1)
-1065 -440 -530	Entrance to the Blood Kelp Trench Caves (2)
-1025 -370 -610	Entrance to the Blood Kelp Trench Caves (1)
-1015 -435 -500	Entrance to the Blood Kelp Trench Caves (2)
-950 -420 -580	Entrance to the Blood Kelp Trench Caves (2)
-890 -155 590	Lower entrance to the caves inside the Giant Tree Mushroom (1)
-855 -78 575	Upper entrance to the caves inside the Giant Tree Mushroom (1)
-855 -150 575	Entrance to small cave (1) at the bottom of the Giant Tree Mushroom
-850 -155 595	Entrance to small cave (1) at the bottom of the Giant Tree Mushroom
-800 -130 -150	Sea Crown Caves entrance
-756 -430 -1444	Grand Reef Caves
-700 -115 -100	Grassy Plateaus Caves entrance (1)
-680 -130 -140	Grassy Plateaus Caves entrance (1)
-645 -125 -150	Grassy Plateaus Caves entrance
-625 -125 -195	Sea Crown Caves entrance
-505 -100 -100	Grassy Plateaus Caves entrance
-110 -55 450	Entrance to Kelp Forest Caves with Eye Stalks (1)
-90 -60 265	Entrance to Kelp Forest Caves with Crashfish (2)
-25 -40 470	Entrance to Kelp Forest Caves with Eye Stalks (1)
55 -60 475	Entrance to Kelp Forest Caves with Eye Stalks (1)
65 -115 -610	Grassy Plateaus Caves entrance (2)
80 -80 245	Entrance to Kelp Forest Caves with Crashfish (2)
115 -120 -715	Grassy Plateaus Caves entrance (2)
180 -80 630	Entrance to Kelp Forest Caves (3)
205 -70 570	Entrance to Kelp Forest Caves (3)
240 -120 970	Entrance to Mountain Island's Mountains Caves (1) underwater portion
250 -100 290	Sea Crown Caves entrance
300 -75 635	Entrance to Kelp Forest Caves (3)
335 10 1025	Entrance to Mountain Island's Mountains Caves (1) surface portion
740 -185 580	Mushroom Forest Caves entrance connecting to Bulb Zone Caves (1)
860 -235 520	Bulb Zone Caves entrance (1) connecting to Mushroom Forest Caves
860 -345 1360	Mountains Caves entrance (1)
885 -295 1515	Mountains Caves entrance (1)
910 -220 615	Bulb Zone Caves entrance (2)
910 -220 650	Bulb Zone Caves entrance (2)
960 -350 1200	Mountains Caves entrance (1)
985 -285 1385	Mountains Caves entrance (1)
1085 -366 1325	Mountains Caves entrance (1)
1205 -250 560	Entrance to Bulb Zone Caves with one Eye Stalk (3)
1215 -230 565	Entrance to Bulb Zone Caves (4)
1315 -430 1320	Mountains Caves entrance

Degasi Seabases
-800 80 -1055	Degasi Seabase (1A) on Floating Island
-705 80 -1165	Degasi Seabase (1B) on Floating Island
-760 15 -1115	Degasi Seabase (1C) on Floating Island
95 -250 -375	Degasi Seabase 2 in the Jellyshroom Cave
-680 -515 -941	Degasi Seabase 3 in the Deep Grand Reef

Lava Geysers and Thermal Vents
-1735 -225 715	Dunes	Thermal Vents
-1640 -360 410	Dunes	Thermal Vents
-1500 -400 500	Dunes	Thermal Vents
-1490 -320 910	Dunes	Thermal Vent
-1470 -300 90	Dunes	Thermal Vents
-1400 -340 270	Dunes	Thermal Vent
-1340 -310 250	Dunes	Thermal Vents
-1250 -330 1000	Dunes	Thermal Vent
-1150 -400 -1450	Grand Reef	Thermal Vents
-1090 -180 10	Dunes	Thermal Vents
-1070 -900 520	Lost River	Thermal Vents
-1030 -910 370	Lost River	Thermal Vents
-1000 -690 -50	Lost River	Thermal Vents
-975 -410 -1380	Grand Reef	Thermal Vents
-930 -910 310	Lost River	Thermal Vents
-920 -750 -40	Lost River	Thermal Vents
-820 -750 -200	Lost River	Thermal Vent
-800 -720 -250	Lost River	Thermal Vent
-750 -750 -100	Lost River	Thermal Vent
-720 -520 -1110	Deep Grand Reef	Thermal Vents
-645 -840 355	Lost River	Thermal Vent
-615 -495 -1235	Deep Grand Reef	Thermal Vents
-615 -480 -1140	Deep Grand Reef	Thermal Vents
-600 -850 260	Lost River	Thermal Vents
-590 -760 -110	Lost River	Thermal Vent
-575 -300 -190	Jellyshroom Cave	Lava Geyser
-570 -830 350	Lost River	Thermal Vents
-560 -560 -900	Deep Grand Reef	Thermal Vents
-530 -810 200	Lost River	Thermal Vents
-460 -380 -1260	Grand Reef	Thermal Vents
-430 -250 -800	Grand Reef	Thermal Vents
-420 -270 -220	Jellyshroom Cave	Chain of Lava Geysers
-380 -200 -730	Grand Reef	Thermal Vents
-310 -275 -50	Jellyshroom Cave	Lava Geyser
-175 -505 1025	Underwater Islands	Lava Geyser
-150 -510 950	Underwater Islands	Lava Geyser
-80 -515 930	Underwater Islands	Lava Geyser
-80 -515 965	Underwater Islands	Lava Geyser
-75 -25 -445	Safe Shallows	Lava Geyser
-70 -515 1025	Underwater Islands	Lava Geyser
-60 -505 1065	Underwater Islands	Lava Geyser
-30 -520 975	Underwater Islands	Lava Geyser
-25 -495 1100	Underwater Islands	Lava Geyser
25 -90 245	Kelp Forest Caves	Lava Geyser
310 -280 1450	Mountains	Thermal Vent
450 -740 980	Lost River	Thermal Vents
515 -260 1605	Mountains	Thermal Vents
540 -305 1445	Mountains	Thermal Vent
555 -190 995	Mountains	Thermal Vent
590 -285 1270	Mountains	Thermal Vents
640 -680 1020	Lost River	Thermal Vents
770 -290 1395	Mountains	Thermal Vent
775 -250 510	Bulb Zone Caves	Lava Geyser
840 -330 1260	Mountains	Thermal Vent
865 -600 965	Lost River	Thermal Vent
945 -345 1440	Mountains Caves	Thermal Vent
965 -260 470	Bulb Zone	Lava Geyser
965 -250 625	Bulb Zone	Lava Geyser
1045 -365 1270	Mountains Caves	Thermal Vent
1130 -285 1690	Mountains	Thermal Vent
1145 -275 555	Bulb Zone	Lava Geyser
1330 -335 1065	Mountains	Thermal Vents

Leviathan Spawns
445 -16 -490	Crash Zone Trench	Reaper Leviathan
594 -47 -646	Crash Zone Trench	Reaper Leviathan
312 -28 -829	Crash Zone Trench	Reaper Leviathan
684 -216 -1038	Crash Zone Mesas	Reaper Leviathan
875 -86 -714	Crash Zone	Reaper Leviathan
1015 -288 -1024	Crash Zone	Reaper Leviathan
1375 -78 -446	Crash Zone	Reaper Leviathan
1587 -234 -61	Crash Zone	Reaper Leviathan
1436 -186 218	Crash Zone	Reaper Leviathan
1112 -87 287	Crash Zone	Reaper Leviathan
478 -135 992	Mountains	Reaper Leviathan
648 -337 1404	Mountains	Reaper Leviathan
698 -295 1646	Mountains	Reaper Leviathan
967 -237 -1598	Mountains	Reaper Leviathan
1266 -361 1420	Mountains	Reaper Leviathan
1075 -224 1220	Mountains	Reaper Leviathan
1303 -308 1091	Mountains	Reaper Leviathan
-1119 -116 21	Dunes	Reaper Leviathan
-1460 -275 -17	Dunes	Reaper Leviathan
-1742 -303 103	Dunes	Reaper Leviathan
-1412 -224 223	Dunes	Reaper Leviathan
-1610 -273 404	Dunes	Reaper Leviathan
-1782 -202 849	Dunes	Reaper Leviathan
-1371 -288 942	Dunes	Reaper Leviathan
-1419 -293 1139	Dunes	Reaper Leviathan
-441 -304 -1371	Grand Reef	Ghost Leviathan (Adult)
-1239 -273 -1282	Grand Reef	Ghost Leviathan (Adult)
-612 -306 1424	Northern Blood Kelp Zone	Ghost Leviathan (Adult)
-776 -684 -256	Lost River Bone Fields	Ghost Leviathan (Juvenile)
-884 -590 866	Lost River Ghost Forest	Ghost Leviathan (Juvenile)
250 -833 742	Lost River Mountains Corridor	Ghost Leviathan (Juvenile)
57 -1158 307	Inactive Lava Zone	Sea Dragon Leviathan
-96 -1101 -118	Inactive Lava Zone	Sea Dragon Leviathan
100 -1400 -90	Lava Lakes	Sea Dragon Leviathan

Precursor Structures
430 -90 1190	Quarantine Enforcement Platform
-380 -750 410	Disease Research Facility
-75 -1182 5	Alien Thermal Plant
200 -1440 -222	Primary Containment Facility
-1111 -685 -655	Lost River Laboratory Cache
-1190 -380 1128	Dunes Sanctuary Cache
-905 -300 -775	Deep Sparse Reef Sanctuary Cache
-589 -555 1482	Northern Blood Kelp Zone Sanctuary Cache
-931 -611 991	Ghost Forest Alien Arch
-750 -239 435	Northwestern Mushroom Forest Alien Arch
-662 2 -1050	Floating Island Alien Arch
-81 -290 -1360	Crag Field Alien Arch
340 61 903	Mountain Island Alien Arch
463 -165 1353	Mountains Alien Arch
1383 -296 757	Bulb Zone Alien Arch
-1160 -245 -140	Dunes Alien Vent Entrance Point
-940 -335 -1220	Grand Reef Alien Vent Entrance Point
-725 -300 -725	Deep Sparse Reef Alien Vent Entrance Point
-465 -70 870	Underwater Islands Alien Vent Entrance Point
650 -170 480	Northeastern Mushroom Forest Alien Vent Entrance Point
750 -285 1020	Mountains Alien Vent Entrance Point

Skeletons and Minor Structures
-1070 -685 -568	Ancient Skeleton in the Lost River
-705 -760 -260	Gargantuan Fossil in the Lost River Bone Fields
-625 -830 285	Sea Dragon Leviathan Skeleton in the Lost River Junction
-230 -800 250	Research Specimen Theta in the Disease Research Facility
-250 -1240 250	Reaper Leviathan skull in the Inactive Lava Zone
-230 -1250 -17	Reaper Leviathan Skeleton in the Inactive Lava Zone
-20 -1250 300	Reaper Leviathan Skeleton in the Inactive Lava Zone
175 -1250 280	Reaper Leviathan Skeleton in the Inactive Lava Zone
712 -670 965	Reaper Leviathan Skeleton in the Lost River Mountains Corridor
878 -594 945	Reaper Leviathan Skeleton in the Lost River Mountains Corridor
-1650 -340 165	Arch-like formation in the Dunes
-1500 -370 500	Dunes Sinkhole
-1144 -329 1147	Meteor crater in the Dunes
-1020 -180 -1100	Building-like formations in the Grand Reef
-990 -190 710	Small cave fissure in the Northwestern Mushroom Forest
-920 -860 425	Giant Cove Tree in the Lost River Tree Cove
-870 -50 580	Top of the Giant Tree Mushroom in the Northwestern Mushroom Forest
-285 -1325 -155	The Lava Pit in the Inactive Lava Zone
-75 -1070 130	Apex of the Lava Castle in the Inactive Lava Zone
20 -40 -440	Stonehenge-like structure in the Kelp Forest close to Wreck 15
1040 0 -160	Center of the radiation zone (the radius being 940m)
'''


def scan_data(s):
    topic = ''
    for line in s.split('\n'):
        if line == '':
            topic = ''
            continue
        if topic == '':
            topic = line
            continue
        try:
            x, y, z, name = line.split(maxsplit=3)
        except ValueError:
            print(f'cannot split {line}')
            continue
        yield {
            'x': x, 'y': y, 'z': z,
            'name': f'{topic} - {name}',
            'submitter': 'Subnautica Fandom Wiki',
        }

client = MongoClient('mongodb://mongodb')
db = client.subnautica

locs = scan_data(data)
db.locations.insert_many(locs)
