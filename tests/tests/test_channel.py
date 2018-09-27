import xml.etree.ElementTree as ET
from functools import reduce

import requests
from sqlalchemy import text

from tests.conftest import TEST_PROXY_URL, TEST_RADIO_DNS_URL
from tests.utilities.utilities import compare_lists, sql_alchemy_result_to_list

CHANNELS_MSQL_QUERY = "SELECT name, cc, ecc_id, eid, fqdn, frequency, pi, scids, serviceIdentifier, sid, tx," \
                      "type_id, bitrate, mime_type, stream_url FROM channel"

CHANNELS_HTML_TR = [
    'Station Type Name RadioDNS entry / Url DNS Authoritative FQDN Services',
    'Classical Station amss CS_AMSS 4001.amss.radiodns.org. classicalstation.standalone.radio.ebu.io\nEPG standalone.127.0.0.1:5000standalone.ebu.io\nDelete Edit',
    'Classical Station dab CS_DAB 0.4001.43e1.fe1.dab.radiodns.org. classicalstation.standalone.radio.ebu.io\nEPG standalone.127.0.0.1:5000standalone.ebu.io\nDelete Edit',
    'Classical Station drm CS_DRM 4001.drm.radiodns.org. classicalstation.standalone.radio.ebu.io\nEPG standalone.127.0.0.1:5000standalone.ebu.io\nDelete Edit',
    'Classical Station fm CS_VHF_FM 00917.c00f.fe1.fm.radiodns.org. classicalstation.standalone.radio.ebu.io\nEPG standalone.127.0.0.1:5000standalone.ebu.io\nDelete Edit',
    'Classical Station hd CS_HD_RADIO 0eaff.fe1.hd.radiodns.org. classicalstation.standalone.radio.ebu.io\nEPG standalone.127.0.0.1:5000standalone.ebu.io\nDelete Edit',
    'Classical Station id CS_IP http://server/stream classicalstation.standalone.radio.ebu.io Delete Edit'
]

CHANNELS_MYSQL_TR = [
    'CS_VHF_FM None 1 None None 00917 C00F None None None None fm None None None',
    'CS_DAB None 1 43e1 None None None 0 None 4001 None dab None audio/mpeg None',
    'CS_DRM None None None None None None None None 4001 None drm None None None',
    'CS_AMSS None None None None None None None None 4001 None amss None None None',
    'CS_HD_RADIO fE1 None None None None None None None None 0EAFF hd None None None',
    'CS_IP None None None classicalstation.standalone.radio.ebu.io None None None ebu1standalone None None id 200 audio/mpeg http://server/stream'
]


def test_create_channel(stack_setup, browser_setup):
    db = stack_setup
    driver = browser_setup

    # Fill inputs for VHF/FM
    driver.get(TEST_PROXY_URL + "channels/edit/-")
    driver.find_element_by_name("name").send_keys("CS_VHF_FM")
    driver.find_element_by_id("type").find_element_by_css_selector("option[value=fm]").click()
    driver.find_element_by_name("pi").send_keys("C00F")
    driver.find_element_by_name("frequency").send_keys("00917")
    driver.find_element_by_css_selector("input[type=submit][value=Save]").click()

    # Fill inputs for DAB
    driver.get(TEST_PROXY_URL + "channels/edit/-")
    driver.find_element_by_name("name").send_keys("CS_DAB")
    driver.find_element_by_id("type").find_element_by_css_selector("option[value=dab]").click()
    driver.find_element_by_name("eid").send_keys("43e1")
    driver.find_element_by_name("sid").send_keys("4001")
    driver.find_element_by_name("scids").send_keys("0")
    driver.find_element_by_name("mime_type").send_keys("audio/mpeg")
    driver.find_element_by_css_selector("input[type=submit][value=Save]").click()

    # Fill inputs for DRM
    driver.get(TEST_PROXY_URL + "channels/edit/-")
    driver.find_element_by_name("name").send_keys("CS_DRM")
    driver.find_element_by_id("type").find_element_by_css_selector("option[value=drm]").click()
    driver.find_element_by_name("sid").send_keys("4001")
    driver.find_element_by_css_selector("input[type=submit][value=Save]").click()

    # Fill inputs for AMSS
    driver.get(TEST_PROXY_URL + "channels/edit/-")
    driver.find_element_by_name("name").send_keys("CS_AMSS")
    driver.find_element_by_id("type").find_element_by_css_selector("option[value=amss]").click()
    driver.find_element_by_name("sid").send_keys("4001")
    driver.find_element_by_css_selector("input[type=submit][value=Save]").click()

    # Fill inputs for HD Radio
    driver.get(TEST_PROXY_URL + "channels/edit/-")
    driver.find_element_by_name("name").send_keys("CS_HD_RADIO")
    driver.find_element_by_id("type").find_element_by_css_selector("option[value=hd]").click()
    driver.find_element_by_name("tx").send_keys("0EAFF")
    driver.find_element_by_id("cc").find_element_by_css_selector("option[value='1']").click()
    driver.find_element_by_css_selector("input[type=submit][value=Save]").click()

    # Fill inputs for HD Radio
    driver.get(TEST_PROXY_URL + "channels/edit/-")
    driver.find_element_by_name("name").send_keys("CS_IP")
    driver.find_element_by_id("type").find_element_by_css_selector("option[value=id]").click()
    driver.find_element_by_id("stream_url").send_keys("http://server/stream")
    driver.find_element_by_name("mime_type").send_keys("audio/mpeg")
    driver.find_element_by_name("bitrate").send_keys("200")
    driver.find_element_by_css_selector("input[type=submit][value=Save]").click()

    # Check entered data
    channel_tr = list(map(lambda x: x.text, driver
                          .find_element_by_id("radiodns-channel-table")
                          .find_elements_by_css_selector("tr")))
    assert compare_lists(channel_tr, CHANNELS_HTML_TR)

    # Check DB
    result = db.engine.execute(text(CHANNELS_MSQL_QUERY))
    assert result.rowcount == 6
    station_mysql_tr = []
    for row in sql_alchemy_result_to_list(result):
        station_mysql_tr.append(reduce(lambda x, y: str(x) + " " + str(y), row))
    assert compare_lists(station_mysql_tr, CHANNELS_MYSQL_TR, True)

    # Check XML
    res = requests.get(TEST_RADIO_DNS_URL + "radiodns/spi/3.1/SI.xml")
    assert res.status_code == 200
    bearers = ET.fromstring(res.text).findall(".//{http://www.worlddab.org/schemas/spi/31}bearer")
    assert len(bearers) == 7
    assert bearers[0].attrib["id"] == "amss:4001"
    assert bearers[0].attrib["cost"] == "100"
    assert bearers[1].attrib["id"] == "dab:fe1.43e1.4001.0"
    assert bearers[1].attrib["cost"] == "20"
    assert bearers[1].attrib["mimeValue"] == "audio/mpeg"
    assert bearers[2].attrib["id"] == "drm:4001"
    assert bearers[2].attrib["cost"] == "100"
    assert bearers[3].attrib["id"] == "hd:fe1.0eaff"
    assert bearers[3].attrib["cost"] == "100"
    assert bearers[4].attrib["id"] == "http://server/stream"
    assert bearers[4].attrib["cost"] == "100"
    assert bearers[4].attrib["offset"] == "2000"
    assert bearers[4].attrib["mimeValue"] == "audio/mpeg"
    assert bearers[4].attrib["bitrate"] == "200"
    assert bearers[5].attrib["id"] == "fm:fe1.c00f.00917"
    assert bearers[5].attrib["cost"] == "50"
    assert bearers[6].attrib["id"] == "fm:fr.c00f.00917"
    assert bearers[6].attrib["cost"] == "50"
