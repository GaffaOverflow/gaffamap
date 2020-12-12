#!/usr/bin/env python3

import json


def merge_tilesets(m):
    tileset_map = {}
    global merged_map, merged_map_next_tileset_gid
    for tileset in m["tilesets"]:
        found = False
        merged_tileset_start = -1
        for merged_tileset in merged_map["tilesets"]:
            if tileset["image"] == merged_tileset["image"]:
                found = True
                merged_tileset_start = merged_tileset["firstgid"]
                break
        if found:
            for i in range(tileset["tilecount"]):
                tileset_map[tileset["firstgid"]+i] = merged_tileset_start + i
        else:
            for i in range(tileset["tilecount"]):
                tileset_map[tileset["firstgid"]+i] = merged_map_next_tileset_gid + i
            tileset["firstgid"] = merged_map_next_tileset_gid
            merged_map_next_tileset_gid = merged_map_next_tileset_gid + tileset["tilecount"]
            merged_map["tilesets"].append(tileset)
    return tileset_map


def merge_tilelayer(layer, m):
    global merged_map, min_x, min_y
    found = False
    for merged_layer in merged_map["layers"]:
        if merged_layer["name"] == layer["name"]:
            found = True
            for x in range(m["width"]):
                merged_x = m["offset_x"] - min_x + x
                for y in range(m["height"]):
                    merged_y = m["offset_y"] - min_y + y
                    merged_pos = merged_y * merged_layer["width"] + merged_x
                    layer_pos = y * layer["width"] + x
                    merged_layer["data"][merged_pos] = layer["data"][layer_pos]
            break
    if not found:
        new_layer = {}
        new_layer["data"] = [0] * merged_map["height"] * merged_map["width"]
        new_layer["height"] = merged_map["height"]
        new_layer["id"] = merged_map["nextlayerid"]
        merged_map["nextlayerid"] = merged_map["nextlayerid"] + 1
        new_layer["name"] = layer["name"]
        new_layer["opacity"] = layer["opacity"]
        if "properties" in layer:
            new_layer["properties"] = layer["properties"]
        new_layer["startx"] = 0
        new_layer["starty"] = 0
        new_layer["type"] = "tilelayer"
        new_layer["visible"] = layer["visible"]
        new_layer["width"] = merged_map["width"]
        new_layer["x"] = 0
        new_layer["y"] = 0
        for x in range(m["width"]):
            merged_x = m["offset_x"] - min_x + x
            for y in range(m["height"]):
                merged_y = m["offset_y"] - min_y + y
                merged_pos = merged_y * new_layer["width"] + merged_x
                layer_pos = y * layer["width"] + x
                new_layer["data"][merged_pos] = layer["data"][layer_pos]
        merged_map["layers"].append(new_layer)


merged_map = {}
merged_map["compressionlevel"] = -1
merged_map["infinite"] = False
merged_map["layers"] = []
merged_map["nextlayerid"] = 1
merged_map["nextobjectid"] = 1
merged_map["orientation"] = "orthogonal"
merged_map["renderorder"] = "right-down"
merged_map["tileheight"] = 32
merged_map["tilesets"] = []
merged_map["tilewidth"] = 32
merged_map["type"] = "map"
merged_map["version"] = 1.4
merged_map_next_tileset_gid = 1

min_x = 0
max_x = 0
min_y = 0
max_y = 0

map_parts = []

map_list = json.load(open("merge.json", "r"))
for m in map_list:
    map_data = json.load(open(m["path"], "r"))
    if map_data["infinite"]:
        print("skipping map", m["path"], "(can't handle infinite maps)")
        continue
    if map_data["compressionlevel"] != -1:
        print("skipping map", m["path"], "(can't handle compression at the moment)")
        continue
    map_data["offset_x"] = m["x"]
    map_data["offset_y"] = m["y"]
    map_parts.append(map_data)
    if m["x"] < min_x:
        min_x = m["x"]
    if m["y"] < min_y:
        min_y = m["y"]
    if m["x"] + map_data["width"] > max_x:
        max_x = m["x"] + map_data["width"]
    if m["y"] + map_data["height"] > max_y:
        max_y = m["y"] + map_data["height"]

print("min_x:", min_x, "max_x:", max_x)
print("min_y:", min_y, "max_y:", max_y)
merged_map["width"] = max_x - min_x
merged_map["height"] = max_y - min_y
print("map size: ", merged_map["width"], "x", merged_map["height"])

for m in map_parts:
    tileset_map = merge_tilesets(m)

    # merge layers
    for layer in m["layers"]:
        if "compression" in layer and layer["compression"] != "":
            print("skipping layer", layer["name"], "because it is compressed")
            continue
        if layer["type"] == "tilelayer":
            merge_tilelayer(layer, m)
        else:
            print("skipping layer", layer["name"], "(can't handle", layer["type"], "yet)")
            continue
json.dump(merged_map, open("src/maps/merged_map.json", "w"))
