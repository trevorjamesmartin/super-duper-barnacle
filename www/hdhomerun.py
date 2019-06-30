#!/usr/bin/env python3
import datetime
import json
import subprocess
import sys
import urllib.request
import xml.etree.cElementTree as ET
from xml.dom import minidom

output_folder = "/www/static"


def loadGuideFromWeb(device_ip):
    device_auth = json.loads(urllib.request.urlopen("http://%s/discover.json" % device_ip).read())['DeviceAuth']
    return json.loads(urllib.request.urlopen("http://my.hdhomerun.com/api/guide.php?DeviceAuth=%s" % device_auth).read())


def genM3u(device_ip):
    channel_lineup = json.loads(urllib.request.urlopen("http://{}/lineup.json".format(device_ip)).read())
    header = "#EXTM3U"
    fmt = '#EXTINF:0 tvg-chno="{CHNO}" tvg-name="{NAME}" group-title="Antenna",{CHNO}\n{URL}'
    m3u_info = [fmt.format(NAME=chan["GuideName"],
                           CHNO=chan["GuideNumber"],
                           URL=chan["URL"]) for chan in channel_lineup]
    m3u_info.insert(0, header)
    return "\n".join(m3u_info)


def generatXMLTV(data):
    timezone_offset = subprocess.check_output(['date', '+%z']).strip().decode()
    xml = ET.Element("tv")
    for channel in data:
        xmlChannel = ET.SubElement(xml, "channel", id=channel['GuideName'])
        ET.SubElement(xmlChannel, "display-name").text = channel['GuideName']
        ET.SubElement(xmlChannel, "display-name").text = channel['GuideNumber']
        if 'Affiliate' in channel:
            ET.SubElement(xmlChannel, "display-name").text = channel['Affiliate']
        if 'ImageURL' in channel:
            ET.SubElement(xmlChannel, "icon", src=channel['ImageURL'])
        if 'URL' in channel:
            ET.SubElement(xmlChannel, "url").text = channel['URL']
        for program in channel["Guide"]:
            xmlProgram = ET.SubElement(xml, "programme", channel=channel['GuideName'])
            xmlProgram.set("start", " ".join([datetime.datetime.fromtimestamp(program['StartTime']).strftime(
                '%Y%m%d%H%M%S'), timezone_offset]))
            xmlProgram.set("stop", " ".join([datetime.datetime.fromtimestamp(program['EndTime']).strftime(
                '%Y%m%d%H%M%S'), timezone_offset]))
            ET.SubElement(xmlProgram, "title").text = program['Title']
            if 'EpisodeNumber' in program:
                ET.SubElement(xmlProgram, "episode-num").text = program['EpisodeNumber']
            if 'EpisodeTitle' in program:
                ET.SubElement(xmlProgram, "sub-title").text = program['EpisodeTitle']
            if 'Synopsis' in program:
                ET.SubElement(xmlProgram, "desc").text = program['Synopsis']
            if 'OriginalAirdate' in program:
                ET.SubElement(xmlProgram, "date").text = datetime.datetime.fromtimestamp(
                    program['OriginalAirdate']).strftime('%Y%m%d%H%M%S') + " " + timezone_offset
            if 'PosterURL' in program:
                ET.SubElement(xmlProgram, "icon", src=program['PosterURL'])
            if 'Filter' in program:
                for filter in program['Filter']:
                    ET.SubElement(xmlProgram, "category").text = filter
    reformed_xml = minidom.parseString(ET.tostring(xml))
    return reformed_xml.toprettyxml(encoding='utf-8')


def printGuide(data):
    for channel in data:
        print("-----------------CHANEL-----------------")
        print(channel['GuideNumber'])
        print(channel['GuideName'])
        if 'Affiliate' in channel:
            print(channel['Affiliate'])
        if 'ImageURL' in channel:
            print(channel['ImageURL'])
        if 'URL' in channel:
            print(channel['URL'])
        # VideoCodec
        # AudioCodec
        # HD
        # Favorite
        for program in channel["Guide"]:
            print("\t---------------PROGRAM---------------")
            print("\t" + program['Title'].encode('utf-8'))
            print("\t" + str(program['StartTime']))
            print("\t" + str(program['EndTime']))
            if 'EpisodeNumber' in program:
                print("\t" + program['EpisodeNumber'])
            if 'EpisodeTitle' in program:
                print("\t" + program['EpisodeTitle'])
            if 'Synopsis' in program:
                print("\t" + program['Synopsis'].encode('utf-8'))
            if 'OriginalAirdate' in program:
                print("\t" + str(program['OriginalAirdate']))
            print("\t" + program['SeriesID'])
            if 'PosterURL' in program:
                print("\t" + program['PosterURL'])
            if 'Filter' in program:
                for filter in program['Filter']:
                    print("\t\t" + filter.encode('utf-8'))


def saveStringToFile(strData, filename):
    with open(filename, 'w') as outfile:
        outfile.write(strData.decode())


def loadJsonFromFile(filename):
    return json.load(open(filename))


def saveJsonToFile(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def write_m3u(m3u):
    with open("{}/hdhomerun.m3u".format(output_folder), "w") as o:
        o.write(m3u)


def txt_m3u(hdip):
    m3u = genM3u(hdip)
    return m3u


def main(hdip):
    print('ip of hdhomerun is %s' % hdip)
    saveStringToFile(generatXMLTV(loadGuideFromWeb(hdip)),
                     "{}/hdhomerun.xml".format(output_folder))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide device ip as first command line argument.")
        exit(0)
    else:
        _ = sys.argv[1]  # ip
        main(_)
