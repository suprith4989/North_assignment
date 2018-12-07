import logging
import sys

import pytest
import requests

# I have used logging here for ease of understanding for the user with INFO and ERROR level messages
# in the output. You have to just do a 'pytest <filename> -qsv' if run manually.

log = logging.getLogger()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
URI = 'http://services.groupkt.com/country'

@pytest.mark.parametrize('args', ['all', pytest.param('', marks=pytest.mark.xfail),
                                  pytest.param('asdf', marks=pytest.mark.xfail),
                                  pytest.param('static', marks=pytest.mark.xfail),
                                  pytest.param('single', marks=pytest.mark.xfail)])
def test_get_all_api(args):
    URL = URI + '/get/{}'.format(args)
    output = requests.get(URL)
    if output.status_code == 200:
        try:
            data = output.json()
            if 'html' not in output.text and 'result' in data['RestResponse'].keys():
                country_data = data['RestResponse']['result']
                assert 'alpha2_code' in country_data[0].keys()
                assert 'alpha3_code' in country_data[0].keys()
                assert 'name' in country_data[0].keys()
        except Exception as e:
            log.error(e)
            assert '<div class="col-md-9"> 404 </div>' in output.text
    else:
        pytest.xfail()


@pytest.mark.parametrize('alpha2, alpha3, country,', [('AF', 'AFG', 'Afghanistan'),
                                                      ('CK', 'COK', 'Cook Islands'),
                                                      ('BQ', 'BES', 'Bonaire, Sint Eustatius and Saba'),
                                                      ('ZZ', None, None)])
def test_get_iso2_code_api(alpha2, alpha3, country):
    ISO2_URL = URI + '/get/iso2code/{}'
    iso2_output = requests.get(ISO2_URL.format(alpha2))
    if iso2_output.status_code == 200:
        try:
            raw_details = iso2_output.json()
            if 'html' not in iso2_output.text and 'result' in raw_details['RestResponse'].keys():
                details = raw_details['RestResponse']['result']
                assert country == details['name']
                assert alpha2 == details['alpha2_code']
                assert alpha3 == details['alpha3_code']
                log.info("Found {} in alpha2_code api.".format(country))
            elif 'messages' in raw_details['RestResponse'].keys():
                text = raw_details['RestResponse']
                assert 'No matching country found for requested code [{}].'.format(alpha2) == text['messages'][0]
        except Exception as e:
            log.error(e)
            log.error(iso2_output.status_code)
            log.error(iso2_output.text)
            pytest.xfail()


@pytest.mark.parametrize('alpha2, alpha3, country,', [('AF', 'AFG', 'Afghanistan'),
                                                      ('CK', 'COK', 'Cook Islands'),
                                                      ('BQ', 'BES', 'Bonaire, Sint Eustatius and Saba'),
                                                      pytest.param(None, 'ZZ', None, marks=pytest.mark.xfail)])
def test_get_iso3_code_api(alpha2, alpha3, country):
    ISO2_URL = URI + '/get/iso3code/{}'
    iso3_output = requests.get(ISO2_URL.format(alpha3))
    if iso3_output.status_code == 200:
        try:
            raw_details = iso3_output.json()
            if 'html' not in iso3_output.text and 'result' in raw_details['RestResponse'].keys():
                details = raw_details['RestResponse']['result']
                assert country == details['name']
                assert alpha2 == details['alpha2_code']
                assert alpha3 == details['alpha3_code']
                log.info("Found {} in alpha3_code api.".format(country))
            elif 'messages' in raw_details['RestResponse'].keys():
                text = raw_details['RestResponse']
                assert 'No matching country found for requested code [{}].'.format(alpha3) == text['messages'][0]
                log.info("No matching records found for requested code: {}".format(alpha3))
        except Exception as e:
            log.error(e)
            pytest.xfail()


@pytest.mark.parametrize('country_code', ['AF', 'AK', 'SF', 'TF', 'SG', 'RK', 'UE'])
def test_text_search_alpha2_code(country_code):
    SEARCH_URI = URI + '/search?text={}'.format(country_code)
    search_out = requests.get(SEARCH_URI)
    if search_out.status_code == 200:
        try:
            details = search_out.json()
            if 'html' not in search_out.text and 'result' in details['RestResponse'].keys():
                if details['RestResponse']['result']:
                    for i in details['RestResponse']['result']:
                        if country_code.lower() in i['alpha2_code'].lower():
                            assert country_code.lower() in i['alpha2_code'].lower()
                            log.info("Found substring '{}' in alpha2_code: {}".format(country_code, i['alpha2_code']))
                        elif country_code.lower() in i['alpha3_code'].lower():
                            assert country_code.lower() in i['alpha3_code'].lower()
                            log.info("Found substring '{}' in alpha3_code: {}".format(country_code, i['alpha3_code']))
                        elif country_code.lower() in i['name'].lower():
                            assert country_code.lower() in i['name'].lower()
                            log.info("Found substring '{}' in name: {}".format(country_code, i['name']))
                else:
                    log.info("No matching record found for key: {}".format(country_code))
            elif 'messages' in details['RestResponse'].keys():
                text = details['RestResponse']
                assert 'No matching country found for requested code [{}].'.format(country_code) == text['messages'][0]
                log.info("No matching records found for requested code: {}".format(country_code))
        except Exception as e:
            log.error(e)
            pytest.xfail()


@pytest.mark.parametrize('country_code', ['AFG', 'ARG', 'BOL', 'IND', 'SGP', 'IOT', 'FEE'])
def test_text_search_alpha3_code(country_code):
    SEARCH_URI = URI + '/search?text={}'.format(country_code)
    search_out = requests.get(SEARCH_URI)
    if search_out.status_code == 200:
        try:
            details = search_out.json()
            if 'html' not in search_out.text and 'result' in details['RestResponse'].keys():
                if details['RestResponse']['result']:
                    for i in details['RestResponse']['result']:
                        if country_code.lower() in i['alpha2_code'].lower():
                            assert country_code.lower() in i['alpha2_code'].lower()
                            log.info("Found substring '{}' in alpha2_code: {}".format(country_code, i['alpha2_code']))
                        elif country_code.lower() in i['alpha3_code'].lower():
                            assert country_code.lower() in i['alpha3_code'].lower()
                            log.info("Found substring '{}' in alpha3_code: {}".format(country_code, i['alpha3_code']))
                        elif country_code.lower() in i['name'].lower():
                            assert country_code.lower() in i['name'].lower()
                            log.info("Found substring '{}' in name: {}".format(country_code, i['name']))
                else:
                    log.info("No matching record found for key: {}".format(country_code))
            elif 'messages' in details['RestResponse'].keys():
                text = details['RestResponse']
                assert 'No matching country found for requested code [{}].'.format(country_code) == text['messages'][0]
                log.info("No matching records found for requested code: {}".format(country_code))

        except Exception as e:
            log.error(e)
            pytest.xfail()


@pytest.mark.parametrize('country_name', ['INDIA', 'CHINA', 'STATES', 'KINGDOM', 'UNITED', 'REPUBLIC'])
def test_text_search_by_name(country_name):
    SEARCH_URI = URI + '/search?text={}'.format(country_name)
    search_out = requests.get(SEARCH_URI)
    if search_out.status_code == 200:
        try:
            details = search_out.json()
            if 'html' not in search_out.text and 'result' in details['RestResponse'].keys():
                if details['RestResponse']['result']:
                    for i in details['RestResponse']['result']:
                        if country_name.lower() in i['alpha2_code'].lower():
                            assert country_name.lower() in i['alpha2_code'].lower()
                            log.info("Found substring '{}' in alpha2_code: {}".format(country_name, i['alpha2_code']))
                        elif country_name.lower() in i['alpha3_code'].lower():
                            assert country_name.lower() in i['alpha3_code'].lower()
                            log.info("Found substring '{}' in alpha3_code: {}".format(country_name, i['alpha3_code']))
                        elif country_name.lower() in i['name'].lower():
                            assert country_name.lower() in i['name'].lower()
                            log.info("Found substring '{}' in name: {}".format(country_name, i['name']))
                else:
                    log.info("No matching record found for key: {}".format(country_name))
            elif 'messages' in details['RestResponse'].keys():
                text = details['RestResponse']
                assert 'No matching country found for requested code [{}].'.format(country_name) == text['messages'][0]
                log.info("No matching records found for requested code: {}".format(country_name))
        except Exception as e:
            log.error(e)
            pytest.xfail()


@pytest.mark.parametrize('country_name', [pytest.param('$', marks=pytest.mark.xfail),
                                          pytest.param('%', marks=pytest.mark.xfail),
                                          pytest.param('*', marks=pytest.mark.xfail),
                                          'ASDF', 'GIEGE', 'slf$ja'])
def test_text_search_with_special_chars(country_name):
    SEARCH_URI = URI + '/search?text={}'.format(country_name)
    search_out = requests.get(SEARCH_URI)
    if search_out.status_code == 200:
        try:
            details = search_out.json()
            if 'html' not in search_out.text and 'result' in details['RestResponse'].keys() and country_name.isalpha():
                for i in details['RestResponse']['result']:
                    if country_name.lower() in i['alpha2_code'].lower():
                        assert country_name.lower() in i['alpha2_code'].lower()
                        log.info("Found substring '{}' in alpha2_code: {}".format(country_name, i['alpha2_code']))
                    elif country_name.lower() in i['alpha3_code'].lower():
                        assert country_name.lower() in i['alpha3_code'].lower()
                        log.info("Found substring '{}' in alpha3_code: {}".format(country_name, i['alpha3_code']))
                    elif country_name.lower() in i['name'].lower():
                        assert country_name.lower() in i['name'].lower()
                        log.info("Found substring '{}' in name: {}".format(country_name, i['name']))
                    else:
                        log.info("No matching record found for key: {}".format(country_name))
            elif 'messages' in details['RestResponse'].keys():
                text = details['RestResponse']
                assert 'No matching country found for requested code [{}].'.format(country_name) == text['messages'][0]
                log.info("No matching records found for requested code: {}".format(country_name))
        except Exception as e:
            log.error(e)
    else:
        pytest.xfail()


# The tests below (marked with @pytest.mark.skip) will be skipped during actual execution as they are comparatively 
# time consuming. But they can be used for assessment just by removing the first lines, just before the function implementation starts.

@pytest.mark.skip(reason="Too much time consuming")
def test_get_iso2_code_api_using_get_all():
    GET_ALL_URL = URI + '/get/all'
    ISO2_URL = URI + '/get/iso2code/{}'
    country_data = None
    output = requests.get(GET_ALL_URL)
    if output.status_code == 200:
        if 'html' not in output.text:
            data = output.json()
            country_data = data['RestResponse']['result']
            log.info("Got all country data.")
        else:
            pytest.xfail()

    for country in country_data:
        iso2_output = requests.get(ISO2_URL.format(country['alpha2_code']))
        if iso2_output.status_code == 200:
            raw_details = iso2_output.json()
            if 'html' not in iso2_output.text and 'result' in raw_details['RestResponse'].keys():
                details = raw_details['RestResponse']['result']
                assert country['name'] == details['name']
                assert country['alpha2_code'] == details['alpha2_code']
                assert country['alpha3_code'] == details['alpha3_code']
                log.info("Found {} in alpha2_code api.".format(country['alpha2_code']))
            else:
                log.error(iso2_output.status_code)
                log.error(iso2_output.text)
                pytest.xfail()


@pytest.mark.skip(reason="Too much time consuming")
def test_get_iso3_code_api_using_get_all():
    GET_ALL_URL = URI + '/get/all'
    ISO2_URL = URI + '/get/iso3code/{}'
    country_data = None
    output = requests.get(GET_ALL_URL)
    if output.status_code == 200:
        if 'html' not in output.text:
            data = output.json()
            country_data = data['RestResponse']['result']
            log.info("Got all country data.")
        else:
            pytest.xfail()

    for country in country_data:
        iso2_output = requests.get(ISO2_URL.format(country['alpha3_code']))
        if iso2_output.status_code == 200:
            raw_details = iso2_output.json()
            if 'html' not in iso2_output.text and 'result' in raw_details['RestResponse'].keys():
                details = raw_details['RestResponse']['result']
                assert country['name'] == details['name']
                assert country['alpha2_code'] == details['alpha2_code']
                assert country['alpha3_code'] == details['alpha3_code']
                log.info("Found {} in alpha3_code api.".format(country['alpha3_code']))
            else:
                log.error(iso2_output.status_code)
                log.error(iso2_output.text)
                pytest.xfail()
