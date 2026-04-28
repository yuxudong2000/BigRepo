#!/usr/bin/env python3
"""Fix keys to match admissions.json exactly and add missing school-major combos"""
import json

with open('/Users/yuxudong/Downloads/高考/gaokao-web/data/admissions.json') as f:
    admissions = json.load(f)

with open('/Users/yuxudong/Downloads/高考/gaokao-web/data/school_details.json') as f:
    details = json.load(f)

# Get all combos from admissions
combos = set()
for row in admissions:
    combos.add((row['school_name'], row['major_name']))

# Build a lookup: school -> existing detail data (normalize by matching school name)
# We need to remap some keys

# Key remapping - map our old keys to correct admissions keys
remappings = {
    # HIT - map generic to actual majors
    "哈尔滨工业大学|计算机类(计算机)": None,  # This key doesn't exist in admissions, expand
    # BJTU - fix
    "北京邮电大学|计算机类(网络安全)": None,  # fix
    # HUST - fix  
    "华中科技大学|工科试验班(AI先进技术拔尖班)": None,  # fix
    # SCUEC - fix
    "华南理工大学|工科试验班(计算机与电子信息)": None,  # fix
}

print("=== Keys in details vs admissions ===")
for key in sorted(details.keys()):
    school, major = key.split('|', 1)
    if (school, major) in combos:
        print(f"  ✓ MATCH: {key}")
    else:
        # Find closest match
        school_majors = [(s, m) for s, m in combos if s == school]
        if school_majors:
            print(f"  ✗ NO MATCH: {key}")
            print(f"    Available for {school}:")
            for s, m in sorted(school_majors):
                print(f"      '{s}|{m}'")
        else:
            print(f"  ✗ SCHOOL NOT FOUND: {key}")
